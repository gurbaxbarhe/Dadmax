import cv2
import numpy as np

# Load the pre-trained Haar Cascade face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the webcam (assuming CAM 313 is at index 1)
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Using cv2.CAP_DSHOW based on common compatibility requirements

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the captured frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the resulting frame with detected faces
    cv2.imshow('Face detection', frame)

    # If 'q' is pressed, break from the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Example stepper height adjustment logic based on the first detected face's size
    if len(faces) > 0:
        face_height = faces[0][3]  # Height of the first detected face
        print(f"Adjusting stepper height based on face size: {face_height} pixels")

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
