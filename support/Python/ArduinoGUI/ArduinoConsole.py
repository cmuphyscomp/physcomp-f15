"""\
ArduinoConsole.py

PyQt4 window implementing a generic control console for an Arduino sketch,
including command line, plot window, and serial port controls.  Functions are
provide to allow extending the basic interface with custom buttons and sliders
without needing to use Qt Designer.

Copyright (c) 2013-2015, Garth Zeglin. All rights reserved. Licensed under the
terms of the BSD 3-clause license as included in LICENSE.
"""

# for documentation on the PyQt4 API, see http://pyqt.sourceforge.net/Docs/PyQt4/index.html

from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8

except AttributeError:
    def _fromUtf8(s):
        return s

# import the underlying class created using Qt Designer and pyuic
from ArduinoConsoleWindow import Ui_ArduinoConsoleWindow

#================================================================
# The Qwt technical widgets system may or may not be available for showing the plot widget.
# For details see:
#  https://github.com/PyQwt
#  http://qwt.sourceforge.net/

try:
    from ArduinoScope import ArduinoScope
    
except ImportError:
    print("Unable to load the ArduinoScope module, perhaps the pyqwt or qwt52 modules are not installed.")
    ArduinoScope = None

################################################################

class ArduinoConsole( QtGui.QMainWindow, Ui_ArduinoConsoleWindow ):
    """A custom window which inherits both from the QMainWindow class and the custom
    Ui_ArduinoConsoleWindow defined using Qt Designer."""

    def __init__( self, view = None):
        QtGui.QMainWindow.__init__( self )
        self.setupUi( self )
        self.scope = None
        self.connect_callback = None
        self.command_callback = None
        self.show()
        return

    def write( self, string ):
        """Write output to the console text area."""
        self.consoleOutput.insertPlainText(str(string))
        self.consoleOutput.ensureCursorVisible()
        return

    # --------- callbacks from Ui_ArduinoConsoleWindow ---------------
    def commandEntered( self ):
        """Callback invoked whenever command line text is entered."""
        command = self.commandLine.text()
        self.commandLine.clear()
        if self.command_callback is not None:
            self.command_callback(str(command))
        return

    def ArduinoConnectToggled( self, flag ):
        """Callback invoked whenever the Arduino Connect checkbox changes state."""
        if self.connect_callback is not None:
            self.connect_callback( str(self.ArduinoPortName.text()), flag )
        return

    def ArduinoPortEntered( self ):
        """Callback invoked whenever text is entered into the Arduino Port field."""
        port_name = self.ArduinoPortName.text()
        return
    
    def resetPlotPressed( self ):
        """Callback invoked whenever the Reset Plot button is clicked."""
        if self.scope is not None:
            self.scope.reset_plot()
        return
    
    #----- functions to manage events -------------------------------
    def attachConnectCallback(self, callback):
        """Set the callback function to be invoked when the user requests a connect or disconnect from the Arduino.

        :param callback: callback( port_name, flag )  flag is True for connect, False for disconnect
        """
        self.connect_callback = callback
        return

    def attachCommandCallback(self, callback):
        """Set the callback function to be invoked when the user enters a command.

        :param callback: callback( command_string )
        """
        self.command_callback = callback
        return

    def setArduinoPortName(self, name):
        """Set the initial state of the Arduino Port name field (e.g., from command-line arguments)."""
        self.ArduinoPortName.setText(name)
        return

    def isShowingRawData(self):
        """Returns true if the Show Raw Data checkbox is selected."""
        return self.ArduinoRawSwitch.isChecked()

    def newPeriodicTimer( self, interval, callback ):
        """Convenience function to create a periodic timer which calls a function at the
        given interval.

        :param interval: interval in milliseconds
        :param callback: no-argument function callback() to be called at intervals
        :return: the underlying QTimer object
        """
        timer = QtCore.QTimer()         # create a polling timer
        timer.start(int(interval)   )   # units are milliseconds
        timer.timeout.connect(callback) # attach to callback
        return timer

    def newSingleShotTimer( self, interval, callback ):
        """Convenience function to set up a single-shot timer which calls a function
        once after the given interval.

        :param interval: interval in milliseconds
        :param callback: no-argument function callback() to be called once after a delay
        """
        QtCore.QTimer.singleShot( int(interval), callback )
        return

    def newInputMonitor( self, fd, callback ):
        """Convenience function to create a notification callback when input is available on a file descriptor.

        :param fd: integer file descriptor
        :param callback: one-argument function callback(fd) to be called with the file descriptor
        :return: the underlying QSocketNotifier object
        """
        notifier = QtCore.QSocketNotifier( fd, QtCore.QSocketNotifier.Read )
        QtCore.QObject.connect( notifier, QtCore.SIGNAL( QtCore.QString.fromUtf8("activated(int)")), callback )
        return notifier

    #------ functions to programmatically extend the GUI ------------
    def addButton( self, title, callback ):
        """Add a button to the general-purpose button area of the interface.  The title
        argument should be a short string to appear on the face of the button.
        The callback function is invoked whenever the button is pressed.
        """
        newButton = QtGui.QPushButton(self.centralwidget)
        newButton.setObjectName(_fromUtf8( title ))
        self.buttonLayout.addWidget( newButton )
        newButton.setText( title )
        QtCore.QObject.connect( newButton, QtCore.SIGNAL(_fromUtf8("clicked()")), callback )
        return

    def addSlider( self, title, callback ):
        """Add a horizontal slider to the controls area.  The range is fixed over [0,1.0).

        :param title: string used as a tooltip
        :param callback: function receiving floating slider value
        """

        newSlider = QtGui.QSlider(self.centralwidget)
        newSlider.setOrientation(QtCore.Qt.Horizontal)
        newSlider.setObjectName(_fromUtf8( title ))
        self.sliderLayout.addWidget( newSlider )

        # This sets a fixed maximum larger than any current screen resolution; the user can scale to what they require.
        newSlider.setMaximum( 10000 )

        # this slider does not itself have text, so this sets a tooltip for it
        newSlider.setToolTip( "<html><head/><body><p>%s</p></body></html>" % title )

        # create a wrapper function to rescale the slider value to [0,1]
        wrapper = lambda ticks: callback(0.0001*ticks)

        # connect the slider motion signal to the wrapper
        QtCore.QObject.connect( newSlider, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), wrapper)
        
        return newSlider

    #------ functions to control the data plot area -----------------
    def addScope(self):
        """Add an ArduinoScope widget to the top of the layout."""
        if ArduinoScope is None:
            print("Warning, the ArduinoScope object is not available.")
        else:
            # add the plot area to the top of the window
            self.scope = ArduinoScope(self.centralwidget)
            self.verticalLayout.insertWidget(0, self.scope)
            
    def addScopeChannel(self, *args, **kwargs ):
        """Add a named channel to the ArduinoScope plotting widget.  The arguments are
        passed unchanged to add_channel()."""
        
        if self.scope is not None:
            self.scope.add_channel( *args, **kwargs )

    def addScopeSamples(self, name, y, t ):
        """Add a set of new samples to a given named channel to the ArduinoScope
        plotting widget.  The arguments are passed unchanged to
        add_samples().
        """

        if self.scope is not None:
            self.scope.add_samples( name, y, t )

    def replotScope(self):
        """Update the ArduinoScope plot area after all new data has been added."""
        if self.scope is not None:
            self.scope.replot()


################################################################
