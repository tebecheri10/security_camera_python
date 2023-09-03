import cv2

camera = cv2.VideoCapture(0)

while camera.isOpened():
    ret, frame = camera.read()
    ret, new_frame = camera.read()
    
    difference = cv2.absdiff(frame, new_frame)  
    
    gray = cv2.cvtColor(difference, cv2.COLOR_RGB2GRAY)    
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
    
    dilate = cv2.dilate(thresh, None, iterations=3)
    contour, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        
    for c in contour:
        if cv2.contourArea(c) < 5000:
            continue
        
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Status: {}'.format('Movement Detected'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 
        
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cv2.imshow('Personal Security Camera', frame)