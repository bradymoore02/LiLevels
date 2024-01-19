import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import imageio
import csv
import numpy as np

# Function to generate updated data for the plot based on the frame

def read_the_csv(filename):
    plotting_dict = {}
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        next(csv_reader, None)
        for row in csv_reader:
            frame = int(row[0])
            if len(row)>1:
                plotting_dict[frame] = {'x': [], 'y': []} 
            for coord in row[1:]:
                plotting_dict[frame]['x'].append(float(coord.strip('()').split(',')[0]))
                plotting_dict[frame]['y'].append(float(coord.strip('()').split(',')[1]))
    return plotting_dict

def correct(xlist,ylist):
    newy = []
    slope_correction = (plotting_dict[0]['y'][1]-plotting_dict[0]['y'][0])/(plotting_dict[0]['x'][1]-plotting_dict[0]['x'][0])
    intercept = plotting_dict[0]['x'][0]*slope_correction+plotting_dict[0]['y'][0]
    for i, x in enumerate(xlist):
        newy.append(ylist[i]-slope_correction*x)
    return np.array(newy)

def generate_line_data(frame):
    x = np.array(plotting_dict[frame]['x'])
    y = np.array(plotting_dict[frame]['y'])
    return x, y

def update_plot(frame):
    global plotting_dict
    global oldx
    global oldy
    
    ax[1].cla()  # Clear the current axis
    ax[0].cla()
    # Read the frame from the video
    ret, img = cap.read()
    if not ret:
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
    
    ax[0].set_xlim(0,50)
    ax[0].set_ylim(0,6)
    ax[0].set_xlabel('x [mm]')
    ax[0].set_ylabel('y [mm]')
    ax[0].plot(x/35.4, -correct(x,y)/35.4+25)
    
    ax[0].set_title(f't = {frame/60} s')
    plt.draw()
    plt.pause(0.1)  # Pause for a short duration to allow the plot to update

# Upload line date
plotting_dict = read_the_csv("OutputCSVs/1-2-30to40A.csv")
# Path to the video file
video_path = 'VideoSnippets/leveltest2.mp4'  # Replace with the actual path to your video file

# Open the video file
cap = cv2.VideoCapture(video_path)

# Create a figure and axis
fig, ax = plt.subplots(2)

# Create a list to store frames for GIF creation
frames_for_gif = []

# Create the animation
ani = FuncAnimation(fig, update_plot, frames=200, interval=200)  # Update every 200 milliseconds

# Show the plot and save frames for GIF
try:
    plt.show()
finally:
    # Append the frames to the list
    frames_for_gif.append(plt.gcf().canvas.copy_from_bbox(ax.bbox))
    ani.event_source.stop()
    plt.close()

# Save the frames as a GIF
imageio.mimsave('output.gif', frames_for_gif, fps=10)  # Adjust the fps as needed

# Release the video capture object
cap.release()
