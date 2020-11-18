import datetime, time
from threading import Thread
from collections import deque
from multiprocessing import Process
import gc
import cv2
# from flask import Flask
# from flask_sockets import Sockets
import Config
import os
import multiprocessing
Config.Config()
import ctypes
import logging


# app = Flask(__name__)
# sockets = Sockets(app)
try:
    temp = ctypes.cdll.LoadLibrary('libopenh264-1.8.0-linux64.4.so')
    temp1 = ctypes.cdll.LoadLibrary('libopenh264-1.8.0-linux64.4.so.sig')

except:
    pass
def producer(cap, q, camera_index, outVideo, path1):
    # cap = cv2.VideoCapture(int(0), cv2.CAP_DSHOW)
    global log
    # log.info("camera {}".format(camera_index) + " Success")
    index = 0
    timelog = 0
    count = 0
    a = 0
    while True:
        try:
            if cap.isOpened():
                a = 0 
                if index == 0:
                    index = index+1
                    log.info("camera {}".format(camera_index) + " Success")
                fps = cap.get(cv2.CAP_PROP_FPS)
                # print("camera {}".format(camera_index) + ": " + str(int(fps)))
                ret, img = cap.read()
                try:
                    if ret == True:
                        # img = cv2.flip(img, -1)
                        # AA=0
                        # if(camera_index != str(0)):
                        #     img = cv2.flip(img, 0)
                        # cv2.waitKey(2)
                        # lock.acquire()
                        q.append(img)

                        if len(q) >= 100:
                            del q[:]
                            gc.collect()
                            print("gc", camera_index)
                    else:
                        cap.release()
                        cv2.destroyWindow("camera {}".format(camera_index))

                    if len(q) == 0:
                        print("NO IMAGE", camera_index)
                        pass
                    else:
                        if(timelog == datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')):
                            count += 1
                        else:
                            print('Video_{} '.format((camera_index)) +str(count))
                            count = 0
                        timelog = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
                        img = q.pop()

                        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_AREA)
                        outVideo.write(img)
                        cv2.imshow("camera {}".format(camera_index), img)
                        time.sleep(int(Config.Delaytime))
                        cv2.waitKey(1)
                        # print(datetime.datetime.today().strftime('%m-%d-%H.%M.%S'))
                        # lock.release()
                        if not os.path.exists(path1 + 'Video_{}//'.format(camera_index) + datetime.datetime.today().strftime(
                                '%Y-%m-%d') + '//'):
                            os.makedirs(path1 + 'Video_{}//'.format(camera_index) + datetime.datetime.today().strftime(
                                '%Y-%m-%d') + '//')
                        if os.path.exists(path1 + 'Video_{}//'.format(camera_index) + datetime.datetime.today().strftime(
                                '%Y-%m-%d') + '//' + datetime.datetime.today().strftime(
                                '%m-%d.%H') + '.avi'.format(camera_index)):
                            pass
                        else:
                            # filename1 = datetime.datetime.today().strftime('%Y.%m.%d.%H') + ".avi"
                            # print(filename1)
                            outVideo = cv2.VideoWriter((path1 + 'Video_{}//'.format(
                                camera_index) + datetime.datetime.today().strftime(
                                '%Y-%m-%d') + '//' + datetime.datetime.today().strftime('%m-%d.%H') + '.avi'.format(
                                camera_index)), cv2.VideoWriter_fourcc('h', '2', '6', '4'), 30, (640, 480))
                        if os.path.exists(path1 + 'Video_{}//'.format(camera_index) + (datetime.datetime.today() - datetime.timedelta(days=(int(Config.Cameranumber)))).strftime(
                            '%Y-%m-%d') + '//' + (datetime.datetime.today() - datetime.timedelta(days=(int(Config.Cameranumber)))).strftime(
                            '%m-%d.%H') + '.avi'.format(camera_index)):
                            os.remove(path1 + 'Video_{}//'.format(camera_index) + (datetime.datetime.today() - datetime.timedelta(days=(int(Config.Cameranumber)))).strftime(
                            '%Y-%m-%d') + '//' + (datetime.datetime.today() - datetime.timedelta(days=(int(Config.Cameranumber)))).strftime(
                                '%m-%d.%H') + '.avi'.format(camera_index))
                        if os.path.exists(path1 + 'Video_{}//'.format(camera_index) + (datetime.datetime.today() - datetime.timedelta(days=(int(Config.Cameranumber)))).strftime(
                            '%Y-%m-%d')):
                            if not os.listdir(path1 + 'Video_{}//'.format(camera_index) + (datetime.datetime.today() - datetime.timedelta(days=(int(Config.Cameranumber)))).strftime(
                            '%Y-%m-%d')):
                                os.rmdir(path1 + 'Video_{}//'.format(camera_index) + (datetime.datetime.today() - datetime.timedelta(days=(int(Config.Cameranumber)))).strftime(
                            '%Y-%m-%d'))
                except Exception as e:
                    log.error("camera {}".format(camera_index) + ": " + str(e))
            else:
                a = a + 1
                # print("camera {} ".format(camera_index) + str(a))
                if(a > int(3000000)):
                    log.info("camera {}".format(camera_index) + " close")
                    break
        except Exception as e:
            log.error("camera {}".format(camera_index) + ": " + str(e))
            # cap.release()
            # cv2.destoryWindow("camera {}".format(camera_index))
            # print("close " + "camera {}".format(camera_index))


def multithread_run(camera_index, path):
    try:
        initial_log(path)
        if not os.path.exists(path + 'Video_{}//'.format(camera_index)):
            os.makedirs(path + 'Video_{}//'.format(camera_index))
        files = walk(path+'Video_{}//'.format(camera_index))
        for i1 in files:
            if not shouldkeep(i1):
                # print(i1)
                print(str(datetime.datetime.fromtimestamp(os.path.getmtime(i1))) + ' Video_{}'.format(camera_index))
                os.remove(i1)

        walk1(path+'Video_{}//'.format(camera_index))

        cap = cv2.VideoCapture(int(camera_index))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(fps)
        cap.set(5, 30)
        fourcc = cv2.VideoWriter_fourcc('h', '2', '6', '4')  # 'X', 'V', 'I', 'D', 'M', 'P', '4', '2'
        print(path)

        filename1 = datetime.datetime.today().strftime('%m-%d.%H')
        outVideo = cv2.VideoWriter(path+'Video_{}//'.format(camera_index) + datetime.datetime.today().strftime('%Y-%m-%d') + '//' +
                    filename1 +'.avi'.format(camera_index), fourcc, 30, (640, 480))
        q = deque(maxlen=10)
        print("index", camera_index)



        # lock = threading.Lock()
        p1 = Thread(target=producer, args=(cap, q, camera_index, outVideo, path))
        # c1 = Thread(target=consumer, args=(camera_index, outVideo, q, Config.path1))

        p1.start()
        # c1.start()

        p1.join()
    except Exception as e:
        log.error("camera {}".format(camera_index) + ": " + str(e))
    # c1.join()

def walk(dir):
  ret = []
  dir = os.path.abspath(dir)
  for file in [file for file in os.listdir(dir) if not file in [".",".."]]:
    nfile = os.path.join(dir,file)
    if os.path.isdir(nfile):
      ret.extend(walk(nfile))
    else:
      ret.append(nfile)
  return ret

def walk1(dir1):
    dir1 = os.path.abspath(dir1)
    for file1 in os.listdir(dir1):
        nfile1 = os.path.join(dir1, file1)
        if os.path.isdir(nfile1):
            if not os.listdir(nfile1):
                os.rmdir(nfile1)

def shouldkeep(file):
  if '.py' in file:
    return True
  elif '.conf' in file:
    return True
  elif 'current' in file:
    return True
  elif 'rtb' in file and datetime.datetime.fromtimestamp(os.path.getmtime(file)) > datetime.datetime.now() - datetime.timedelta(3):
    return True
  elif datetime.datetime.fromtimestamp( os.path.getmtime(file)) < \
     datetime.datetime.now() - datetime.timedelta(7)\
     and ('webdebug' in file\
     or 'potperr' in file\
     or 'webaccess' in file\
     or 'controller_slow' in file\
     or 'game.' in file\
     or 'checkin_social' in file\
     ):
    return False
  elif datetime.datetime.fromtimestamp( os.path.getmtime(file)) < \
     datetime.datetime.now() - datetime.timedelta(2)\
     and ('queue.master.info' in file):
    return False
  elif datetime.datetime.fromtimestamp( os.path.getmtime(file)) > \
     datetime.datetime.now() - datetime.timedelta((int(Config.Day)-1)):
    return True
  else:
    return False

def initial_log(pathlog):
    global log
    log = logging.getLogger("Log")
    log.setLevel(logging.DEBUG)
    if not os.path.exists(pathlog + "Log//"):
        os.makedirs(pathlog + "Log//")
        fileg = logging.FileHandler(pathlog + "Log//" + datetime.datetime.today().strftime('%Y-%m-%d.%H') + "-Log記錄")
    else:
        fileg = logging.FileHandler(pathlog + "Log//" + datetime.datetime.today().strftime('%Y-%m-%d.%H') + "-Log記錄")
    fileg.setLevel(logging.DEBUG)
    log_handler = logging.StreamHandler()
    log_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
    fileg.setFormatter(formatter)
    log_handler.setFormatter(formatter)
    log.addHandler(fileg)
    log.addHandler(log_handler)
    #log.info("Success")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    processes = []
    print("Cameranumber", Config.Cameranumber)
    nloops = range(int(Config.Cameranumber))
    print("Day", Config.Day)
    print("Delaytime", Config.Delaytime)
    for i in nloops:
        # print(i)
        if i != 0:
            i = i*2
        print(i)
        t = Process(target=multithread_run, args=(str(int(i)), Config.path1))
        print(i, t)
        processes.append(t)

    for i in nloops:
        processes[i].start()

    for i in nloops:
        processes[i].join()
