'''
  *  The MIT License (MIT)
  *
  *  G213Colors v0.1 Copyright (c) 2016 SebiTimeWaster
  *
  *  Permission is hereby granted, free of charge, to any person obtaining a copy
  *  of this software and associated documentation files (the "Software"), to deal
  *  in the Software without restriction, including without limitation the rights
  *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  *  copies of the Software, and to permit persons to whom the Software is
  *  furnished to do so, subject to the following conditions:
  *
  *  The above copyright notice and this permission notice shall be included in all
  *  copies or substantial portions of the Software.
  *
  *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  *  SOFTWARE.
'''


import sys
import usb.core
import usb.util
import binascii


standardColor  = 'ffb4aa'         # Standard color, i found this color to produce a white color on my G213
idVendor       = 0x046d           # The id of the Logitech company
idProduct      = 0xc084           # The id of the G203
bmRequestType  = 0x21             # --.
bmRequest      = 0x09             #    \ The controll transfer
wValue         = 0x0210           #    / configuration for the G203
wIndex         = 0x0001           # --'
colorCommand   = "11ff0e3c0001{}0200000000000000000000"   # binary commands in hex format
breatheCommand = "11ff0e3c0003{}{}006400000000000000"     # color; speed; brightness
cycleCommand   = "11ff0e3c00020000000000{}64000000000000" # speed; brightness
device         = ""               # device resource
isDetached     = False            # If kernel driver needs to be reattached
#confFile       = "/etc/G213Colors.conf"


def connectG():
    global device, isDetached
    # find G product
    device = usb.core.find(idVendor = idVendor, idProduct = idProduct)
    # if not found exit
    if device is None:
        raise ValueError("USB device not found!")
    # if a kernel driver is attached to the interface detach it, otherwise no data can be send
    if device.is_kernel_driver_active(wIndex):
        device.detach_kernel_driver(wIndex)
        isDetached = True

def disconnectG():
    # free device resource to be able to reattach kernel driver
    usb.util.dispose_resources(device)
    # reattach kernel driver, otherwise special key will not work
    if isDetached:
        device.attach_kernel_driver(wIndex)

def sendData(data):
    # decode data to binary and send it
    device.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, binascii.unhexlify(data))

def sendColorCommand(colorHex):
    sendData(colorCommand.format(colorHex))

def sendBreatheCommand(colorHex, speed):
    sendData(breatheCommand.format(colorHex, str(format(speed, '04x'))))

def sendCycleCommand(speed):
    sendData(cycleCommand.format(str(format(speed, '04x'))))

#def saveData(data):
#    file = open(confFile,"w")
#    file.write(data)
#    file.close()
