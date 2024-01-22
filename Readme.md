### Point Picker for Li Videos on SLiDE

## Getting Started

1. Clone this git repository
2. Download the cropped videos from box.illinois.edu

## First Video

1. Edit the input_video_name and csv_name variables at the top of PointPicker.py to indicate the input video you want and where to save the data.
2. Run PointPicker.py.
3. Select two points that are far apart along the top edge of the distributer by clicking on them with the mouse. The frame counter should indicate frame zero for this. These will be used to determine the slop in the video so accuracy here is key.
4. Other key commands. 'u' is undo last point placed on current frame. 'b' go back to previous frame. ' ' (space) is move to next frame. 'q' is save and exit ('x' will also exit and save)..
5. Progress the frames until you see a change in the lithium level. At that frame, begin selecting points by clicking on the locations where the lithium touches the front of the distributer dividers.
6. Move forward a few frames (3-10) until there is a noticable difference in the picture and repeat the point selection process.

## Future Videos

Make sure to change the csv_name file before running the script again or else you will lose the saved data by overwriting. If you accidentally start the python script without changing the name, change the name of the csv file the old data is stored to before closing out of the point picker window.
