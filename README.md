
This script captures from RTSP or USB camera connected to device and sends images to azure blob.

Prerequiste 
    python3 :: installon windows using link https://www.python.org/downloads/windows/

install following packages

    pip3 install opencv-python
    
    pip3 install --upgrade azure-storage

How to use 

    on device 
    
        python3 edge_to_blob.py -s "usb" -t 4 -m True
            -s == sets the source replace with rtsp strema address in case you want images from rtsp stream
            -t == sets the time delay between transfer to blob 4 means we will capture images every 4 sec and send to cloud
            -m = manual mode open a window and only sends an image when user press SPACE and stop at ESC 


