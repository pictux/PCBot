import platform
if 'edison' in platform.platform():
	edison=True
	print("I'm running on a edison")
else:
	edison=False
	print("I'm not running on a edison")


if edison==True:
	import mraa

import urllib
from urlparse import urlparse
from os.path import splitext

import sys
sys.path.insert(0, './Python-Thermal-Printer-master')

from Adafruit_Thermal import *
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = False

#open the serial port on TX RX on the edison
if edison==True:
	x=mraa.Uart(0)

#Instantiate the pronter
if edison==True:
	printer = Adafruit_Thermal("/dev/ttyMFD1", 19200, timeout=5)


def printImageByUrl (url):

	urlpath=urlparse(url)
	root, ext = splitext(urlpath.path)
	print root
	print ext


	filename='./gfx/printfile'+ext
	urllib.urlretrieve(url, filename)


	#here I downscale the Image
	baseWidth = 384

	# Open the image file.
	try:
	    im =  Image.open(filename)

	except:
	    print "Unable to load image"
  	# Calculate the height using the same aspect ratio
	widthPercent = (baseWidth / float(im.size[0]))
	height = int((float(im.size[1]) * float(widthPercent)))
	size = (baseWidth, height)

	try:
	    im.load()
	except IOError:
	    pass # You can always log it to logger

	newName="./gfx/printfile_scaled"+ext
	#here I really scale the image
	im.thumbnail(size,Image.ANTIALIAS)
	im.save(newName)

	#print the image on the printer
	printer.printImage(Image.open(newName))

	#add some empty lines
	printer.feed(7)
