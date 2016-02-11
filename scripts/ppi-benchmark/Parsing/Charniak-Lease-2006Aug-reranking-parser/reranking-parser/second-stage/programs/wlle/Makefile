SOURCES = avper.cc cvlm.cc cvwlle.cc data.c gavper.cc lm.cc oracle.cc wavper.cc wlle.cc
TARGETS = avper cvlm gavper # lm oracle wavper
OBJECTS = $(patsubst %.l,%.o,$(patsubst %.c,%.o,$(SOURCES:%.cc=%.o)))

CC = gcc

all: $(TARGETS)

lm: liblmdata.a lm.o
	$(CXX) lm.o liblmdata.a $(TAO_PETSC_LIBS) -o lm

cvlm: liblmdata.a cvlm.o
	$(CXX) cvlm.o liblmdata.a $(TAO_PETSC_LIBS) -o cvlm

cvlm-nolib: cvlm.o lmdata.o
	$(CXX) cvlm.o lmdata.o $(TAO_PETSC_LIBS) -o cvlm-nolib

lnne: libdata.a lnne.o 
	$(CXX) lnne.o libdata.a $(TAO_PETSC_LIBS) -o lnne

avper: avper.o liblmdata.a
	$(CXX) $^ -o $@ 

gavper: gavper.o liblmdata.a 
	$(CXX) $^ -o $@ 

wavper: wavper.o liblmdata.a
	$(CXX) $^ -o $@ 

wlle: libdata.a wlle.o
	$(CXX) wlle.o libdata.a $(TAO_PETSC_LIBS) -o wlle

cvwlle: libdata.a cvwlle.o
	$(CXX) cvwlle.o libdata.a $(TAO_PETSC_LIBS) -o cvwlle

oracle: libdata.a oracle.o
	$(CXX) oracle.o libdata.a -o oracle

libdata.a: data.o
	ar rcv libdata.a data.o; ranlib libdata.a

liblmdata.a: lmdata.o
	ar rcv liblmdata.a lmdata.o; ranlib liblmdata.a

# TAO stuff

# PETSC_DIR = /usr/local/share/petsc
# PETSC_ARCH = linux
# TAO_DIR = /usr/local/share/tao
# BOPT = O_c++

TAO_PETSC_INCLUDE = -I${PETSC_DIR} -I${PETSC_DIR}/bmake/linux -I${PETSC_DIR}/include -I${PETSC_DIR}/include/mpiuni -I${TAO_DIR} -I${TAO_DIR}/include

TAO_PETSC_LIBS = -L${TAO_DIR}/lib/${PETSC_ARCH} -ltaopetsc -ltao -Wl,-rpath,${TAO_DIR}/lib/${PETSC_ARCH} -Wl,-rpath,${PETSC_DIR}/lib/${PETSC_ARCH} -L${PETSC_DIR}/lib/${PETSC_ARCH} -lpetscsnes -lpetscksp -lpetscdm -lpetscmat -lpetscvec -lpetsc   -Wl,-rpath,${PETSC_DIR}/lib/${PETSC_ARCH} -L${PETSC_DIR}/lib/${PETSC_ARCH} -lmpiuni -llapack -lblas -lm -lstdc++ -lgcc_s


CFLAGS = -MMD -O6 -ffast-math -fstrict-aliasing -Wall -finline-functions $(GCCFLAGS)
# CFLAGS = -g -MMD -O6 -ffast-math -fstrict-aliasing -Wall -finline-functions $(GCCFLAGS)
CXXFLAGS =  ${CFLAGS} ${TAO_PETSC_INCLUDE} 

# end of TAO stuff

.PHONY: real-clean
real-clean: clean

.PHONY: clean
clean:
	rm -fr *.a *.d *.o *~ $(TARGETS)

# this command tells GNU make to look for dependencies in *.d files
-include $(patsubst %.l,%.d,$(patsubst %.c,%.d,$(SOURCES:%.cc=%.d)))
