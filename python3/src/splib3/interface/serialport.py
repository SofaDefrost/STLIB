import Sofa
import serial
import serial.tools.list_ports


def getDevicePort(entry, method="manufacturer"):
    """
    Returns list of serial ports from chosen method. Available method:
     - manufacturer
     - description
     - serial_number
    """
    ports = []
    comports = serial.tools.list_ports.comports()

    if comports is None:
        Sofa.msg_error("stlib3.interface.serialport",
                       "Serial ports check failed, list of ports is empty.")
        return

    if method == "manufacturer":
        ports = [p for p in comports if entry in p.manufacturer]
    if method == "description":
        ports = [p for p in comports if entry in p.description]
    if method == "serial_number":
        ports = [p for p in comports if entry in p.serial_number]

    if not ports:
        Sofa.msg_error("stlib3.interface.serialport",
                       "No serial port found with " + method + " = " + entry)
        return

    if len(ports) > 1:
        Sofa.msg_warning("stlib3.interface.serialport",
                         "Multiple port found with " + method + " = " + entry + ". Using the first.")

    Sofa.msg_info("stlib3.interface.serialport",
                  "Found port with " + method + " = " + entry + ": \n" +
                  "device : " + ports[0].device + "\n" +
                  "manufacturer : " + ports[0].manufacturer + "\n" +
                  "description : " + ports[0].description + "\n" +
                  "serial number : " + ports[0].serial_number
                  )
    return ports[0].device


def createScene(rootnode):
    getDevicePort("Arduino", method="manufacturer")
