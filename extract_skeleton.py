import os

# '''
import pip
def pip_install(pkg):
    pip.main(['install', pkg, '--user'])
# pip_install('numpy')
# pip_install('tqdm')
# pip_install('open3d')
# '''

import numpy as np
# import open3d as o3d

def mkdir(dst):
    os.makedirs(dst, exist_ok=True)

def run(cmd):
    print(cmd)
    os.system(cmd)

def load_pcd(src):
    pcd = o3d.io.read_point_cloud(src)
    return pcd

def main():
    root_dir = '/mnt/d/Simulation/PlantModel/data/plant-002'
    pointcloud_dir = os.path.join(root_dir, 'Branch-Segmentation')
    skeleton_dir = os.path.join(root_dir, 'Branch-Skeleton')
    mkdir(skeleton_dir)

    tmp_skeleton_filename = 'tmp.skel'
    segment_names = ['Branch-{:03}'.format(i) for i in range(2, 34)] + ['Junction-{:03}'.format(i) for i in range(1, 7)]
    # for i in range(1, 27):
    for name in segment_names:
        pointcloud_filename = os.path.join(pointcloud_dir, '{}.ply'.format(name))
        skeleton_filename = os.path.join(skeleton_dir, 'Skeleton-{}.skel'.format(name))

        # sample_num = min(1000, len(np.asarray(load_pcd(pointcloud_filename).points)))
        sample_num = 1000
        cmd = './PointCloud/build/fakegui {} {} {}'.format(pointcloud_filename, skeleton_filename, sample_num)
        run(cmd)

        '''
        print(pointcloud_filename)
        # Parse skeleton file
        content = open(tmp_skeleton_filename, "r").read()
        content = content[:content.find("EN 0")]
        content = content[content.find("CNN") + len("CNN"):]
        lines = content.split("\n")
        skeleton_node_num = int(lines[0])
        # print("# of skeleton nodes: {}".format(skeleton_node_num))
        lines = lines[1:]   
        lines = [l for l in lines if len(l) > 0]
        nodes = np.array([[float(a) for a in l.split()] for l in lines])

        # Save skeleton nodes
        np.save(skeleton_filename, nodes)
        '''

if __name__ == '__main__':
    main()

