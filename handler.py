import serial

def handle_write(inp):
	# struktutra ramki  addr;funkcja;adres poczatkowy;liczba rejestro;crc

	#wyciaganie wartosci z wejscia
	addr=inp['addr']
	baud=inp['baud']
	starting_address=inp['st']
	num_of_registers=inp['reg']


	return {'result' : 100, 'status': 'ack'}

def handle_read(inp):
	
	#wyciaganie wartosci z wejscia
	addr=inp['addr']
	baud=inp['baud']
	starting_address=inp['st']
	num_of_registers=inp['reg']

	#przygotowanie ramki
	frame=construct_frame(addr,starting_address,num_of_registers)
	#wyslanie ramki i odbior odpowiedzi	
	anws=send_and_get_anws(frame)
	#wyciagniecie wartosci z odpowiedzi
	ret=decompose_frame(anws)

	#pokazowka
	print addr
	print baud
	print starting_address
	print num_of_registers

	#dopoki kod nie dziala, zwraca 100
	ret = {'result' : 100}
	return ret

def construct_frame(device_address,start_register_address,number_of_registers):
	#TO-DO
	return 0

def send_and_get_anws(frame):
	#TO-DO
	return anwser

def decompose_frame(frame):
	#TO-DO
	return value

def calc_crc16(msg):
	#TO-DO
	return crc