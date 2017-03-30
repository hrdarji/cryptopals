import itertools
import binascii
import base64

def openFile(fname):
	with open(fname) as f:
		return f.readlines()

def bytesFromFile(fname):
	with open(fname, 'r') as myfile:
		return myfile.read()

def hamming(str1,str2):
	hammingdistance = 0
	#print "hamming ", str1, " ",str2
	if len(str1)!=len(str2):
		print "ohh no, both string are not equal length."
		return
	for a,b in itertools.izip(str1,str2):
		#print charTobin(a)," ", charTobin(b)
		for x,y in itertools.izip(charTobin(a),charTobin(b)):
			if (x != y):
				hammingdistance += 1
	return hammingdistance

def charTobin(i):
	out = ""
	if len(i)!=1:
		print "I'm just expeting a char"
		return 
	out = bin(ord(i))
	out = out[2:]
	#print out
	while len(out)!=8:
		out = "0" + out
	return out

def base64decode(text):
	return base64.b64decode(text)