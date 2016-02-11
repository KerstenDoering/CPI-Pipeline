#! /bin/sh

# This script recompiles the reranker code, rebuilds the nbest trees
# and retrains and evaluates the reranker itself.

make clean
make reranker 
make -j 2 nbesttrain
make eval-reranker
