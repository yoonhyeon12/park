# Code by Simon Monk https://github.com/simonmonk/

from MFRC522 import MFRC522
import RPi.GPIO as GPIO
  
class SimpleMFRC522:

  READER = None
  
  KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
  BLOCKS_4TH = [ 3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63 ]
  
  def __init__(self):
    self.READER = MFRC522()
  
  def get_block_add(self, index):
    return [index * 4 + 0, index * 4 + 1, index * 4 + 2]
    
  def read_block(self, index):
      id, text = self.read_block_by_i(index)
      while not id:
          id, text = self.read_block_by_i(index)
      return id, text
  
  def read_block_by_i(self, index):
    BLOCK_ADDRS = self.get_block_add(index)
    (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.MFRC522_SelectTag(uid)
    status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, self.BLOCKS_4TH[index], self.KEY, uid)
    data = []
    text_read = ''
    if status == self.READER.MI_OK:
        for block_num in BLOCK_ADDRS:
            block = self.READER.MFRC522_Read(block_num) 
            if block:
                    data += block
        if data:
             text_read = ''.join(chr(i) for i in data)
    self.READER.MFRC522_StopCrypto1()
    return id, text_read
    
  def write_block(self, text, index):
      id, text_in = self.write_block_by_i(text, index)
      while not id:
          id, text_in = self.write_block_by_i(text, index)
      return id, text_in
      
  def write_block_by_i(self, txt, index):
      BLOCK_ADDRS = self.get_block_add(index)
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None, None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None, None
      id = self.uid_to_num(uid)
      self.READER.MFRC522_SelectTag(uid)
      status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, self.BLOCKS_4TH[index], self.KEY, uid)
      self.READER.MFRC522_Read(self.BLOCKS_4TH[index])
      if status == self.READER.MI_OK:
          data = bytearray()
          data.extend(bytearray(txt.ljust(len(BLOCK_ADDRS) * 16).encode('ascii')))
          i = 0
          for block_num in BLOCK_ADDRS:
            self.READER.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
            i += 1
      self.READER.MFRC522_StopCrypto1()
      return id, txt[0:(len(BLOCK_ADDRS) * 16)]
      
  def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
          n = n * 256 + uid[i]
      return n
