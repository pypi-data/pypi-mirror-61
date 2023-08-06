# usb_can_analyzer_py
Python library for the usb can analyzer.
========================================================

The Converter class allows to read/write data from/to a USB connection with a
usb can analyzer.

You can install it with pip:

    pip install usb_can_analyzer

Exemple d'usage:

    Read data:
    >>> from usb_can_analyzer import Converter
    >>> converter = Converter("/dev/ttyUSB0")
    >>> while True:
    ...   data = converter.readMessage()
    ...     if type(data) != int:
    ...       print(data)
