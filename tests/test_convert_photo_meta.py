
import serial
import struct
import time
import cv2
import zlib
import os
from PIL import Image
import piexif
import pickle
import io


def get_frame():
    frame1 = cv2.imread('/Users/p4sh4bsc/python_projects/nto/NTO_AKS/image_mod.jpeg') 
    frame = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
    resized_img = cv2.resize(frame, (100, 100))
    compressed_img = cv2.imencode('.jpeg', frame1)[1].tobytes()
    img_len = len(compressed_img)

    return compressed_img, img_len

def main():
    data = "{'x_cords': 123.122, 'y_cords': 213, 'btn': True}"
    with Image.open('/Users/p4sh4bsc/python_projects/nto/NTO_AKS/tests/photo_test.jpeg') as img:
        exif_ifd = {piexif.ExifIFD.UserComment: data.encode()}
        exif_dict = {"0th": {}, "Exif": exif_ifd, "1st": {}, "thumbnail": None, "GPS": {}}

        exif_dat = piexif.dump(exif_dict)
        img.save('image_mod.jpeg',  exif=exif_dat)
    bytes = get_frame()[0]
    img = Image.open(io.BytesIO(bytes))
    img.save("/Users/p4sh4bsc/python_projects/nto/NTO_AKS/meta_meta.jpeg")

if __name__ == "__main__":
    main()