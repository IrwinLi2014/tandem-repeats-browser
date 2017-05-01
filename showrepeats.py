
import argparse
import math
import sys
import numpy
from math import ceil
from itertools import permutations
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from Bio import SeqIO

def printrepeats(s, output):
    for window in output:
        for repeat in window:
            start = repeat[0]
            end = repeat[2]
            print(s[start:end+1])

# stitch together repeats that cross windows
# Input: L - list of results to be stitched together ([[]])
#def stitch():

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
    #parser.add_argument('-wn', '--windownumber', help='the repeats in which window to be displayed', type=int, default='0')
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
    #wn = args.windownumber
    #winlowerind = int(w*wn*rate)
    #winupperind = winlowerind + w

    print(rpts)
    print(len(rpts))

    lli = rpts[rn]

    if (s=='' and infile==''):
        parser.print_help()
        sys.exit()
    
    output=[]
    bond = int(math.log(w,4))

    fasta_sequences=None
    if (infile != ''):
        fasta_sequences = SeqIO.parse(open(infile), 'fasta')
    if (fasta_sequences==None):
        fasta_sequences=[s]
    
    resi=""


    #print the one repeat the user chooses
    opt = ""
    i = 0
    # total = 0
    done = False
    for fasta in fasta_sequences:
        if (infile==''):
            buffer = fasta.upper()
        else:
            buffer = resi + str(fasta.seq).upper().strip('N')
        if (len(buffer)<w):
            resi = buffer
            continue
        #  local index
        j = 0
        while (int(w*(j+1)*3/4)<=len(buffer)):
            s=buffer[int(w*j*3/4):int(w*j*3/4)+w]

            if lli[0]>=0 and lli[0]<w:
                lwr = lli[0]
                upr = lli[2]
                if upr < w:
                    opt = opt + s[lwr:upr+1]
                    done = True
                    break
                else:
                    opt = opt + s[lwr:]
                    lli[0] = 0
                    lli[2] = lli[2]-w
                    j+=1
                    i+=1
                    continue
            
            lli[0] = lli[0] - w
            lli[2] = lli[2] - w

            j+=1
            i+=1
            if done:
                break
        resi=buffer[int(j*w*3/4):]
        if done:
            break
    #if(len(resi)>0):
        #print(resi)

    print("No. " + rn + " of the repeats found: " + opt)


