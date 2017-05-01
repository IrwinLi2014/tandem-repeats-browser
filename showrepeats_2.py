
import argparse
import math
import sys
import numpy
from math import ceil
from itertools import permutations
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from Bio import SeqIO

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Finding tandem repeats.')

    parser.add_argument('-m', '--mismatch', help='Mismatch tolerance in percentage.', type=int, default=0)
    parser.add_argument('-w', '--window', help='Window size.', type=int, default=-1)
    parser.add_argument('-s', '--sequence', help='sequence to be searched', type=str, default='')
    parser.add_argument('-a', '--alphabet', help='sequence to be searched', type=str, default='ATCG')
    parser.add_argument('-i', '--input', help='input file', type=str, default = '')
    parser.add_argument('-o', '--output', help='output file', type=str, default='out.csv')
    parser.add_argument('-b', '--bond', help='lower boundary', type=int, default='0')
    parser.add_argument('-rn', '--repeatnumber', help='the index of the repeat the user wants to print out', type=int, default='0')
    
    args = parser.parse_args()

    rpts = numpy.loadtxt(open("out.csv", "rb"), delimiter=",")
    rpts = numpy.ndarray.tolist(rpts)

    m=args.mismatch
    w=args.window
    s=args.sequence
    alphabet=args.alphabet
    infile=args.input
    outfile=args.output
    lower_bond=args.bond
    rate = float(3/4)
    rn = args.repeatnumber

    #cut paste sequence
    if s!="":
        fo = open("myrpts.csv", "w")
        rpt = rpts
        lwr = int(rpt[0])
        upr = int(rpt[2])
        myrpt = s[lwr:upr+1]
        fo.write(myrpt+"\n")
        fo.close()
    #input fasta file
    else:
        lli = rpts[rn]
        lli[0] = int(lli[0])
        lli[1] = int(lli[1])
        lli[2] = int(lli[2])
        #[int(a) for a in lli]
        start = int(lli[0])
        end = int(lli[2])
        s_len = end-start+1

        if (s=='' and infile==''):
            parser.print_help()
            sys.exit()
        
        fasta_sequences=None
        if (infile != ''):
            fasta_sequences = SeqIO.parse(open(infile), 'fasta')
        if (fasta_sequences==None):
            fasta_sequences=[s]
        
        resi=""

        #print the one repeat the user chooses
        opt = ""
        i = 0

        done = False
        for fasta in fasta_sequences:
            if (infile==''):
                buffer = fasta.upper()
            else:
                buffer = resi + str(fasta.seq).upper().strip('N')
            if (len(buffer)>=s_len):
                opt += buffer[:s_len]
                print("No. " + str(rn) + " of the repeats found: " + str(opt))
                exit()
            else:
                opt += buffer
                s_len -= len(buffer)
                continue

        print("not available")
        exit()           


