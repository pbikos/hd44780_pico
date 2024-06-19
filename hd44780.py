


"""
TODO: Modify comments in Doxygen friendly form

"""


"""

hd44780 is a module providing connectivity to an LCD display with a Hitachi
HD44780 or compatible controller.

Functionality is provided as a class, thus enabling the simultaneous use
of more than one displays.

"""
from machine import Pin
import time



class lcd():

    """

    lcd class is the module's sole class.

    """



    def __init__(self,four_bit_mode,lines,font,read_write_mode,pinout):

        """

        Constructor needs following arguments:


        four_bit_mode: Boolean.
        True if data interface with display is 4 bits, False if 8 bits.

        lines: Integer.
        1 for a module with 2 display lines, 0 for a module with 1 display line.

        font: Integer.
        1 for 5x10 font, 0 for 5x8 font

        read_write_mode: Boolean.
        True if communication with display is bidirectional (especially Busy Flag/D7),
        False if unidirectional (only from microcontroller to display)

        pinout: A dictionary containing entries with the following keys.
        'RS_GP_PIN'
        'RW_GP_PIN'
        'E_GP_PIN'
        'D0_GP_PIN' (for 8 bit mode)
        'D1_GP_PIN' (for 8 bit mode)
        'D2_GP_PIN' (for 8 bit mode)
        'D3_GP_PIN' (for 8 bit mode)
        'D4_GP_PIN'
        'D5_GP_PIN'
        'D6_GP_PIN'
        'D7_GP_PIN'
        All values must be integers and correspond to the GPIO pins connected
        to the respective display module pins.

        IMPORTANT: pinout must be passed as an existing dictionary variable,
        and not as arguments (thus no **kwargs)

        """

        self.four_bit_mode=four_bit_mode			# 4 bit mode
        self.lines=lines					# rows of the display
        self.font=font						# font
        self.read_write_mode=read_write_mode			# Busy Flag probing
        self.rs=Pin(pinout['RS_GP_PIN'],Pin.OUT,value=0)	# RS
        self.rw=Pin(pinout['RW_GP_PIN'],Pin.OUT,value=0)	# RW
        self.e=Pin(pinout['E_GP_PIN'],Pin.OUT,value=0)		# E
        self.d=[
        0 if four_bit_mode else Pin(pinout['D0_GP_PIN'],Pin.OUT,value=0),	# D0
        0 if four_bit_mode else Pin(pinout['D1_GP_PIN'],Pin.OUT,value=0),	# D1
        0 if four_bit_mode else Pin(pinout['D2_GP_PIN'],Pin.OUT,value=0),	# D2
        0 if four_bit_mode else Pin(pinout['D3_GP_PIN'],Pin.OUT,value=0),	# D3
        Pin(pinout['D4_GP_PIN'],Pin.OUT,value=0),	# D4
        Pin(pinout['D5_GP_PIN'],Pin.OUT,value=0),	# D5
        Pin(pinout['D6_GP_PIN'],Pin.OUT,value=0),	# D6
        Pin(pinout['D7_GP_PIN'],Pin.OUT,value=0)	# D7
        ]
        self.reset()



    def reset(self,fourbit=None,lines=None,font=None):
        """
        reset() resets the board by performing the Initializing by Instruction procedure
        it is possible to bypass the settings provided during object instantiation:
        four bit mode, number of lines and font can be provided as arguments.
        For their values refer to documentation of __init__()
        """
        rwm=self.read_write_mode	# temporarily store Busy Flag probing setting
        self.read_write_mode=0		# temporarily disable Busy Flag probing, if set
        if fourbit is None:		# if fourbit is not provided:
            fourbit=self.four_bit_mode	# use the default mode
        if lines is None:		# if lines is not provided:
            lines=self.lines		# use the default mode
        if font is None:		# if font is not provided:
            font=self.font		# use the default mode
        time.sleep_ms(40)		# initial internal reset duration in ms, refer to datasheet
        for i in range(3):		# send the initialization command 3 times
            self.command('000011',True,40000)	# refer to Hitachi datasheet figures 23 & 24
        if fourbit is False:		# 8 bit interface
            self.command('000011'+str(lines)+str(font)+'00',False,40000)	# function set
        else:				# 4 bit interface
            self.command('000010',True,40000)	# set to 4 bits
            self.command('000010',True,40000)	# set to 4 bits
            self.command('00'+str(lines)+str(font)+'00',True,40000)	# function set
        self.read_write_mode=rwm	# reenable Busy Flag probing, if applicable


    def status(self):

        """
        status() prints the status of module's pins.
        Sequence is identical to the one depicted in HD44780 datasheet:
        RS RW D7 D6 D5 D4 D3 D2 D1 D0	for 8-bit operations,
        RS RW D7 D6 D5 D4		for 4-bit operations
        """

        print(self.rs.value(),self.rw.value(),\
        self.d[7].value(),self.d[6].value(),self.d[5].value(),self.d[4].value(),end='')
        if not (self.four_bit_mode):
            print('',self.d[3].value(),self.d[2].value(),self.d[1].value(),self.d[0].value(),end='')
        print("")



    def issue(self,delay):

        """

        TODO:
        READ-WRITE MODE BY SAMPLING E

        issue() signals the module to read or write data in bus, by a positive pulse of E pin
        if the module is in read write mode, Busy flag from D7 is sampled
        if the module is in read only mode, timing is achieved by appropriate delays
        between commands

        delay is provided in microseconds

        """

        if(self.read_write_mode):
            print("TODO")
        else:
            if delay==0:		# command() had been called with no delay argument
                delay=53		# execution time related to Fosc, refer to datasheet
            self.e.value(1)		# positive edge of E pin
            time.sleep_us(delay)	# delay
            self.e.value(0)		# negative edge of E pin toggles display
            time.sleep_us(delay)	# delay



    def command(self,cmdstr,fourbit=None,delay=0):

        """
        command() issues the given command to the display.

        Command must be provided as a 10-character length string for 8 bit commands,
        or as a 6-character length string for 4 bit commands.
        Command string must consist only of characters '1' or '0'
        Command sequence is identical to the one depicted in HD44780 datasheet:
        RS RW D7 D6 D5 D4 D3 D2 D1 D0   for 8-bit operations,
        RS RW D7 D6 D5 D4       for 4-bit operations

        fourbit must be True for 4 bit data bus, or False for 8 bit data bus.
        If not provided, the default mode provided at class initialization will be used.

        delay is the delay(in microseconds) passed to issue()

        IMPORTANT: size of command and size of data bus are not identical.
        We can issue 8 bit commands with a 4 bit data bus (split in 4 bit 2 commands)
        as well as issue 4 bit commands (for example '000010', "set 4 bit operation")
        under any circumstances.

        """
        if fourbit is None:			# if fourbit is not provided:
            fourbit=self.four_bit_mode		# use the default mode
        self.rs.value(int(cmdstr[0]))		# set RS pin
        self.rw.value(int(cmdstr[1]))		# set RW pin
        self.d[7].value(int(cmdstr[2]))		# set D7 pin
        self.d[6].value(int(cmdstr[3]))		# set D6 pin
        self.d[5].value(int(cmdstr[4]))		# set D5 pin
        self.d[4].value(int(cmdstr[5]))		# set D4 pin
        if len(cmdstr)==10:			# if we have an 8 bit command
            if not (fourbit):			# and we are in 8 bit mode
                self.d[3].value(int(cmdstr[6]))	# set D3 pin
                self.d[2].value(int(cmdstr[7]))	# set D2 pin
                self.d[1].value(int(cmdstr[8]))	# set D1 pin
                self.d[0].value(int(cmdstr[9]))	# set D0 pin
                self.issue(delay)		# issue command to display
            else:				# 8 bit command but 4 pin mode
                self.issue(delay)		# issue the first 4 bits
                self.d[7].value(int(cmdstr[6]))	# set D7 pin
                self.d[6].value(int(cmdstr[7]))	# set D6 pin
                self.d[5].value(int(cmdstr[8]))	# set D5 pin
                self.d[4].value(int(cmdstr[9]))	# set D4 pin
                self.issue(delay)		# issue the last 4 bits
        else:					# 4 bit command
            self.issue(delay)			# issue command to display
