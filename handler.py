#import serial
import binascii
import crc16

def handle_write(inp):
	# struktutra ramki  addr;funkcja;adres poczatkowy;liczba rejestro;crc

	#wyciaganie wartosci z wejscia
	addr=inp['addr']
	baud=inp['baud']
	starting_address=inp['st']
	value=inp['val']

	frame=construct_frame_set(addr,starting_address,value)
	anws=send_and_get_anws(frame,baud)
	ret=decompose_frame(anws)

	#dopoki kod nie dziala, zwraca 100
	ret={'result' : 100, 'status': 'ack'}
	return ret

def handle_read(inp):
	
	#wyciaganie wartosci z wejscia
	addr=inp['addr']
	baud=inp['baud']
	starting_address=inp['st']
	num_of_registers=inp['reg']

	#przygotowanie ramki
	frame=construct_frame_request(addr,starting_address,num_of_registers)
	#wyslanie ramki i odbior odpowiedzi	
	anws=send_and_get_anws(frame,baud)
	#wyciagniecie wartosci z odpowiedzi
	ret=decompose_frame(anws)

	#pokazowka
	print addr
	print baud
	print starting_address
	print num_of_registers

	ret = {'result' : ret}
	return ret


def construct_frame_request(device_address,start_register_address,number_of_registers):
	number_of_registers=1 # na razie ograniczam liczbe rejestrow do odczytu na raz do 1
	ret=construct_frame(device_address,start_register_address,number_of_registers)
	return ret

def construct_frame_set(device_address,start_register_address,value):
	ret=construct_frame(device_address,start_register_address,value)
	return ret

def construct_frame(device_address,start_register_address,data):
	#frame=input_to_binary(device_address,start_register_address,data)
	if (start_register_address>255):
		lo_reg_addr=start_register_address%256
		hi_reg_addr=start_register_address/256
	else:
		hi_reg_addr=0
		lo_reg_addr=start_register_address
	frame=add_crc(chr(device_address)+chr(3)+chr(hi_reg_addr)+chr(lo_reg_addr)+chr(0)+chr(data))
	return frame

def input_to_binary(device_address,start_regiter_address,data): #obsolete
	frame=device_address
	frame=256*frame + 3 #funkcja
	frame=65536*frame + start_regiter_address #adres rejestru
	frame=65536*frame + data #data lub liczba rejestrow
	return frame

def add_crc(frame):
	crc_hi=chr(calc_crc16(frame)/256)
	crc_lo=chr(calc_crc16(frame)%256)
	return frame + crc_hi +crc_lo

def send_and_get_anws(frame,baud):
	ser = serial.Serial(port=get_port_name(),baudrate=baud,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
	ser.open()
	ser.write(frame)
	anwser=ser.read(8)
	ser.close()
	return anwser


def get_port_name():
	return 'COM2'

def decompose_frame(frame): #zwraca wartosc z ostatniego odpytanego rejestru
	#frame=frame/65536
	#mask=0b1111111111111111 #wycina z ramki ostatnie dwa bajty, po usunieciu crc
	#value=frame & mask
	print (frame)
	value=ord(frame[4])+ord(frame[5])
	return value

def calc_crc16(msg):
	return crc16.crc16xmodem(msg)

def calc_crc16_old(msg):
	l=get_msg_len(msg)
	crc = 0xFFFF
	poly=0x1021
	while (l):
		crc ^= (msg+1)<<8
		if (crc & 0x8000):
			crc=(crc << 1) ^ poly
		else:
			crc=crc << 1

		if (crc & 0x8000):
			crc=(crc << 1) ^ poly
		else:
			crc=crc << 1
		if (crc & 0x8000):
			crc=(crc << 1) ^ poly
		else:
			crc=crc << 1
		if (crc & 0x8000):
			crc=(crc << 1) ^ poly
		else:
			crc=crc << 1
		if (crc & 0x8000):
			crc=(crc << 1) ^ poly
		else:
			crc=crc << 1
		if (crc & 0x8000):
			crc=(crc << 1) ^ poly
		else:
			crc=crc << 1
		if (crc & 0x8000):
			crc=(crc << 1) ^ poly
		else:
			crc=crc << 1
		if (crc & 0x8000):
			crc=(crc << 1) ^ poly
		else:
			crc=crc << 1
		l -= 1
	return crc

def get_msg_len(msg):
	l=0
	while (msg>0):
		msg=msg>>1
		l += 1
	return l