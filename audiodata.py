#Not to be used directly, only call getData function via python

from scipy.io import wavfile
import pysptk as sptk
from numpy import float64

voiced = ['a', 'a:', 'e', 'e:', 'i', 'i:', 'o', 'o:', 'u', 'u:', 'r', 'r:', 'd', 'g', 'dz', 'DZ', 'j', 'l', 'L', 'm', 'n', 'N', 'v', 'z', 'Z', 'b']
unvoiced = ['c', 'cc', 'C', 'f', 'h', 'p', 's', 'S', 't', 'k']

def shortTermEnergy(sample):
	return float64(sum( [ abs(x)**2 for x in sample ] ) / len(sample))

def getData(filename, lpc_o):
	c = []
	d = []
	
	rate, wavdata = wavfile.read(filename + ".wav")
	labdata = open(filename + ".lab")
	
	for ln in labdata.readlines():
		sta, end, cls = ln.split()

		sta = int(sta) * rate / 10000000
		end = int(end) * rate / 10000000 - 1
		
		data = []
		
		fr = float64(wavdata[sta:end])
		fr = fr * sptk.blackman(len(fr))
		
		data.extend(sptk.lpc(fr, order = int(lpc_o)))
		data.append(shortTermEnergy(fr))
		
		if cls in voiced:
			c.append('v')
			d.append(data)
		elif cls in unvoiced:
			c.append('u')
			d.append(data)
		
	return (d, c)
