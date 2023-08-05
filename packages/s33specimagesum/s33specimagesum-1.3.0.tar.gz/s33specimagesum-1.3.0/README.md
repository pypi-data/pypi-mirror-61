# Introduction

This program was developed for Reika Yokoshi (University of Chicago) and Evguenia Karapetrova (APS-XSD) for use with DataCollected at Sector 33-BM.  The program works with x-ray data collected using SPEC to control the spectrometer, reading the output spec files to get information about the collected data and data collected with a particular file organization that allows the user & programs easily match information in the spec file to image files collected at each point in the scan.  

This program is written in python uses a fairly simple PyQt interface.  The initial interface for this program is shown below.

# Installation

This application requires a python to be installed on the computer.  For simplicity, this documentation assumes that the user has installed The [Anaconda Python Distribution](https://www.anaconda.com/distribution/) which is available for Windows, MacOS, and Linux.  This application should run on any of these platforms.  On the download page there are two download options, one for Python 3.x and one for Python 2.7.  It does not matter which is installed.  For generic user computers it is best to install for a single user, using the default install path since the install scripts discussed below will try to determine the location based on these defaults.  
Once the user installs the Anaconda Python distribution, the user should be able to install by running the installation script:
 * [For Windows](https://git.aps.anl.gov/hammonds/s33specimagesum/raw/master/Scripts/installS33specimagesum.bat).
 * [For MacOS and Unix](https://git.aps.anl.gov/hammonds/s33specimagesum/raw/master/Scripts/installS33specimagesum.sh).
 
# Running overview

Run the application by clicking on the start script in Desktop/s33specimagesum/s33specimagesum(.bat or .sh).  You should see a window such as the following.

![Application on startup](docs/images/AppAtStartup.png)

At startup, you can open the spec file by either entering the filename in the text box & hitting return or using brouse button and navigating to the file.  Once the scan is entered, you can enter a list of scans to process (sum the images & save to new file).  See the image below.

![Application after selecting specfile and entering scans](docs/images/AppWithFileAndScans.png)

After entering the scans, two areas for selecting parameters from the scan file are enabled. You can use these to see the ranges of scan values for the selected scans.  At this point the Range fields are not operating but are intended to further select scans to process from a subset of those selected in the scan range.  See image below with *samZ* and *temp_sp* selected for the two parameters.

![Application with parameters selected](docs/images/AppWithParams.png)

Note at this point the window expands to accomodate the list of Parameter 1 values (shown as a set below the selection).  At this point you should be able to hit run.  The summed images will be stored in 

analysis_runtime/*file-prefix*/S*scanno*/*file-prefix*_S*scanno*_*p1name*_*p1value*_*p2name*_*p2value*

An example output directory is shown below.

![Application with parameters selected](docs/images/OutputFileDirectories.png)
