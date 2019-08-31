import cv2
import os, uuid, sys, time, socket, shutil, argparse, math
from azure.storage.blob import BlockBlobService, PublicAccess
from azure.storage.queue import QueueService
from dotenv import load_dotenv

#reading parametes from .env file 
load_dotenv()

STORAGE_ACCOUNT_NAME = os.getenv('STORAGE_ACCOUNT_NAME')
STORAGE_ACCOUNT_KEY = os.getenv('STORAGE_ACCOUNT_KEY')
STORAGE_ACCOUNT_SUFFIX = os.getenv('STORAGE_ACCOUNT_SUFFIX')

container_name = None 
queue_service = None
block_blob_service = None
queue_service = None
manual_mode = None



#Parsing command line parameters
parser = argparse.ArgumentParser(description= "This sample takes rtsp stream address as argument and send images to azureblob")
parser.add_argument('-s','--source',help ='pass the rtsp stream to module or usb dev id eg:- python3 rtsptoblob -s \"rtsp://192.168.0.106:8900/live\" or for usb -s "usb"')
parser.add_argument('-t','--time_delay',help ='specify time to wait between image uploads as numeric value example -t 2 will upload an image every 2 secs',type=int, default=1)
parser.add_argument('-m','--manual_mode',help ='setting manual mode will pop up a window end a picture will be uploaded when a SPACE ',type=bool,default=False)

args = parser.parse_args()
if args.source is not None:
    capture_url = args.source 
    if(capture_url == "usb"):
        capture_url = 0
        print("capture from usb cam :: " + str(capture_url))
    else:
        print("capture url is :: " + capture_url)
else:
    print("please pass the rtsp string to prcoess by using parameter -r eg:- python3 rtsptoblob -r \"rtsp://192.168.0.106:8900/live\"")
    exit
if args.time_delay is not None:
    time_delay = args.time_delay
    print("set time delay to : " + str(time_delay))

if args.manual_mode :
    manual_mode = args.manual_mode
    print("set time delay to : " + str(manual_mode))

def __createstorage():
    global container_name
    global queue_service
    global capture_url
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
    global capture_url
    global time 
    global time_delay
    global manual_mode
    #Creating storage with given credentials
    __createstorage()
    i = 0


    cap = cv2.VideoCapture(capture_url)
    ret = True

    print('Created stream')
    while ret:
        # reading frames 
        ret, frame = cap.read()

        # starting a window on device if manaul mode is selected
        if(manual_mode):
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
            print("frame capture function retuned :: " +  str(ret) + " storing to container :: " + container_name)
            image_jpg = cv2.imencode('.jpg',frame)[1].tostring()
            blob_name='image' + str(i) +'.jpg'
            blobprops = block_blob_service.create_blob_from_bytes(container_name, blob_name, image_jpg)
            queueprops = queue_service.put_message(container_name, str(block_blob_service.make_blob_url(container_name, blob_name)))
            print("Total files stored :: " + str(i))
            time.sleep(time_delay)
    cap.release()
    print('Released stream')


if __name__ == "__main__":
    main()
