import cv2
import os, uuid, sys, time, socket, shutil, argparse, math
from azure.storage.blob import BlockBlobService, PublicAccess
from azure.storage.queue import QueueService
from dotenv import load_dotenv

#reading parametes from .env file 
load_dotenv()
#Storage account credentials to load files 
STORAGE_ACCOUNT_NAME = os.getenv('STORAGE_ACCOUNT_NAME')
STORAGE_ACCOUNT_KEY = os.getenv('STORAGE_ACCOUNT_KEY')
STORAGE_ACCOUNT_SUFFIX = os.getenv('STORAGE_ACCOUNT_SUFFIX')
#input to take frames support usb and rtsp address  
SOURCE = os.getenv('SOURCE')
#time to wait between image uploads as numeric value example 2 will upload an image every 2 secs
TIME_DELAY = os.getenv('TIME_DELAY')
#manual mode will pop up a window and a picture will be uploaded when SPACE is pressed, press ESC to quit
MANUAL_MODE = os.getenv('MANUAL_MODE')

container_name = None 
queue_service = None
block_blob_service = None
queue_service = None


def __createstorage():
    global container_name
    global queue_service
    global SOURCE
    global block_blob_service
    global queue_service 
    block_blob_service = BlockBlobService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY, endpoint_suffix=STORAGE_ACCOUNT_SUFFIX)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    container_name = 'fromcamera' + timestr
    block_blob_service.create_container(container_name)
    block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
    queue_service = QueueService(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY, endpoint_suffix=STORAGE_ACCOUNT_SUFFIX)
    queue_service.create_queue('fromcamera' + timestr)

def main():
    global container_name
    global block_blob_service
    global queue_service
    global SOURCE
    global time 
    global TIME_DELAY
    global MANUAL_MODE
    #Creating storage with given credentials
    __createstorage()
    i = 0

    if SOURCE is not None:
        if SOURCE == 'usb':
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(SOURCE)
    else:
        print("Please set the valuse of SOURCE variable in .env file")

    ret = True

    print('Created stream')
    while ret:
        # reading frames 
        ret, frame = cap.read()
        if(frame is None):
            print("Unable to capture frame from source :" + SOURCE)
            print("Please check correct SOURCE variable is set in .env file")
            ret= False
            break   

        # starting a window on device if manual mode is selected
        if(MANUAL_MODE):
            cv2.namedWindow("Press SPACE to capture or ESC to quit")
            cv2.imshow("Press SPACE to capture or ESC to quit", frame)
            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                cv2.destroyAllWindows()
                ret=False
               
            elif k%256 == 32:
                # SPACE pressed
                i+=1
                print("frame capture function retuned :: " +  str(ret) + " storing to container :: " + container_name)
                image_jpg = cv2.imencode('.jpg',frame)[1].tostring()
                blob_name='image' + str(i) +'.jpg'
                blobprops = block_blob_service.create_blob_from_bytes(container_name, blob_name, image_jpg)
                queueprops = queue_service.put_message(container_name, str(block_blob_service.make_blob_url(container_name, blob_name)))
                print("Total files stored :: " + str(i))
        else:    
            ret, frame = cap.read()
            i+=1
            print("frame capture function returned :: " +  str(ret) + " storing to container :: " + container_name)
            image_jpg = cv2.imencode('.jpg',frame)[1].tostring()
            blob_name='image' + str(i) +'.jpg'
            blobprops = block_blob_service.create_blob_from_bytes(container_name, blob_name, image_jpg)
            queueprops = queue_service.put_message(container_name, str(block_blob_service.make_blob_url(container_name, blob_name)))
            print("Total files stored :: " + str(i))
            time.sleep(TIME_DELAY)
    cap.release()
    print('Released stream')


if __name__ == "__main__":
    main()
