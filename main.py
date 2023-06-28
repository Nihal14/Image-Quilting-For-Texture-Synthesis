from pathlib import Path
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
import tkinter as tk
import threading
from tkinter import filedialog
from utils.texture import *

CURRENT_FOLDER = Path(__file__).parent

def select_input_image():
    # Open file dialog to select input image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    
    # Check if a file was selected
    if file_path:
        # Display the selected input image
        input_image = Image.open(file_path)
        input_photo = ImageTk.PhotoImage(input_image)
        input_label.config(image=input_photo)
        input_label.image = input_photo  # Update the reference to avoid garbage collection
        
        # Update the output label text
        output_label.config(text="Click 'Display Output Image'")

        # Enable the output button
        output_button.config(state=tk.NORMAL)

        # Update the file path for processing
        global input_file_path
        input_file_path = file_path

def display_input_image():
    if input_file_path:
        # Read and display the input image
        input_image = Image.open(input_file_path)
        input_photo = ImageTk.PhotoImage(input_image)
        input_label.config(image=input_photo)
        input_label.image = input_photo  # Update the reference to avoid garbage collection

        # Update the output label text
        output_label.config(text="Click 'Display Output Image'")

        # Enable the output button
        output_button.config(state=tk.NORMAL)
    else:
        # No input image selected
        output_label.config(text="No input image selected")

def process_output_image():
    # Reading image file
    img = cv.imread(input_file_path)

    # define the constants
    block_size = 50
    overlap_size = block_size // 6
    num_blocks = 10
    tolerance_factor = 0.1

    # convert image to double
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB) / 255.0
    H, W = img.shape[:2]
    H1 = W1 = num_blocks * (block_size - overlap_size)

    # generate output mask
    texFunc = textureMain(img, block_size, overlap_size, num_blocks, H, W, H1, W1, tolerance_factor)
    texFunc.generateOutputMask()
    output_img = texFunc.createTexture()

    # Get the proper size of the output image
    proper_h1 = proper_w1 = (block_size - overlap_size) * num_blocks - (overlap_size * (num_blocks - 1))
    output_img = output_img[0:proper_h1, 0:proper_w1, :]

    # Create a black image with the same size as the output image
    black_image = Image.new("RGB", (proper_w1, proper_h1), (0, 0, 0))

    # Paste the output image onto the black image
    black_image.paste(Image.fromarray((output_img * 255).astype(np.uint8)), (0, 0))

    # Update the output label with the processed image
    output_photo = ImageTk.PhotoImage(black_image)
    output_label.config(image=output_photo, text="")
    output_label.image = output_photo  # Update the reference to avoid garbage collection

    # Re-enable the button
    output_button.config(state=tk.NORMAL)
    
    output_path = CURRENT_FOLDER / "output_files" / "out12.png"
    black_image.save(output_path)

def display_output_image():
    # Disable the button to prevent multiple clicks during processing
    output_button.config(state=tk.DISABLED)

    # Update the output label with "Processing" message
    output_label.config(text="Processing...")

    # Create a thread to process the output image
    thread = threading.Thread(target=process_output_image)
    thread.start()

# Create the main Tkinter window
root = tk.Tk()
root.title("Image Display")

# Initialize input file path
input_file_path = None

# Load and display the input image
input_label = tk.Label(root)
input_label.pack()

# Create the output image label
output_label = tk.Label(root, text="No input image selected")
output_label.pack()

# Create the buttons
select_button = tk.Button(root, text="Select Input Image", command=select_input_image)
select_button.pack()

#display_button = tk.Button(root, text="Display Input Image", command=display_input_image)
#display_button.pack()

output_button = tk.Button(root, text="Display Output Image", state=tk.DISABLED, command=display_output_image)
output_button.pack()

# Configure output_label to be centered in the frame
output_label.pack(anchor=tk.CENTER)

# Run the Tkinter event loop
root.mainloop()
