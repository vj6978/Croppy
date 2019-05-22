"""
    Croppy
    Author: Vimal James
"""

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from ImageProcessing import ImageProcessing
from parameters import Parameters

"""    
    Croppy is a tool for image manipulation. Images to be fed into CNNs need to be preprocessed.
    Having to write scripts to do this everytime and having to tweak parameters in code everytime
    to obtain the required results can be cumbersome.
"""

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Croppy")
        self.setGeometry(300, 300, 500, 450)
        self.init_gui()

    def init_gui(self):
        
        self.payload = QLineEdit()
        self.file_payload = QLineEdit()
        self.destination_folder = QLineEdit()
        self.width_input = QLineEdit()
        self.height_input = QLineEdit()
        self.skew_parameter = QLineEdit()
        self.progress_bar = QProgressBar(self)
        self.payload.setPlaceholderText("Directory")
        self.destination_folder.setPlaceholderText("Send Output Here")
        self.file_payload.setPlaceholderText("File")
        self.skew_parameter.setText("0")
        self.colour_selection_title = QLabel("Convert To")
        self.image_resize_title = QLabel("Resize To")
        self.change_size_label = QLabel("Resize")
        self.width_label = QLabel("Width")
        self.height_label = QLabel("Height")
        self.open_directory = QLabel("Open Directory")
        self.open_file = QLabel("Open File")
        self.skew_label = QLabel("Skew (Default is 0)")
        self.gray_colour_scale_radio = QRadioButton("Grayscale")
        self.process_files_button = QPushButton("Start")
        self.open_input_directories = QPushButton("Select Input Directory Path")
        self.open_output_path = QPushButton("Select Output Path")
        self.open_file_path = QPushButton("Select Input File Path")
        self.help_button = QPushButton("Help")
        self.help_text = """Croppy can take images as input in the 
                       form of single image input files at a time, or multiple images
                       together in a directory.
                       
                       If you wish to manipulate one image at a time, enter the image path to the 
                       input field with the text Select Input File Path. If you wish to manipulate
                       multiple images at a time, store all images into a directory and input the path
                       to the directory in the input filed that contains the text Select Input Directory Path.
                       Enter other choices and press Start.
                       
                       Note: When entering file paths, use \ and not /."""

        self.help_button.clicked.connect(self.help_button_clicked)

        #The Selection Files Option Panel
        
        selectDirectoryHBox = QHBoxLayout()
        directorySelectionVBox = QVBoxLayout()
        directorySelectionVBox.addWidget(self.payload)
        directorySelectionVBox.addWidget(self.open_input_directories)
        directorySelectionVBox.addWidget(self.file_payload)
        directorySelectionVBox.addWidget(self.open_file_path)
        self.open_input_directories.clicked.connect(self.open_directories_clicked)
        self.open_file_path.clicked.connect(self.open_file_path_clicked)

        outputPathVBox = QVBoxLayout()
        outputPathVBox.addWidget(self.destination_folder)
        outputPathVBox.addWidget(self.open_output_path)
        self.open_output_path.clicked.connect(self.open_output_path_clicked)

        selectDirectoryHBox.addStretch()
        selectDirectoryHBox.addLayout(directorySelectionVBox)
        selectDirectoryHBox.addStretch()
        selectDirectoryHBox.addLayout(outputPathVBox)

        #The Hyperparameters

        colourScaleVBox = QVBoxLayout()
        colourScaleVBox.addWidget(self.colour_selection_title)
        colourScaleVBox.addWidget(self.gray_colour_scale_radio)
        
        imageResizeVBox = QVBoxLayout()
        imageResizeVBox.addWidget(self.image_resize_title)
        widthOptionsContainer = QHBoxLayout()
        widthOptionsContainer.addWidget(self.width_label)
        widthOptionsContainer.addStretch()
        widthOptionsContainer.addWidget(self.width_input)
        heightOptionsContainer = QHBoxLayout()
        heightOptionsContainer.addWidget(self.height_label)
        heightOptionsContainer.addStretch()
        heightOptionsContainer.addWidget(self.height_input)
        imageResizeVBox.addLayout(widthOptionsContainer)
        imageResizeVBox.addLayout(heightOptionsContainer)

        imageParametersHBox = QHBoxLayout()
        imageParametersHBox.addStretch()
        imageParametersHBox.addLayout(colourScaleVBox)
        imageParametersHBox.addStretch()
        imageParametersHBox.addLayout(imageResizeVBox)
        imageParametersHBox.addStretch()

        skewParametersVBox = QVBoxLayout()
        skewParametersVBox.addWidget(self.skew_label)
        skewParametersVBox.addWidget(self.skew_parameter)

        #The Processing Button Panel

        processButtonHBox = QHBoxLayout()
        processButtonHBox.addStretch()
        processButtonHBox.addWidget(self.process_files_button)
        processButtonHBox.addStretch()
        processButtonHBox.addWidget(self.help_button)

        windowSetting = QVBoxLayout()
        windowSetting.addLayout(selectDirectoryHBox)
        windowSetting.addLayout(imageParametersHBox)
        windowSetting.addLayout(skewParametersVBox)
        windowSetting.addLayout(processButtonHBox)

        self.setLayout(windowSetting)
        self.process_files_button.clicked.connect(self.process_files_button_clicked)
        self.show()

    def process_files_button_clicked(self):
        params = Parameters()
        colour_option = 0
        self.process_files_button.setDisabled(True)
        if self.gray_colour_scale_radio.isChecked():
            colour_option = True

        params.setColourOption(colour_option)
        params.setHeightInput(self.height_input.text())
        params.setSkew(self.skew_parameter.text())
        params.setWidthInput(self.width_input.text())
        params.setDestination( self.destination_folder.text())
        
        if len(self.payload.text()) > 0:
            params.setFile(self.payload.text())
        else:
            params.setFile(self.file_payload.text())

        processor = ImageProcessing()
        processor.process(params)

        self.process_files_button.setEnabled(True)
        finishedProcessing = QMessageBox()
        finishedProcessing.setText("Finished Processing!")
        self.resetAll()
        finishedProcessing.exec_()

    def open_directories_clicked(self):
        options = QFileDialog.Options()
        filePath = QFileDialog.getExistingDirectory(self)
        if filePath:
            self.payload.setText(filePath)

    def open_file_path_clicked(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Folder", "", "All Files (*)", options=options)
        if filePath:
            self.file_payload.setText(filePath)

    def open_output_path_clicked(self):
        options = QFileDialog.Options()
        filePath = QFileDialog.getExistingDirectory(self)
        if filePath:
            self.destination_folder.setText(filePath)

    def help_button_clicked(self):
        help_message = QMessageBox()
        help_message.setText(self.help_text)
        help_message.exec_()

    def resetAll(self):
        self.payload.setText("")
        self.file_payload.setText("")
        self.destination_folder.setText("")
        self.width_input.setText("")
        self.height_input.setText("")
        self.skew_parameter.setText("")

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
