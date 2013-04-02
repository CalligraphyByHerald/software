#!/usr/bin/env python
"""
Stream g-code to grbl controller

This script differs from the simple_stream.py script by 
tracking the number of characters in grbl's serial read
buffer. This allows grbl to fetch the next line directly
from the serial buffer and does not have to wait for a 
response from the computer. This effectively adds another
buffer layer to prevent buffer starvation.

TODO: - Add runtime command capabilities

Version: 12/5 9:00PM
"""

import serial
import re
import time
import sys
import argparse
# import threading

RX_BUFFER_SIZE = 128
if __name__ == "__main__":
    # Define command line argument interface
    parser = argparse.ArgumentParser(description='Stream g-code file to grbl. (pySerial and argparse libraries required)')
    parser.add_argument('gcode_file', type=argparse.FileType('r'),
            help='g-code filename to be streamed')
    parser.add_argument('device_file',
            help='serial device path')
    parser.add_argument('-q','--quiet',action='store_true', default=False, 
            help='suppress output text')
    args = parser.parse_args()
    
    arg_stream()

# Periodic timer to query for status reports
# TODO: Need to track down why this doesn't restart consistently before a release.
# def periodic():
#     s.write('?')
#     t = threading.Timer(0.1, periodic) # In seconds
#     t.start()

device_file_default = "/dev/ttyACM2"
gcode_file_default = "grbl.gcode"
baudrate_default = 9600

def arg_stream():
    '''
    The default script behavior: call from the command line with usage
        > stream_test.py [-h] [-q] gcode_file device_file
    Supplies input to the limit of GRBL's buffer.
        
    Does not take or return
    '''
# Initialize
    s = serial.Serial(args.device_file,9600)
    f = args.gcode_file
    verbose = True
    if args.quiet : verbose = False

    # Wake up grbl
    print "Initializing grbl..."
    s.write("\r\n\r\n")

    # Wait for grbl to initialize and flush startup text in serial input
    time.sleep(2)
    s.flushInput()

    # Stream g-code to grbl
    print "Streaming ", args.gcode_file.name, " to ", args.device_file
    l_count = 0
    g_count = 0
    c_line = []
    # periodic() # Start status report periodic timer
    for line in f:
        l_count += 1 # Iterate line counter
    #     l_block = re.sub('\s|\(.*?\)','',line).upper() # Strip comments/spaces/new line and capitalize
        l_block = line.strip()
        c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
        grbl_out = '' 
        while sum(c_line) >= RX_BUFFER_SIZE-1 | s.inWaiting() :
            out_temp = s.readline().strip() # Wait for grbl response
            if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                print "  Debug: ",out_temp # Debug response
            else :
                grbl_out += out_temp;
                g_count += 1 # Iterate g-code counter
                grbl_out += str(g_count); # Add line finished indicator
                del c_line[0]
        if verbose: print "SND: " + str(l_count) + " : " + l_block + '\n',
        s.write(l_block + '\n') # Send block to grbl
        if verbose : print "BUF:",str(sum(c_line)),"REC:",grbl_out

    # Wait for user input after streaming is completed
    print "G-code streaming finished!\n"
    print "WARNING: Wait until grbl completes buffered g-code blocks before exiting."
    raw_input("  Press <Enter> to exit and disable grbl.") 

    # Close file and serial port
    f.close()
    s.close()
    
def stream(gcode_file = gcode_file_default,device_file = device_file_default, baudrate = 9600, quiet = False, flush=True):
    '''
    A function version of the script-like arg_stream, using normal parameters rather than terminal arguments.
    gcode_file = the path to the desired output gcode, defaulting to a local grbl.gcode.
    device_file = the path to the device file, defaulting to the 0th /Dev/ttyACM_ (appropriate for a linux machine without other usb devices). There is no check on this path! It is up the user to know what port they are using.
    baudrate = serial rate on the arduino. Default of 9600 works and is stably. Higher speeds are possible, up to a point, but may cause complications. May or may not warrant experimentation.
    quiet = boolean setting output strings. By default stream() reports every sent line. Even a quiet stream() will report starting, source and sink files, and finishing
    flush = flushes the GRBL start-up text ("type '$' for help"). 99.9% of the time, you won't want this. If false, the start-up text will remain in the buffer until read.
    '''
# Initialize
    s = serial.Serial(device_file,9600)
    f = open(gcode_file,'r')
    verbose = True
    if quiet : verbose = False

    # Wake up grbl
    print "Initializing grbl..."
    s.write("\r\n\r\n")

    # Wait for grbl to initialize and flush startup text in serial input
    time.sleep(2)
    if flush:
        s.flushInput()

    # Stream g-code to grbl
    print "Streaming ", gcode_file, " to ", device_file
    l_count = 0
    g_count = 0
    c_line = []
    # periodic() # Start status report periodic timer
    for line in f:
        l_count += 1 # Iterate line counter
    #     l_block = re.sub('\s|\(.*?\)','',line).upper() # Strip comments/spaces/new line and capitalize
        l_block = line.strip()
        c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
        grbl_out = '' 
        while sum(c_line) >= RX_BUFFER_SIZE-1 | s.inWaiting() :
            out_temp = s.readline().strip() # Wait for grbl response
            if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                print "  Debug: ",out_temp # Debug response
            else :
                grbl_out += out_temp;
                g_count += 1 # Iterate g-code counter
                grbl_out += str(g_count); # Add line finished indicator
                del c_line[0]
        if verbose: print "SND: " + str(l_count) + " : " + l_block,
        s.write(l_block + '\n') # Send block to grbl
        if verbose : print "BUF:",str(sum(c_line)),"REC:",grbl_out

    # Wait for user input after streaming is completed
    print "G-code streaming finished!\n"
    print "WARNING: Wait until grbl completes buffered g-code blocks before exiting."
    raw_input("  Press <Enter> to exit and disable grbl.") 

    # Close file and serial port
    f.close()
    s.close()

def setup(device_file = device_file_default, baudrate = baudrate_default, flush = True):
    '''
    Setup function from the stream() function. Sets up *and returns* a serial streaming object. Encapsulated here for general use.
    device_file = the path to the device file, defaulting to the 0th /Dev/ttyACM_ (appropriate for a linux machine without other usb devices). There is no check on this path! It is up the user to know what port they are using.
    flush = flushes the GRBL start-up text ("type '$' for help"). Some applications may want this, others may not. If false, the start-up text will remain in the buffer until read.
    '''
# Initialize
    s = serial.Serial(device_file,baudrate)

    # Wake up grbl
    print "Initializing grbl..."
    s.write("\r\n\r\n")

    # Wait for grbl to initialize and flush startup text in serial input
    time.sleep(2)
    if flush:
        s.flushInput()
        
    return s
    
def just_stream(s,gcode_file = gcode_file_default,quiet = False,flush=True):
    '''
    Just the streaming part of stream.stream(). Named to avoid conflict.
    s = mandatory serial streaming object, like the one returned by stream.setup(). Wants at least baudrate of 9600-?, 8-bits, no parity, 1 stop bit. The only non-standard parameter is the baudrate.
    gcode_file = the path to the desired output gcode, defaulting to a local grbl.gcode
    quiet = boolean setting output strings. By default stream() reports every sent line. Even a quiet stream() will report starting, source and sink files, and finishing
    '''
    verbose = True
    if quiet : verbose = False
    
    f = open(gcode_file,'r')

    # Wake up grbl
    # print "Initializing grbl..."
    s.write("\r\n\r\n")

    # Wait for grbl to initialize and flush startup text in serial input
    time.sleep(2)
    if flush:
        s.flushInput()
    else:
        print s.readline()

    # Stream g-code to grbl
    # Commented out for lack of a good way to name the device (laziness)
    # print "Streaming ", gcode_file, " to ", device_file
    l_count = 0
    g_count = 0
    c_line = []
    # periodic() # Start status report periodic timer
    for line in f:
        l_count += 1 # Iterate line counter
    #     l_block = re.sub('\s|\(.*?\)','',line).upper() # Strip comments/spaces/new line and capitalize
        l_block = line.strip()
        c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
        grbl_out = '' 
        while sum(c_line) >= RX_BUFFER_SIZE-1 | s.inWaiting() :
            out_temp = s.readline().strip() # Wait for grbl response
            if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                print "  Debug: ",out_temp # Debug response
            else :
                grbl_out += out_temp;
                g_count += 1 # Iterate g-code counter
                grbl_out += str(g_count); # Add line finished indicator
                del c_line[0]
        if verbose: print "SND: " + str(l_count) + " : " + l_block,
        s.write(l_block + '\n') # Send block to grbl
        if verbose : print "BUF:",str(sum(c_line)),"REC:",grbl_out

    # Wait for user input after streaming is completed
    print "G-code streaming finished!\n"
    print "WARNING: Wait until grbl completes buffered g-code blocks before exiting."
    raw_input("  Press <Enter> to exit and disable grbl.") 

    # Close file and serial port
    f.close()
    s.close()

