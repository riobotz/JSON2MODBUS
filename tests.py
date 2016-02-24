from time import sleep
import unittest
from handler import calc_crc16
from handler import input_to_binary
from handler import decompose_frame
from handler import get_msg_len
from handler import construct_frame
from handler import handle_write
from handler import handle_read
from handler import split8bit
from handler import read
from handler import write
import binascii
import json
import session

class MyTestCase(unittest.TestCase):



    def test_msg_len(self):
        l= get_msg_len(0x123456789)
        #print bin(0x123456789)
        self.assertEqual(l,33)

    def test_crc(self):
        crc =  calc_crc16('730707')
        print bin(crc)
        print bin(0x2590)
        print bin(0x40EB)
        self.assertEqual(crc,0xD4F2)

    def test_frame_no_crc(self):
        out=input_to_binary(7,7,7)
        desired_output=0b000001110000001100000000000001110000000000000111
        self.assertEqual(out,desired_output)

    def test_compose_frame(self):
        out=construct_frame(7,3,7,7)
        desired_output="730707"
        self.assertEqual(out[0:-2],desired_output)

    def test_decompose_frame(self):
        #out=decompose_frame(0b0000011100000011000000000000011100000000000001110000000000000000)
        out = decompose_frame('\x07\x03\x00\x07\x00\x07\x00\x00')
        self.assertEqual(out,7)

    def test_handle_write(self):
        print 'Sending communiaction'
        r=handle_write(json.loads('{"addr":"7","baud":"9600","st":"300","val":"100"}'))
        print r
        sleep(30)

    def test_handle_read(self):
        print 'Recieving data'
        r=handle_read(json.loads('{"addr":"7","baud":"9600","st":"1","reg":"1"}'))
        print r

    def test_split8bit1(self):
        print 'check split1'
        out=split8bit(1023)
        self.assertEqual([3, 255], out)

    def test_split8bit2(self):
        print 'check split2'
        out=split8bit(2048)
        self.assertEqual([8, 0], out)

    def test_write(self):
        print 'Sending communiaction'
        s=session.session()
        r=write(json.loads('{"addr":"7","baud":"9600","st":"300","val":"100"}'),s)
        print r
        sleep(30)

    def test_read(self):
        s=session.session()
        r=read(json.loads('{"addr":"7","baud":"9600","st":"1","reg":"1"}'),s)
        print r

    def test_read2(self):

        s=session.session()
        r=read(json.loads('{"addr":"7","baud":"9600","st":"100","reg":"1"}'),s)
        print r

if __name__ == '__main__':
    unittest.main()
