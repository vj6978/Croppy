import numpy as np
import os
import cv2
import pickle

"""
    This class contains the algorithm that actually manipulates the images.
"""

class ImageProcessing():

    # def __init__(self):
    #     super(ImageProcessing, self).__init__()

    """
        Croppy provides a picked file of information if required
    """
    def create_pickle_file(self):
        pickle_out = open("CroppyPickle.pickle","a")
        pickle.dump(training_data, pickle_out)
        pickle_out.close()

    """
            Folder paths need to be converted into suitable formats for opening
            Example: C:\Desktop\ExampleFilePath
                becomes
                C:\\Desktop\\ExampleFilePath
    """
    def fix_path(self, payload, destination):
        payload = payload.replace("\\", "\\\\")
        destination = destination.replace("\\", "\\\\")
        return (payload, destination)

    """
            Input and Output destination file paths converted into suitable formats
    """ 
    def create_training_data(self, directoryPath, destinationPath, colorToGrayOption, width, height):

        directoryPath, destinationPath = self.fix_path(directoryPath, destinationPath)

        if os.path.isdir(directoryPath):
        
            for img in os.listdir(directoryPath):
                try:
                    path = directoryPath+"\\\\"+img
                    if colorToGrayOption:
                        img_array = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    else:
                        img_array = cv2.imread(path, cv2.IMREAD_COLOR)
                    norm_img = cv2.resize(img_array, (int(width), int(height)))
                    cv2.imwrite(destinationPath+"\\\\"+img+"_processed.jpg", norm_img)
                except Exception as e:
                    with open("ErrorLog.txt", "w+") as fileHandle:
                        fileHandle.write(str(img)+" [Error: "+str(e)+"]\n")
                    fileHandle.close()

        else:
            try:
                path = directoryPath
                if colorToGrayOption:
                    img_array = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                else:
                    img_array = cv2.imread(path, cv2.IMREAD_COLOR)
                norm_img = cv2.resize(img_array, (int(width), int(height)))
                cv2.imwrite(destinationPath+"\\\\"+"croppy_processed.jpg", norm_img)
            except Exception as e:
                with open("ErrorLog.txt", "w+") as fileHandle:
                    fileHandle.write(str(directoryPath)+" [Error: "+str(e)+"]\n")
                fileHandle.close()


        # self.create_pickle_file()


            
