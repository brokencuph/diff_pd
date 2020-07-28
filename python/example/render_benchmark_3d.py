import sys
sys.path.append('../')

from pathlib import Path
import numpy as np

from py_diff_pd.common.common import create_folder, print_info
from py_diff_pd.common.mesh import hex2obj
from py_diff_pd.core.py_diff_pd_core import Mesh3d
from py_diff_pd.env.benchmark_env_3d import BenchmarkEnv3d

if __name__ == '__main__':
    seed = 42
    folder = Path('benchmark_3d')
    env = BenchmarkEnv3d(seed, folder, { 'refinement': 8 })
    deformable = env.deformable()

    thread_ct = 4
    method = 'pd'
    opt = { 'max_pd_iter': 5000, 'max_ls_iter': 1, 'abs_tol': 1e-9, 'rel_tol': 1e-6, 'verbose': 0, 'thread_ct': 4,
            'method': 1, 'bfgs_history_size': 10 }

    dofs = deformable.dofs()
    act_dofs = deformable.act_dofs()
    q0 = env.default_init_position()
    v0 = env.default_init_velocity()
    a0 = np.random.uniform(size=act_dofs)
    f0 = np.random.normal(scale=0.1, size=dofs) * 1e-3

    dt = 1e-2
    frame_num = 25
    env.simulate(dt, frame_num, method, opt, q0, v0, [a0 for _ in range(frame_num)],
        [f0 for _ in range(frame_num)], require_grad=False, vis_folder='groundtruth')

    # Load meshes.
    def generate_mesh(vis_folder, mesh_folder):
        create_folder(folder / mesh_folder)
        for i in range(frame_num + 1):
            mesh_file = folder / vis_folder / '{:04d}.bin'.format(i)
            mesh = Mesh3d()
            mesh.Initialize(str(mesh_file))
            hex2obj(mesh, obj_file_name=folder / mesh_folder / '{:04d}.obj'.format(i), obj_type='tri')

    generate_mesh('groundtruth', 'groundtruth_mesh')