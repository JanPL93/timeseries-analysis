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
    
import os
import numpy as np
from tifffile import imwrite
from tkinter import Tk, filedialog
import glob
import time

#%% define input and output folder
root = Tk()
root.withdraw()
root.attributes('-topmost', True)

#prompt for directory of .h5 files
h5_folder = filedialog.askdirectory(title="Select folder containing .h5 files.")
print("Selected directory of .h5 files: " + h5_folder + '/n')

#prompt for directory to output .tif files
output_folder = filedialog.askdirectory(title="Select folder to output .tif files.")
print("Selected directory of .tif files: " + output_folder + '/n')

#create a list of .h5 files
cam_name = input('What is the name of the camera? Long, Short, Left, Right, etc. ')
cam_filename = 'Cam_' + cam_name + '_*.lux.h5'
h5_list = glob.glob(os.path.join(h5_folder, cam_filename))
h5_list_len = str(len(h5_list))
print("Number of .h5 files detected: ", h5_list_len)

#name output
output_name = input('Name the .tif output prefix: ')

#%% define h5 to numpy array function
def h5_to_proj(filename):
    h5_file = h5py.File(filename,'r')
    h5_data = h5_file.get('Data')
    h5_array = np.array(h5_data)
    max_projection = np.max(h5_array, axis = 0)
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
    print("--- %0.3s seconds per frame ---" % (time.time() - start_time))