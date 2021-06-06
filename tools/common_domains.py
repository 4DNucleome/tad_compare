#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka
"""

import numpy as np
from matplotlib_venn import venn3, venn2
import matplotlib.pyplot as plt


def find_common_domains(set1, set2, shift):
    """Find all common domains in two sets of tads and given accepted shift in boundaries position"""
    common_domains = []
    for i in range(len(set1)):
        for j in range(len(set2)):
            if shift == 0:
                if check_domains(domain1=set1[i], domain2=set2[j]):
                    common_domains.append(set1[i])
            else:
                if check_shifted_domains(domain1=set1[i], domain2=set2[j], shift=shift):
                    common_domains.append(set1[i])
    return common_domains


def check_shifted_domains(domain1, domain2, shift):
    """Check if two domains positions are identical (with accepted shift)"""
    if domain1[0] != domain2[0]:
        return False
    if domain2[1] - shift < 0:
        start = 0
    else:
        start = domain2[1] - shift
    if domain1[1] in range(start, domain2[1] + shift):
        if domain1[2] in range(domain2[2] - shift, domain2[2] + shift):
            return True
    return False


def check_domains(domain1, domain2):
    """Check if two domains have exact same boundaries"""
    if domain2[0] != domain1[0]:
        return False
    if domain1[1] == domain2[1] and domain1[2] == domain2[2]:
        return True
    return False


def save_domains_matrix(tad_matrix, outfile):
    """Format nicely and save conserved domains matrix with sets names"""
    tad_matrix.to_csv(outfile, sep=",", header=True, index=True)
    print(f"Conserved domains matrix saved in {outfile}.")


def common_domains_multiple_sets(domains_sets, shift):
    """Return a matrix with common domains for different sets."""
    matr = np.zeros((len(domains_sets), len(domains_sets)), dtype=int)
    for i in range(len(domains_sets)):
        for j in range(i, len(domains_sets)):
            if i == j:
                matr[i][j] = len(domains_sets[i])
            else:
                matr[i][j] = matr[j][i] = len(find_common_domains(set1=domains_sets[i], set2=domains_sets[j], shift=shift))
    return matr


def plot_venn_diagram_of_3_sets(sets, names, outname, show):
    """Plot Venn diagram from three different sets of TADs (ex. trio family from 1000genomes)"""
    venn3(subsets=sets, set_labels=names)
    if outname:
        plt.savefig(outname, dpi=100)
    if show:
        plt.show()


def plot_venn_diagram_of_2_sets(sets, names, outname, show):
    """Plot Venn diagram from two differen sets of TADs"""
    venn2(sets, names)
    if outname:
        plt.savefig(outname, dpi=100)
    if show:
        plt.show()
