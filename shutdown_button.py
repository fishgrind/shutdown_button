#!/usr/bin/python3
# -*- coding: utf-8 -*-
# example gpiozero code that could be used to have a reboot
#  and a shutdown function on one GPIO button
# scruss - 2017-10

use_button=27                       # lowest button on PiTFT+

from gpiozero import Button
from signal import pause
from subprocess import check_call
from subprocess import Popen

held_for=0.0

def rls():
        global held_for
        if (held_for > 15.0):
                check_call(['/sbin/poweroff'])
        elif (held_for > 10.0):
                check_call(['/sbin/reboot'])
        elif (held_for > 5.0):
                Popen("sudo touch /root/.pwnagotchi-manu && sudo service pwnagotchi restart", shell=True)
        elif (held_for > 1.0):
                Popen("sudo touch /root/.pwnagotchi-auto && sudo service pwnagotchi restart", shell=True)
        else:
        	held_for = 0.0

def hld():
        # callback for when button is held
        #  is called every hold_time seconds
        global held_for
        # need to use max() as held_time resets to zero on last callback
        held_for = max(held_for, button.held_time + button.hold_time)

button=Button(use_button, hold_time=1.0, hold_repeat=True)
button.when_held = hld
button.when_released = rls

pause() # wait forever
