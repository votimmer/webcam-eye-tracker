import cv2 as cv
import numpy as np
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = [362, 382, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]
NOSE_TIP = 4

class IrisDetector:

    """
    The IrisDetector class detects and follows a person's eye and iris positions by employing Mediapipe.  
    """

    def __init__(self):
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1, 
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def processImage(self, image):
        """Processes the webcam feed so it can be used by mediapipe"""
        image = cv.flip(image, 1)
        rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_image)
        return image, results
 
    def detectIris(self, image):
        """Detects the irises of the person recorded by the webcam."""
        image, results = self.processImage(image)
        img_h, img_w = image.shape[:2]
        l_cx, l_cy, r_cx, r_cy = None, None, None, None

        if results.multi_face_landmarks:
            mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark]) 
            (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS]) #l_cx en l_cy are the coordinates of the center of the left iris
            (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right= np.array([r_cx, r_cy], dtype=np.int32)

            #Draw circles around each iris
            cv.circle(image, center_left, int(l_radius), (255, 0, 255), 1, cv.LINE_AA)
            cv.circle(image, center_right, int(r_radius), (255, 0, 255), 1, cv.LINE_AA)

            #Draw cross at the center of each iris
            cv.drawMarker(image, tuple(center_left), (0, 0, 255), cv.MARKER_CROSS, 5, thickness=1)
            cv.drawMarker(image, tuple(center_right), (0, 0, 255), cv.MARKER_CROSS, 5, thickness=1)

            #Draw line from one iris center to the other
            #cv.line(image, tuple(center_left), tuple(center_right), (0, 0, 255), 1)
        
        return image, l_cx, l_cy, r_cx, r_cy

if __name__ == '__main__':
    detector = IrisDetector()
    cap = cv.VideoCapture(0)

    while True:
        ret, image = cap.read()
        if not ret:
            break
        
        image, l_cx, l_cy, r_cx, r_cy = detector.detectIris(image)
        cv.imshow('img', image)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()
