from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import cv2
from matplotlib import pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import io, os
import numpy as np
from menu import mainMenu, sizeMenu, codecMenu
from progress.bar import IncrementalBar

def cutVideo(s1, s2, inputFile):

    ffmpeg_extract_subclip(inputFile, s1, s2, targetname='cuttedVideo7-15.mp4')


def getFrames(videoFile):

    images = []

    cap = cv2.VideoCapture(videoFile)
    success, image = cap.read()

    while success:
        images.append(image)
        success, image = cap.read()

    return np.array(images)

def get_img_from_fig(fig, dpi=180):

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

def getYUVHist(image):

    yuvImage = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
    numPixels = np.prod(yuvImage.shape[:2])
    bins = 16

    (y, u, v) = cv2.split(yuvImage)
    histogramY = cv2.calcHist([y], [0], None, [bins], [0, 1]) / numPixels
    histogramU = cv2.calcHist([u], [0], None, [bins], [-0.436, 0.436]) / numPixels
    histogramV = cv2.calcHist([v], [0], None, [bins], [-0.615, 0.615]) / numPixels

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(histogramY)
    ax.plot(histogramU)
    ax.plot(histogramV)

    return get_img_from_fig(fig)

def createVideoFramAndHist(videoFile):

    frames = getFrames(videoFile)
    height, width, layers = frames[0].shape
    size = (width,height)

    cont = 0
    bar = IncrementalBar("Adding frames", max=len(frames))

    for frame in frames:
        hist = getYUVHist(frame)

        fig = plt.figure()
        fig.add_subplot(1, 2, 1)
        plt.imshow(frame)
        fig.add_subplot(1, 2, 2)
        plt.imshow(hist)

        fig.savefig(f'frame_{cont:04d}.png')
        cont += 1
        plt.cla()
        bar.next()
    
    os.system("ffmpeg -i frame_%04d.png -c:v libx264 -r 25 -pix_fmt yuv420p frameAndHist.mp4")
    bar.finish()
        

def resizeVideo(value, videoFile):


    if len(value) == 1:
        if value[0] == 720:

            os.system("ffmpeg -i {} -vf scale=1280:720 BBB_720p.mp4".format(videoFile))
        
        elif value[0] == 480:

            os.system("ffmpeg -i {} -vf scale=640:480 BBB_480p.mp4".format(videoFile))

    elif len(value) == 2:

        os.system("ffmpeg -i {} -vf scale={}:{} BBB_{}x{}.mp4".format(videoFile, value[0], value[1], value[0], value[1]))


def changeCodecAndMono(videoFile, codec):

    os.system("ffmpeg -i {} -vcodec copy -acodec {} BBB_codecChanged.mp4".format(videoFile, codec))
    os.system("ffmpeg -i BBB_codecChanged.mp4 -ac 1 BBB_Mono.mp4")



if __name__ == "__main__":

    menu = mainMenu()
    action = menu['Action menu']
    print (menu)
    videoFile = menu['video file']

    if action == 'Cut video':

        cutVideo(7, 15, videoFile)

    elif action == 'Extract YUV + create Video':

        createVideoFramAndHist(videoFile)

    elif action == 'Resize video':

        sMenu = sizeMenu()
        size = sMenu['Resizing size']

        s = None

        if size == '720p':

            s = [720]
        
        elif size == '480p':

            s = [480]

        elif size == '360x240':

            s = [360, 240]

        elif size == '160x120':

            s = [160, 120]


        resizeVideo(s, videoFile)

    elif action == 'Change audio codec + mono':

        cMenu = codecMenu()
        codec = cMenu['codec']

        changeCodecAndMono(videoFile, codec)

    else:

        print("Please, select a correct answer")

    
