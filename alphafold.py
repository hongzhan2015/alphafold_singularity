#!/usr/bin/env python3.8

import argparse
import datetime
import subprocess
import sys
from os.path import abspath


def read_fasta(file_path):
    with open(file_path, 'r') as fp:
        name, seq = None, []
        for line in fp:
            line = line.rstrip()
            if line.startswith(">"):
                if name:
                    yield name, ''.join(seq)
                name, seq = line, []
            else:
                seq.append(line)
        if name:
            yield name, ''.join(seq)


def run(arguments):
    sequences = list(read_fasta(arguments.FASTA_file))
    num_chains = len(sequences)

    if num_chains == 0:
        raise ValueError('Your FASTA file does\'t appear to be valid. Please consult documentation here: '
                         'https://en.wikipedia.org/wiki/FASTA_format')

    # Build the command
    command = ['singularity', 'exec', '--nv', '-B', abspath(arguments.database), 'alphafold.sif']
    if num_chains == 1:
        print('Found FASTA file with one sequence, treating as a monomer.')
        command.append('/opt/alphafold/monomer.sh')
    elif num_chains > 1:
        print(f'Found FASTA file with {num_chains} sequences, treating as a multimer.')
        command.append('/opt/alphafold/multimer.sh')
    command.extend([abspath(arguments.database), abspath(arguments.FASTA_file), abspath(arguments.output),
                    arguments.max_template_date])

    print(f'Running AlphaFold, this will take a long time.')
    try:
        result = subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as err:
        print(f"AlphaFold raised an exception. Exception: {err}\nstdout:\n{err.output}\n\nstderr:\n{err.stderr}")
        sys.exit(1)

    print(f"AlphaFold completed without exception. stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}")


parser = argparse.ArgumentParser()
parser.add_argument("--database", "-d", action="store", default="/home/nmrbox/jwedell/alphafold_db",
                    help='The path to the AlphaFold database to use for the calculation.')
parser.add_argument("--output-dir", "-o", action="store", default=".", dest='output',
                    help='The path where the output data should be stored. Defaults to the current directory.')
parser.add_argument("--max_template_date", "-t", action="store", default=str(datetime.date.today()),
                    help='If you are predicting the structure of a protein that is already in PDB'
                         ' and you wish to avoid using it as a template, then max_template_date must be set to'
                         ' be before the release date of the structure.')
parser.add_argument('FASTA_file', action="store",
                    help='The FASTA file to use for the calculation.')
args = parser.parse_args()
run(args)
