import nibabel as nib
from cloudvolume import Skeleton
import numpy as np
import open3d as o3d


def view_nib(idx, seg_idx):
    path = f"seg/RibFrac{idx}-rib-seg.nii.gz"
    vol = nib.load(path).get_fdata()
    pc = np.argwhere(vol == seg_idx)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pc)
    o3d.visualization.draw_geometries([pcd])


def view_skel(idx, seg_idx):
    path = f"ribcl/RibFrac{idx}/{seg_idx}.npz"
    data = dict(np.load(path))
    vertices, edges = data["vertices"], data["edges"]
    skel = Skeleton(vertices, edges)
    skel.viewer()


if __name__ == "__main__":
    view_nib(377, 12)
    view_skel(377, 12)
    # view_skel(132, 1)
    # view_nib("seg/RibFrac117-rib-seg.nii.gz", 24)
