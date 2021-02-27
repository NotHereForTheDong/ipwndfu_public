import dfu
import usbexec

# Define nonce below, every 2 units separated by \x
# Default nonce is 0x1111111111111111

nonce = '\x11\x11\x11\x11\x11\x11\x11\x11'
HOST2DEVICE = 0x21
DEVICE2HOST = 0xA1
DFU_DNLOAD = 1
DFU_ABORT = 4

# rm SigChecks
device = usbexec.PwnedUSBDevice()
device.write_memory(0x100006ca8, '\x1F\x20\x03\xD5') #SigPatch1
device.write_memory(0x100006c80, '\x21\x00\x80\x52\xE1\xE7\x03\x39\xE1\xEF\x03\x39\xE1\xF7\x03\x39\x1F\x20\x03\xD5\x1F\x20\x03\xD5\x1F\x20\x03\xD5\x1F\x20\x03\xD5\x1F\x20\x03\xD5') #SigPatch2

# set NONC
device.write_memory(0x20e0b8028, nonce ) #nonc

# reset USB
device = dfu.acquire_device()
device.ctrl_transfer(HOST2DEVICE, DFU_ABORT, 0, 0, 0, 0)
dfu.usb_reset(device)
dfu.release_device(device)

# Thanks LinusHenze/Fugu for signature patch values.
# Thanks @marijuanARM + @exploit3dguy for the advice.
