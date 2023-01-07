import cv2     # for capturing videos
import numpy as np    # for mathematical operations
import glob
import skvideo.io 
import os
from PIL import Image
import moviepy.editor

# Image Extraction ---------------------------------------------------------------------------------------------------------------

count = 0
filename = str(input("Enter file name: "))
videoFile = './../Testcases/' + filename
cap = cv2.VideoCapture(videoFile)   # capturing the video from the given path
frameRate = cap.get(5) #frame rate

while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if count<10:
        filename ="./../Org_Frames/frame0%d.jpg" % count;count+=1
    else:
        filename ="./../Org_Frames/frame%d.jpg" % count;count+=1
    cv2.imwrite(filename, frame)
     
cap.release()

# Taking crop dimensions -----------------------------------------------------------------------------------------------------------

img = cv2.imread('./../Org_Frames/frame00.jpg', cv2.IMREAD_UNCHANGED)
 

height = img.shape[0]
width = img.shape[1]
channels = img.shape[2]
 
print('Frame Height       : ',height)
print('Frame Width        : ',width)

top = int(input("Enter cropping pixels from top: "))
bottom = int(input("Enter cropping pixels from bottom: "))
left = int(input("Enter cropping pixels from left: "))
right = int(input("Enter cropping pixels from right: "))

# Cropping frames -------------------------------------------------------------------------------------------------------------------

for i in range(count):
    if i<10:
        buffer = cv2.imread('./../Org_Frames/frame0' + str(i) + '.jpg', cv2.IMREAD_UNCHANGED)
        cropped_image = buffer[top:bottom, left:right]
        cv2.imwrite('./../Cur_Frames/frame0'+ str(i) + '_c.jpg', cropped_image)
    else:
        buffer = cv2.imread('./../Org_Frames/frame' + str(i) + '.jpg', cv2.IMREAD_UNCHANGED)
        cropped_image = buffer[top:bottom, left:right]
        cv2.imwrite('./../Cur_Frames/frame'+ str(i) + '_c.jpg', cropped_image)
        
# Saving video with new frames ------------------------------------------------------------------------------------------------------ 

base_path = "./../Cur_Frames/"
list_of_files = sorted( filter( os.path.isfile,    glob.glob(base_path + '*') ) )

video_save_path = "./../Output/output.mp4"
fps = frameRate

# create writer using FFmpegWriter
writer = skvideo.io.FFmpegWriter(video_save_path, inputdict={'-r': str(fps)}, outputdict={'-r': str(fps), '-c:v': 'libx264', '-preset': 'ultrafast', '-pix_fmt': 'yuv444p'})

# iterate over each image using os module
for img in list_of_files:
    image = Image.open(os.path.join(base_path, img)) # read image
    image = np.array(image, dtype=np.uint8) #convert to unit8 numpy array
    writer.writeFrame(image)

# close writer
writer.close()

# Deleting all frames ----------------------------------------------------------------------------------------------------------------

path1 = r"./../Org_Frames/"
for file_name in os.listdir(path1):
    file = path1 + file_name
    if os.path.isfile(file):
        os.remove(file)

path2 = r"./../Cur_Frames/"
for file_name in os.listdir(path2):
    file = path2 + file_name
    if os.path.isfile(file):
        os.remove(file)
        
# Adding sound -----------------------------------------------------------------------------------------------------------------------

video = moviepy.editor.VideoFileClip(videoFile)
audio = video.audio
audio.write_audiofile("./../AudioFiles/sample.mp3")
audio = moviepy.editor.AudioFileClip("./../AudioFiles/sample.mp3")
out_video = moviepy.editor.VideoFileClip("./../Output/output.mp4")
final_clip = out_video.set_audio(audio)
os.remove("./../AudioFiles/sample.mp3")
os.remove("./../Output/output.mp4")
final_clip.write_videofile("./../Output/output.mp4")


print ("Done Cropping!")