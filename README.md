### ImagesForTraining
This script and docker container captures images from RTSP or USB camera connected to device and sends images to azure blob as per credentials provided in .env file

#### Run using Docker 
1. Clone this repo
2. **Make sure you modify the .env file with your storage credentials**
3. If using manual mode use below command to allow display to work from container 
              **sudo xhost +**
4. Use below command to download and run the docker container
      -       sudo docker run --rm -it -e DISPLAY=:0 --ipc host -v /tmp/.X11-unix:/tmp/.X11-unix --network host --privileged -v /dev:/dev --env-file .env initmahesh/getimagefromedge:0.1

#### Run with python 

 ######Prerequiste 
   -  python3
   -  pip3 

 ######How to run this sample

   1. Clone this repo
   2. **Update .env file with required setting to run the script**
   3. Install following packages in requirements.txt
       -      pip3 install -r requirements.txt
   4. For using manual mode use below command only once to allow opencv to open windows on host 
        -     sudo xhost +
   5. Start the script
         -    python3 edge_to_blob.py 
