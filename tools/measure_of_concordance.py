#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka
"""
import numpy as np
import pandas as pd


def read_domains_from_bedfile(bedfile):
    """Read domains from bed with three first columns "chr start end" file
    and return as a list [[chr, start1, end1], ...]"""
    with open(bedfile) as bed:
        line = bed.readline()
        domains = []
        while line:
            lline = line.strip().split()
            domains.append((lline[0], int(lline[1]), int(lline[2])))
            line = bed.readline()
    return domains


def calculate_moc(set1, set2):
    n1 = len(set1)  # number fo domains in set 1
    n2 = len(set2)  # number of domains in set 2
    if n1 == n2 == 1:
        return 1
    moc = 0
    for i in range(n1):
        p_i = set1[i][2] - set1[i][1]  # domain length
        for j in range(n2):
            if set1[i][0] == set2[j][0]:  # check if same chromosome
                q_j = set2[j][2] - set2[j][1]  # domain length
                overlap = check_overlap(start1=set1[i][1], end1=set1[i][2], start2=set2[j][1],
                                            end2=set2[j][2])  # calculate overlap in bp
                if overlap > 0:
                    moc += (overlap ** 2 / (p_i * q_j))
    return (1 / ((n1 * n2) ** (1 / 2) - 1)) * (moc - 1)


def check_overlap(start1, end1, start2, end2):
    """Return the overlap between two domains"""
    overlap = min(end1, end2) - max(start1, start2)
    if overlap < 0:
        overlap = 0
    return overlap


def moc_for_multiple_sets(set_list):
    """Return MoC similarity matrix for all set of TADs given in list."""
    n = len(set_list)
    moc_matr = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                moc_matr[i, j] = 1
                continue
            if moc_matr[i, j] == 0:
                moc = calculate_moc(set_list[i], set_list[j])
                moc_matr[i, j] = moc
                moc_matr[j, i] = moc
    return moc_matr


def save_moc_matrix(moc_matrix, outfile):
    """Format nicely and save MoC matrix with sets names"""
    moc_matrix.to_csv(outfile, sep=",", header=True, index=True)
    print(f"MoC matrix saved in {outfile}.")


def add_row_and_columns_id(names, moc_matrix):
    """Add column and row names by transforming to pandas"""
    df = pd.DataFrame(moc_matrix, columns=names, index=names)
    return df
