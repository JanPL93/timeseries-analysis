# -*- coding: utf-8 -*-
"""
03/16/2022
Jan C. Frankowski, Ph.D.
Create max projections from a time series of luxdata h5 files.
"""
try:
    import h5py
except ImportError:
    print("Install h5py using the following command in the terminal: pip install h5py")
    
try:
    import tifffile
except ImportError:
    print("Install tifffile using the following command in the terminal: pip install tifffile")
    
try:
    import numpy
except ImportError:
    print("Install numpy using the following command in the terminal: pip install numpy")
    
try:
    import tkinter
except ImportError:
    print("Install tkinter using the following command in the terminal: pip install tkinter")   
    
try:
    import natsort
except ImportError:
    print("Install natsort using the following command in the terminal: pip install natsort")
import os
import numpy as np
from tifffile import imwrite
from tkinter import Tk, filedialog
import glob
import time
from natsort import natsorted

#%% welcome message
print(""" Jan C. Frankowski, Ph.D. - Jan.Frankowski@Bruker.com
      This script creates maximum intensity projections from a time series of 
      luxdata .h5 files. This script is for data processed with Luxendo Data 
      Processor. You will be prompted for:
          - A folder containing processed .lux.h5 files.
          - A folder to output exported .tif files.
          - The name of the channel (eg. 0, 1, 2, etc).
          - The name of the stack (eg. 0, 1, 2, etc).
          - The name of the detection objective (eg. Bottom, left, etc).
          - The name of the camera (eg. Long, left, etc).
          - Whether to slice the Z series, if so, the start and end planes. (starting at 0).
          
    The script will report each file being read, the file being written, and the estimated time
    remaining.
      """)
print('\n')

#%% define input and output folder
root = Tk()
root.withdraw()
root.attributes('-topmost', True)

#prompt for directory of .h5 files
h5_folder = filedialog.askdirectory(title="Select folder containing .h5 files.")
print("Selected directory of .h5 files: " + h5_folder + '/n')

#prompt for directory to output .tif files
output_folder = filedialog.askdirectory(title="Select folder to output .tif files.")
print("Selected directory of .tif files: " + output_folder)

#create a list of .h5 files
ch_name = input('What is the name of the channel? ')
st_name = input('What is the name of the stack? ')
ob_name = input('What is the name of detection objective? ')
cam_name = input('What is the name of the camera? ')
#create filename based off inputs
filename = '*_tp-*_ch-' + ch_name + '_st-' + st_name + '*obj-' + ob_name + '_cam-' + cam_name + '_etc.lux.h5'
#find .h5 files matching above filename
h5_list = glob.glob(os.path.join(h5_folder, filename))
#sort in natural order
h5_list = natsorted(h5_list)
#report number of .h5 files found
h5_list_len = str(len(h5_list))
print("Number of .h5 files detected: ", h5_list_len)

#name output
output_name = input('Name the .tif output prefix: ')

#slice z series
z_start = None
z_end = None
slice_yn = input("Slice the Z series? y/n : ")

if slice_yn == 'y':
    z_start = int(input("Type the start Z plane: "))
    z_end = int(input("Type the end Z plane: "))
elif slice_yn == 'n':
    pass
else:
    print("Invalid input for slicing; defaulting to Z projecting full stack.")

#keep track of time taken to create projecton
seconds_per_frame = []

#%% define h5 to numpy array function
def h5_to_proj(filename):
    h5_file = h5py.File(filename,'r')
    print("Reading: ", filename)
    h5_data = h5_file.get('Data')
    h5_array = np.array(h5_data)
    if z_start != z_end:
        max_projection = np.max(h5_array, axis = 0)
    else:
        max_projection = h5_array[z_start]
    return max_projection

#%% process the list of .h5 files
for count, item in enumerate(h5_list):
    start_time = time.time()
    #create max intensity projection
    max_proj = h5_to_proj(item)
    #create .tif filename
    tif_filename = output_name + '_' + str(count) + '.tif'
    #create path to save max projection to .tif file
    tif_file_path = os.path.join(output_folder, tif_filename)
    #write file
    imwrite(tif_file_path, max_proj, photometric='minisblack')
    print('Writing: ', tif_file_path)
    
    #calculate time remaining
    print("--- %0.3s s / frame ---" % (time.time() - start_time))
    time_per_frame = (time.time() - start_time)
    seconds_per_frame.append(time_per_frame)    
    #wait to average 3 values
    if len(seconds_per_frame) < 3:
        print("...")
    else:
        t1 = seconds_per_frame[-1]
        t2 = seconds_per_frame[-2]
        t3 = seconds_per_frame[-3]
        avg_time = (t1 + t2 + t3) / 3
        frames_left = len(h5_list) - count
        hours_left = (frames_left * avg_time) / 3600
        print("~ %0.4s hours left" % hours_left)
    
    