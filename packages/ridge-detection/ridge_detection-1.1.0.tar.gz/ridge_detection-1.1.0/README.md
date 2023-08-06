# ridge_detection
This package implements and extends the ridge / line detection algorithm described in:

Steger, C., 1998. An unbiased detector of curvilinear structures. IEEE Transactions on Pattern Analysis and Machine Intelligence, 20(2), pp.113–125.  

It is basically the translation from java to python of https://github.com/thorstenwagner/ij-ridgedetection.
For more informations about the params visit "https://imagej.net/Ridge_Detection".

## **Please pay attention that we removed some part of the code and some parameters** 

EXAMPLE CONFIG FILE
-
I has to be a json format


    "path_to_file": "../example.tif",
	"mandatory_parameters": {
        "Sigma": 3.39,
        "Lower_Threshold": 0.34,
        "Upper_Threshold": 1.02,
        "Maximum_Line_Length": 0,
        "Minimum_Line_Length": 0,
        "Darkline": "LIGHT",
        "Overlap_resolution": "NONE"
    },

  	"optional_parameters": {
		"Line_width": 10.0,
        "High_contrast": 200,
        "Low_contrast": 80
	},

	"further_options": {
		"Correct_position": true,
		"Estimate_width": true,
        "doExtendLine": true,
		"Show_junction_points": true,
        "Show_IDs": false,
		"Display_results": true,
        "Preview": true,
        "Make_Binary": false,
        "save_on_disk": true
	}


PARAMETER SELECTION

There are three parameters which have to be specified. These are the mandatory parameters. The optional parameters can be used to estimate the mandatory parameters


MANDATORY PARAMETERS:
-

SIGMA  -->  Determines  the sigma for the derivatives. It depends on the line width

LOWER THRESHOLD --> Line points with a response smaller as this threshold are rejected 

UPPER THRESHOLD --> Line points with a response larger as this threshold are accepted. 

DARKLINE (true/false) --> This parameter determines whether dark or bright lines are extracted. 

OVERLAP RESOLUTION (None/Slope) --> You can select a method to attempt automatic overlap resolution. The accuracy of this method will depend on the structure of your data.
 * NONE --> The default behavior: no assumption of overlap is made. Any point of potential intersection will be treated as an end point for the ridges involved.
 * SLOPE --> This method makes the assumption that when two ridges overlap, it is more likely that they will continue on their path than make turns. **This is best suited to datasets with brief periods of overlap!** If two ridges have a significant portion of overlap, the accuracy of this method will rapidly diminish. 

OPTIONAL PARAMETERS: 
-
They are used to estimate the mandatory parameters. At version 1.0.0 it is still not implemented


LINE WIDTH (w)  --> The line diameter in pixels. It estimates the mandatory parameter 'Sigma' by: <img src="https://latex.codecogs.com/svg.latex?{\color{White} \frac{w}{2\sqrt{3}}+0.5}"/>

HIGH CONTAST (Bupper) -->  Highest grayscale value of the line. It estimates the mandatory parameter 'Upper threshold' by: <img src="https://latex.codecogs.com/svg.latex?{\color{White} 0.17*\frac{2*Bupper*\frac{w}{2}}{\sqrt{2\pi}\sigma^{3}} *   e^{-\frac{(\frac{w}{2})^{2}}{2\sigma ^{2}}} } "/>

LOW CONTAST  (Blow) --> Lowest grayscale value of the line. It estimates the mandatory parameter 'Lower threshold' by: <img src="https://latex.codecogs.com/svg.latex?{\color{White} 0.17*\frac{2*Blow*\frac{w}{2}}{\sqrt{2\pi}\sigma^{3}} *   e^{-\frac{(\frac{w}{2})^{2}}{2\sigma ^{2}}} }"/>

FURTHER OPTIONS (True/False)
-

CORRECTION POSITION --> Correct the line position if it has different contrast on each side of it

ESTIMATE WIDTH: If this option is selected the width of the line is estimated.

SHOW JUNCTION POINTS: If this option is selected the junctions points will be displayed.

SHOW IDs: The ID of each line will be shown.

DISPLAY RESULTS: If this option is selected, all contours and junctions are filled into a results table.





 
 