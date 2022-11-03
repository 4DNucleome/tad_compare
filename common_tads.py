#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka
"""

import argparse
from tools.measure_of_concordance import read_domains_from_bedfile, add_row_and_columns_id
from tools.common_domains import find_common_domains, common_domains_multiple_sets, save_domains_matrix
from os import path
import glob
from tools.str2bool import str2bool


def main():
    parser = argparse.ArgumentParser(description="Identify common domains in given sets.")
    parser.add_argument("-a", "--bedfile_1",
                        help="Bedfile with first set of domains or path to multiple domains files.",
                        type=str, required=True)
    parser.add_argument("-b", "--bedfile_2",
                        help="Bedfile with second set of domains. Used only if --bedfile_1 is not a directory.",
                        type=str)
    parser.add_argument("-o", "--output",
                        help="Directory to save output file. Output is saved only when analysing multiple sets of TADs "
                             "(When --bedfile_1 is a directory. If None save in input directory.", default=None)
    parser.add_argument("-r", "--report", help="If True print output matrix to stdout. Default=True", default=True, type=str2bool)
    parser.add_argument("-s", "--shift", default=0, type=int,
                        help="Accepted shift of two domain boundaries positions in base pair.")
    args = parser.parse_args()

    if args.output:
        if path.isdir(args.output):
            outname = path.join(args.output, f"common_tads_shift_{args.shift}bp.csv")
        else:
            if not args.output.endswith(".csv"):
                raise Exception("Wrong file format! --output should be either a directory or a .csv file.")
            outname = args.output
    else:
        outname = path.join(args.bedfile_1, f"common_tads_shift_{args.shift}bp.csv")

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
        common_tads_matr = common_domains_multiple_sets(domains_sets=domain_sets, shift=args.shift)
        common_tads_df = add_row_and_columns_id(names=names, moc_matrix=common_tads_matr)
        if args.report:
            print(common_tads_df)
        save_domains_matrix(tad_matrix=common_tads_df, outfile=outname)

    else:

        name1 = path.basename(args.bedfile_1).split('.')[0]
        name2 = path.basename(args.bedfile_2).split('.')[0]
        domain_set1 = read_domains_from_bedfile(bedfile=args.bedfile_1)
        domain_set2 = read_domains_from_bedfile(bedfile=args.bedfile_2)
        common_tads = find_common_domains(set1=domain_set1, set2=domain_set2, shift=args.shift)
        print(f"Number of common TADs between {name1} and {name2} with shift {args.shift} bp equals "
              f"to: {len(common_tads)}.")


if __name__ == '__main__':
    main()
