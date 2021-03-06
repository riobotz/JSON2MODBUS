from crc import crc
import sys,os
import serial
import binascii
import crc16
import session
import subprocess

def handle_write(inp):
	# struktutra ramki  addr;funkcja;adres poczatkowy;liczba rejestro;crc
	print inp
	#wyciaganie wartosci z wejscia
	addr=inp['addr']
	baud=int(inp['baud'])
	starting_address=inp['st']
	value=inp['val']

	frame=construct_frame_set(addr,starting_address,value)
	frame_viz(frame);
	anws=send_and_get_anws(frame,baud)
	ret=decompose_frame(anws)

	#dopoki kod nie dziala, zwraca 100
	#ret={'result' : 100, 'status': 'ack'}
	return ret

def write(inp,s):
	addr=s.addr
	baud=s.baud
	starting_address=inp['st']
	value=inp['val']

	frame=construct_frame_set(addr,starting_address,value)
	frame_viz(frame);
	anws=send_and_get_anws(frame,s)
	ret=decompose_frame(anws)

	return ret

def handle_read(inp):
	
	#wyciaganie wartosci z wejscia
	addr=inp['addr']
	baud=inp['baud']
	starting_address=inp['st']
	num_of_registers=inp['reg']
	baud=int(baud)

	#przygotowanie ramki
	frame=construct_frame_request(addr,starting_address,num_of_registers)
	#wyslanie ramki i odbior odpowiedzi
	anws=send_and_get_anws(frame,baud)
	frame_viz(anws)
	#wyciagniecie wartosci z odpowiedzi
	ret=decompose_frame(anws)

	#pokazowka
	print addr
	print baud
	print starting_address
	print num_of_registers

	ret = {'result' : ret}
	return ret

def read(inp,s):
	#wyciaganie wartosci z wejscia
	addr=s.addr
	baud=s.baud
	starting_address=inp['st']
	num_of_registers=inp['reg']
	baud=int(baud)

	#przygotowanie ramki
	frame=construct_frame_request(addr,starting_address,num_of_registers)
	#wyslanie ramki i odbior odpowiedzi
	anws=send_and_get_anws(frame,s)
	frame_viz(anws)
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
	ret=construct_frame(device_address,3,start_register_address,number_of_registers)
	return ret

def construct_frame_set(device_address,start_register_address,value):
	ret=construct_frame(device_address,6,start_register_address,value)
	return ret

def construct_frame(device_address,func,start_register_address,data):
	#frame=input_to_binary(device_address,start_register_address,data)
	print 'constructing frame'
	[data1,data0]=split8bit(int(data))
	start_register_address=int(start_register_address)
	device_address=int(device_address)
	#data=int(data)
	lo_reg_addr=start_register_address%256
	hi_reg_addr=start_register_address/256
	frame=add_crc(chr(device_address)+chr(func)+chr(hi_reg_addr)+chr(lo_reg_addr)+chr(data1)+chr(data0))
	print 'frame constructed'
	print frame_viz(frame)
	return frame

def split8bit(inp):
	return [inp//256, inp%256]

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

def send_and_get_anws(frame,meta):
	if (type(meta)==int):
		return send_over_default_port(frame,meta)
	else:
		return send_over_session(frame,meta)

def send_over_default_port(frame,baud):
	print "sending frame..."
	ser = serial.Serial(port=get_port_name(),baudrate=9600,timeout=3)
	ser.write(frame)
	print "waiting for anwser..."
	anwser=ser.read(7)
	ser.close()
	print "anwser recieved"
	return anwser

def send_over_session(frame,s):
	print "sending frame..."
	ser = serial.Serial(port=s.port,baudrate=s.baud,timeout=3)
	ser.write(frame)
	print "waiting for anwser..."
	anwser=ser.read(7)
	ser.close()
	print "anwser recieved"
	return anwser

def get_port_name():
	return 'COM3'

def decompose_frame(frame): #zwraca wartosc z ostatniego odpytanego rejestru
	#frame=frame/65536
	#mask=0b1111111111111111 #wycina z ramki ostatnie dwa bajty, po usunieciu crc
	#value=frame & mask
	print 'decomposing...'
	frame_viz(frame)
	value=256*ord(frame[3])+ord(frame[4])
	return value

def calc_crc16(msg):
	if (True):
		msg=ensure_hex(msg)
		msg=msg.replace('0x','').upper()
		c=subprocess.call("modbus_calc.exe "+str(msg))
		h=c/256
		l=c%256
		ret=l*256+h
		print hex(ret)
	else:
		ret=0x4872
	return ret

def ensure_hex(inp):
	ret=''
	for l in inp:
		if ord(l)<16:
			ret=ret+'0'+str(hex(ord(l)))
		else:
			ret=ret+str(hex(ord(l)))
	return ret

def crc16_ccitt(crc, data):
    msb = crc >> 8
    lsb = crc & 255
    for c in data:
        x = ord(c) ^ msb
        x ^= (x >> 4)
        msb = (lsb ^ (x >> 3) ^ (x << 4)) & 255
        lsb = (x ^ (x << 5)) & 255
    return (msb << 8) + lsb

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

def frame_viz(inp):
	if(len(inp)==8):
		print 'Addr  |Func	|Reg_addr	|V		|CRC'
		print '#	'+str(ord(inp[0]))+'#	'+str(ord(inp[1]))+'#	'+str(256*ord(inp[2])+ord(inp[3]))+'#	'+str(256*ord(inp[4])+ord(inp[5]))+'#	'+str(256*ord(inp[6])+ord(inp[7]))+'#'
	elif (len(inp)==7):
		print 'Addr  |Func	|Reg_addr	|V		|CRC'
		print '#	'+str(ord(inp[0]))+'#	'+str(ord(inp[1]))+'#	'+str(256*0+ord(inp[2]))+'#	'+str(256*ord(inp[3])+ord(inp[4]))+'#	'+str(256*ord(inp[5])+ord(inp[6]))+'#'
	else:
		print 'too short frame'
		print 'Addr  |Func	|Err		|CRC'
		print '#	'+str(ord(inp[0]))+'#	'+str(ord(inp[1]))+'#	'+str(ord(inp[2]))+'#	'+str(256*ord(inp[3])+ord(inp[4]))+'#'