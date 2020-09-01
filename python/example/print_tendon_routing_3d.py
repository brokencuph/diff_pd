import sys
sys.path.append('../')

from pathlib import Path
import pickle
import matplotlib.pyplot as plt
import numpy as np

from py_diff_pd.common.common import print_info

from py_diff_pd.common.common import ndarray

if __name__ == '__main__':
    folder = Path('tendon_routing_3d')
    for thread_ct in [8]:
        data_file = Path('tendon_routing_3d') / 'data_{:04d}_threads.bin'.format(thread_ct)
        if data_file.exists():
            print_info('Loading {}'.format(data_file))
            data = pickle.load(open(data_file, 'rb'))
            for method in ['newton_pcg', 'newton_cholesky', 'pd_eigen']:
                total_time = 0
                avg_forward = 0
                average_backward = 0
                for d in data[method]:
                    print('loss: {:8.3f}, |grad|: {:8.3f}, forward time: {:6.3f}s, backward time: {:6.3f}s'.format(
                        d['loss'], np.linalg.norm(d['grad']), d['forward_time'], d['backward_time']))
                    total_time += d['forward_time'] + d['backward_time']
                    average_backward += d['backward_time']
                    avg_forward += d['forward_time']
                avg_forward /= len(data[method])
                average_backward /= len(data[method])
                print_info('Optimizing with {} finished in {:6.3f}s with {:d} iterations. Average Backward time: {:6.3f}s, Average Forward Time = {:6.3f}s'.format(
                    method, total_time,  len(data[method]), average_backward, avg_forward))

    plt.rc('pdf', fonttype=42)
    plt.rc('font', size=30)             # Controls default text sizes.
    # plt.rc('axes', titlesize=16)        # Fontsize of the axes title.
    # plt.rc('axes', labelsize=16)        # Fontsize of the x and y labels.
    # plt.rc('xtick', labelsize=16)       # Fontsize of the tick labels.
    # plt.rc('ytick', labelsize=16)       # Fontsize of the tick labels.
    # plt.rc('legend', fontsize=16)       # Legend fontsize.
    # plt.rc('figure', titlesize=16)      # Fontsize of the figure title.

    acts = {}
    losses = {}
    for method in ['newton_pcg', 'newton_cholesky', 'pd_eigen']:
        acts[method] = [np.linalg.norm(d['x']) for d in data[method]]
        losses[method] = [d['loss'] for d in data[method]]

    fig = plt.figure(figsize=(18, 9))

    ax_act = fig.add_subplot(121)

    ax_loss= fig.add_subplot(122)

    titles = ['Muscle Actuation', 'loss']
    for title, ax, y in zip(titles, (ax_act, ax_loss), (acts, losses)):

        if 'Muscle' in title:
            ax.set_ylabel("|Actuation Effort|")
            ax.grid(True, which='both')
        else:
            ax.set_ylabel("loss")
            ax.set_yscale('log')
            ax.grid(True)
        ax.set_xlabel('iterations')
        for method, method_ref_name, color in zip(['newton_pcg', 'newton_cholesky', 'pd_eigen'],
            ['Newton-PCG', 'Newton-Cholesky', 'DiffPD (Ours)'], ['tab:blue', 'tab:red', 'tab:green']):
            ax.plot(y[method], color=color, label=method_ref_name, linewidth=4)
        ax.set_title(title, pad=25)
        handles, labels = ax.get_legend_handles_labels()

    plt.subplots_adjust(bottom = 0.25, wspace=0.3)
    # Share legends.
    fig.legend(handles, labels, loc='lower center', ncol=3)#, bbox_to_anchor=(0.5, 0.17))

    fig.savefig(folder / 'tendon_routing_3d_opt.pdf')
    fig.savefig(folder / 'tendon_routing_3d_opt.png')
    plt.show()