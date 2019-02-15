# Makefile for BLLIP/reranking-parser/second-stage
#
# Mark Johnson, 15th November 2005
#

export CFLAGS
export CXXFLAGS

.PHONY: all
all:
	$(MAKE) -C programs

.PHONY: clean
clean:
	rm -fr *~ nbest features eval
	$(MAKE) -C programs clean

.PHONY: real-clean
real-clean: clean
	rm -fr models
	$(MAKE) -C programs real-clean
