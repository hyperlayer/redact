import cv2
from PIL import Image, ImageFilter
import numpy
from hyperlayer.classes import Mob, MobManager
from util.image import isHumanColor

def blurVideo(writer, events, video, blurType='motion'):
    """
    Writes video where faces are blurred.
    
    video -- source video to blur
    events -- list of blurring events
    """
    #setupWindows()
    print 'rendering video...'
    #very basic implementation
    
    #first restart video
    video.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO, 0)
    for eventNumber, event in enumerate(events):
        #read source video frames
        ret, frame = video.read()
        #draw on each frame
        if event['type'] == 'spawn' or event['type'] == 'move':
            faces = event['faces']
            if frame is None:
                return
            frameImage = Image.fromarray(numpy.uint8(frame))
            blurredImage = None
            blurredFrame = None
            if len(faces) > 0:
                for eachFace in faces:

                    eachFaceRect = eachFace
                    ic = frameImage.crop((eachFaceRect[0], eachFaceRect[1], eachFaceRect[0]+eachFaceRect[2], eachFaceRect[1]+eachFaceRect[3]))
                    for i in range(20):  # with the BLUR filter, you can blur a few times to get the effect you're seeking
                        ic = ic.filter(ImageFilter.BLUR)
                    frameImage.paste(ic, (eachFaceRect[0], eachFaceRect[1]))
                    blurredImage = frameImage
                    #blurredImage = frameImage
                    blurredFrame = numpy.array(blurredImage)
                #cv2.rectangle(frame, (eachFaceRect[0], eachFaceRect[1]), (eachFaceRect[0] + eachFaceRect[2], eachFaceRect[1]+eachFaceRect[3]), (255,100,100), thickness = 1, lineType=8, shift=0)

            #eachFaceRect = event['faces']
            #cv2.rectangle(frame, (eachFaceRect[0], eachFaceRect[1]), (eachFaceRect[0] + eachFaceRect[2], eachFaceRect[1]+eachFaceRect[3]), (255,100,100), thickness = 1, lineType=8, shift=0)
        #drawVisualization(source_frame, frame)
        
        #write frame
        print 'writing frame %s' % eventNumber
        writer.write(blurredFrame)

def boxVideo(writer, events, video):
    """
    Writes video where faces have boxes drawn around them.
    
    video -- source video to draw boxes around
    events -- list of blurring events
    """
    #setupWindows()
    print 'rendering video...'
    #very basic implementation
    
    #first restart video
    video.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO, 0)
    for event in events:
        #read source video frames
        ret, frame = video.read()
        #draw on each frame
        if event['type'] == 'spawn' or event['type'] == 'move':
            faces = event['faces']
            frameImage = Image.fromarray(numpy.uint8(frame))
            blurredImage = None
            blurredFrame = None
            if len(faces) > 0:
                for eachFace in faces:
                    eachFaceRect = eachFace
                    croppedImage = frameImage.crop((eachFaceRect[0], eachFaceRect[1], eachFaceRect[0]+eachFaceRect[2], eachFaceRect[1]+eachFaceRect[3]))
                    if isHumanColor(croppedImage):
                        cv2.rectangle(frame, (eachFaceRect[0], eachFaceRect[1]), (eachFaceRect[0] + eachFaceRect[2], eachFaceRect[1]+eachFaceRect[3]), (255,100,100), thickness = 1, lineType=8, shift=0)

        #write frame
        writer.write(frame)

    writer.release()

def boxVideoMob(writer, events, video):
    print 'boxing video with mobs...'
    video.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO, 0)
    #create mob manager
    capone = MobManager()
    for event in events:
        print 'rendering mobs...'
        ret, frame = video.read()
        capone.tick(event)
        renderedFrame = capone.render(frame)
        writer.write(frame)

def setupWindows():
    cv2.namedWindow('Source', flags=cv2.WINDOW_NORMAL)
    cv2.namedWindow('Render', flags=cv2.WINDOW_NORMAL)

def drawVisualization(source_frame, drawn_frame):
    if cv2.waitKey(25) == 27:
        exit()
    cv2.imshow('Source', source_frame)
    cv2.imshow('Render', drawn_frame)
