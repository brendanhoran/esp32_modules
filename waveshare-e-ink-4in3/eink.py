# Author Brendan Horan
# License : BSD 3-Clause
# Description : Control the Wave Share 4.2" e-ink display

from machine import UART
from time import sleep


class EINK_serial_not_ready(Exception):
    pass


class EINK_invalid_cmd(Exception):
    pass


class EINK_invalid_line_position(Exception):
    pass


class EINKBase:
    def __init__(self, rx_pin, tx_pin):
        """Initialize the sensor.

        Keyword arguments:
        rx_pin -- pin number of the rx pin
        tx_pin -- pin number of the tx pin


        """

        # Set up the serial port according to the docs
        uart = UART(1)
        uart.init(115200, bits=8, parity=None, stop=1, rx=rx_pin, tx=tx_pin)
        self.uart = uart


class EINK_display(EINKBase):
    # See manual section 3.1.2 command frame format
    _FRAME_END = bytes([0xCC, 0x33, 0xC3, 0x3C])
    _FRAME_HEADER = bytes([0xA5])

    # See manual section 3.2.2 command expiation
    _SYS_CMD_HANDSHAKE = \
        bytes([0xA5, 0x00, 0x09, 0x00, 0xCC, 0x33, 0xC3, 0x3C, 0xAC])
    _SYS_CMD_REFRESH = \
        bytes([0xA5, 0x00, 0x09, 0x0A, 0xCC, 0x33, 0xC3, 0x3C, 0xA6])
    _SYS_CMD_CLEAR_SCREEN = \
        bytes([0xA5, 0x00, 0x09, 0x2E, 0xCC, 0x33, 0xC3, 0x3C, 0x82])
    _SYS_CMD_UPDATE_SCREEN = \
        bytes([0xA5, 0x00, 0x09, 0x0A, 0xCC, 0x33, 0xC3, 0x3C, 0xA6])
    _SYS_CMD_ENG_FONT_SIZE_32 = \
        bytes([0xA5, 0x00, 0x0A, 0x1E, 0x01, 0xCC, 0x33, 0xC3, 0x3C, 0xB0])
    _SYS_CMD_ENG_FONT_SIZE_48 = \
        bytes([0xA5, 0x00, 0x0A, 0x1E, 0x02, 0xCC, 0x33, 0xC3, 0x3C, 0xB3])
    _SYS_CMD_ENG_FONT_SIZE_64 = \
        bytes([0xA5, 0x00, 0x0A, 0x1E, 0x03, 0xCC, 0x33, 0xC3, 0x3C, 0xB2])
    _SYS_CMD_GET_ENG_FONT_SIZE = \
        bytes([0xA5, 0x00, 0x09, 0x1D, 0xCC, 0x33, 0xC3, 0x3C, 0xB1])
    _DISPLAY_CMD_STRING = bytes([0x30])
    _PADDING = bytes([0x00])

    def _calculate_parity(self, frame):
        """Calculate the parity bit, from frame header to frame end."""

        # Set the initial parity to zero so we have something to XOR
        parity = 0
        # For each byte in the frame, XOR it against the previous parity value
        for byte in frame:
            parity ^= byte
        return(parity)

    def hand_shake(self):
        """Try handshake with the e-ink controller.

        Returns OK as two bytes if the handshake was successful


        """

        self.uart.write(self._SYS_CMD_HANDSHAKE)

        # the e-ink controller takes around 100ms to reply
        sleep(0.100)
        hand_shake_status = self.uart.read(2)
        if hand_shake_status.decode() == "OK":
            return (hand_shake_status)
        else:
            raise EINK_serial_not_ready("Handshake failed")

    def clear_display(self):
        """Clear the display, takes no arguments."""

        # send the clear display command , followed by an screen update
        self.uart.write(self._SYS_CMD_CLEAR_SCREEN)
        self.uart.write(self._SYS_CMD_REFRESH)

    def set_font_size(self, size):
        """Set the English display font size.

        Keyword arguments:
        size -- font size small,medium and large


        """
        # write a command to the display to set the size based on args
        # Only changed once per update
        if size == "small":
            self.uart.write(self._SYS_CMD_ENG_FONT_SIZE_32)
        elif size == "medium":
            self.uart.write(self._SYS_CMD_ENG_FONT_SIZE_48)
        elif size == "large":
            self.uart.write(self._SYS_CMD_ENG_FONT_SIZE_64)
        else:
            raise EINK_invalid_cmd("Invalid size command")

    def get_font_size(self):
        """Get the currently set font size

        Takes no arguments, returns the currently set font size

        """

        # List of bytes we can expect as valid front index's
        _VALID_FONT_INDEXES = [b'1', b'2', b'3', b'11', b'22', b'33']

        # query the display for the font size
        self.uart.write(self._SYS_CMD_GET_ENG_FONT_SIZE)
        # sleep to ensure the command returns, then read the result
        sleep(0.100)
        current_font_index = self.uart.read(2)
        # If we get "OK" back means we need to re-read the serial line
        # for the actual returned value
        if current_font_index == b"OK":
            current_font_index = self.uart.read(2)
            self.get_font_size()
        # Match a font index and return the English size name
        if current_font_index in _VALID_FONT_INDEXES:
            if (current_font_index == b'1') or (current_font_index == b'11'):
                return("small")
            if (current_font_index == b'2') or (current_font_index == b'22'):
                return("medium")
            if (current_font_index == b'3') or (current_font_index == b'33'):
                return("large")
            else:
                print("no size")

    def write_string(self, string, x_pos, y_pos):
        """Write a text string to the eink display

        Keyword arguments:
        string -- Text string to write to the display
        x_pos -- X position of the start of the string
        y_pos -- Y position of the start of the string


        """

        # convert the x and y pos into bytes
        # x and y pos are two bytes wide
        x_pos = x_pos.to_bytes(2, 'big')
        y_pos = y_pos.to_bytes(2, 'big')

        # convert the string into hex
        string = bytes(string.encode('hex'))

        # get length of string add up total length of frame
        # see section 3.1.2 only the string length is variable
        # frame length is also two bytes wide
        frame_length = len(string)
        frame_length = frame_length + 14
        frame_length = frame_length.to_bytes(2, 'big')

        # construct the pre parity bit frame
        frame = self._FRAME_HEADER + frame_length + \
            self._DISPLAY_CMD_STRING + x_pos + \
            y_pos + string + self._PADDING + self._FRAME_END

        # work out the parity bit
        # parity bit is always one byte wide
        parity_bit = self._calculate_parity(frame)
        parity_bit = parity_bit.to_bytes(1, 'big')

        # construct the complete frame
        frame = frame + parity_bit

        # write the frame to the internal buffer, then update the eink display
        # do not issue a clear, user should control when to clear the screen
        self.uart.write(frame)
        self.uart.write(self._SYS_CMD_REFRESH)

    def write_line(self, string, size, line_number):
        """Write text based on a line number and size

        Keyword arguments:
        string -- Text string to write to the display
        font size -- size of the font to use (small, medium, large)
        line number - vertical line number to write text to, max 10, 13, 21


        """

        # Define the maximum lines per font size
        _large_font = [0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600]
        _medium_font = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500,
                        550, 600]
        _small_font = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300,
                       330, 360, 390, 420, 450, 480, 510, 540, 570, 600]

        # Not a huge fan of the below if blocks
        # will try find a cleaner, simpler way later
        # for now just select a line number and write to it

        if size == "large":
            self.set_font_size("large")
            _max_lines = 10
            if line_number == 1:
                self.write_string(string, _large_font[0], _large_font[0])
            elif line_number == 2:
                self.write_string(string, _large_font[0], _large_font[1])
            elif line_number == 3:
                self.write_string(string, _large_font[0], _large_font[2])
            elif line_number == 4:
                self.write_string(string, _large_font[0], _large_font[3])
            elif line_number == 5:
                self.write_string(string, _large_font[0], _large_font[4])
            elif line_number == 6:
                self.write_string(string, _large_font[0], _large_font[5])
            elif line_number == 7:
                self.write_string(string, _large_font[0], _large_font[6])
            elif line_number == 8:
                self.write_string(string, _large_font[0], _large_font[7])
            elif line_number == 9:
                self.write_string(string, _large_font[0], _large_font[8])
            elif line_number == 10:
                self.write_string(string, _large_font[0], _large_font[9])
            else:
                raise EINK_invalid_line_position("Invalid line number {0}, \
                    max lines supported are {1}".format(line_number,
                                                        _max_lines))
        elif size == "medium":
            self.set_font_size("medium")
            _max_lines = 13
            if line_number == 1:
                self.write_string(string, _medium_font[0], _medium_font[0])
            elif line_number == 2:
                self.write_string(string, _medium_font[0], _medium_font[1])
            elif line_number == 3:
                self.write_string(string, _medium_font[0], _medium_font[2])
            elif line_number == 4:
                self.write_string(string, _medium_font[0], _medium_font[3])
            elif line_number == 5:
                self.write_string(string, _medium_font[0], _medium_font[4])
            elif line_number == 6:
                self.write_string(string, _medium_font[0], _medium_font[5])
            elif line_number == 7:
                self.write_string(string, _medium_font[0], _medium_font[6])
            elif line_number == 8:
                self.write_string(string, _medium_font[0], _medium_font[7])
            elif line_number == 9:
                self.write_string(string, _medium_font[0], _medium_font[8])
            elif line_number == 10:
                self.write_string(string, _medium_font[0], _medium_font[9])
            elif line_number == 11:
                self.write_string(string, _medium_font[0], _medium_font[10])
            elif line_number == 12:
                self.write_string(string, _medium_font[0], _medium_font[11])
            elif line_number == 13:
                self.write_string(string, _medium_font[0], _medium_font[12])
            else:
                raise EINK_invalid_line_position("Invalid line number {0}, \
                    max lines supported are {1}".format(line_number,
                                                        _max_lines))
        elif size == "small":
            self.set_font_size("small")
            _max_lines = 21
            if line_number == 1:
                self.write_string(string, _small_font[0], _small_font[0])
            elif line_number == 2:
                self.write_string(string, _small_font[0], _small_font[1])
            elif line_number == 3:
                self.write_string(string, _small_font[0], _small_font[2])
            elif line_number == 4:
                self.write_string(string, _small_font[0], _small_font[3])
            elif line_number == 5:
                self.write_string(string, _small_font[0], _small_font[4])
            elif line_number == 6:
                self.write_string(string, _small_font[0], _small_font[5])
            elif line_number == 7:
                self.write_string(string, _small_font[0], _small_font[6])
            elif line_number == 8:
                self.write_string(string, _small_font[0], _small_font[7])
            elif line_number == 9:
                self.write_string(string, _small_font[0], _small_font[8])
            elif line_number == 10:
                self.write_string(string, _small_font[0], _small_font[9])
            elif line_number == 11:
                self.write_string(string, _small_font[0], _small_font[10])
            elif line_number == 12:
                self.write_string(string, _small_font[0], _small_font[11])
            elif line_number == 13:
                self.write_string(string, _small_font[0], _small_font[12])
            elif line_number == 14:
                self.write_string(string, _small_font[0], _small_font[13])
            elif line_number == 15:
                self.write_string(string, _small_font[0], _small_font[14])
            elif line_number == 16:
                self.write_string(string, _small_font[0], _small_font[15])
            elif line_number == 17:
                self.write_string(string, _small_font[0], _small_font[16])
            elif line_number == 18:
                self.write_string(string, _small_font[0], _small_font[17])
            elif line_number == 19:
                self.write_string(string, _small_font[0], _small_font[18])
            elif line_number == 20:
                self.write_string(string, _small_font[0], _small_font[19])
            elif line_number == 21:
                self.write_string(string, _small_font[0], _small_font[20])
            else:
                raise EINK_invalid_line_position("Invalid line number {0}, \
                    max lines supported are {1}".format(line_number,
                                                        _max_lines))
