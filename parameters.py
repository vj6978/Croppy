"""
    Croppy
    Aurthor: Vimal James
"""

class Parameters:
    def __init__(self):
        self.file = ""
        self.destination = ""
        self.colour_option = ""
        self.width_input = ""
        self.height_input = ""
        self.skew = ""
        self.directory_path = ""
        self.destination_path = ""

    def getFile(self):
        return self.file

    def setFile(self, param):
        self.file = param

    def getDestination(self):
        return self.destination

    def setDestination(self, param):
        self.destination = param
        
    def getColourOption(self):
        return self.colour_option

    def setColourOption(self, param):
        self.colour_option = param

    def getWidthInput(self):
        return self.width_input

    def setWidthInput(self, param):
        self.width_input = param

    def getHeightInput(self):
        return self.height_input

    def setHeightInput(self, param):
        self.height_input = param

    def getSkew(self):
        return self.skew

    def setSkew(self, param):
        self.skew = param

    def getDirectoryPath(self):
        return self.directory_path

    def setDirectoryPath(self, param):
        self.directory_path = param

    def getDestinationPath(self):
        return self.destination_path

    def setDestinationPath(self, param):
        self.destination_path = param

    def __str__(self):
        return str(self.__dict__)