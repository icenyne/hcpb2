# many dependencies, all should be brought in with this import...
from photoboothlib import *

# ========= COMMAND LINE ARGUMENTS =============

# use camera or dummy source images...
if 'nousecamera' in sys.argv:
	camera_arg=False
else:
	camera_arg=True

# move the files when done? Assume true...
move=True
if 'nomove' in sys.argv:
	print 'Not moving files...'
	move=False

# set lastphoto via command line... 
lastphoto=False
for i in sys.argv:
	if 'lastphoto' in i:
		lastphoto = True
		temp = split(i, '=')[1]
		break
if not(lastphoto):
	# this should be rolled into the filename function but for now it's here...
	last = eval(open('lastphoto', 'r').read())
	print 'Change current photo number '+str(last)+'?'
	temp = raw_input( 'Enter valid new number or nothing to keep: ')
if temp not in ['']: 
	last = eval(temp) 
	open('lastphoto', 'w').write(str(last))

# increment output photo index? default is true...
increment=True
if 'noincrement' in i:
	increment = False

# ========= DONE COMMAND LINE ARGUMENTS =============

# verify command line args...
print 'nousecamera:', repr(camera_arg)
print 'nomove:', repr(move)
print 'lastphoto:', last
print 'increment:', repr(increment)

filename= new_filename()
print 'filename:', filename

# prime threads for compositing images...
t_ = []
t_.append( threading.Thread(target=generate_composite, args=('display', filename)) )
t_.append( threading.Thread(target=generate_composite, args=('phone', filename)) )
# t_.append( threading.Thread(target=generate_print, args=('phone', filename)) )
for i in t_: i.start()

start = time.time()
for i in range(4):
     print 
     print 'Grabbing image: ', i+1
     grab_image(filename, i, camera_arg)
     time.sleep(1.5)

living=True
while ( living ):# or t_print.isAlive() ): 
	living=False
	time.sleep(1)
	print '    ===> still processing...'
	for i in t_: 
		if i.isAlive(): living=True

cleanup_temp_files(filename)

print 
print 'Done: ', time.time()-start



