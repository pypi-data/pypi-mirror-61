# pyeasyb
Python tools for EASYBus Sensor modules from GMH Messtechnik GmbH


### Features

* easyb-tool.py to run commands for a list of devices or reading data continuously.

## Installation

You can install unqlite using `pip`.

    pip install easyb

## Usage

```
Usage: easyb-tool.py [options] arg1 arg2

Options:
  -h, --help            show this help message and exit
  -v 1, --verbose=1     run verbose level [0..3]
  -r, --read            read values continuously
  -l, --list            list device and commands
  -i 2.0, --interval=2.0
                        interval between measurements for read mode (in seconds)

  Device Options:
    Set device type, command or address to use.

    -d DEVICE, --device=DEVICE
                        use device
    -c 0, --command=0   run command

  Serial Options:
    Set serial port options.

    -p /dev/ttyUSB0, --port=/dev/ttyUSB0
                        serial port
    -b 4800, --baudrate=4800
                        serial port baudrate
    -t 2, --timeout=2   serial port timeout (in seconds)
    -w 2, --writetimeout=2
                        serial port write timeout
    -o excel/text, --output=excel/text
                        output type
    -f measurement, --filename=measurement
                        filename for output

  Output Options:
    Set output to file.
```
