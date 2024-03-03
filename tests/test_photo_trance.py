import zmq
import struct
import time
import io
from PIL import Image
import cv2
import socket


def compres_func():
    frame = cv2.imread('/Users/p4sh4bsc/python_projects/nto/NTO_AKS/tests/photo_test.jpeg') 
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    resized_img = cv2.resize(frame, (100, 100))
    compressed_img = cv2.imencode('.jpeg', resized_img)[1].tobytes()
    img_len = len(compressed_img)

    return compressed_img, img_len

def main():
    global data
    global data_length
    time.sleep(1)
    request_context = zmq.Context()
    response_context = zmq.Context()


    RECEIVE_PORT = 3333
    REQUEST_PORT = 2222

    response_queue = response_context.socket(zmq.PUSH)
    response_queue.bind(f"tcp://*:{RECEIVE_PORT}")

    request_queue = request_context.socket(zmq.PULL)
    request_queue.connect(f"tcp://localhost:{REQUEST_PORT}")



    while True:
        frame, img_len = compres_func()
        for i in range(img_len // 512):
            try:
                response_queue.send_pyobj(b"BGN" + frame[512*i:512*(i+1)] + b"END")
            except zmq.ZMQError:
                response_queue.send_pyobj(b"")
        ost = img_len % 512
        if ost != 0:
            try:
                response_queue.send_pyobj(b"BGN" + frame[-ost:] + b"END")
            except zmq.ZMQError:
                request_queue.send_pyobj(b"")
            response_queue.send_pyobj(b" ")
            break

if __name__ == "__main__":
    main()
    print('done')