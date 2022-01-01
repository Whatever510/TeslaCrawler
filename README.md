# TeslaCrawler
This program pull the source code of the Model S, 3, X and Y configurator and calculates the differences to the 
previous day. 

## Setup

1. Clone this repository. 

2. Install the necessary requirements.
```
pip install jsbeautifier
pip install diff-match-patch
pip install beautifulsoup4
pip install urllib3
pip install PyQt5
```

### Using the code
1. Clone the Repo
2. Run:
Note: You need the pulls of at least two different days to generate a diff file.
```
python main.py
```
- In the GUI select the desired countries. (1)

- Press the start button (2).
- The output will show if differences to the previous day were found.

![Alt text](assets/Ui.png?raw=true "GUI")
![Alt text](assets/output.png?raw=true "GUI")

NOTE: The GUI will freeze during execution. Please wait until it becomes responsive again.

The *differences/* directory contains the generated .diff files for the specified countries.
If the file is larger than 1kB, there most likely were changes in the configurator.

In the *previous_saves/* directory the relevant source code from the configurator for each country is saved. Please note,
this code was beautified to enable the difference extraction and is no longer executable. It can be used to gather additional information
about the changes.

Example of the difference file:
![Alt text](assets/differences.png?raw=true "GUI")


