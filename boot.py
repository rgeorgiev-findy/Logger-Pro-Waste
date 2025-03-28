import gc
import uos
from flashbdev import bdev

try:
    if bdev:
        uos.mount(bdev, '/')
except OSError:
    import inisetup
    vfs = inisetup.setup()

gc.collect()
# This file is executed on every boot (including wake-boot from deepsleep)

import sys
import machine
import utime 
import os
import esp32
import uos
import uasyncio as asyncio

sys.path[1] = '/flash/lib'
def wdtAlert(p):
    import machine
    machine.reset() 

wdt = machine.Timer(10)
wdt.init(period=300000,mode=machine.Timer.ONE_SHOT,callback=wdtAlert)



import time
try:
    from last import fw
    f = fw()
 
except Exception as e:
    print(str(e))
    from base import fw
    f = fw()
    
f.start()

