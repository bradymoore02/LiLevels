import cv2
import numpy as np
import csv


input_video_name = 'VideoSnippets/leveltest2.mp4'
csv_name = 'OutputCSVs/1-1-30A--.csv'
important_info = '' # This is added at the top of the csv file
# List to store selected points
selected_points = []

# Variables for frame navigation and click counter
current_frame = 0
click_counter = 0

output_dict = {0: [],}
# Mouse callback function
def select_points(event, x, y, flags, param):
    global click_counter
    global output_dict
    global current_frame
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_points.append((x, y))
        click_counter += 1
        output_dict[current_frame].append((x,y))
        print(f"Selected Point {click_counter}: ({x}, {y})")

# Draw a small cross at the clicked coordinates

# Read the video file
cap = cv2.VideoCapture(input_video_name)
cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
ret, frame = cap.read()
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# Create a window and set the mouse callback
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', select_points)
last_click = 10

while True:
    # Display the frame number in the top right corner


    if click_counter != last_click:
        updatenow = True
    last_click = click_counter
    # Wait for key press
    key = cv2.waitKey(1) & 0xFF

    # Handle key events
    if key == ord('q'):
        break
    elif key == ord(' '):  # Spacebar to advance to the next frame
        if current_frame < total_frames:
            current_frame += 1
        try:
            a = output_dict[current_frame]
        except:
            output_dict[current_frame] = []

        click_counter = len(output_dict[current_frame])
        updatenow = True
    elif key == ord('b'):  # 'B' to go back to the previous frame
        if current_frame > 0:
            current_frame -= 1
        click_counter = len(output_dict[current_frame])
        updatenow = True
    elif key == ord('x'):  # 'x' to exit the video window
        break
    elif key == ord('u'):
        output_dict[current_frame].pop()
        click_counter = click_counter-1
        updatenow = True
    elif key == ord('s'):
        with open(csv_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Frame', important_info])  # Write header
            for key in output_dict.keys():
                row = [key]
                for point in output_dict[key]:
                    row.append(point)
                csv_writer.writerow(row)




    if updatenow:
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        ret, frame = cap.read()
        cv2.putText(frame, f'Frame: {current_frame}/{total_frames}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Clicks: {click_counter}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        for cross in output_dict[current_frame]:
            x = cross[0]
            y = cross[1]
            cross_size = 25
            color = (0, 255, 0)  # White
            cv2.line(frame, (x - cross_size, y), (x + cross_size, y), color, 2)
            cv2.line(frame, (x, y - cross_size), (x, y + cross_size), color, 2)
        cv2.imshow('Frame', frame)
        updatenow = False
# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()
with open(csv_name, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Frame', important_info])  # Write header
    for key in output_dict.keys():
        row = [key]
        for point in output_dict[key]:
            row.append(point)
        csv_writer.writerow(row)

# Print the selected points
print("Selected Points:", output_dict)
print(f"Selected points saved to {csv_name}")
