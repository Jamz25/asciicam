# asciicam

A (badly written) program written in python that uses data from a webcam, and converts it into ascii based on the brightness.

OpenCV for python was used in order to get webcam data and convert that data into an array of black/white values.
I have then written an algorithm that breaks this data down into corresponding "brightnesses"/sizes of ascii characters.
It was originally designed to print to the console, clearing it every camera refresh. On testing however, this was extremely slow and clunky.
Because of this, I am using the pygame library in order to draw pre-rendered white text onto a window with a black background.

Reading data from the camera and converting it into ascii runs on a seperate thread, so camera refresh should not affect FPS of the overall program. 
