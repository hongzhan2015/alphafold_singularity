#!/bin/bash

# testing output variables from condor arguments
echo Check values of arguments =
echo $1
echo $2
echo $3
echo $4

# run program using multimer mode
bash ./multimer.sh $1 $2 $(pwd) $4 -m multimer

# create tar file for [basename] files
tar cvf `basename $2 .fasta`.tar `basename $2 .fasta`
gzip `basename $2 .fasta`.tar

mv `basename $2 .fasta`.tar.gz /staging/hzhan3/`basename $2 .fasta`.tar.gz

mkdir PDBs
cp `basename $2 .fasta`/*.pdb PDBs/*
tar cvf `basename $2 .fasta`_PDBs.tar PDBs/*
gzip `basename $2 .fasta`_PDBs.tar

mv *.tar.* /staging/hzhan3/*

rm -r `basename $2 .fasta`
