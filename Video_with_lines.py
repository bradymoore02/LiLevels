import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import numpy as np
import Plot

# Function to generate updated data for the plot based on the frame

VIDEO_NAME = 'PunchMouth-Set2-1'
#VIDEO_NAME = 'Distributor_Filling_Crop'

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
    ax[1].plot(x+x0, y+y0, color='red', linewidth=2)
    ax[1].axis('off')

    ax[1].set_xlabel('X-axis')
    ax[1].set_ylabel('Y-axis')
    ax[0].set_xlim(0, 45)
    ax[0].set_aspect('equal')
    ax[0].set_ylim(0, 7)

    ax[0].set_xlabel('x [mm]')
    ax[0].set_ylabel('y [mm]')
    
    if frame > 3:
        ax[0].plot(x*scale_factor, -Plot.correct(x,y, slope_correction)*scale_factor+6.7, marker = 'o')
    
    ax[0].set_title(f't = {round(frame/60,3)} s')
    plt.draw()
    plt.pause(0.1)  # Pause for a short duration to allow the plot to update

# Upload line date
data, x0, y0 = Plot.read_the_csv(f"OutputCSVs/{VIDEO_NAME}.csv")
# Path to the video file
video_path = f'VideoSnippets/{FOLDER}/{VIDEO_NAME}.mp4'  # Replace with the actual path to your video file
slope_correction = (data[0]['y'][1]-data[0]['y'][0])/(data[0]['x'][1]-data[0]['x'][0])

# Open the video file
cap = cv2.VideoCapture(video_path)

# Create a figure and axis
fig, ax = plt.subplots(2, figsize=(6,5), gridspec_kw={'height_ratios': [1, 2]})

# Create a list to store frames for GIF creation
frames_for_gif = []

scale_factor = Plot.scaling(10, data)
# Create the animation
for frame in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
    update_plot(frame)
    plt.draw()
    plt.savefig(f'Video-Plot/{VIDEO_NAME}/{str(frame).zfill(3)}.png',dpi=300)
    plt.pause(0.1)


plt.show()
