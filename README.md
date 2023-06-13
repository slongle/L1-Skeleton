# L1-Skeleton
![Sample skeleton](https://user-images.githubusercontent.com/35003073/245417281-bf76c95c-ab43-4240-badd-5c6976a585d4.png)

This repo implements a compatibility wrapper for the [L1-Skeletonization](http://vcc.tech/research/2013/L1skeleton) method atop https://github.com/HongqiangWei/L1-Skeleton, allowing for `.ply` files to be processed into [Cloud Volume](https://github.com/seung-lab/cloud-volume) skeletons. L1-Skeletonization is a robust and efficient point-cloud based method, and may be useful as an alternative to volumetric methods such as [Kimimaro](https://github.com/seung-lab/kimimaro).

## Usage guide
### Prerequisites
- Build the container using
```
docker build -t pointcloudl1 - < Dockerfile
```
- The program can be run interactively/graphically by forwarding a X-Server socket into the container (run the `PointCloudL1` binary with no flags)
### CLI
- Generate the `.skel` file for any _isotropic_ `.ply` by running
```
./pointcloudl1.sh <ply input path> <skel output path> <path to config json>
```
- `l1_skeleton.py` provides various convenience functions to convert the `np` arrays into `.ply` files, `.skel` files into Cloud Volume skeletons, a Python function to wrap the call to the shell script, etc.
- `generate_skeleton.py` provides an example of how to run multiple skeletonization jobs concurrently
- `viewer.py` demonstrates how to visualize the point clouds and skeletons
### Hyperparameters
The two most important settings are `Down Sample Num` (which specifies the number of points to approximate the skeleton) and `Init Radius Para` (specifies the initial size of the expanding sphere). The GUI automatically calculates reasonable settings for `Init Radius Para`, but the CLI requires you to manually specify it.

In practice, I keep `Init Radius Para` constant and [downscale the input point cloud](https://github.com/jasonkena/ChunkPipeline/blob/e03ea6db3a157db4859036acf6258be3436c1ff2/chunk_pipeline/tasks/generate_l1.py#LL237C5-L237C5) by an appropriate factor.

## Tips
- Adding random noise to the input point cloud aids the convergence of the skeletonization on "barely-disconnected" components; see [this](https://github.com/jasonkena/ChunkPipeline/blob/e03ea6db3a157db4859036acf6258be3436c1ff2/chunk_pipeline/tasks/generate_l1.py#L235)
- The repo can be compiled natively on Arch Linux; see https://github.com/jasonkena/L1-Skeleton/issues/2

 
## Citing
Please cite the original paper:
```
@article{huang2013l1,
  title={L1-medial skeleton of point cloud.},
  author={Huang, Hui and Wu, Shihao and Cohen-Or, Daniel and Gong, Minglun and Zhang, Hao and Li, Guiqing and Chen, Baoquan},
  journal={ACM Trans. Graph.},
  volume={32},
  number={4},
  pages={65--1},
  year={2013}
}
```
