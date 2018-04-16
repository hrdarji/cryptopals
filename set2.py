#! /usr/bin/python
import set1
import utils
import binascii

def PKCS7Padding(inputtext,nbytes):
	if len(inputtext) > nbytes:
		print "there seems to be some issue in padding"
		return
	output = ""
	paddingbytes = nbytes - len(inputtext)
	for x in inputtext:

		output += x.encode("hex")
	for i in range(0,paddingbytes):
		output += "0" + hex(paddingbytes)[2] if len(hex(paddingbytes)[2])==1 else hex(paddingbytes)[2] 	
	return output

def DecryptAESinCBC(inputtext,KEY,IV):
	plaintext = ""
	numberOfblocks = (len(inputtext)/len(KEY) if len(inputtext)%len(KEY)==0 else len(inputtext)/len(KEY)+1)/2
	blocks = []

	for i in range(0,numberOfblocks):
		blocks.append(inputtext[i*32:i*32+32])

	BCD = set1.decryptAESinECB(blocks[0].decode("hex"),KEY)
	plaintext = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(BCD,IV.decode("hex")))
	
	for i in range(1,numberOfblocks):
		BCD = set1.decryptAESinECB(blocks[i].decode("hex"),KEY)
		plaintext = plaintext + ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(BCD,blocks[i-1].decode("hex")))
	
	return plaintext

def main():
	#9
	#print PKCS7Padding("YELLOW SUBMARINE",20)	

	#10
	IV = ""
	for i in range(0,16):
		IV+= "0" + hex(0)[2]
	#print IV
	Ciphertext = utils.base64decode(utils.bytesFromFile("inputdata\\10.txt").replace('\n', '').replace('\r', '')).encode("hex")
	print Ciphertext
	print DecryptAESinCBC(Ciphertext,"YELLOW SUBMARINE",IV)

if __name__ == "__main__": main()