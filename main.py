import cv2
import numpy as np

teamOne = 0
teamTwo = 0

fields = [[0,350,450,200], [500,350,500,200]]
DELAY = 50


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
    
def main():
    video_path = "volei1.mp4";
    video = cv2.VideoCapture(video_path);

    if not video.isOpened():
        print(f"Erro ao abrir o video: {video_path}")
        return

    while True:
        check, img = video.read();

        if not check:
            break
        
        imgDilated = processImage(img);

        scoreBoardFields = verifyFields(img, imgDilated[0], fields)

        showScoreboard(img, scoreBoardFields)

        cv2.imshow('Video', img)
        
        cv2.namedWindow('Processamento', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Processamento', 350, 200)
        cv2.imshow('Processamento', imgDilated[0])
        
        cv2.namedWindow('Passo', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Passo', 350, 200)
        cv2.imshow('Passo', imgDilated[1])

        if cv2.waitKey(DELAY) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()




main()