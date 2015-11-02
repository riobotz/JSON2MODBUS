def handle_write(inp):
	return "xxx"

def handle_read(inp):
	print 'y'
	addr=inp['addr']
	baud=inp['baud']
	starting_address=inp['st']
	num_of_registers=inp['reg']
	print addr
	print baud
	print starting_address
	print num_of_registers
	ret = {'result' : 100}
	return ret