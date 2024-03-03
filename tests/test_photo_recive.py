import zmq
import struct
import time
import io
from PIL import Image
import cv2


def main():
    request_context = zmq.Context()
    response_context = zmq.Context()


    RECEIVE_PORT = 2222
    REQUEST_PORT = 3333

    response_queue = response_context.socket(zmq.PUSH)
    response_queue.bind(f"tcp://*:{RECEIVE_PORT}")

    request_queue = request_context.socket(zmq.PULL)
    request_queue.connect(f"tcp://localhost:{REQUEST_PORT}")
    print('c]q')
    time.sleep(4)
    data = b''
    print('z')
    while True:
        print('c')
        try:
            part_of_photo = request_queue.recv_pyobj()
            if len(part_of_photo)<3:
                print(len(part_of_photo))
                break
            else:
                print(len(data))
                data+=part_of_photo[3:-3]
        except zmq.ZMQError:
            data+=b''
            print('123')
    print(data, len(data))
    img = Image.open(io.BytesIO(data))
    img.save("/Users/p4sh4bsc/python_projects/nto/NTO_AKS/tests/img_from_bytes_for_main.jpeg")

if __name__ == "__main__":
    main()