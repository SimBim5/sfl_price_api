import os
from PIL import Image

# Directory containing the images
image_folder = 'assets'

# Desired size for the images
new_size = (128, 128)  # Change this to your desired width and height

# Check if the image folder exists
if not os.path.exists(image_folder):
    print(f"Directory {image_folder} does not exist.")
else:
    # Loop through all files in the image folder
    for image_file in os.listdir(image_folder):
        # Only process .png files
        if image_file.endswith('.png'):
            image_path = os.path.join(image_folder, image_file)

            # Open the image
            with Image.open(image_path) as img:
                # Resize the image while maintaining transparency (if any)
                img_resized = img.resize(new_size, Image.LANCZOS)

                # Save the resized image, overwriting the original
                img_resized.save(image_path)

            print(f"Resized {image_file} to {new_size}")
