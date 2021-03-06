#!/usr/bin/python
#
# Image Average Hashing + Hamming Distance
# Author: Justin Wong
#
# Usage:
# python hash.py <image1> <image2>

import Image
import os, sys
from opencv.cv import *
import cv

# find the average value
def average(image):
	count = 0
	pix = image.load()
	for i in range(0,8):
		for j in range(0,8):
			count += pix[i, j]
	val = count / 64
	print "Total:\t\t%d" % count
	print "Average:\t%d" % val
	return val

# find the DCT value
def hashDct(image):
	mean = average(image)	
	#src = compute(image, mean, 32)
	#data = src.tostring()
	#ci = Image.fromstring("L", Image.getSize(image), )
	#cvSetData(ci, void * data, len(data))
	src = cv.CreateImageHeader(image.size, cv.IPL_DEPTH_8U, 1)
	data = image.tostring()
	cv.SetData(src, data, len(data))
	dest = cv.CreateImage((32,32), IPL_DEPTH_8U, 1)
	print "1**************"
	#dest = cv.CreateImageHeader(image.size, cv.IPL_DEPTH_8U, 1) 
	#cv.SetData(dest, data, len(data))
	cv.DCT(src, dest, CV_DXT_FORWARD)
	print "2**************"
	dest.save("dctsave.jpg")
	print "Average:\t%d" % mean

# compute the hash
def compute(image, av, size):
	testString = ""
	for i in range(0,size):
		for j in range(0,size):
			pix = image.load()
			if(pix[i, j] >= av):
				pix[i, j] = 1
			else:
				pix[i, j] = 0
			testString += `pix[i, j]`
	print "testString:\t" + testString
	encoded = "%x" % int(testString,2)
	print "Hash:\t\t" + encoded + "\n"
	return encoded
	
# computes the hamming distance
def hamming_distance(s1, s2):
	if len(s1) > len(s2):
		s2 = s2.zfill(len(s1))
	elif len(s2) > len(s1):
		s1 = s1.zfill(len(s2))
	assert len(s1) == len(s2)
	return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

# printing things out
def main():
	if len(sys.argv) <= 1 or len(sys.argv) > 3:
		print "Usage %s: <image1> <image2>" % sys.argv[0]
	im = Image.open(sys.argv[1])
	im = im.resize((8, 8))
	im = im.convert("L")
	avVal = average(im)
	hash1 = compute(im, avVal, 8)
# -------- DCT ----------
	imDct = Image.open(sys.argv[1])
	imDct = imDct.resize((32, 32))
	imDct = imDct.convert("L")
	hashDct(imDct)
# -------- DCT ----------
	print "\nResolution:\t%s" % (im.size,)
	print "Mode:\t\t" + im.mode
	im.save("output.jpg")
	im2 = Image.open(sys.argv[2])
	im2 = im2.resize((8, 8))
	im2 = im2.convert("L")
	avVal2 = average(im2)
	hash2 = compute(im2, avVal2, 8)
	print "-------------Hamming Distance-------------"
	print "Threshold = 26"
	result = hamming_distance(hash1, hash2)	
	if result < 26:
	  print "Hamming distance = %d. Images are similar." % result
	else:
	  print "Hamming distance = %d. Images are not similar" % result

if __name__ == "__main__":
	main()
