#!/usr/bin/python
import threading
import time
import piggyphoto
import os, sys
import shutil
import pygame
from pygame.locals import *

def shellcmd(command):
	print ' =>', command
	os.system(command)

# filename function: returns next sequential filename
def new_filename(storename='lastphoto', increment=True):
	last = eval(open(storename, 'r').read())
	filename = 'DSC' + (4-len(str(last)))*'0' + str(last)
	if increment: last=last+1
	open(storename, 'w').write(str(last))
	return filename

# move files into local subdirectories and SAMBA share at path
def move_files(filename, path='/media/PHOTOBOOTH/', copy=True):
      if copy: cmd='cp '
      else: cmd='mv '
      try:
	print
	print 'filename = ', filename
	print cmd+'raw images...'
	shellcmd(cmd+filename+'_[a-d].jpg '+path+'raw-images')
	print cmd+'dislay images...'
        shellcmd(cmd+filename+'_display.jpg '+path+'for-display')
	print cmd+'print image...'
        shellcmd(cmd+filename+'_print.jpg '+path+'for-print')
	print cmd+'phone image...'
        shellcmd(cmd+filename+'_phone.jpg '+path+'for-phone')
      except:
	print 'PROBLEMS!!'

suffix = [ 'a', 'b', 'c', 'd' ]
finish = 5 # use this with grab_image to complete the composites...

# create PTP connection to camera...
# C = piggyphoto.camera()

def grab_image(filename, i, quiet=True, process=False, usecamera=True):
	if not(quiet): 
		print
		print 'Count down: 3...'
		time.sleep(0.25)
		print '2...'
		time.sleep(0.25)
		print '1...'
		time.sleep(0.25)
		print 'Capturing image', i+1
	else: time.sleep(1)
	# Only capture image if it's one of the four... 
	# This allows generating the final image using the same grab call...
	if i in range(4): 
		# grab from camera or make a copy of the dummy images (for testing...)
		if usecamera: C.capture_image(filename+'_'+suffix[i] + '.jpg')
		else: shellcmd('cp DSCdummy'+str(i+1)+'.jpg '+filename+'_'+suffix[i] + '.jpg')
	open(filename+'_'+suffix[i]+'_done', 'w').write('done') # flag that file is complete...
	if not(quiet): 
		print 'Downloading image', i+1
		print
	if (process==True):
		display_4upHD(filename, i)
		print_4upbig(filename, i)

def process_image(filename, i):
		display_4upHD(filename, i)
		print_4upbig(filename, i)

# function to make full HD (1280x720) display 4-tile-up
def display_4upHD(filename, partial=None):
	x1, x2, y1, y2 = 124, 652, 12, 373
	loc = ['+'+str(x1)+'+'+str(y1)+' ', '+'+str(x1)+'+'+str(y2)+' ', 
		'+'+str(x2)+'+'+str(y1)+' ', '+'+str(x2)+'+'+str(y2)+' ']
        for i in range(4):
		cmd = 'gm composite -resize 504x336 -geometry  ' 
		cmd = cmd + loc[i] + filename + '_' + suffix[i] + '.jpg '
		if i==0: cmd = cmd + ' images/backscreen-hd.jpg'
		else: cmd = cmd + ' boutput.jpg'
        	cmd = cmd + ' -quality 100 boutput.jpg'
	        if (partial==None or partial==i): shellcmd(cmd)
	if (partial==None or partial>3):
		shellcmd('gm composite -geometry +522+243 -resize x233 images/overlay-disp.png  boutput.jpg -quality 95 ' + filename + '_display.jpg')

# function to make full HD (1920x1080) display 4-tile-up
def display_4upfullHD(filename, partial=None):
	x1, x2, y1, y2 = 186, 978, 18, 560
	loc = ['+'+str(x1)+'+'+str(y1)+' ', '+'+str(x1)+'+'+str(y2)+' ', 
		'+'+str(x2)+'+'+str(y1)+' ', '+'+str(x2)+'+'+str(y2)+' ']
        for i in range(4):
		cmd = 'gm composite -resize 756x504 -geometry  ' 
		cmd = cmd + loc[i] + filename + '_' + suffix[i] + '.jpg '
		if i==0: cmd = cmd + ' images/backscreen-hd.jpg'
		else: cmd = cmd + ' boutput.jpg'
        	cmd = cmd + ' -quality 100 boutput.jpg'
	        if (partial==None or partial==i): shellcmd(cmd)
	if (partial==None or partial>3):
		shellcmd('gm composite -geometry +783+365 -resize x350 images/overlay-disp.png  boutput.jpg -quality 95 ' + filename + '_display.jpg')

# generate large print and phone composite image, 4000x6000 and 2000x6000 respectively 
def print_4upbig(filename, partial=None, twostrip=False, nice=False, block=False):
	if nice: nice = 'nice -n 20 '
	else: nice = ''
	x1, ybase, yinc = 120, 996, 1252
	y1, y2, y3, y4 = ybase, ybase+yinc, ybase+2*yinc, ybase+3*yinc	
	loc = ['+'+str(x1)+'+'+str(y1)+' ', '+'+str(x1)+'+'+str(y2)+' ', 
		'+'+str(x1)+'+'+str(y3)+' ', '+'+str(x1)+'+'+str(y4)+' ']
        for i in range(4):
		cmd = 'gm composite -resize 1756x1164 -geometry ' 
		cmd = cmd + loc[i] + filename + '_' + suffix[i] + '.jpg '
		if i==0: cmd = cmd + ' images/background-half-big.jpg'
		else: cmd = cmd + ' output.jpg'
        	cmd = cmd + ' -quality 100 output.jpg'
		if (partial==None or partial==i):
			if block: 
				while (filename+'_'+suffix[i]+'_done' not in os.listdir(os.curdir)):
					pass #if block is true, wait until the file is there 
			shellcmd(nice+cmd)

	if (partial==None or partial>3):
		shellcmd(nice+'gm composite -geometry +250+50 -resize 1500x images/overlay-phone.png  output.jpg -quality 95 ' + filename + '_phone.jpg')
		if twostrip:
			shellcmd(nice+'gm composite -geometry +0+0 ' + filename + '_phone.jpg images/background-big.jpg -quality 100 done.jpg')
			shellcmd(nice+'gm composite -geometry +2001+0 ' + filename + '_phone.jpg done.jpg -quality 100 done.jpg')
			shellcmd(nice+'gm convert -stroke gray -draw "line 2000,0 2000,6000" done.jpg -quality 95 ' + filename + '_print.jpg')

def print_4upbigall(filename, i):
	#print_4upbig(filename, twostrip=True, nice=True, block=True)
	print_4upbig(filename, twostrip=False, nice=True, block=True)
	move_files(filename, path='/media/PHOTOBOOTH/', copy=True)	
	move_files(filename, path='/media/files-n-stuff/', copy=True)
	move_files(filename, path='/media/backup/', copy=False)
	print 'Deleting flag files...'
	shellcmd('rm '+ filename+'_*_done')
	

# threaded compositing after all four photos taken...
def do_thread(function, filename, i):
	t_ = threading.Thread( target=function, args=(filename, i) )
	t_.start()
	return t_


#size = width, height = 960, 540
#camerasize = camw, camh =  810,540
size = width, height = 1230, 692
camerasize = camw, camh =  1037,692
cameraloc = (width-camw)/2, 0
black = (0,0,0)
white = (255,255,255)

def waitforkey(key, quitable = True):
	userkey = False
	while not(userkey):
		time.sleep(1)
		for event in pygame.event.get():
			#print repr(event)
			if event.type == QUIT: sys.exit()
			elif event.type == KEYDOWN: 
				#print 'keydown...'
				if event.key in key: return
				if quitable and event.key == K_q: sys.exit()
	pygame.event.clear()

def fillscreen(screen, color):
	screen.fill(color)
	pygame.display.flip()

def displayimage(screen, filename, size, location=(0,0)):
		image = pygame.image.load(filename)
		imagerect = image.get_rect()
		image = pygame.transform.scale(image, size)
		screen.blit(image, location)
		pygame.display.flip()

def flashtext(duration, rate, screen, text, size, location=None):
	bgwhite = pygame.Surface(screen.get_size())
	bgblack = pygame.Surface(screen.get_size())
	bgwhite = bgwhite.convert()
	bgblack = bgblack.convert()
	bgwhite.fill(white)
	bgblack.fill(black)
	
	fontname = pygame.font.match_font('freeserif')
	font = pygame.font.Font(fontname, 128)
	textw = font.render(text, 1, white)
	textb = font.render(text, 1, black)
	textwpos = textw.get_rect()
	textbpos = textb.get_rect()
	if location==None:
		textwpos.centerx = textbpos.centerx = bgwhite.get_rect().centerx	
		textwpos.centery = textbpos.centery = bgwhite.get_rect().centery
	else:
		w,h = location
		textwpos.centerx = textbpos.centerx = w
		textwpos.centery = textbpos.centery = h
	bgwhite.blit(textb, textbpos)
	bgblack.blit(textw, textbpos)

	start = time.time()
	while (time.time()-start < duration):
		screen.blit(bgblack, (0,0))
		pygame.display.flip()
		time.sleep(rate/2.)
		screen.blit(bgwhite, (0,0))
		pygame.display.flip()
		time.sleep(rate/2.)


def showtext(screen, text, size, location=None):
	bgwhite = pygame.Surface(screen.get_size())
	bgwhite = bgwhite.convert()
	bgwhite.fill(black)#white)
	
	fontname = pygame.font.match_font('freeserif')
	font = pygame.font.Font(fontname, 128)
	textb = font.render(text, 1, white)#black)

	textbpos = textb.get_rect()
	if location==None:
		textbpos.centerx = bgwhite.get_rect().centerx	
		textbpos.centery = bgwhite.get_rect().centery
	else:
		w,h = location
		textbpos.centerx = w	
		textbpos.centery = h
	bgwhite.blit(textb, textbpos)

	screen.blit(bgwhite, (0,0))
	pygame.display.flip()


def toggle_fullscreen():
	screen = pygame.display.get_surface()
	tmp = screen.convert()
	caption = pygame.display.get_caption()
	cursor = pygame.mouse.get_cursor()

	w,h = screen.get_width(),screen.get_height()
	flags = screen.get_flags()
	bits = screen.get_bitsize()

	pygame.display.quit()
	pygame.display.init()

	screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
	screen.blit(tmp, (0,0))
	pygame.display.set_caption(*caption)

	pygame.key.set_mods(0)

	pygame.mouse.set_cursor(*cursor)

	return screen






