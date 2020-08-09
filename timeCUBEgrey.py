#GREY VERSION WITHOUT ROTATE
import numpy as np
import cv2
#using frontCamera: source = 1
#using file:        source = 'path.avi'
source = 0    # backCamera
camerastream = cv2.VideoCapture(source)
#Define the codec and create VideoWriter object note: isColor is False for Gray
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out2stream = cv2.VideoWriter('out2.avi',fourcc, 20.0, (640,480), isColor = False)
#build cube with (y,x,t)*8Bit
cube = np.zeros((480,640,640),dtype = np.uint8)

play_x_foreward = True
rec_t = 0
play_x = 0
while True:
    #take each frame from camerastream
    _, orginalframe = camerastream.read() # "_," häh ??? aber notwendig
    #convert from BGR to GRAY
    grayframe = cv2.cvtColor(orginalframe, cv2.COLOR_BGR2GRAY)
    #load videoframe to 2D+TimeCube
    cube[:,:,rec_t] = grayframe
    #build outputframe use magic rolling view(y,t,x) is faster then cube = np.roll(cube,1,axis=2)
    outputframe = np.concatenate([cube[:,play_x,rec_t:], cube[:,play_x,:rec_t]], axis=1)
    
    #calc next rec_t and play_x
    rec_t += 1
    if rec_t >= cube.shape[2]:
        play_x_foreward = False
        rec_t = 0
        
    if play_x_foreward == True:
        play_x += 1
    else: 
        play_x -= 1
        
    if play_x <= 0:
        play_x_foreward = True
        play_x = 0
    
    #show images in 2 windows (gray, output)
    cv2.imshow('gray', grayframe)
    cv2.imshow('output', outputframe)
    
    #write stream to .avi -file
    out2stream.write(outputframe)
    
    #pause 1ms (wait for space-key (0 = endless, 1 = 1ms, 0xFF need only for 64Bit CPU)) 
    if cv2.waitKey(1) & 0xFF == ord(' '):
        #for debug only
        print("orginalframe.shape  .dtype:",  orginalframe.shape,"   ",orginalframe.dtype)
        print("        cube.shape  .dtype:",                    cube.shape," ",cube.dtype)
        print(" outputframe.shape  .dtype:", outputframe.shape,"      ",outputframe.dtype)
        break

# release everything if job is finished
camerastream.release()
out2stream.release()
cv2.destroyAllWindows()