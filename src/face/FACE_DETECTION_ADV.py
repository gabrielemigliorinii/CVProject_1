import cv2
import mediapipe as mp
import time

class FaceDetector:

    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, draw=True):
        try:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.faceDetection.process(imgRGB)
        except:
            print(['END_VIDEO'])
            exit(0)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = [int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)]
                if draw:
                    img = self.drawLines(img,bbox)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,2, (255, 255, 0), 2)
                    bbox = [[int(bboxC.xmin * iw)], [int(bboxC.ymin * ih)], [int(bboxC.width * iw)], [int(bboxC.height * ih)]]
                    bboxs.append([["FACE_ID", id], bbox, ["DETECTION_SCORE", detection.score[0]]])

            return img, bboxs
        else:
            bboxs.append("DETECTION_ERROR")
            return img, bboxs

    def drawLines(self, img, bbox, l=30, t=5, rt= 1):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h
        cv2.rectangle(img, bbox, (255, 255, 0), rt)
        # Top Left  x,y
        cv2.line(img, (x, y), (x + l, y), (255, 255, 0), t)
        cv2.line(img, (x, y), (x, y+l), (255, 255, 0), t)
        # Top Right  x1,y
        cv2.line(img, (x1, y), (x1 - l, y), (255, 255, 0), t)
        cv2.line(img, (x1, y), (x1, y+l), (255, 255, 0), t)
        cv2.line(img, (x, y1), (x + l, y1), (255, 255, 0), t)
        cv2.line(img, (x, y1), (x, y1 - l), (255, 255, 0), t)
        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 255, 0), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 255, 0), t)
        return img

def printDetectionArray(array):
    print(array)

def rescaleFrame(frame, percent=50):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def main():
    cap = cv2.VideoCapture("../../vid/face_det_1.mp4")
    pTime = 0
    detector = FaceDetector()
    while True:
        success, img = cap.read()
        img, bboxs = detector.findFaces(img)
        printDetectionArray(bboxs)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 2)
        cv2.imshow("FRAME", rescaleFrame(img))
        cv2.waitKey(1)

if __name__ == "__main__":
    try:
        main()
    except:
        print(['EXIT'])
        exit(-1)
