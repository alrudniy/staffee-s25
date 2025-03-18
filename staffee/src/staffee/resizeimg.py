'''
This program uses pillow to resize uploaded profile pictures. 

'''
from PIL import Image
import os 

def resize_profile_pictures(folder_path, pfp_size=(120,120)): 
    # pfp (width, height)

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        try:
            # open image to check size
            with Image.open(file_path) as img:
                width, height = img.size

                if width != pfp_size[0] or height != pfp_size[1]:

                    img = img.resize(pfp_size)

                    img.save(file_path)
                else:
                    continue

        except Exception as failed_resizing:
            print(f"Error resizing icon: {failed_resizing}")