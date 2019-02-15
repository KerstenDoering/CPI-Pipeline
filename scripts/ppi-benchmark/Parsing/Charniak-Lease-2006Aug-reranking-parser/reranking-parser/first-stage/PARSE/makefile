default: parseIt

clean:
	rm -f *.o parseIt wwBCTest rParse *~ threads

.C.o:
	g++ $(CFLAGS) -c -O5 $<

WWBCTEST_OBJS = \
	Bchart.o \
	BchartSm.o \
	Bst.o \
	FBinaryArray.o \
	CntxArray.o \
	ChartBase.o \
	ClassRule.o \
	ECArgs.o \
	Edge.o \
	EdgeHeap.o \
	Feat.o \
	Feature.o \
	FeatureTree.o \
	Field.o \
	FullHist.o \
	GotIter.o \
	InputTree.o \
	Item.o \
	Link.o \
	Params.o \
	ParseStats.o \
	SentRep.o \
	ScoreTree.o \
	Term.o \
	TimeIt.o \
	UnitRules.o \
	ValHeap.o \
	edgeSubFns.o \
	ewDciTokStrm.o \
	extraMain.o \
	fhSubFns.o \
	headFinder.o \
	headFinderCh.o \
	utils.o \
	MeChart.o \
	wwBCTest.o 

wwBCTest: $(WWBCTEST_OBJS)
	g++ $(CFLAGS) ${WWBCTEST_OBJS} -o wwBCTest  -D_REENTRANT -D_XOPEN_SOURCE=600 -lpthread


PARSE_OBJS = \
	Bchart.o \
	BchartSm.o \
	Bst.o \
	FBinaryArray.o \
	CntxArray.o \
	ChartBase.o \
	ClassRule.o \
	ECArgs.o \
	Edge.o \
	EdgeHeap.o \
	Feat.o \
	Feature.o \
	FeatureTree.o \
	Field.o \
	FullHist.o \
	GotIter.o \
	InputTree.o \
	Item.o \
	Link.o \
	Params.o \
	ParseStats.o \
	SentRep.o \
	Term.o \
	TimeIt.o \
	UnitRules.o \
	ValHeap.o \
	edgeSubFns.o \
	ewDciTokStrm.o \
	extraMain.o \
	fhSubFns.o \
	headFinder.o \
	headFinderCh.o \
	utils.o \
	MeChart.o \
	parseIt.o 

parseIt: $(PARSE_OBJS)
	g++ $(CFLAGS) $(PARSE_OBJS) -o parseIt   -D_REENTRANT -D_XOPEN_SOURCE=600 -lpthread


OPARSE_OBJS = \
	Bchart.o \
	BchartSm.o \
	Bst.o \
	FBinaryArray.o \
	CntxArray.o \
	ChartBase.o \
	ClassRule.o \
	ECArgs.o \
	Edge.o \
	EdgeHeap.o \
	Feat.o \
	Feature.o \
	FeatureTree.o \
	Field.o \
	FullHist.o \
	GotIter.o \
	InputTree.o \
	Item.o \
	Link.o \
	Params.o \
	ParseStats.o \
	SentRep.o \
	Term.o \
	TimeIt.o \
	UnitRules.o \
	ValHeap.o \
	edgeSubFns.o \
	ewDciTokStrm.o \
	extraMain.o \
	fhSubFns.o \
	headFinder.o \
	headFinderCh.o \
	utils.o \
	MeChart.o \
	oparseIt.o 

oparseIt: $(OPARSE_OBJS)
	g++ $(CFLAGS) $(PARSE_OBJS) -o oparseIt 


FPT_OBJS = \
	ECArgs.o \
	utils.o \
	ParseStats.o \
	finPTest.o

finPTest: $(FPT_OBJS)
	g++ $(CFLAGS) $(FPT_OBJS) -o finPTest



EVALTREE_OBJS = \
	Bchart.o \
	BchartSm.o \
	Bst.o \
	FBinaryArray.o \
	CntxArray.o \
	ChartBase.o \
	ClassRule.o \
	ECArgs.o \
	Edge.o \
	EdgeHeap.o \
	Feat.o \
	Feature.o \
	FeatureTree.o \
	Field.o \
	FullHist.o \
	GotIter.o \
	InputTree.o \
	Item.o \
	Link.o \
	Params.o \
	ParseStats.o \
	SentRep.o \
	ScoreTree.o \
	Term.o \
	TimeIt.o \
	UnitRules.o \
	ValHeap.o \
	edgeSubFns.o \
	ewDciTokStrm.o \
	extraMain.o \
	fhSubFns.o \
	headFinder.o \
	headFinderCh.o \
	utils.o \
	MeChart.o \
	evalTree.o 

evalTree: $(EVALTREE_OBJS)
	g++ $(CFLAGS) ${EVALTREE_OBJS} -o evalTree  -D_REENTRANT -D_XOPEN_SOURCE=600 -lpthread

