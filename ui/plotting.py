#!/usr/bin/env python
#coding=utf-8
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.pyplot import show, figure

cmap = plt.cm.jet

def label_normalize(labels):
    """Map labels to number range [0,1]"""
    
    num_labels = np.linspace(0,1., len(labels))
    map = dict(zip(labels, num_labels))

    def map_func(lab):
        return map[lab]

    return map_func


def plot_spikes(spike_data, clust_idx=None,ecolor='k', alpha=0.2,
        n_spikes='all'):

    spikes =  spike_data['data']
    time = spike_data['time']
    
    if not clust_idx is None:
        norm = label_normalize(np.unique(clust_idx))
        legend = True
    else:
        clust_idx = np.ones(spikes.shape[1])
        norm = plt.normalize(0,1)
        legend = False


    for c in np.unique(clust_idx): 
        spikes_to_plot = spikes[:, clust_idx==c]
        if not n_spikes=="all":
            i = np.random.rand(spikes_to_plot.shape[1]).argsort()
            spikes_to_plot = spikes_to_plot[:,i[:n_spikes]]
        plt.plot(time, spikes_to_plot,
                color=cmap(norm(c)), alpha=alpha)
        plt.plot(time, spikes_to_plot.mean(1),
                color=cmap(norm(c)), lw=2, label=str(c))

    if legend:
        plt.legend()


def plot_features(features_dict, clust_idx=None, size=1):

    features = features_dict['data']
    names = features_dict['names']

    n_spikes, n_feats = features.shape
    
    if not clust_idx is None:
        norm = label_normalize(np.unique(clust_idx))
    else:
        clust_idx = np.ones(n_spikes)
        norm = plt.normalize(0,1)

    fig = plt.gcf()
    for i in range(n_feats):
        for j in range(n_feats):
            ax = fig.add_subplot(n_feats, n_feats, j*n_feats + i + 1)
            if i<>j:
                for c in np.unique(clust_idx):
                    plt.plot(features[clust_idx==c,i],
                             features[clust_idx==c,j],".", 
                            color=cmap(norm(c)), markersize=size)
            else:
                ax.set_frame_on(False)
                for c in np.unique(clust_idx):
                    plt.hist(features[clust_idx==c,i],20, 
                            [0,1], ec="none", fc=cmap(norm(c)),
                            alpha=0.5, normed=True)
            plt.xticks([])
            plt.yticks([])
    
    for i in range(n_feats):
        ax = plt.subplot(n_feats, n_feats, i+1)
        ax.set_xlabel(names[i])
        ax.xaxis.set_label_position("top")
        ax = plt.subplot(n_feats, n_feats, i*n_feats + 1)
        ax.set_ylabel(names[i])



