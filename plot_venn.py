#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka
"""
import argparse
from os import path
import glob
from tools.measure_of_concordance import read_domains_from_bedfile
from tools.common_domains import plot_venn_diagram_of_3_sets, plot_venn_diagram_of_2_sets


def main():
    parser = argparse.ArgumentParser(description="Plot Venn diagram of common TADs between different sets of TADs.")
    parser.add_argument('-d', '--domains_files', nargs='+',
                        help='List of files (two or three) with different domains sets.', required=True)
    parser.add_argument("-o", "--output",
                        help="Directory or filename to save a plot in.", default=None)
    parser.add_argument("-s", "--show", help="If True show the plot.", default=True, type=bool)
    args = parser.parse_args()

    if args.output:
        if path.isdir(args.output):
            outname = path.join(args.output, "venn_diagram.png")
        else:
            if not args.output.endswith(".png"):
                raise Exception("Wrong file format! --output should be either a directory or a .png file.")
            outname = args.output
    else:
        outname = path.join(path.dirname(args.domains_files[0]), "venn_diagram.png")
        print(outname)

    domain_sets = []
    names = []
    for doms in args.domains_files:
        if not doms.endswith("bed"):
            continue
        names.append(path.basename(doms).split('.')[0])
        domain_sets.append(set(read_domains_from_bedfile(bedfile=doms)))

    if len(args.domains_files) == 3:
        plot_venn_diagram_of_3_sets(sets=domain_sets, names=names, outname=outname, show=args.show)
    elif len(args.domains_files) == 2:
        plot_venn_diagram_of_2_sets(sets=domain_sets, names=names, outname=outname, show=args.show)
    else:
        raise Exception("Wrong number of domain files. You must provide two or three files.")


if __name__ == '__main__':
    main()
