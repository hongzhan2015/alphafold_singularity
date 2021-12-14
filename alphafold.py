#!/usr/bin/env python3

import argparse
import datetime
import re
import subprocess
from os.path import abspath


def run(arguments):
    num_chains = 0
    with open(arguments.fasta, 'r') as fasta_file:
        for pos, line in fasta_file:
            if pos % 2 == 0 and not line.startswith('>'):
                raise ValueError(f"The {pos} line of a FASTA file should start with '>'.")
            if pos % 2 == 1 and not re.match(line, r'[A-Z].*'):
                raise ValueError(f"The {pos} line of a FASTA file should have a residue sequence.")
            num_chains += 1

    command = ['singularity', 'exec', '--nv', '-B', abspath(arguments.database), 'alphafold.sif']
    if num_chains == 0:
        raise ValueError('No sequences found in your FASTA file.')
    if num_chains == 1:
        print('Found FASTA file with one sequence, treating as a monomer.')
        command.append('/opt/alphafold/monomer.sh')
    if num_chains > 1:
        print(f'Found FASTA file with {num_chains} sequences, treating as a multimer.')
        command.append('/opt/alphafold/multimer.sh')
    command.extend([abspath(arguments.database), abspath(arguments.fasta), abspath(arguments.output),
                    abspath(arguments.max_template_date)])

    result = subprocess.run(command, check=True, capture_output=True)
    print(f"Command completed without exception. stdout:\n{result.stdout}\n\n\nstderr:\n{result.stderr}")


parser = argparse.ArgumentParser()
parser.add_argument("--database", "-d", action="store", default="/home/nmrbox/jwedell/alphafold_db",
                    help='The path to the AlphaFold database to use for the calculation.')
parser.add_argument("--output-dir", "-o", action="store", default=".", dest='output',
                    help='The path where the output data should be stored.')
parser.add_argument("--max_template_date", "-t", action="store", default=str(datetime.date.today()),
                    help='If you are predicting the structure of a protein that is already in PDB'
                         ' and you wish to avoid using it as a template, then max_template_date must be set to'
                         ' be before the release date of the structure.')
parser.add_argument('FASTA_file', action="store", dest='fasta',
                    help='The FASTA file to use for the calculation. Strict check applied.')
args = parser.parse_args()
run(args)
