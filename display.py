from datetime import datetime
from time import sleep
import psutil
import serial
import os

version = '0.0.1'
debug = False#True

if not debug:
    serial = serial.Serial("/dev/ttyACM0");
    serial.flush()
    # Wait for arduino reset
    sleep(5)

lines = [ "", "" ]
def write_disp():
    if not debug:
        serial.write("{}{}".format(lines[0], lines[1]))
        serial.flush()
    print(lines[0])
    print(lines[1])

def set_line(num, line):
    if num < 2 and num >= 0:
        lines[num] = '{:^16s}'.format(line)[0:16]

def print_init():
    set_line(0, 'Pit Master');
    set_line(1, 'LCD v{}'.format(version));

#### DISPLAY FUNCTIONS ####

def print_ram():
    virt = psutil.virtual_memory()
    set_line(0, 'RAM USED / FREE')
    set_line(1, '{} / {} M'.format(virt.used / 1024 / 1024, virt.total / 1024 / 1024))

def print_load():
    av1, av2, av3 = os.getloadavg()
    set_line(0, 'LOAD')
    set_line(1, '{:.2f} {:.2f} {:.2f}'.format(av1, av2, av3))

def print_uptime():
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    set_line(0, 'UPTIME')
    set_line(1, '{}'.format(str(uptime).split('.')[0]))

## END DISPLAY FUNCTIONS ##

func = [
    print_ram,
    print_load,
    print_uptime
]

print_init()
write_disp()
sleep(5)
while True:
    for f in func:
	for i in range(0,5):
        	f()
        	write_disp()
        	sleep(1)
