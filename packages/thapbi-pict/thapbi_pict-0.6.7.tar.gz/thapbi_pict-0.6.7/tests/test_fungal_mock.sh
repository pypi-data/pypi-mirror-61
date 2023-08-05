#!/bin/bash

# Copyright 2020 by Peter Cock, The James Hutton Institute.
# All rights reserved.
# This file is part of the THAPBI Phytophthora ITS1 Classifier Tool (PICT),
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

IFS=$'\n\t'
set -euo pipefail

export TMP=${TMP:-/tmp}

echo "Preparing sample data for fungal mock communities example"

rm -rf $TMP/fungal_mock_1
mkdir $TMP/fungal_mock_1
mkdir $TMP/fungal_mock_1/raw_data/
mkdir $TMP/fungal_mock_1/intermediate
mkdir $TMP/fungal_mock_1/summary
mkdir $TMP/fungal_mock_1/expected/
for f in tests/fungal_mock/amp_lib_one/expected/*.known.tsv; do ln -s $PWD/$f $TMP/fungal_mock_1/expected/ ; done



# Idea here is to mimic what "thapbi_pict pipeline" would do if we had
# the FASTQ files here:
# thapbi_pict pipeline -i sample_data/raw_data/ \
#	    -s $TMP/fungal_mock/intermediate \
#	    -o $TMP/fungal_mock/summary -r fungal-mock \
#	    -t tests/fungal_mock/site_metadata.tsv \
#            -c 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 -x 16 -f 20


echo "=================================="
echo "Decompressing prepare-reads output"
echo "=================================="
time tar -jxvf tests/fungal_mock/intermediate.tar.bz2 -C $TMP/fungal_mock/ | wc -l

if [ -d tests/fungal_mock/raw_data/ ]; then
   echo "================================="
   echo "Running fungal mock prepare-reads"
   echo "================================="
   mkdir $TMP/fungal_mock/intermediate_new
   time thapbi_pict prepare-reads -i tests/fungal_mock/raw_data/ -o $TMP/fungal_mock/intermediate_new -n tests/fungal_mock/raw_data/NEGATIVE*.fastq.gz
   for f in $TMP/fungal_mock/intermediate/*.fasta; do
       diff $f $TMP/fungal_mock/intermediate_new/${f##*/}
   done
fi

echo "======================================="
echo "Running fungal mock fasta-nr & classify"
echo "======================================="
thapbi_pict fasta-nr -i $TMP/fungal_mock/intermediate/*.fasta -o $TMP/fungal_mock/all.fasta
diff $TMP/fungal_mock/all.fasta tests/fungal_mock/all.fasta
for M in onebp identity blast; do
    # Writing to stdout to set a single filename.
    # Discarding the comment column, and the header,
    # leaving the most stable core part of the output
    thapbi_pict classify -i $TMP/fungal_mock/all.fasta -o - -m $M | grep -v "^#" | cut -f 1-3 > $TMP/fungal_mock/all.$M.tsv
    diff $TMP/fungal_mock/all.$M.tsv tests/fungal_mock/all.$M.tsv
done

echo "============================"
echo "Running fungal mock classify"
echo "============================"
# Default for -o should be the same next to the inputs, which is fine
time thapbi_pict classify -i $TMP/fungal_mock/intermediate/

echo "=================================="
echo "Running fungal mock sample-summary"
echo "=================================="
time thapbi_pict sample-summary -i $TMP/fungal_mock/intermediate/ \
            -o $TMP/fungal_mock/summary/no-metadata.samples.tsv \
            -e $TMP/fungal_mock/summary/no-metadata.samples.xlsx \
            -r $TMP/fungal_mock/summary/no-metadata.samples.txt
ls $TMP/fungal_mock/summary/no-metadata.samples.*

time thapbi_pict sample-summary -i $TMP/fungal_mock/intermediate/ \
            -o $TMP/fungal_mock/summary/with-metadata.samples.tsv \
            -e $TMP/fungal_mock/summary/with-metadata.samples.xlsx \
            -r $TMP/fungal_mock/summary/with-metadata.samples.txt \
            -t tests/fungal_mock/site_metadata.tsv \
            -c 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 -x 16 -f 20
ls $TMP/fungal_mock/summary/with-metadata.samples.*
if [ `grep -c "^Site: " "$TMP/fungal_mock/summary/with-metadata.samples.txt"` -ne 17 ]; then echo "Wrong site count"; false; fi
if [ `grep -c "^Sequencing sample: " "$TMP/fungal_mock/summary/with-metadata.samples.txt"` -ne 122 ]; then echo "Wrong sample count"; false; fi

# Should be identical apart from row order if discard extra leading columns
# Discarding the header row as only one will still have hash at start
diff <(grep -v "^#" $TMP/fungal_mock/summary/no-metadata.samples.tsv | sort) <(grep -v "^#" $TMP/fungal_mock/summary/with-metadata.samples.tsv | cut -f 16- | sort)

echo "================================"
echo "Running fungal mock read-summary"
echo "================================"
time thapbi_pict read-summary -i $TMP/fungal_mock/intermediate/ \
            -o $TMP/fungal_mock/summary/no-metadata.reads.tsv \
            -e $TMP/fungal_mock/summary/no-metadata.reads.xlxs
ls $TMP/fungal_mock/summary/no-metadata.reads.*
if [ `grep -c -v "^#" $TMP/fungal_mock/summary/no-metadata.reads.tsv` -ne 100 ]; then echo "Wrong unique sequence count"; false; fi
# Expect 99 + total line

time thapbi_pict read-summary -i $TMP/fungal_mock/intermediate/ \
	    -o $TMP/fungal_mock/summary/with-metadata.reads.tsv \
	    -e $TMP/fungal_mock/summary/with-metadata.reads.xlxs \
	    -t tests/fungal_mock/site_metadata.tsv \
	    -c 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 -x 16 -f 20
ls $TMP/fungal_mock/summary/with-metadata.reads.*
if [ `grep -c -v "^#" $TMP/fungal_mock/summary/with-metadata.reads.tsv` -ne 100 ]; then echo "Wrong unique sequence count"; false; fi
# Expect 99 + total line

echo "=============================="
echo "Running fungal mock edit-graph"
echo "=============================="
time thapbi_pict edit-graph -i $TMP/fungal_mock/intermediate/ -o $TMP/fungal_mock/summary/no-metadata.edit-graph.xgmml
if [ `grep -c "<node " $TMP/fungal_mock/summary/no-metadata.edit-graph.xgmml` -ne 99 ]; then echo "Wrong node count"; false; fi
if [ `grep -c "<edge " $TMP/fungal_mock/summary/no-metadata.edit-graph.xgmml` -ne 69 ]; then echo "Wrong edge count"; false; fi

echo "=========================="
echo "Running fungal mock assess"
echo "=========================="
time thapbi_pict assess -i $TMP/fungal_mock/expected/ $TMP/fungal_mock/intermediate/ -o $TMP/fungal_mock/DNA_MIXES.assess.tsv
diff $TMP/fungal_mock/DNA_MIXES.assess.tsv tests/fungal_mock/DNA_MIXES.assess.tsv

echo "$0 - test_fungal_mock.sh passed"
