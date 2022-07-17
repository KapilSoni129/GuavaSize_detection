import cv2
import mail_demo
import numpy as np

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

classlabels = [] # empty list of python
file_name = 'Labels.txt'
with open(file_name, 'rt') as fpt:
    classlabels = fpt.read().rstrip('\n').split('\n')

config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'frozen_inference_graph.pb'

model = cv2.dnn_DetectionModel(frozen_model, config_file)

model.setInputSize(320, 320)
model.setInputScale(1.0/127.5) ## 255/2 = 127.5
model.setInputMean((127.5, 127.5, 127.5)) ## mobilenet => [-1, 1]
model.setInputSwapRB(True)

# img = cv2.imread('jeff-david-king-ehWdBropexc-unsplash.jpg')
# img = image_resize(img, height=800)

video_file = "pexels-charles-parker-5825806.mp4"

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

font_scale = 3
font = cv2.FONT_HERSHEY_PLAIN

mail_sent = 0
count = 0
lst=[]

while True:
    # images = requests.get("http://192.168.1.22:8080/shot.jpg")
    # video = np.array(bytearray(images.content), dtype = np.uint8)
    # frame = cv2.imdecode(video, -1)

    ret, frame = cap.read()
    # frame = image_resize(frame, height=1024)

    ClassIndex, confidece, bbox = model.detect(frame, confThreshold=0.52)
    
    print(ClassIndex)

    if(len(ClassIndex)!=0):
        for ClassInd, conf, boxes in zip(ClassIndex, confidece, bbox):
            ci = ClassInd[0]
            if(ClassInd<=80):
                cv2.rectangle(frame, boxes, (255,0,0), 2)
                cv2.putText(frame, classlabels[ci-1], (boxes[0]+10, boxes[1]+40), font, fontScale = font_scale, color = (0,255,0), thickness = 3)
                if ClassInd==53:
                    lst.append(boxes)

    flatlist = []
    for sublist in ClassIndex:
        for element in sublist:
            flatlist.append(element)

    if 53 in flatlist:
        if mail_sent == 0:
            count+=1
            cv2.imwrite("images/frame%d.jpg" % count, frame)
            mail_demo.send_mail("images/frame%d.jpg" % count, lst)
            mail_sent = 1
            with open(r'file.txt', 'w') as fp:
                for item in lst:
                    fp.write("%s" % item)
    else:
        mail_sent = 0

    cv2.imshow("Output", frame)
    cv2.waitKey(1)



