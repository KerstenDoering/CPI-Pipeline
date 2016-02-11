#Generate the learning format for AllGraph Kernel
cp="/home/philippe/workspace/learning-format-api/"
data="/home/philippe/workspace/Kernels/airola/data/"
mkdir -p ${data}CV/corpus

for file in ${data}CC/corpus/*.xml.gz; 
do
    java -Xmx2g -classpath ${cp}bin/:${cp}src/main/resources/jargs.jar org.learningformat.transform.AllGraphTransformer -f $file -s ${data}splits/ -o ${data}CV/corpus;
done

find  ${data}CV/corpus/  -name *.txt -exec gzip {} \;


