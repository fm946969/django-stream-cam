import cv2

cap:cv2.VideoCapture = cv2.VideoCapture(1)
print(f'{type(cap) = } : {cap}')
run = True
while run:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        run = False

cap.release()
cv2.destroyAllWindows()