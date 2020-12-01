import cv2
import datetime
import Config
import logging
import os
import gc
from collections import deque
# 刪除超過7天log
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

 #刪除空目錄
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
  elif 'rtb' in file and datetime.datetime.fromtimestamp( os.path.getmtime(file) ) > datetime.datetime.now() - datetime.timedelta(3):
    return True
  elif datetime.datetime.fromtimestamp( os.path.getmtime(file) ) < \
     datetime.datetime.now() - datetime.timedelta(7)\
     and ('webdebug' in file \
     or 'potperr' in file\
     or 'webaccess' in file\
     or 'controller_slow' in file\
     or 'game.' in file\
     or 'checkin_social' in file\
     ):
    return False
  elif datetime.datetime.fromtimestamp( os.path.getmtime(file) ) < \
     datetime.datetime.now() - datetime.timedelta(2)\
     and ('queue.master.info' in file):
    return False
  elif datetime.datetime.fromtimestamp( os.path.getmtime(file) ) > \
     datetime.datetime.now() - datetime.timedelta((int(Config.Cameranumber)-1)):
    return True
  else:
    return False
def initial_log(path):
    global log
    # Log紀錄
    log = logging.getLogger("Log")
    log.setLevel(logging.DEBUG)
    # 判斷檔案路徑
    if not os.path.exists(path + "Log//"):
        os.makedirs(path + "Log//")
        fileg = logging.FileHandler(
            path + "Log//" + datetime.datetime.today().strftime('%Y-%m-%d.%H') + "-Log紀錄")
    else:
        fileg = logging.FileHandler(
            path + "Log//" + datetime.datetime.today().strftime('%Y-%m-%d.%H') + "-Log紀錄")
    fileg.setLevel(logging.DEBUG)
    # Log Handler輸出控制台
    log_handler = logging.StreamHandler()
    log_handler.setLevel(logging.DEBUG)
    # 定義Handler輸出格式
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
    fileg.setFormatter(formatter)
    log_handler.setFormatter(formatter)
    log.addHandler(fileg)
    log.addHandler(log_handler)
try:
    camera_index = 2
    initial_log(Config.path1)
    if not os.path.exists(Config.path1 + 'Video_{}//'.format(camera_index)):
        os.makedirs(Config.path1 + 'Video_{}//'.format(camera_index))
    files = walk(Config.path1+'Video_{}//'.format(camera_index))
    for i1 in files:
        if not shouldkeep(i1):
            # print(i1)
            print(str(datetime.datetime.fromtimestamp(os.path.getmtime(i1))) + ' Video_{}//'.format(camera_index))
            os.remove(i1)
    walk1(Config.path1 + 'Video_{}//'.format(camera_index))
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc('h', '2', '6', '4')
    filename1 = datetime.datetime.today().strftime('%m-%d.%H')
    outVideo = cv2.VideoWriter(Config.path1+'Video_{}//'.format(camera_index) + datetime.datetime.today().strftime('%Y-%m.%d') + '//' +
                    filename1 +'.avi'.format(camera_index), fourcc, 30, (640, 480))
    index = 0
    timelog = 0
    count = 0
    a = 0
    q = deque(maxlen=10)
    path1 = Config.path1
    while True:
        try:
            if cap.isOpened():
                a = 0
                if index == 0:
                    index = index + 1

                ret, img = cap.read()
                try:
                    if ret == True:
                        # img = cv2.flip(img,1)  # linux不符合
                        # if(camera_index != str(0)):  # linux不符合
                        # img = cv2.flip(img,1)  # linux不符合
                        q.append(img)
                        if len(q) >= 100:
                            del q[:]
                            gc.collect()
                            print("gc", camera_index)
                    else:
                        cap.release()
                        cv2.destroyWindow("camera {}".format(camera_index))

                    if len(q) == 0:
                        # print("影像不顯示", camera_index)
                        pass
                    else:
                        if (timelog == datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')):
                            count += 1
                        else:
                            print('Video_{} '.format(camera_index) + str(count))
                            count = 0
                            count += 1
                        timelog = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
                        img = q.pop()

                        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_AREA)  # INTER_LINEAR
                        outVideo.write(img)
                        cv2.imshow("camera {}".format(camera_index), img)
                        cv2.waitKey(1)

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
                        # 刪除舊Log
                        if os.path.exists(path1 + 'Video_{}//'.format(camera_index) + (datetime.datetime.today() - datetime.timedelta(days=int(Config.Day))).strftime(
                            '%Y-%m-%d') + '//' + (datetime.datetime.today() - datetime.timedelta(days=int(Config.Day))).strftime(
                            '%m-%d.%H') + '.avi'.format(camera_index)):
                            os.remove(path1 + 'Video_{}//'.format(camera_index) + ( datetime.datetime.today() - datetime.timedelta(days=int(Config.Day))).strftime(
                            '%Y-%m-%d') + '//' + (datetime.datetime.today() - datetime.timedelta(days=int(Config.Day))).strftime(
                                '%m-%d.%H') + '.avi'.format(camera_index))
                        # 刪除空資料夾
                        if os.path.exists(path1 + 'Video_{}//'.format(camera_index) + (datetime.datetime.today() - datetime.timedelta(days=int(Config.Day))).strftime(
                            '%Y-%m-%d')):
                            if not os.listdir(path1 + 'Video_{}//'.format(camera_index) + (datetime.datetime.today() - datetime.timedelta(days=int(Config.Day))).strftime(
                            '%Y-%m-%d')):
                                os.rmdir(path1 + 'Video_{}//'.format(camera_index) + (datetime.datetime.today() - datetime.timedelta(days=int(Config.Day))).strftime(
                            '%Y-%m-%d'))
                except Exception as e:
                    log.error('Video_{}'.format(camera_index) + str(e))
            else:
                a = a + 1
                if (a > int(25000)):
                    log.info('Video_{}'.format(camera_index) + " close")
                    cap.release()
                    break
        except Exception as e:
            log.error('Video_{}'.format(camera_index) + str(e))
except Exception as e:
    log.error('Video_{}'.format(camera_index) + str(e))