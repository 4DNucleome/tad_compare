#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka
"""

import argparse
from tools.measure_of_concordance import calculate_moc, read_domains_from_bedfile, moc_for_multiple_sets, \
    save_moc_matrix, add_row_and_columns_id
from os import path
import glob


def main():
    parser = argparse.ArgumentParser(description="Calculate Measure of Concordance as described in Comparison of "
                                                 "computational methods for the identification of  topologically  "
                                                 "associating domains. (Genome Biology 2018)")
    parser.add_argument("-a", "--bedfile_1", help="Bedfile with first set of domains or path to multiple domains files.",
                        type=str, required=True)
    parser.add_argument("-b", "--bedfile_2",
                        help="Bedfile with second set of domains. Used only if --bedfile_1 is not a directory.",
                        type=str)
    parser.add_argument("-o", "--output",
                        help="Directory to save output file. Output is saved only when analysing multiple sets of TADs "
                             "(When --bedfile_1 is a directory. If None save in input directory.", default=None)
    parser.add_argument("-r", "--report", help="If True return MoC to stdout. Default=True", default=True)
    args = parser.parse_args()

    if args.output:
        if path.isdir(args.output):
            outname = path.join(args.output, "MoC_matrix.csv")
        else:
            if not args.output.endswith(".csv"):
                raise Exception("Wrong file format! --output should be either a directory or a .csv file.")
            outname = args.output
    else:
        outname = path.join(args.bedfile_1, "MoC_matrix.csv")

    if path.isdir(args.bedfile_1):
        domain_sets = []
        sets = [f for f in glob.glob(args.bedfile_1 + "*")]
        sets.sort()
        names = []
        for set in sets:
            if not set.endswith("bed"):
                continue
            names.append(path.basename(set).split('.')[0])
            domain_sets.append(read_domains_from_bedfile(bedfile=set))
        moc_matrix = moc_for_multiple_sets(set_list=domain_sets)
        pd_moc = add_row_and_columns_id(names=names, moc_matrix=moc_matrix)
        if args.report:
            print(pd_moc)
        save_moc_matrix(moc_matrix=pd_moc, outfile=outname)

    else:

        name1 = path.basename(args.bedfile_1).split('.')[0]
        name2 = path.basename(args.bedfile_2).split('.')[0]

        domain_set1 = read_domains_from_bedfile(bedfile=args.bedfile_1)
        domain_set2 = read_domains_from_bedfile(bedfile=args.bedfile_2)
        moc = calculate_moc(set1=domain_set1, set2=domain_set2)
        print(f"MoC for {name1} and {name2} equals to: {moc}.")


if __name__ == '__main__':
    main()
