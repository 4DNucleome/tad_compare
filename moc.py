#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka
"""
""" Calculate Measure of Concordance as described in Comparison of computational methods forthe identification of 
topologically  associating domains Genome Biology 2018"""

import argparse
from tools.measure_of_concordance import calculate_moc, read_domains_from_bedfile
from os import path
import glob


def main():
    parser = argparse.ArgumentParser(description="opis")
    parser.add_argument("-a", "--bedfile_1", help="Bedfile with first set of domains.", type=str)
    parser.add_argument("-b", "--bedfile_2", help="Bedfile with second set of domans.", type=str)
    parser.add_argument("-o", "--output",
                        help="Directory to save your result in. Used only with multiple sets (when --bedfile_1 is a directory).")
    args = parser.parse_args()


    name1 = path.basename(args.bedfile_1).split('.')[0]
    name2 = path.basename(args.bedfile_2).split('.')[0]

    domain_set1 = read_domains_from_bedfile(args.bedfile_1)
    domain_set2 = read_domains_from_bedfile(args.bedfile_2)
    moc = calculate_moc(domain_set1, domain_set2)
    print(f"MoC for {name1} and {name2} equals to: {moc}")


if __name__ == '__main__':
    main()
