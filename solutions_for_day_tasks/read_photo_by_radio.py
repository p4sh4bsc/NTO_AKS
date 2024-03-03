import rospy
import serial
import struct
import time
import io
from PIL import Image

rospy.init_node("radio_receiver")

ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0', 38400, timeout=0.2)
ser.setDTR(False)

def main():
    data = b''
    while not rospy.is_shutdown():
        time.sleep(0.1)
        if ser.inWaiting() > 4:
            begin_pack = ser.read(4).decode('utf-8') # BGN
            if begin_pack == "BGN":
                data += ser.read_until(b"META")[:-4]
                meta = struct.unpack('3df?', ser.read_until(b"END")[:-3]) # 3 doble 1 float 1 bool (? - bool, f - float, d - double)
                rospy.loginfo(meta)
            ser.reset_input_buffer()
    img = Image.open(io.BytesIO(data))
    img.save("./img_from_bytes_for_main.jpg")

if __name__ == "__main__":
    main()