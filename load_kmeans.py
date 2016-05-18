#!/usr/bin/env python

import numpy as np
import os
import pickle
import sys

from scipy import spatial


DATA_FILE = 'kmeans_data.txt'


def get_user(all_pkgs, popcon_file_path):
    popcon_entry = read_popcon_file(popcon_file_path)
    user = [0 for x in range(len(all_pkgs))]

    for pkg_index, pkg in enumerate(all_pkgs):
        if pkg in popcon_entry:
            user[pkg_index] = 1

    return user


def read_popcon_file(file_path):
    popcon_entry = []
    with open(file_path, 'r') as text:
        lines = text.readlines()
        print file_path
        popcon_entry = [line.split()[2] for line in lines[1:-1]
                        if '/' not in line.split()[2]]

    return popcon_entry


def main():
    if len(sys.argv) < 2:
        usage = "Usage: {} [user_popcon_path] [kmeans_file_path]"
        print usage.format(sys.argv[0])
        exit(1)

    kmeans_file_path = os.path.expanduser(sys.argv[2])
    with open(kmeans_file_path, 'rb') as text:
        loaded_data = pickle.load(text)

    all_pkgs = loaded_data['all_pkgs']
    clusters = loaded_data['clusters']

    popcon_file_path = os.path.expanduser(sys.argv[1])
    user = get_user(all_pkgs, popcon_file_path)
    cluster = clusters[spatial.KDTree(clusters).query(user)[1]]
    cluster_index = np.where(clusters == cluster)[0][0]

    # import ipdb; ipdb.set_trace()

    print "Loaded KMeans data"
    print "cluster_index: {}".format(cluster_index)


if __name__ == '__main__':
    main()
