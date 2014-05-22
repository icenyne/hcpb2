#!/usr/bin/python
import sys, threading, time
import pygame 
from pygame.locals import *
from pbgmlib import *
from progress import *
import random

queue = {}

# prompts for in between photos...
random.seed()
prompt = [ 'Make a fist', 'Look up', 'Close your eyes', 'Look at each other', 
	'Fist bump', 'Wave', 'Smile', 'Frown', 'Look angry', 'Open your mouth' ]

# assume we will move files unless command line arg says no...
move=True
if 'nomove' in sys.argv:
	print 'Not moving files...'
	move=False

# assume we will use camera unless command line arg says no...
if 'nousecamera' in sys.argv:
	camera_arg=False
else:
	C = piggyphoto.camera()
	camera_arg=True


# this should be rolled into the filename function but for now it's here...
last = eval(open('lastphoto', 'r').read())
print 'Change current photo number '+str(last)+'?'
temp = raw_input( 'Enter valid new number or nothing to keep: ')
if temp not in ['']: 
	last = eval(temp) 
	open('lastphoto', 'w').write(str(last))


pygame.init()
screen = pygame.display.set_mode(size)
#toggle_fullscreen()

# main run loop...
while 1:
	showtext(screen, "Push a button to start", 100)

	waitforkey([K_g, K_r, K_y])

	# get the next sequential filename from nonvolatile store (a file...)
	filename = new_filename(increment=True) 

	totaltime = time.time()

	# grab and begin processing four images...
	for i in range(4):  
		
		fillscreen(screen, black)
		# show text prompting between pics so they can be shown later during processing...
#		showtext(screen, prompt[random.randrange(len(prompt))], 100)
		showtext(screen, 'Image: '+str(i+1), 100)
		time.sleep(1.75)

		flashtext(1.1, 0.30, screen, "Look at camera", 100, (width/2, height*3/4))
		showtext(screen, '', 200)
		grab_image(filename, i, usecamera=camera_arg) # take photo with camera
		
	#	showtext(screen, 'Importing...', 100)
		displayimage(screen, filename+'_'+suffix[i]+'.jpg', camerasize, cameraloc)

		start = time.time()
		# process incrementally only the display image...
		t_disp = do_thread(display_4upHD, filename, i)
		# kick off phone and print processing with blocking, so it can run in background...
		if (i==0): queue[filename] = do_thread(print_4upbigall, filename, finish)

		time.sleep(1.5) # wait before entering loop...  
		while ( t_disp.isAlive() ):# or t_print.isAlive() ): 
			time.sleep(1)
			print 'processing...'
		print 'Proc time: ', time.time()-start



	# finish out the compositing...
	start = time.time()
	t_disp = do_thread(display_4upHD, filename, finish)

	showtext(screen, 'Singles', 100)
	time.sleep(1)

	# show the single images... 
	for i in range(4):  	
		showtext(screen, str(i+1), 200)
		time.sleep(0.5)
		displayimage(screen, filename+'_'+suffix[i]+'.jpg', camerasize, cameraloc)
		time.sleep(3)

	while ( t_disp.isAlive() ):
		time.sleep(3)


	showtext(screen, 'Composite', 100)
	time.sleep(0.5)
	# show the composite...
	displayimage(screen, filename+'_display.jpg', size)
	time.sleep(5)

	while (queue[filename].isAlive() ): 
		time.sleep(3)
		print 'processing...'

	print 'Proc time: ', time.time()-start
	queue.pop(filename, None) # delete thread from queue, since it's finished...

	print 'Total time: ', time.time()-totaltime
	pygame.event.clear() # clear to make sure no buttons were pushed while processing...



