#!/usr/bin/python
import threading
import time
import piggyphoto
import os, sys
import shutil
import pygame
from string import split,join
from pygame.locals import *

# list with raw image suffixes, used for appending to files as they are created
suffix = [ 'a', 'b', 'c', 'd' ]

# execute a shell command, printing it to the console for debugging purposes...
def shellcmd(command):
	print ' =>', command
	os.system(command)

# new filename generation function: returns next sequential filename
def new_filename(storename='lastphoto', increment=True):
	last = eval(open(storename, 'r').read())
	filename = 'DSC' + (4-len(str(last)))*'0' + str(last)
	if increment: last=last+1
	open(storename, 'w').write(str(last))
	return filename


# dictionary to store templates for composite images, basically sizes, locations, and temp file names
templates = {'display':[ ['504x336', '+124+12', 'images/backscreen-hd.jpg', 'boutput.jpg'],
			['504x336', '+124+373', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+652+12', 'boutput.jpg', 'boutput.jpg'],
			['504x336', '+652+373', 'boutput.jpg', 'boutput.jpg'],
			['+522+243', 'x233', 'images/overlay-disp.png', 'boutput.jpg'] ],

	      'phone':[ ['1756x1164', '+120+996', 'images/background-half-big.jpg', 'output.jpg'],
			['1756x1164', '+120+2248', 'output.jpg', 'output.jpg'],
			['1756x1164', '+120+3500', 'output.jpg', 'output.jpg'],
			['1756x1164', '+120+4752', 'output.jpg', 'output.jpg'],
			['+250+50', '1500x', 'images/overlay-phone.png', 'output.jpg'] ]
		}	

# generate a composite image from a template, horizontal or vertical, abstracted 
#    and genericized so that various combinations of templates can be created...
def generate_composite(template, filename, blocking=True, generateprint=False):
	# base graphicsmagick commands to generate composites...
	interrim = 'gm composite -resize &ARG1 -geometry &ARG2 &FILENAME_&I.jpg &ARG3 -quality 98 &ARG4 '
	ending = 'gm composite -geometry &ARG1 -resize &ARG2 &ARG3 &ARG4 -quality 95 &FILENAME_&TEMPLATE.jpg '
	
	# generate interrim commands...
	for i in range(1,5):
		command = join(split(interrim, '&FILENAME'), filename)
		command = join(split(command, '&I'), suffix[i-1])
		for j in range(4):
			command = join(split(command, '&ARG'+str(j+1)), templates[template][i-1][j])
		if blocking:
			while (filename+'_'+suffix[i-1]+'_done' not in os.listdir(os.curdir)):
				pass #if block is true, wait until the file is there 
		shellcmd(command)

	# generate ending command...
	command = join(split(ending, '&FILENAME'), filename)
	command = join(split(command, '&TEMPLATE'), template)
	for j in range(4):
		command = join(split(command, '&ARG'+str(j+1)), templates[template][4][j])
	shellcmd(command)

	# do this extra step to make a double print strip, 
	#    assumes use of 'phone' template/ending file...
	#    (requires a vertical 2000x6000 final composite image to start)
	if generateprint: 
		shellcmd('gm composite -geometry +0+0 ' + filename + '_phone.jpg images/background-big.jpg -quality 100 done.jpg')
		shellcmd('gm composite -geometry +2001+0 ' + filename + '_phone.jpg done.jpg -quality 100 done.jpg')
		shellcmd('gm convert -stroke gray -draw "line 2000,0 2000,6000" done.jpg -quality 95 ' + filename + '_print.jpg')

# generate print fascade to generate_composite...
def generate_print(template, filename, blocking=True, generateprint=True):
	generate_composite(template, filename, blocking, generateprint)

# delete the temporary files created during creation of composites...
def cleanup_temp_files(filename):
	# remove temp files...
	shellcmd('rm *output.jpg done.jpg '+filename+'*done')

# filename function: returns next sequential filename (as a string)
def new_filename(storename='lastphoto', increment=True):
	last = eval(open(storename, 'r').read())
	filename = 'DSC' + (4-len(str(last)))*'0' + str(last)
	if increment: last=last+1
	open(storename, 'w').write(str(last))
	return filename

# function to grab the sequence of raw images. 
#    copied dummy images to a new 'filename' for testing 
#    so that camera does not need to be used...
def grab_image(filename, i, usecamera=True):
	# Only capture image if it's one of the four... 
	if i in range(4): 
		# grab from camera or make a copy of the dummy images (for testing...)
		if usecamera: C.capture_image(filename+'_'+suffix[i] + '.jpg')
		else: shellcmd('cp images/DSCdummy'+str(i+1)+'.jpg '+filename+'_'+suffix[i] + '.jpg')
	open(filename+'_'+suffix[i]+'_done', 'w').write('done') # flag that file is complete...





