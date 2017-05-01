#! /usr/bin/env python
"""
Seach for tandem repeats with mismatch and partial repeats tolerance.

Authors: Chuchu Ding; Dejia Tang

Reference:

Burrows M, Wheeler DJ: A Block Sorting Lossless Data Compression Algorithm.

    Technical Report 124. Palo Alto, CA: Digital Equipment Corporation; 1994.

bw_transform() function implemented in https://gist.github.com/dmckean/9723bc06254809e9068f
"""
import argparse
import math
import sys
from math import ceil
from itertools import permutations
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from Bio import SeqIO

def bw_transform(s, n):
    # this line referenced the code in https://gist.github.com/dmckean/9723bc06254809e9068f
    m = sorted([s[i:n]+s[0:i]+str(i) for i in range(n)])
    return m;

# Inputs: str1, str2 - two strings with the same length to compare (strings)
# Input:  m - number of mismatches allowed (int)
# Output:  strings match or not (boolean)
def str_match(str1, str2, m=0):
    if m==0:
        return str1==str2
    else:
        score = pairwise2.align.globalms(str1, str2, float(m/100), float((m/100)-1), float((m/100)-1), float((m/100)-1), score_only=True)
        if (type(score)!=float):
            return False
        return (score>=0)

# get consensus reference pattern from records of previous repeats
# Input: record - list of dictionaries recording the number of each letter's appearance in each position ([dictionary*pattern])
# Input: pattern - leagth of pattern (int)
# Output: consensus pattern
def get_consensus(record, pattern):
    consensus = ""
    for i_pattern in range (pattern):
                consensus += max(record[i_pattern], key=record[i_pattern].get)
    return consensus

# Input: nl - new potential item of l, with indices in current window (int, int, int)
# Input: s - the sequence to be searched, current window (String)
# Input: ws - the start index of the current window (int)
# Input: l - list of int tuples representing repeats already found  ([(int, int, int)])
# Output: l - updated list of found repeats  ([(int, int, int)])
def cyclic_update(nl, s, ws, l):
    for li in l:
        if li[1]-li[0]==nl[1]-nl[0]:
            lipat = s[li[0]-ws:li[1]-ws+1]
            nlpat = s[nl[0]:nl[1]+1]
            patlen = len(lipat)
            for j in range(patlen):
                if li[1]-li[0]==nl[1]-nl[0] and min(li[2]-ws,nl[2]) - max(li[0]-ws,nl[0]) >= patlen:
                    # cyclic item already included
                    if nl[2]-nl[0]>li[2]-li[0]:
                        li[0] = nl[0]+ws
                        li[1] = nl[1]+ws
                        li[2] = nl[2]+ws
                    return l
    # no cyclic item included
    for i in range(len(nl)):
        nl[i] = nl[i]+ws
    l.append(nl)
    return l

# Input: 
# Output: l - updated list of found repeats  ([(int, int, int)])
#def cyclic_update():

# search for tandem repeats with length less than or equal to n
# Input: s - the sequence to be searched (String)
# Input: ws - the start index of the current window (int)
# Input: n - upper boundary of length of repeats to be found
# Input: lb - lower boundary of length of repeats to be found
# Input: m - mismatch tolerance (int)
# Input: a - alphabet of possible letters in sequence (String)
# Output: l - list of int tuples representing all found repeats  ([(int, int, int)])
def search_short(l, s, ws, n, lb, m=0, a='ATCG'):
    lens = len(s)
    for lamb in range(lb, n):
        combi = [''.join(cb) for cb in permutations(a, lamb)]
        for u in combi:
            if u=='':
                continue;
            uu = u + u
            for i in range(lens):
                lenuu = len(uu)
                if i+lenuu<=lens and str_match(s[i:i+lenuu], uu, m):
                    j = i+lenuu
                    k = j
                    while k<lens and str_match(s[j:k+1], uu[0:k-j+1], m):
                        k += 1
                        if k-j>=lenuu:
                            j += lenuu
                    nl = [i, i+len(u)-1, k-1]
                    cyclic_update(nl, s, ws, l)
    return l


        
# search for tandem repeats with length greater or equal to n
# Input: start - start point of the window
# Input: n - lower boundary of repeats
# Input: s - the sequence to be searched (String)
# Input: m - mismatch tolerance (int)
# Input: a - alphabet of possible letters in sequence (String)
# Output: L - list of tuples reppresenting found repeats ( (int, int, int)[] )
def search_long(start, n, s, m, a='ATCG'):
    l = len(s)
    bw = bw_transform(s, l)
    # for r in bw:
    #     print(r)
    L=[]
    i = 0
    index1=0
    index2=0
    while i < l-1:
        index1 = int(bw[i][l:])
        pattern = abs(int(bw[i][l:]) - int(bw[i+1][l:]))
        if (int(bw[i][l:])+pattern>l or int(bw[i+1][l:])+pattern>l or pattern <n) :
            i+=1
            continue
        index2
        j = i+1
        # keep the records 
        record=[]
        for i_pattern in range(pattern):
            dic = {}
            for letter in a:
                dic[letter] = 0
            dic[bw[i][i_pattern]] = 1
            record.append(dic)
        while (j < l-1):
            #  check index
            if (abs(int(bw[j-1][l:]) - int(bw[j][l:])) != pattern) :
                break
            # check complete match
            if (str_match(get_consensus(record, pattern), bw[j][:pattern], m)) :
                # update record
                for i_pattern in range (pattern):   
                    record[i_pattern][bw[j][i_pattern]] += 1
                index2 = int(bw[j][l:])
                j += 1
            else :
                break
        
        if (j-i<=1) :
            # repeat not found
            i = j;
            continue;
        else:
            # repeat found
			# extend forwards
            if (index1>index2):
                index1, index2 = index2, index1
            while (index1-pattern>=0 and str_match(get_consensus(record, pattern), s[index1-pattern:index1], m)):
                # update record
                index1 -= pattern
                for i_pattern in range (pattern):   
                    record[i_pattern][s[index1+i_pattern]] += 1
            # extend backwards
            while (index2+2*pattern<=l and str_match(get_consensus(record, pattern), s[index2+pattern:index2+2*pattern], m)):
                j+=1
                index2 += pattern
                # update record
                for i_pattern in range (pattern):   
                    record[i_pattern][s[index2+i_pattern]] += 1
            end = min (index2+pattern-1, l-1)
            # check partial match in the end
            for k in range (pattern-1,0,-1):
                if (end+k >= l):
                    continue
                if (str_match(get_consensus(record, pattern)[:k], s[index2+pattern:index2+pattern+k], m)):
                    end += k
                    break
            # update i
            i = j;
            # print()
            cyclic_update( [index1, index1+pattern-1, end], s, start, L )
    return L

# stitch together repeats that cross windows
# Input: L - list of results to be stitched together ([[]])
# Input: w - window size, int
# Input: rate - rate of window overlap, float
def stitch(L, w, rate):
    lenl = len(L)
    for i in range(lenl):
        if i!=0:
            # stitch with the window before the current window
            for li in L[i-1]:
                if li[2]>=int(rate*(i-1)*w)+w-1:
                    for cli in L[i]:
                        if cli[0]<=int(rate*(i-1)*w)+w-1 and li[1]-li[0]==cli[1]-cli[0]:
                            cli[0] = li[0]
                            cli[1] = li[1]
                            L[i-1].remove(li)
                            break
    return L

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
    
    args = parser.parse_args()

    m=args.mismatch
    w=args.window
    s=args.sequence
    alphabet=args.alphabet
    infile=args.input
    outfile=args.output
    lower_bond=args.bond

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
    # window index
    i = 0
    # total = 0
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
            if (lower_bond>bond+1):
                output.append(search_long(int(i*3*w/4), lower_bond, s, m, alphabet))
            else:
                output.append(search_long(int(i*3*w/4), bond+1, s, m, alphabet))
            search_short(output[i], s, int(i*3*w/4), bond+1, lower_bond, m, alphabet)
            print(i+1,"window finished")
            sys.stdout.flush()

            j+=1
            i+=1
        resi=buffer[int(j*w*3/4):]
    if(len(resi)>0):
        if (lower_bond>bond+1):
            output.append(search_long(int(i*3*w/4), lower_bond, resi, m, alphabet))
        else:
            output.append(search_long(int(i*3*w/4), bond+1, resi, m, alphabet))
        search_short(output[i], resi, int(i*3*w/4), bond+1, lower_bond, m, alphabet)
    stitch(output, w, float(3/4))
    print(output)
    fo = open(outfile, "w")
    for w in output:
        for r in w:
            fo.write(str(r[0])+","+str(r[1])+","+str(r[2])+"\n");
    fo.close()


