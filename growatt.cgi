#!/usr/bin/python
import array
import serial
import sys

print 'Content-Type: application/json'
print ''

def bytes(num):
  return [num >> 8, num & 0xFF]
def checksum(bytearr):
  sum=0
  for i in range(len(bytearr)):
    sum+=bytearr[i]^i;
  if (sum==0 or sum>0xFFFF):
    sum=0xFFFF
  return bytes(sum);

def twobytestofloat(bytes):
  return ord(bytes[0])*16.0*16.0+ord(bytes[1])
def twobytestoint(bytes):
  return ord(bytes[0])*16*16+ord(bytes[1])
def fourbytestofloat(bytes):
  return ord(bytes[0])*16.0*16.0*16.0*16.0*16.0*16.0+ord(bytes[1])*16.0*16.0*16.0*16.0+ord(bytes[2])*16.0*16.0+ord(bytes[3])
def fourbytestoint(bytes):
  return ord(bytes[0])*16*16*16*16*16*16+ord(bytes[1])*16*16*16*16+ord(bytes[2])*16*16+ord(bytes[3])

ser = serial.Serial('/dev/rfcomm1', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
if ser.is_open:
  pass
else:
  ser.open()

# get energy
addr=0x7E
c1=0x42
msg=[0x3F, 0x23, addr, 0x32, c1, 0]
chk=checksum(msg)
msg.extend(chk)
msgb = array.array('B', msg).tostring()
ser.write(msgb)
x=[]
d=[]
chks=[]
try:
  x=ser.read(6)
  dl=ord(x[5])
  d=ser.read(dl)
  chks=ser.read(2)
except:
  print '{"error": "no response"}'
  ser.close()
  sys.exit()

chk=[ord(elem) for elem in chks]
#check checksum
alldatabytes=[ord(elem) for elem in x+d]
if chk!=checksum(alldatabytes):
  print '{"error": "checksum mismatch for totals"}'
  ser.close()
  sys.exit()

if c1==0x42:
  print '{"energy_today": '+str(twobytestofloat(d[7:9])/10.0)+','
  print '"energy_total": '+str(fourbytestofloat(d[9:13])/10.0)+','
  print '"hours_total": '+str(fourbytestoint(d[13:17]))+','
  
# get energy
addr=0x7E
c1=0x41
msg=[0x3F, 0x23, addr, 0x32, c1, 0]
chk=checksum(msg)
msg.extend(chk)
msgb = array.array('B', msg).tostring()
ser.write(msgb)
try:
  x=ser.read(6)
  dl=ord(x[5])
  d=ser.read(dl)
  chks=ser.read(2)
except:
  print '"error": "no response"}'
  ser.close()
  sys.exit()

ser.close()
chk=[ord(elem) for elem in chks]
#check checksum
alldatabytes=[ord(elem) for elem in x+d]
if chk!=checksum(alldatabytes):
  print '"error": "checksum mismatch for data"}'
  sys.exit()

elif c1==0x41:
  print '"temperature": '+str(twobytestofloat(d[31:33])/10.0)+','
  print '"input_power": '+str(twobytestofloat(d[5:7])/10.0)+','
  print '"output_power": '+str(twobytestofloat(d[13:15])/10.0)+','
  print '"input_voltage": '+str(twobytestofloat(d[1:3])/10.0)+','
  print '"grid_voltage": '+str(twobytestofloat(d[7:9])/10.0)+','
  print '"input_voltage2": '+str(twobytestofloat(d[3:5])/10.0)+','
  print '"current": '+str(twobytestofloat(d[9:11])/10.0)+','
  print '"frequency": '+str(twobytestofloat(d[11:13])/100.0)+','
  status=ord(d[0])
  print '"status_code": '+str(status)+','
  if status==0:
    print '"status_desc": "waiting",'
  elif status==1:
    print '"status_desc": "normal",'
  elif status==2:
    print '"status_desc": "fault",'
  else:
    print '"status_desc": "unknown",'
  print '"fault_codes": {"iso": '+str(twobytestoint(d[15:17]))+','
  print '"gfci": '+str(twobytestoint(d[17:19]))+','
  print '"dci": '+str(twobytestoint(d[19:21]))+','
  print '"input_voltage": '+str(twobytestoint(d[21:23]))+','
  print '"output_voltage": '+str(twobytestoint(d[23:25]))+','
  print '"frequency": '+str(twobytestoint(d[25:27]))+','
  print '"temperature": '+str(twobytestoint(d[27:29]))+','
  print '"fault_type": '+str(twobytestoint(d[29:31]))+'}}'

