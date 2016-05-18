#!/usr/bin/env python

import numpy as np
import os
import pickle
import random
import sys

from scipy import spatial
from scipy.spatial import distance
from sklearn.cluster import KMeans


DATA_FILE = 'k_means.txt'


def get_user(all_pkgs, popcon_file_path):
    popcon_entry = read_popcon_file(popcon_file_path)
    user = [0 for x in range(len(all_pkgs))]

    for pkg_index, pkg in enumerate(all_pkgs):
        if pkg in popcon_entry:
            user[pkg_index] = 1

    return user


def get_users(all_pkgs, popcon_entries):
    rows = len(all_pkgs)
    cols = len(popcon_entries)
    users = [[0 for x in range(rows)] for y in range(cols)]

    for pkg_index, pkg in enumerate(all_pkgs):
        for entry_index, popcon_entry in enumerate(popcon_entries):
            if pkg in popcon_entry:
                users[entry_index][pkg_index] = 1

    return users


def get_all_pkgs(popcon_entries):
    all_pkgs = set()

    for popcon_entry in popcon_entries:
        for pkg in popcon_entry:
            all_pkgs.add(pkg)

    all_pkgs = list(sorted(all_pkgs))
    return all_pkgs


def read_popcon_file(file_path):
    popcon_entry = []
    with open(file_path, 'r') as text:
        lines = text.readlines()
        popcon_entry = [line.split()[2] for line in lines[1:-1]
                        if '/' not in line.split()[2]]

    return popcon_entry


def get_popcon_entries(popcon_entries_path):
    folders = os.listdir(popcon_entries_path)

    popcon_entries = []
    for folder in folders:
        folder_path = os.path.join(popcon_entries_path, folder)
        file_path = os.path.join(folder_path, os.listdir(folder_path)[0])
        popcon_entry = read_popcon_file(file_path)

        if len(popcon_entry) > 0:
            popcon_entries.append(popcon_entry)

    return popcon_entries


def main():
    if len(sys.argv) < 2:
        print "Usage: {} [popcon-entries_path]".format(sys.argv[0])
        exit(1)

    popcon_entries_path = os.path.expanduser(sys.argv[1])
    popcon_entries = get_popcon_entries(popcon_entries_path)
    all_pkgs = get_all_pkgs(popcon_entries)
    users = get_users(all_pkgs, popcon_entries)

    random_state = 170
    k_means = KMeans(n_clusters=3, random_state=random_state)
    k_means.fit(users)
    users_clusters = k_means.labels_.tolist()
    clusters = k_means.cluster_centers_

    saved_data = {'users': users, 'k_means': k_means}
    with open(DATA_FILE, 'wb') as text:
        pickle.dump(saved_data, text)

    # popcon_file_path = os.path.expanduser(sys.argv[2])
    # user = get_user(all_pkgs, popcon_file_path)
    # cluster = clusters[spatial.KDTree(clusters).query(user)[1]]
    # user_cluster = np.where(clusters == cluster)[0][0]

    # import ipdb; ipdb.set_trace()

    # print "users: {}".format(len(users))
    # print "users_clusters: {}".format(users_clusters)
    # print "user_cluster: {}".format(user_cluster)


if __name__ == '__main__':
    main()
