INTRODUCTION
============
RBM_Autoencoder is a simple Autoencder using RBM + CD1 + backpropgation, based on the stuff I learnt off Coursera's "Neural Networks for Machine Learning" course.
It uses linear neurons for the input/output layer and sigmoid for the remaining hidden layers. In addition, the following run time improvements are also implemented:
 
 - momentum
 - mini batch
 - early stopping
  

USAGE
============
To run, you need the following libraries installed:

- Armadillo (for matrices)
- OpenBLAS (recommended for multi-core support)
- OpenCV (for GUI stuff)

Armadillo and OpenBlas can be found in Ubuntu's repository. You might need to download the latest Armadillo (http://arma.sourceforge.net) if you get compilation errors complaining about unknown functions. If you can't get OpenBLAS working for some reason you can try Atlas, also found in Ubuntu's repository. For some reason my version of Atlas didn't seem to support multi-core out of the box.

This software uses data from the CIFAR-10 datset, which can be downloaded from:
    
    http://www.cs.toronto.edu/~kriz/cifar.html

Download the file http://www.cs.toronto.edu/~kriz/cifar-100-binary.tar.gz

Extract it somewhere and edit main.cpp, change the variable 'DATASET_FILE[]' to point to one of the files.
Compile the project via "make" or using CodeBlocks and run the binary bin/Release/RBM_Autoencoder. After a few minutes it will display the original image and the reconstructed image side by side.


TWEAKING
============
Nearly all the settings are in main.cpp towards the top, and are hopefully self explanatory. If there is anything you don't understand shoot me an email at nghiaho12@yahoo.com


