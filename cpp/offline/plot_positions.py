#!/usr/bin/env python3

"""Plot position trajectory from JSONL output."""

import json
import sys

import numpy as np

POSITION = 'position'

def read_jsonl(fn):
    with open(fn) as f:
        for l in f: yield(json.loads(l))

def read_data(fn):
    pos = []
    for o in read_jsonl(fn):
        if POSITION not in o: continue
        pos.append([o[POSITION][c] for c in 'xyz'])
    return np.array(pos)

def set_axes_equal_3d(ax):
    from mpl_toolkits.mplot3d.axes3d import Axes3D
    assert isinstance(ax, Axes3D)
    limits = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])  # type: ignore[attr-defined]
    center = limits.mean(axis=1)
    half_range = (limits[:, 1] - limits[:, 0]).max() / 2
    ax.set_xlim3d(center[0] - half_range, center[0] + half_range)
    ax.set_ylim3d(center[1] - half_range, center[1] + half_range)
    ax.set_zlim3d(center[2] - half_range, center[2] + half_range)

if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt

    p = argparse.ArgumentParser(__doc__)
    p.add_argument('jsonl', help='VIO output file')
    p.add_argument('--image', help='Save image to this path instead of showing the plot')
    p.add_argument('--3d', action='store_true', dest='plot3d', help='Plot in 3D (interactively rotatable)')
    args = p.parse_args()

    pos = read_data(args.jsonl)
    if pos.size == 0:
        print("No data to plot.")
        sys.exit()

    if args.plot3d:
        from mpl_toolkits.mplot3d.axes3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        assert isinstance(ax, Axes3D)
        ax.plot(pos[:,0], pos[:,1], pos[:,2])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        set_axes_equal_3d(ax)
    else:
        plt.plot(pos[:,0], pos[:,1])
        plt.axis('equal')

    if args.image:
        plt.savefig(args.image)
    else:
        plt.show()
