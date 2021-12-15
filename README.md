# AlphaFold Singularity Container

This repo provides definition files to build a singularity container of AlphaFold v2 
(https://github.com/deepmind/alphafold) that will run and be easy to invoke in the NMRbox
environment.

Build instructions from [non-docker setting](https://github.com/kalininalab/alphafold_non_docker) by kalininalab were used.

## Build container
```
# build base container
sudo /usr/software/singularity/bin/singularity build base.sif base.def
# build alphafold container
sudo /usr/software/singularity/bin/singularity build alphafold.sif alphafold.def
```

## Run AlphaFold
```
./alphafold.py /path/to/fasta/file
```

### Notes

* The alphafold.py run script has no requirements and should run in vanilla python 3.8.
* The run script allows customizing the database location and max_template_date. Call with `-h` to see usage information.
* 