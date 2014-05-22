# many dependencies, all should be brought in with this import...
from photoboothlib import *

# ========= COMMAND LINE ARGUMENTS =============

# use camera or dummy source images...
if 'nousecamera' in sys.argv:
	camera_arg=False
else:
	C = piggyphoto.camera()
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

print 'nousecamera', repr(camera_arg)
print 'nomove', repr(move)
print 'lastphoto', last
print 'increment', repr(increment)
