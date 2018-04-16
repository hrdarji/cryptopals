#!/usr/bin/env

import utils
import binascii
import re
import itertools
import base64
from Crypto.Cipher import AES

#1.1
def hex2base64(inputfile):
	base64list = []
	for aline in utils.openFile(inputfile):
		base64list.append(binascii.b2a_base64(aline.decode("hex")))
	return base64list

#1.2
def fixedXOR(str1,str2):
	str1 = str1.decode("hex")
	#print " str1 hex decoded : ",str1
	str2 = str2.decode("hex")
	#print " str2 hex decoded : ",str2
	binary_Str1 = map(bin,bytearray(str1))
	#print " str1 bin : ",binary_Str1
	binary_Str2 = map(bin,bytearray(str2))
	#print " str2 bin : ",binary_Str2
	hexoutput = []
	for a,b in zip(binary_Str1,binary_Str2):
		hexoutput.append(chr(int(a,base=2)^int(b,base=2)).encode("hex"))
		#print int(a,base=2)^int(b,base=2), chr(int(a,base=2)^int(b,base=2)).encode("hex")
	hexoutputstring = ''.join(hexoutput)
	return hexoutputstring

#1.3
def sbXORcipher(intputstring):
	#intputstring = intputstring.strip()
	possiblelist = []
	possibledict = {}
	try:
		intputcharlist = list(intputstring.decode("hex"))
		#print intputcharlist
	
		for i in range(256):
			templist = []
			for j in intputcharlist:
				templist.append(chr(int(bin(ord(j)),base=2)^int((bin(i)),base=2)))
		#print ''.join(templist)
			possiblelist.append("".join(templist))
			possibledict[i]=templist

		#print possibledict
		#print "key : ",chr(i)," output: ", ''.join(templist).replace("\x00", " ")
	except:
		print "There was some error in sbXORcipher(). check!"
		pass
	return possibledict

# The blow method is same as 1.3 but returns a list instead of a dictionary.
def sbXORcipherlist(intputstring):
	#intputstring = intputstring.strip()
	possiblelist = []
	possibledict = {}
	try:
		intputcharlist = list(intputstring.decode("hex"))
		#print intputcharlist
	
		for i in range(256):
			templist = []
			for j in intputcharlist:
				templist.append(chr(int(bin(ord(j)),base=2)^int((bin(i)),base=2)))
		#print ''.join(templist)
			possiblelist.append("".join(templist))
			possibledict[i]=templist

		#print possibledict
		#print "key : ",chr(i)," output: ", ''.join(templist).replace("\x00", " ")
	except:
		print "There was some error in sbXORcipherlist(). check!"
		pass
	return possiblelist

#the below method is to find english chars form a string list
def findeng(inputlist):
	scoredict={}
	for aline in inputlist:
		linescore = 0

		aline = aline.replace("\x00", " ")
		regex = re.compile('[^a-zA-Z\', ]')
		aline = regex.sub('',aline)
		linescore = len(aline)

		#for achar in list(aline.replace("\x00", " ")):
		#	a = ord(achar)
		#	if ( (a>64 and a<91) or (a>96 and a<123)):
		#		linescore=linescore+1
		
		scoredict[aline]=linescore
	#print scoredict
	return max(scoredict, key = scoredict.get)

#the below method is to find english chars form a dictionary
def findengfromdict(inputdict):
	scoredict={}
	outputdict = {}
	#print inputdict
	for chr_ord,value in inputdict.iteritems():
		linescore = 0
		tempstring = ''.join([x for x in value])
		regex = re.compile('[^a-zA-Z\', ]')
		tempstring = regex.sub('',tempstring)
		tempstring = tempstring.replace("\x00", " ")
		linescore = len(tempstring)
		scoredict[chr_ord]=linescore
	print scoredict
	outputstring = "".join([x for x in inputdict[max(scoredict, key = scoredict.get)]])
	outputdict[chr(max(scoredict, key = scoredict.get))]= outputstring
	return outputdict
	
#1.4
def sbXORfromfile(inputfile):
	p = []
	for aline in utils.openFile(inputfile):
		p.extend(sbXORcipherlist(aline.strip()))
		#print aline.strip()
	#for item in p:
		#print item.replace("\x00", " ")
	return findeng(p)

#1.5
def repeatingkeyXOR(inputtext,key):
	#for aline in utils.openFile(inputfile)
	#inputtext = utils.bytesFromFile(inputfile)
	hexoutput = ""
	fullkey = ""
	for i in range(0,len(inputtext)):
		fullkey+= key[i%len(key)]
	#print "key :", fullkey
	for a,b in itertools.izip(inputtext,fullkey):
		#print ord(a), " ^ ", ord(b), " = ", ord(a) ^ ord(b)
		temphex = hex(ord(a) ^ ord(b)).split('x')[-1]
		hexoutput +=  temphex if len(temphex)==2 else "0"+temphex
	return hexoutput

#1.6
def BreakrepeatingkeyXOR(inputfile):
	hammingdict = {}
	inputdata = utils.base64decode(utils.bytesFromFile(inputfile).replace('\n', '').replace('\r', ''))
	#with open("inputdata.txt", 'wb') as x_file:
	#	x_file.write(inputdata)
	#print len(inputdata)
	#print utils.bytesFromFile(inputfile).replace('\n', '').replace('\r', '')
	inputbytearray = []

	for aChar in inputdata:
		inputbytearray.append(ord(aChar))

	#print len(inputbytearray)
	for i in range(6,40):
		#print "Let's try keylength = ",i
		byte1 = ""
		byte2 = ""
		byte3 = ""
		byte4 = ""
		byte5 = ""
		for j in range(0,i):
			byte1 += chr(inputbytearray[j])
			byte2 += chr(inputbytearray[i+j])
			byte3 += chr(inputbytearray[i+j+i])
			byte4 += chr(inputbytearray[i+j+i+i])
			byte5 += chr(inputbytearray[i+j+i+i+i])
		
		hdistance1 = utils.hamming(byte1,byte2)/float(i)
		hdistance2 = utils.hamming(byte2,byte3)/float(i)
		hdistance3 = utils.hamming(byte3,byte4)/float(i)
		hdistance4 = utils.hamming(byte4,byte5)/float(i)
		avg = (hdistance1+hdistance2+hdistance3+hdistance4)/float(4)
		hammingdict[i] = avg
	#print hammingdict
	KEYSIZE = min(hammingdict, key=hammingdict.get)
	print "Hmm.. I predict that the key length is", KEYSIZE
	
	numberofblocks = len(inputbytearray)/KEYSIZE if len(inputbytearray)%KEYSIZE==0 else len(inputbytearray)/KEYSIZE+1
	#print numberofblocks
	blocksofKEYSIZE = []
	transposedData = []
	templist = []
	
	for i in range(0,len(inputbytearray)):
		templist.append(inputbytearray[i])
		if len(templist)==KEYSIZE or i==len(inputbytearray)-1:
			blocksofKEYSIZE.append(templist)
			templist = []

	for i in range(0,len(inputbytearray)%KEYSIZE):
		templist=[]
		for j in range(0,numberofblocks):
			templist.append(blocksofKEYSIZE[j][i])
		transposedData.append(templist)

	for i in range(len(inputbytearray)%KEYSIZE,KEYSIZE):
		templist=[]
		for j in range(0,numberofblocks-1):
			templist.append(blocksofKEYSIZE[j][i])
		transposedData.append(templist)

	KEY = ""

	for i in range(0,len(transposedData)):
		tempstr = "".join([chr(x) for x in transposedData[i]])
		#print tempstr
		tempkeydict = findengfromdict(sbXORcipher(tempstr.encode("hex")))
		for key in tempkeydict:
			KEY += key

	print "KEY = ",KEY
	print "Here's the decryption:\n"
	return repeatingkeyXOR(inputdata,KEY).decode("hex")

#1.7
def decryptAESinECB(inputdata,KEY):
	return AES.new(KEY,AES.MODE_ECB).decrypt(inputdata)

#1.8
def detectAESinECB(inputlist):
	inputlist = utils.openFile(inputlist)
	outputlist = []
	for aline in inputlist:
		aline = aline.replace('\n','').replace('\r','').decode("hex")
		#print len(aline)
		aline_list = []
		for i in range(0,len(aline)/16):
			#print i*16, i*16+16
			#print aline[i*16:i*16+16]
			if aline[i*16:i*16+16] in aline_list:
				if aline.encode("hex") not in outputlist:
					outputlist.append(aline.encode("hex"))
			aline_list.append(aline[i*16:i*16+16])
	return outputlist

def main():

	#1.1
	base64 = hex2base64('inputdata\\hexinput.txt')
	for item in base64:
		print item

	#1.2
	print fixedXOR('1c0111001f010100061a024b53535009181c','686974207468652062756c6c277320657965')

	#1.3
	pdict = sbXORcipher('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
	print findengfromdict(pdict)

	#1.4
	print sbXORfromfile('inputdata\\sbXORinput.txt')

	#1.5
	print repeatingkeyXOR("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal","ICE")

	#1.6
	print BreakrepeatingkeyXOR("inputdata\\breakrepeatingXOR.txt")

	#1.7
	text = utils.base64decode(utils.bytesFromFile("inputdata\\AESin.txt").replace('\n', '').replace('\r', ''))
	print decryptAESinECB(text,"YELLOW SUBMARINE")

	#1.8
	print detectAESinECB("inputdata\\1.8.txt")
		
if __name__ == "__main__": main()