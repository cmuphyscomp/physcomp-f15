"""\
OneInOneOutGUI.py

GUI controller for the OneInOneOutASCII Arduino sketch.  This interface shell
communicates over a serial port to an Arduino running a sketch which includes
line-oriented text input and output.

Copyright (c) 2015, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license.

"""

from __future__ import print_function
import os, sys, argparse

# import the common GUI library over which this built
from ArduinoGUI.ArduinoConsole import ArduinoConsole

#================================================================
# This requires a pySerial installation.
#  Package details: https://pypi.python.org/pypi/pyserial
#  Documentation:   http://pythonhosted.org/pyserial
import serial

################################################################
class OneInOneOutGUIController(object):
    """Application-specific control object to manage the GUI for OneInOneOutASCII.
    This class creates a generic ArduinoConsole GUI, adds application-specific
    GUI controls, and manages basic I/O.

    :param port: the name of the serial port device
    :param kwargs: collect any unused keyword arguments
    """
    
    def __init__(self, port = None, **kwargs):
        # create the generic interface
        self.window = ArduinoConsole()

        # reroute printed output to the console window; this works because there is a write method defined
        sys.stdout = self.window

        # add custom interface elements.
        self.window.addSlider("PWM", self.pwm_slider_moved)
        self.window.addSlider("Servo", self.servo_slider_moved)
        self.window.addButton("LED On", self.led_on_button_pressed)
        self.window.addButton("LED Off", self.led_off_button_pressed)

        # add a plot window
        self.window.addScope()
        self.window.addScopeChannel('A0', color='blue',  duration=20)

        # set up the connect/disconnect control
        self.window.attachConnectCallback( self._connect_disconnect )

        # set up the command lin
        self.window.attachCommandCallback( self._command_input)
        
        # fill in the default text field for the Arduino port name if provided
        if port is not None:
            self.window.setArduinoPortName(port)

        # initialize connection state
        self.portname = port
        self.port = None
        self.input_monitor = None
        self.input_enabled = False
        self.arduino_time = 0
        
        return

    #=============================================================================
    def _connect_disconnect(self, name, flag ):
        if flag:
            # connect
            if self.port is not None:
                print("Client already connected.")
            else:
                if name is not None and name != "":
                    self.portname = name
                print("Connecting to the Arduino.")
                self.port = serial.Serial( self.portname, 115200, timeout=5 )

                # set up an event after the Arduino has had time to boot
                self.window.newSingleShotTimer( 2000, self._startup_delay_complete)
                self.input_enabled = False
                
                # create a monitor for the serial port device connected to the Arduino to indicate when data is ready
                self.input_monitor = self.window.newInputMonitor( self.port.fileno(), self.port_data_ready )

        else:
            # disconnect
            if self.port is not None:
                if self.input_monitor is not None:
                    self.input_monitor.setEnabled(False)
                self.port.close()
                self.port = None
                self.input_monitor = None
                self.input_enabled = False
                
            else:
                print("Client not connected.")
        return

    def _startup_delay_complete(self):
        print("Arduino bootup delay complete.")
        self.port.flushInput()
        self.window.resetPlotPressed()
        self.input_enabled = True

    def _send_command(self, command):
        if self.port is not None:
            self.port.write( command + '\n')
        else:
            print("Not connected.")
            
    def _command_input(self, command):
        print( "User entered '%s'." % command)
        self._send_command(command)
        return

    #=============================================================================
    def pwm_slider_moved(self, value):
        """Callback function activated when the PWM slider is moved."""
        pwm = int(value * 255.0)
        print("User moved PWM slider to %d, emitting %d." % (value, pwm))
        self._send_command("pwm %d" % pwm)

    def servo_slider_moved(self, value):
        """Callback function activated when the Servo slider is moved."""
        angle = int(value * 180.0)
        print("User moved Servo slider to %d, emitting %d." % (value, angle))
        self._send_command("svo %d" % angle)

    def led_on_button_pressed(self):
        """Callback function activated to enable the LED."""
        print("User turning on LED.")
        self._send_command("led 1")

    def led_off_button_pressed(self):
        """Callback function activated to disable the LED."""
        print("User turning off LED.")
        self._send_command("led 0")

    #=============================================================================
    def port_data_ready(self, fd):
        """Callback function activated when data is received from the Arduino.  This
        performs some basic processing of the status stream, but could be
        extended to handle more events.

        """
        
        line = self.port.readline().rstrip()
        if self.window.isShowingRawData():
            print("Received: '%s'" % line)

        if line and self.input_enabled:
            elements = line.split()
            if elements[0] == 'ana':
                analog_channel = int(elements[1])
                analog_value   = float(elements[2])
                if analog_channel == 0:
                    self.window.addScopeSamples('A0', [analog_value], [self.arduino_time])
                    self.window.replotScope()
                
            elif elements[0] == 'clk':
                self.arduino_time = 1e-6 * int(elements[1])

            elif elements[0] == 'led':
                pass

            elif elements[0] == 'dig':
                pass
                
            elif elements[0] == 'dbg':
                print("Received debugging message: '%s'" % line)
                
            else:
                print("Unknown status message: '%s'" % line)

        return
    
    #=============================================================================
