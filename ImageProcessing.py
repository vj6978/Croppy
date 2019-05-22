"""
    Croppy
    Author: Vimal James
"""

import os
import cv2
import pickle
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

"""
    This class contains the algorithm that actually manipulates the images.
"""

class ImageProcessing():

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


    def process(self, params):

        directoryPath, destinationPath = self.fix_path(params.getFile(), params.getDestination())

        params.setDirectoryPath(directoryPath)
        params.setDestinationPath(destinationPath)

        i = 0

        if os.path.isdir(directoryPath):

            with ThreadPoolExecutor(multiprocessing.cpu_count()) as executor:

                for img in os.listdir(directoryPath):

                    path = directoryPath+"\\\\"+img
                    i = i + 1
                    try:
                        executor.submit(self.algo, path, params, i)
                    except Exception as e:
                        print("Error: ", e)

        else:
                path = directoryPath
                self.algo(path, params, i)


    def algo(self, path, params, i):

        try:
            if params.getColourOption():
                img_array = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            else:
                img_array = cv2.imread(path, cv2.IMREAD_COLOR)

            norm_img = cv2.resize(img_array, (int(params.getWidthInput()), int(params.getHeightInput())))

            num_rows, num_cols = norm_img.shape[:2]
            rotation_matrix = cv2.getRotationMatrix2D((num_cols / 2, num_rows / 2), int(params.getSkew()), 1)
            img_rotation = cv2.warpAffine(norm_img, rotation_matrix, (num_cols, num_rows))

            cv2.imwrite(params.getDestination()+"\\\\"+str(i)+"_processed.jpg", img_rotation)

        except Exception as e:
            with open("ErrorLog.txt", "w+") as fileHandle:
                fileHandle.write(str(params.getDirectoryPath()) + " [Error: " + str(e) + "]\n")
            fileHandle.close()