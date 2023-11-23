import cv2
import mediapipe as mp
from pygame import mixer
import time

# For sound alert
mixer.init()
mixer.music.load('beep.wav') # beep sound

# For face mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
IMAGE_FILES = []
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
font = cv2.FONT_ITALIC

# For detecting sleep
is_sleep = False
t = time.time() # time when the driver is detected to be sleepy

def alert():
  if not mixer.music.get_busy():
    mixer.music.play()

def landmarkToPoint(landmark): # landmark to point
  pre_process = str(landmark).split("\n")
  x = float(pre_process[0].split(" ")[1])
  y = float(pre_process[1].split(" ")[1])
  z = float(pre_process[2].split(" ")[1])
  return (x, y, z)

def detectSleep(left_upper, left_lower, right_upper, right_lower, threshold = 0.1):
  """
  Get the distance between the upper and lower eyelids, and compare them with the threshold.
  Threshold can be adjusted according to the user's face.
  Return True if the driver is sleeping
  """
  left_upper_point = landmarkToPoint(left_upper)
  left_lower_point = landmarkToPoint(left_lower)
  right_upper_point = landmarkToPoint(right_upper)
  right_lower_point = landmarkToPoint(right_lower)
  left = left_lower_point[1] - left_upper_point[1]
  right = right_lower_point[1] - right_upper_point[1] 
  if(left <= threshold and right <= threshold): 
    return True
  return False
  
with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5) as face_mesh:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
      continue
    annotated_image = image.copy()
    for face_landmarks in results.multi_face_landmarks:
      print('face_landmarks:', face_landmarks)
      mp_drawing.draw_landmarks(image=annotated_image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_TESSELATION, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
      mp_drawing.draw_landmarks(image=annotated_image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_CONTOURS, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
      mp_drawing.draw_landmarks(image=annotated_image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_IRISES, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(1)

with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    current_t = time.time()
    if is_sleep == False: # 
      t = time.time()
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks == None: # if face is not detected
      is_sleep = True
      if current_t - t >= 2: 
        cv2.putText(image, "!! Please drive carefully !!", (120, 40), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        alert()
    elif results.multi_face_landmarks:
      landmarks = results.multi_face_landmarks[-1].landmark
      is_sleep = detectSleep(landmarks[159], landmarks[145], landmarks[386], landmarks[374])
      if current_t - t >= 1.5: 
        cv2.putText(image, "!! You are sleepy, please wake up !!", (35, 40), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        alert()
      for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_TESSELATION, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_CONTOURS, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_IRISES, landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())
    cv2.namedWindow('Driving Caution (TPOS)', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Driving Caution (TPOS)',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Driving Caution (TPOS)', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()