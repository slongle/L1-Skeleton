import numpy as np
import cloudvolume
import kimimaro
import glob
import os
from tqdm import tqdm

import scipy.sparse as sp
from scipy.sparse import csgraph

FOLDER_PATH = "./ribcl"
LEN_CENTERLINE = 500


def generate_paths(vertices, edges):
    skel = cloudvolume.Skeleton(vertices=vertices, edges=edges)
    if len(skel.components()) > 1:
        print("Skeleton has multiple components, merging using join_close_components")
        # https://github.com/jasonkena/ChunkPipeline/blob/8e4ae4222a33212467f80ffce1507b4796c8bd35/chunk_pipeline/tasks/generate_skeleton.py#L70
        skel = kimimaro.join_close_components(skel)

    paths = skel.paths()
    return paths, skel


def interpolate_path(path, length):
    l2 = np.linalg.norm(path[1:] - path[:-1], axis=1)
    cumsum = np.cumsum(l2)
    cumsum = np.insert(cumsum, 0, 0)
    total_length = cumsum[-1]

    sample_length = np.linspace(0, total_length, length)

    points = [np.interp(sample_length, cumsum, path[:, i]) for i in range(3)]
    points = np.stack(points, axis=1)

    return points


def longest_path(skel):
    # https://github.com/jasonkena/ChunkPipeline/blob/8e4ae4222a33212467f80ffce1507b4796c8bd35/chunk_pipeline/tasks/generate_skeleton.py#L177
    seed = find_furthest_pt(skel, 0, single=False)[0]
    longest_path = find_furthest_pt(skel, seed, single=False)[1][0]
    return longest_path


def find_furthest_pt(skel, root, single=True):
    # https://github.com/jasonkena/skeleton/blob/11492be58db18688f60666fd909bdc7b4b6fe548/skel.py#L192
    def reconstruct_all_paths(preds):
        leaves = np.nonzero(~np.isin(np.arange(len(preds)), preds))[0]
        return [reconstruct_path(preds, leaf) for leaf in leaves]

    def reconstruct_path(preds, leaf):
        path = []
        curr = leaf
        while curr >= 0:
            path.append(curr)
            curr = preds[curr]
        return path

    num_nodes = len(skel.vertices)
    edges = skel.edges
    g = sp.coo_matrix(
        (
            np.ones(
                len(edges),
            ),
            (edges[:, 0], edges[:, 1]),
        ),
        shape=(num_nodes, num_nodes),
    )
    o = csgraph.breadth_first_order(g, root, directed=False, return_predecessors=False)

    furthest_node = o[-1]

    o2, preds = csgraph.breadth_first_order(
        g, furthest_node, directed=False, return_predecessors=True
    )

    path_inds = reconstruct_all_paths(preds)
    paths = [inds for inds in path_inds if root in inds]

    if single:
        assert len(paths) == 1, "Too many paths"
        return furthest_node, paths[0]

    else:
        return furthest_node, paths


if __name__ == "__main__":
    results = {}
    for file in tqdm(sorted(glob.glob(os.path.join(FOLDER_PATH, "*", "*.npz")))):
        data = dict(np.load(file))
        vertices, edges = data["vertices"], data["edges"]
        paths, skel = generate_paths(vertices, edges)
        if len(paths) > 1:
            print("More than one path found for {}, using longest path".format(file))
            skel.viewer()
            path_idx = longest_path(skel)
            path = skel.vertices[path_idx]
        else:
            path = paths[0]
        centerline = interpolate_path(paths[0], LEN_CENTERLINE)
        results[file] = centerline
    np.savez("centerlines.npz", **results)
