import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import numpy as np
import Plot

# Function to generate updated data for the plot based on the frame

VIDEO_NAME = 'PunchMouth_IIICropped'
FOLDER = "PunchMouth"



def generate_line_data(frame):
    x = np.array(data[frame]['x'])
    y = np.array(data[frame]['y'])
    return x, y

def update_plot(frame):
    global data
    global oldx
    global oldy

    ax[1].cla()  # Clear the current axis
    ax[0].cla()
    # Read the frame from the video
    ret, img = cap.read()
    if not ret:
        return
    if frame <3:
        return
    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    #img_resized = cv2.resize(img_rgb, (int(1920/35.4), int(1080/35.4)), interpolation=cv2.INTER_AREA)
    # Plot the frame
    plt.imshow(img_rgb)

    # Generate line data and plot the line
    try:
        x, y = generate_line_data(frame)
    except:
        x,y = oldx,oldy
    oldx,oldy = x,y
    ax[1].plot(x, y, color='red', linewidth=2)
    ax[1].axis('off')

    ax[1].set_xlabel('X-axis')
    ax[1].set_ylabel('Y-axis')
    ax[0].set_xlim(0, xrange*scale_factor*1.2)
    ax[0].set_aspect('equal')
    ax[0].set_ylim(0, yrange*scale_factor*1.3)

    ax[0].set_xlabel('x [mm]')
    ax[0].set_ylabel('y [mm]')
    
    if frame > 2:
        slope_correction = (data[0]['y'][1]-data[0]['y'][0])/(data[0]['x'][1]-data[0]['x'][0])
        ax[0].plot(x*scale_factor, -Plot.correct(x,y, slope_correction)*scale_factor+maxy*scale_factor*1.1, marker = 'o')
    
    ax[0].set_title(f't = {frame/60} s')
    plt.draw()
    plt.pause(0.1)  # Pause for a short duration to allow the plot to update

# Upload line date
data, minx, maxx, miny, maxy = Plot.read_the_csv(f"OutputCSVs/{VIDEO_NAME}.csv")
xrange = maxx-minx
yrange = maxy-miny
# Path to the video file
video_path = f'VideoSnippets/{FOLDER}/{VIDEO_NAME}.mp4'  # Replace with the actual path to your video file

# Open the video file
cap = cv2.VideoCapture(video_path)

# Create a figure and axis
fig, ax = plt.subplots(2, figsize=(6,5), gridspec_kw={'height_ratios': [1, 3]})

# Create a list to store frames for GIF creation
frames_for_gif = []

scale_factor = Plot.scaling(10, data)
# Create the animation
for frame in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
    update_plot(frame)
    plt.draw()
    plt.savefig(f'Video-Plot/{VIDEO_NAME}/{frame}.png')
    plt.pause(0.1)


plt.show()
