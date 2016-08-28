#arguments <test_directory> <train_directory>

import audiodata
import os, sys
from sklearn import tree

vuvClf = tree.DecisionTreeClassifier()

def wavList(indir):
	infiles = [f for f in os.listdir(indir) if f.endswith('.wav')]
	return infiles;
		
def train(directory):
	global vuvClf
	data = []
	cls = []
	
	files = wavList(directory)	
	
	for f in files:
		filename = directory + f[:-4]
		d, c = audiodata.getData(filename)
		data.extend(d)
		cls.extend(c)
	
	vuvClf = vuvClf.fit(data, cls)
	
	return 1

def test(directory):
	global vuvClf
	files = wavList(directory)
	
	for f in files:
		filename = f[:-4]
		d, c = audiodata.getData(directory + filename)
		p = vuvClf.predict(d)
		miss = len(filter(lambda x: x[0] <> x[1], zip(c, p)))
		mis_p = (miss*100)/len(c)
		print("Speech recording " + filename + ".wav misses: " + str(miss) + "/" + str(len(c)) + " (" + str(mis_p) + "%)")
	
	return 1	
        	
def main(argv):
	testdir = argv[0]
	traindir = argv[1]
	
	train(traindir)
	test(testdir)

if __name__ == "__main__":
   main(sys.argv[1:])
