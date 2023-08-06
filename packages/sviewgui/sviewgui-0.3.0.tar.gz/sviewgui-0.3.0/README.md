# sview-gui

Handy PyQt-based GUI for data visualisation based on a csv file or pandas' DataFrame.
This GUI is based on the matplotlib and you can visualize your csv file in various ways.
Here are the main features;

• Scatter, line, density, histgram, and box plot for visualisation your csv.

• Detail setting for the marker size, line width, number of bins of histgram, color map (from cmocean).

• Save figure as editable PDF

• Handy code of plotted graph are recorded as text in 'Log' tab so that you can readily use its code and modify it after visualization.

# Usage
It is very simple! Just import the library and call the method 'buildGUI()' like bellow.

####################################

## Sample Code 1

import sviewgui.sview as sv

sv.buildGUI()

Then GUI will open and you can import csv file from the GUI.

The method 'buildGUI' can also take one argument of String or pandas' dataframe object.
You can specify the file path of your csv file as String object or create a datafram object directly in your code like below

#####################################

## Sample Code 2

import sviewgui.sview as sv

import pandas as pd

df = pd.DataFrame(data)

sv.buildGUI(df)

#####################################

## Sample Code 3

import sviewgui.sview as sv

FILE_PATH = "User/Documents/FOLDER/yourdata.csv"

sv.buildGUI(FILE_PATH)

#####################################

# About license
© 2019 Sojiro Fukuda All Rightss Reserved.
Free to modify and redistribute by your own responsibility.