import cv2
import numpy as np

teamOne = 0
teamTwo = 0

fields = [[0,350,450,200], [500,350,500,200]]
DELAY = 50

TINY = False

fileCfg = "yolov3{}.cfg".format("-tiny" if TINY else "")
fileWheights = "yolov3{}.weights".format("-tiny" if TINY else "")
fileClass = "coco{}.names".format("-tiny" if TINY else "")

with open(fileClass, "r") as file:
    CLASS = [row.strip() for row in file.readlines()]

# Gerar cores diferentes para cada classe
COLORS = np.random.uniform(0, 255, size=(len(CLASS), 3))

def processImage(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    imgThreshold = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16 );
    imgBlur = cv2.medianBlur(imgThreshold, 5);
    kernel = np.ones((3, 3), np.int8);
    imgDilated = cv2.dilate(imgBlur, kernel);
    return [imgDilated, imgGray]


def verifyFields(img, imgDilated, fields):
    scoreboardFields = [0, 0]

    for  index, listPosition in enumerate(fields):
        isRelease = False
        x, y, w, h = listPosition
        cutout = imgDilated[y:y+h, x:x+w];
        countPxWhite = cv2.countNonZero(cutout);

        cv2.rectangle(img, (x, y+h-22), (x+50, y+h-5), (0, 0, 0), -1)
        cv2.putText(img, str(countPxWhite), (x, y+h-10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        if countPxWhite > 9000 and isRelease == True:
            scoreboardFields[index] = scoreboardFields[index] + 1

        if countPxWhite < 9000:
            isRelease = True
        else:
            isRelease =False

        if isRelease == False:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
        else:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255, 0, 255),4)

    return scoreboardFields


def showScoreboard(img, scoreBoardFields):
    cv2.rectangle(img, (90, 0), (415, 60), (0, 0, 0), -1)
    cv2.putText(img, 'Placar: {}/{}'.format(scoreBoardFields[0], scoreBoardFields[1]), (100, 45), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 5)

def loadPretainedModel():
    model = cv2.dnn.readNetFromDarknet(fileCfg, fileWheights)
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    if model.empty():
        raise IOError("Não foi possivel carregar o modelo!")

    return model 

def preProcessFrame(img):
    blob = cv2.dnn.blobFromImage(img, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
    return blob

def detectObject(img, model):
    blob = preProcessFrame(img)
    model.setInput(blob)
    layersNames = model.getLayerNames()
    layersOutput = [layersNames[i - 1] for i in model.getUnconnectedOutLayers()]
    outputs = model.forward(layersOutput)
    return outputs


def drawDetections(img, detections, limiar=0.5):
    (height, width) = img.shape[:2]
    boxs = []
    trusts = []
    idsClass = []

    for output in detections:
        for detection in output:
            points = detection[5:]
            idClass = np.argmax(points)
            trust = points[idClass]
            if trust > limiar:
                box = detection[0:4] * np.array([width, height, width, height])
                (centerX, centerY, widthBox, heightBox) = box.astype("int")
                x = int(centerX - (widthBox / 2))
                y = int(centerY - (heightBox / 2))

                boxs.append([x, y, int(widthBox), int(heightBox)])
                trusts.append(float(trust))
                idsClass.append(idClass)

    indices = cv2.dnn.NMSBoxes(boxs, trusts, limiar, limiar - 0.1)
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y) = (boxs[i][0], boxs[i][1])
            (widthBox, heightBox) = (boxs[i][2], boxs[i][3])
            color = [int(c) for c in COLORS[idsClass[i]]]
            cv2.rectangle(img, (x, y), (x + widthBox, y + heightBox), color, 2)
            text = f"{CLASS[idsClass[i]]}: {trusts[i]:.2f}"
            cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
def main():
    video_path = "volei1.mp4";
    video = cv2.VideoCapture(video_path);
    model = loadPretainedModel()

    if not video.isOpened():
        print(f"Erro ao abrir o video: {video_path}")
        return
    

    limiarTrust = 0.5

    def ajustLimiar(value):
        nonlocal limiarTrust
        limiarTrust = value / 100


    if TINY:
        cv2.createTrackbar('Limiar de Confiança', 'Detecta Objetos', int(limiarTrust * 100), 100, ajustLimiar)

    while True:
        check, img = video.read();

        if not check:
            break
        
        imgDilated = processImage(img);

        detections = detectObject(img, model)
        drawDetections(img, detections, limiarTrust)

        scoreBoardFields = verifyFields(img, imgDilated[0], fields)

        showScoreboard(img, scoreBoardFields)

        cv2.imshow('Video', img)
        
        cv2.namedWindow('Processamento', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Processamento', 350, 200)
        cv2.imshow('Processamento', imgDilated[0])
      
        if cv2.waitKey(DELAY) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()




main()