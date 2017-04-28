#! /usr/bin/env python
"""

Seach for tandem repeats with mismatch and partial repeats tolerance.

Authors: Chuchu Ding; Dejia Tang

Reference:

Burrows M, Wheeler DJ: A Block Sorting Lossless Data Compression Algorithm.

    Technical Report 124. Palo Alto, CA: Digital Equipment Corporation; 1994.

bw_transform() function implemented in https://gist.github.com/dmckean/9723bc06254809e9068f

USAGE: tandem.py [-m MISMATCH] [-w WINDOW] SEQUENCE

"""
import argparse
import math
from math import ceil
from itertools import permutations
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from Bio import SeqIO


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Finding tandem repeats.')


    # parser.add_argument('-d', '--data', help='data file', type=str)
    # parser.add_argument('-w', '--window', help='Window size.', type=int, default=-1)
    # parser.add_argument('-a', '--sequencea', help='sequence a', type=str)
    # parser.add_argument('-b', '--sequenceb', help='sequence b', type=str)
    
    args = parser.parse_args()
    fasta_sequences=['1234567891234567891234','56','78912345','6789123456789123','456','789123','456','789123456789123']
    w=8
    # a=args.sequencea
    # b=args.sequenceb
    # input_file = args.data
    # for p in pairwise2.align.globalms(a, b, 1, -4, -4, -4):
    #     print(format_alignment(*p))

    # fasta_sequences = SeqIO.parse(open(input_file), 'fasta')
    # print(type(fasta_sequences))
    resi=""
    i = 0
    for fasta in fasta_sequences:
        # print("!", fasta)
        buffer = resi + fasta
        j=0
        if (len(buffer)<w):
            continue
        while (int(w*(j+1)*3/4)<=len(buffer)):
            # print("i", i)
            s=buffer[int(w*j*3/4):int(w*j*3/4)+w]
            j+=1
            # print("buffer before", buffer)
            i+=1
            print("s",s)
            # print("buffer after", buffer)
            print()
        resi=buffer[int(j*w*3/4):]
        print("resi", resi)
    if(len(resi)>0):
        print(resi)