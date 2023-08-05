# justblast
This is a simple program to more efficiently run blast on multicore 
machines, have a simple extension to run and plot the last common
ancestor (LCA) using Tim Kahlke's [BASTA](
https://github.com/timkahlke/BASTA), and allowing the input to be in 
fastq format.

# Requirements
### READ THIS BEFORE INSTALLING

To run this program you will need to have the [blast+ tools](
https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) 
install in your machine. Go to the link above and follow the 
instructions. The installation instruction below should try to install
BASTA, however, BASTA has as requirement the database LevelDB that 
needs to be installed on your system. On Linux systems you can do:
```
sudo apt-get update
sudo apt-get install python-leveldb
```
If you dont have administrative privileges, contact your sys admin.

On mac OS:

```
brew install leveldb
```

### A note for Compute Canada Users
Before installing you will need to load the python packages and the
levelDB modules by:
```
module load nixpkgs/16.09 scipy-stack/2018b # python modules
module load gcc/5.4.0 leveldb/1.20 # leveldb
```

# Installation
justblast in on the PyPI repository, and can be installed by:
```
python3 -m pip install justblast
```
Or you can clone this repository and run the `setup.py install` command.

If you do not have admin privileges, you can add the `--user` option.

# Usage
You can explore the options by typing:
```
justblast -h
```
and you will get

```
usage: justblast [-h] [-e EVALUE] [-p PERCENT_ID] [-m MAX_TARGET_SEQS]
            [-q QUERY_COVERAGE] [-c CPUS] [-i] [-o OUT_FILENAME] [-f OUTFMT]
            query db

positional arguments:
  query                 Fasta file with query sequences
  db                    path to blast database

optional arguments:
  -h, --help            show this help message and exit
  -e EVALUE, --evalue EVALUE
                        evalue for blast search (default: 10)
  -p PERCENT_ID, --percent_id PERCENT_ID
                        Minimum percent identity on blast search (default: 0)
  -m MAX_TARGET_SEQS, --max_target_seqs MAX_TARGET_SEQS
                        Number of aligned sequences to keep (default: 500)
  -q QUERY_COVERAGE, --query_coverage QUERY_COVERAGE
                        Minimum query coverage to retain (default: None)
  -c CPUS, --cpus CPUS  Number of cpus to use (default: -1)
  -i, --identify        Whether to use basta to assign taxopnomy to the hits
                        based on LCA. This is a rough estimate and should be
                        revised carefully (default: False)
  -o OUT_FILENAME, --out_filename OUT_FILENAME
                        name of output (filtered) file (default: hit.hits)
  -f OUTFMT, --outfmt OUTFMT
                        Custom format for BLAST (default: qseqid sseqid pident
                        evalue qcovs qlen length staxid stitle)
```
There are only two positional arguments, the query file and the path to
the BLAST database. Most of the optional characters will filter and/or 
modify the blast search. The two exceptions are `identify`, which will
run basta, and cpus, that can be tailored to your machine (by default it
uses all cores in your machine). **NOTE: if you are in Compute Canada 
you HAVE to pass this value matching the number of cores you requested**.

#### Notes on the BASTA run
justblast performs a **rough** assignment of taxonomy based on BASTA. Here I use
the following parameters:
* -m 10: A minimum of 10 hits have to agree to assign the given taxonomy
* -n 50: Uses the top 50 hits to make the assignment, regardless of you MAX_TARGET_SEQS
* The rest of parameters are either default, or use the same as for the blast.

For basta to run your outfmt must contain **AT LEAST**:
* qseqid
* sseqid
* length
* evalue
* pident


### Dummy Example
Let's say that you have a fasta file called `seqs.fasta`, and you want to
run a blast against the nucleotide database (*nt*) located on you home folder 
(*/home/user*). You want to restrict your blast to an evalue of 1E-10, a percent id 
of 95%, and retrieve only 50 target sequences that have a query coverage of over 90%.
You also want to explore roughly the taxonomic landscape using BASTA. Then you can 
call the program by:

```
justblast.py seqs.fasta /home/user/nt -e 1E-10 -p 95 -m 50 -q 90 -i -o results.hits
```

This will generate a hits file named `results.hits` and will contain the following
columns (note that the outfmt was left default):
1. qseqid 
2. sseqid
3. pident
4. evalue
5. qcovs
6. qlen
7. length
8. staxid
9. stitle

Also a file called `results_annotated.hits` that besides the columns above, will also
contain the column lineage.

It will also contain a PDF with the histograms of all the taxonomic levels identified
called `results_taxadist.pdf'



