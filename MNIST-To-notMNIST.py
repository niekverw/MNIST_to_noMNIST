# just a test. 
import os
from struct import unpack
import scipy.misc 
import numpy as np
from collections import Counter

def mkdir(dir):
	try:
		os.stat(os.path.dirname(dir+"/"))
	except:
		os.mkdir(os.path.dirname(dir+"/"))      

def MNIST_To_NotMNIST(imagefile, labelfile):
	outdir=os.path.dirname(imagefile)+"/MNIST/" if os.path.dirname(imagefile) !="" else ("MNIST/")
	mkdir(outdir)
	fimages= open(imagefile, 'rb')
	flabels= open(labelfile, 'rb')
	# images;
	fimages.read(4) #magic number 
	nimg= unpack('>I', fimages.read(4))[0]
	ncol= unpack('>I', fimages.read(4))[0]
	nrow= unpack('>I', fimages.read(4))[0]
	# labels;
	flabels.read(4) #
	nlab=unpack('>I', flabels.read(4))[0]
	#print ( ["images:",nimg,ncol,nrow,"labels:",nrow,nlab])
	if nlab != nimg: 
		raise ValueError('number of images != number of labels')
	nparrImg=np.zeros((nimg,ncol,nrow))
	cntHashes=Counter()
	for i in range(nimg):
		if i % 500 == 0: print("i={}".format(i))
		for r in range(nrow):
			for c in range(ncol):
				img=unpack('>B', fimages.read(1))[0]
				nparrImg[i,r,c]=img
				#print (img)
		l = unpack('>B', flabels.read(1))[0]
		ldir=outdir+"/"+str(l)+"/"
		mkdir(ldir)
		img=scipy.misc.toimage(nparrImg[i],)
		scipy.misc.imsave(ldir+'/'+str(i)+'.png', img) 
		imghash=hash(tuple( np.hstack(nparrImg[i].tolist()) ))
		cntHashes[imghash]+=1
	print("#unique images: {}, #all images: {}".format( len(cntHashes.keys()),nimg  ))

imagefile="train-images-idx3-ubyte" 
labelfile="train-labels-idx1-ubyte"

MNIST_To_NotMNIST(imagefile,labelfile)
