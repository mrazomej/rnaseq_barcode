import pandas as pd
import scipy as sp
import numpy as np

"""
Title:
    seq.py
Last update:
    2021-05-11
Author(s):
    Courtesy of the RegSeq paper
Purpose:
    This file compiles relevant functions to process sequencing data and
    energy-matrix related functions.
"""

def seq2mat(seq,seq_dict):
    mat = sp.zeros((len(seq_dict),len(seq)),dtype=int)
    for i,bp in enumerate(seq):
        mat[seq_dict[bp],i] = 1
    return mat


def choose_dict(dicttype,modeltype='MAT'):
    '''Creates a necessary tool to convert from bp to an index'''
    if dicttype == 'dna':
        seq_dict = {'A':0,'C':1,'G':2,'T':3}
        inv_dict = {0:'A',1:'C',2:'G',3:'T'}
    elif dicttype == 'rna':
        seq_dict = {'A':0,'C':1,'G':2,'U':3}
        inv_dict = {0:'A',1:'C',2:'G',3:'U'}
    elif dicttype == 'protein':
        seq_dict = {
            '*':0,'A':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'K':9,'L':10,
            'M':11,'N':12,'P':13,'Q':14,'R':15,'S':16,'T':17,'V':18,'W':19,'Y':20}
        inv_dict = {v:k for k,v in seq_dict.items()}
    else:
        raise SortSeqError('Unkonwn dicttype: %s'%dicttype)

    if modeltype == 'NBR' or modeltype == 'PAIR':
        seq_dict = {
            ''.join([inv_dict[i],inv_dict[z]]):i*len(seq_dict)+z
            for i in range(len(seq_dict)) for z in range(len(seq_dict))}
        inv_dict = {seq_dict[i]:i for i in seq_dict.keys()}
    return seq_dict,inv_dict