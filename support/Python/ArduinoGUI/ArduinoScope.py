"""\
ArduinoScope.py : Qt/Qwt widget to show a real-time oscilloscope-like display of signals

Copyright (c) 2015, Garth Zeglin.  All rights reserved. Licensed under the terms
of the BSD 3-clause license.
"""

# Based on the Python version of Qwt-5.0.0/examples/data_plot
# For reference documentation, see:
#   https://github.com/PyQwt
#   http://qwt.sourceforge.net/

import random
import sys
import numpy as np
import bisect

from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt

################################################################
class ScopeChannel(object):
    """Internal class to represent the state of one channel in an ArduinoScope
    widget.  See ArduinoScope.add_channel() for arguments."""
    def __init__( self, name, title=None, color=None, duration=None ):
        self.name = name

        if color is None:
            red   = random.randint(0,255)
            green = random.randint(0,255)
            blue  = random.randint(0,255)
            self.color = Qt.QColor(red, green, blue)
        else:
            self.color = Qt.QColor(color)

        self.title = title if title is not None else name
        self.duration = duration

        # start with an empty sample buffer
        self.t = np.ndarray(0)
        self.y = np.ndarray(0)
        
        # create and configure the associated curve object to show the data
        self.curve = Qwt.QwtPlotCurve( self.title )
        self.curve.setPen(Qt.QPen(self.color))
        return

    #================================================================
    def clear_data(self):
        self.t = np.ndarray(0)
        self.y = np.ndarray(0)
        # update the associated QwtPlotCurve
        self.curve.setData( self.t, self.y )
        return

    #================================================================
    def add_samples( self, y, t ):
        """Add one or more data samples to the buffer in the channel.  If a maximum
        duration was specified during creation, the data buffer will be
        truncated to hold the specified maximum amount of history.

        :param y: list or ndarray of signal values
        :param t: list or ndarray of times, must be same length as y
        """

        # append the new data to the existing buffers
        # N.B. this could be more efficient with memory allocation, but this is simpler
        self.t = np.concatenate((self.t, t))
        self.y = np.concatenate((self.y, y))
        
        if self.duration is not None:
            first_allowable_time = self.t[-1] - self.duration
            if first_allowable_time > self.t[0]:
                # search for the position of the first sample with allowable time index
                first_index = bisect.bisect_left( self.t, first_allowable_time )
                self.t = self.t[first_index:]
                self.y = self.y[first_index:]

        # update the associated QwtPlotCurve
        self.curve.setData( self.t, self.y )
        return
                     
################################################################
class ArduinoScope(Qwt.QwtPlot):
    """Plot widget to show real-time data like a multichannel oscilloscope.
    Implemented as a subclass of the QwtPlot widget provided in the Qwt5
    package.  Requires Qwt5 and PyQwt5.
    """
    
    def __init__(self, *args):

        # initialize the parent class
        Qwt.QwtPlot.__init__(self, *args)

        # set of ScopeChannel objects, indexed by name
        self.channels = dict() 

        # configure the parent QwtPlot widget for a reasonable display
        self.setCanvasBackground(Qt.Qt.white)
        self._alignScales()
        self.setTitle("ArduinoScope")
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);

        self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time (seconds)")
        self.setAxisTitle(Qwt.QwtPlot.yLeft, "Values")

        return

    #================================================================    
    def _alignScales(self):
        """Internal function to configure details of the QwtPlot."""
        self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(Qwt.QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent( Qwt.QwtAbstractScaleDraw.Backbone, False )
    
    #================================================================
    def add_channel( self, name, *args, **kwargs ):
        """Add a new channel to the oscilloscope.  The parameters are passed to ScopeChannel.init.

        :param name: short name with which to identify the channel internally
        :param title: optional title string to use on plot (default is to use the name value)
        :param color: optional color name string.  Examples: 'red', 'purple, '#80ff30' (default is random)
        :param duration: optional limit on the length of the time history to store
        """
        new_channel = ScopeChannel( name, *args, **kwargs )
        self.channels[name] = new_channel

        # attach the associated QwtPlotCurve object to the oscilloscope widgt
        new_channel.curve.attach(self)
        return

    #================================================================
    def add_samples(self, name, y, t):
        """Add one or more data samples to the buffer in the channel.  If a maximum
        duration was specified during creation, the data buffer will be
        truncated to hold the specified maximum amount of history.  After all
        channels have been updated, call the replot() method to update the
        display.

        :param name: channel name as supplied during creation
        :param y: list or ndarray of signal values
        :param t: list or ndarray of times, must be same length as y
        """
        self.channels[name].add_samples(y, t)
        return

    #================================================================
    def reset_plot(self):
        """Clear all the sample buffers."""
        for channel in self.channels.itervalues():
            channel.clear_data()

################################################################
