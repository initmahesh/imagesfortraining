
This script captures images from RTSP or USB camera connected to device and sends images to azure blob as per credentials providedin constants.py

Runing using Docker 

       sudo docker run --rm -it -e DISPLAY=:0 --ipc host -v /tmp/.X11-unix:/tmp/.X11-unix --network host --privileged -v /dev:/dev --env-file .env initmahesh/getimagefromedge:0.1

Runing with python 

    Prerequiste 
        python3
        pip3 

    How to run this sample

    1. Clone this repo
    2. Update .env file with required setting to run the script  
    3. Install following packages in requirements.txt
        pip3 install -r requirements.txt
    4. for using manual mode use below command only once to allow opencv to open windows on host 

        sudo xhost +

    5. start the script

            python3 edge_to_blob.py -s "usb" -t 4 -m True
                -s == sets the source replace with rtsp strema address in case you want images from rtsp stream
                -t == sets the time delay between transfer to blob 4 means we will capture images every 4 sec and send to cloud
                -m = manual mode open a window and only sends an image when user press SPACE and stop at ESC 


