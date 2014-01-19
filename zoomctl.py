#!/usr/bin/python

# used with the Raspberry PI as a "Zoom Remote"

print("ZOOM Remote control")

import time
import serial

# default (impossible) volume levels
curr_vol_level=-1
curr_rec_level=-1

########################################
# functions

# configure the serial port
def zconfig_serial():
    s = serial.Serial("/dev/ttyAMA0")
    s.baudrate = 2400
    return(s)


# show the serial port settings
def zshow_serial():
    print s
    print " "
    return


# handshake
# return true if connected, false if not
def zhandshake(s):
    # send 00, look for 80, then send A1, look for 80 then we are ready
    s.write('\x00')

    zbyte = s.read(1)
    if (zbyte == '\x80'): s.write('\xa1')
        
    zbyte = s.read(1)
    if (zbyte == '\x80'): return(1) 
    return(0)


# RELEASE the button
def zrelease():
    s.write('\x80\x00')
    time.sleep(.06)
    return

# press the RECORD button and unpress
def zrec():
    s.write('\x81\x00')
    zrelease()
    return


# press the RECORD button twice and unpress
def zrecrec():
    zrec()
    zrec()
    return


# press the PLAY button and unpress
def zplay():
    s.write('\x82\x00')
    zrelease()
    return
    

# press the STOP button and unpress
def zstop():
    s.write('\x84\x00')
    zrelease()
    return


# press the NEXT button and unpress
def znext():
    s.write('\x88\x00')
    zrelease()
    return


# press the PREV button and unpress
def zprev():
    s.write('\x90\x00')
    zrelease()
    return


# press MIC
def zmic():
    s.write('\x80\x01')
    zrelease()
    return


# press LINE 1
def zline1():
    s.write('\x80\x02')
    zrelease()
    return


# press LINE 2
def zline2():
    s.write('\x80\x04')
    zrelease()
    return


# start the VOLUME UP
def zvol_up():
    s.write('\x80\x08')
    return


# start the VOLUME DOWN
def zvol_down():
    s.write('\x80\x10')
    return


# start the REC VOLUME UP
def zrec_vol_up():
    s.write('\x80\x20')
    return


# start the REC VOLUME DOWN
def zrec_vol_down():
    s.write('\x80\x40')
    return


def zread_led():
    zled(s.read(1))
    return


def zled(bitval):
    # led function
    # Bits:
    # 01 rec
    # 02 mic red
    # 04 line 1 red
    # 08 line 2 red
    # 10 mic green
    # 20 line 1 green
    # 40 line 2 green
    if (chr(bitval) & chr(01)): rec="REC     "
    else: rec="        "

    if (bitval & '\x02'): micr="Mic     "
    else: micr="       "

    if (bitval & '\x04'): l1r="Line1   "
    else: l1r="        "

    if (bitval & '\x08'): l2r="Line2   "
    else: l2r="        "

    if (bitval & '\x10'): micg="Mic     "
    else: micg="       "

    if (bitval & '\x20'): l1g="Line1   "
    else: l1g="        "

    if (bitval & '\x40'): l2g="Line2   "
    else: l2g="        "

    print(rec, " ", micr, " ", l1r, " ", l2r, " ", micg, " ", l1g, " ", l2g)
    return


# snooze for t seconds
def zsleep(t):
    # add error offset for startup time
    t += .2
    time.sleep(t)
    return


#Set the volume to 80
def zvol(volume):
    global curr_vol_level
    
    if((volume > 100) | (volume < 0)):
        print "zvol(0-100)"
        return

    # if we already know the volume...
    if(curr_vol_level != -1):
        if(curr_vol_level == volume):
            return
        
        # volume up
        elif(curr_vol_level < volume):
            button_presses = volume - curr_vol_level
            while(button_presses > 0):
                zvol_up()
                zrelease()
                button_presses -= 1

        #volume down
        else:
            button_presses = curr_vol_level - volume
            while(button_presses > 0):
                zvol_down()
                zrelease()
                button_presses -= 1
                
    else:
        # drop volume to 0
        zvol_down()
        time.sleep(6)

        # volume up from0
        button_presses = volume
        while(button_presses > 0):
            zvol_up()
            zrelease()
            button_presses -= 1
    
    curr_vol_level = volume    
    return


########################################
# end functions
########################################

s = zconfig_serial()
