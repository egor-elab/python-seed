import os
import json

from instruments.plugins import InstrumentManagerPlugin
from .usb_server.usbdetector import USBDetectorFactory

LOCALROOT = os.path.dirname(__file__)


class USBDetector(InstrumentManagerPlugin):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = os.path.join(LOCALROOT, path)

    def run(self):
        '''
        This function gets called by start_plugins method of
        the instrument manager class
        '''

        with USBDetectorFactory(cpath=self.path)() as usb:
            while True: #not self.halted.is_set():
                if (len(usb.new_devices)):
                    port_info = usb.new_devices.pop()
                    self.instrument_mgr.instruments.add(port_info)

                if (len(usb.removed_devices)):
                    port_info = usb.removed_devices.pop()
                    self.instrument_mgr.instruments.remove(port_info)


