import os
import json

from instruments.plugins import InstrumentManagerPlugin
from .usb_server.usbdetector import USBDetectorFactory

LOCALROOT = os.path.dirname(__file__)


class USBDetector(InstrumentManagerPlugin):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = os.path.join(LOCALROOT, path)
        print('constructing usb detector class')

    def run(self):
        print("starting usb detector class")
        with USBDetectorFactory(cpath=self.path)() as usb:
            while not self.halted.is_set():
                if (not usb.empty):
                    port = json.loads(usb.pop())  # parse json here
                    print('port: ', port)

                    '''
                    try:
                        inst = InstrumentFactory(port, self.timeout)
                    except (
                        serial.SerialException,
                        TimeoutError,
                        KeyError,
                        UnicodeDecodeError
                    ):
                        continue
                    else:
                        if inst is None:
                            self.unknown_insts.append(port)
                            print('unknown {}'.format(inst))
                        else:
                            print('got {}'.format(inst))
                            self.instruments[inst.name] = inst
                    '''
