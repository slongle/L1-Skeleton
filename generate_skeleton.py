# dask pipeline

from l1_skeleton import generate_skeleton
import nibabel as nib
import numpy as np
import os
import dask
import dask.distributed
from dask.diagnostics import ProgressBar

dir_seg = "seg/"
num_sample = 20000
noise_std = 5.0  # in prescaled units
# noise_std = 0.0 # 0 noise
scale_factor = 0.01


def process(dir_case, name, idx):
    try:
        np.random.seed(0)
        filename = dir_case + "/{}".format(idx) + ".npz"
        os.makedirs(dir_case, exist_ok=True)
        if os.path.exists(filename):
            return
        vol = nib.load(dir_seg + name).get_fdata()
        pc = np.argwhere(vol == idx)

        if pc.shape[0] != 0:
            pc = pc + np.random.normal(0, noise_std, pc.shape)
            pc *= scale_factor

            if pc.shape[0] > num_sample:
                choice = np.random.choice(pc.shape[0], num_sample, replace=False)
                pc = pc[choice]
            skeleton = generate_skeleton(pc)
            np.savez_compressed(
                filename, vertices=skeleton.vertices, edges=skeleton.edges
            )
    except Exception as e:
        print(f"{name} {idx}: {e}")


def dask_run():
    client = dask.distributed.Client(n_workers=20, threads_per_worker=1)
    print(client)

    list_seg = [x for x in sorted(os.listdir(dir_seg))]
    tasks = []
    for name in list_seg:
        dir_case = "./ribcl/" + name.split("-")[0]
        for i in range(1, 25):
            tasks.append(dask.delayed(process)(dir_case, name, i))
    print(tasks)

    dask.compute(tasks)
    # dask.compute(tasks[0])


if __name__ == "__main__":
    dask_run()
    # process("./ribcl/RibFrac117", "RibFrac117-rib-seg.nii.gz", 24)
    # process("./ribcl/RibFrac132", "RibFrac132-rib-seg.nii.gz", 1)
