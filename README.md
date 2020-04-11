# Focus Analyzer

## Project File Overview

- [`focus_analyzer.py`](focus_analyzer.py) main file for running your focus analysis.
- [`common/video_handler.py`](common/video_handler.py) class for capturing the contents of a video file and saving the changes made to it.
- [`common/transformer.py`](common/transformer.py) class for editing each frame within our video.
- [`common/io_functions.py`](common/io_functions.py) helper functions for reading/writing our data and video files.
- [`configs/config.json`](configs/config.json) a configuration file for your file paths and preferred visual settings

## Requirements

You’ll need the following:

- [Python 3.6.8](https://www.python.org/downloads/release/python-368/) Other Python 3 versions may work as well.
- Python's PIP package installer
- Eye tracking capability with data output. I recommend using a Tobii (https://gaming.tobii.com/)
- At-home EEG machine with frontal electrodes (FP1, FP2, FPz) and data output. I recommend using a Muse (https://choosemuse.com/)

## Getting Started

The commands below are for Windows and my Python alias is "python" but yours may be "python3, "py -3", etc.

You will first have to watch a video and record your eye tracking and EEG data. Also make sure to identify the max X and Y coordinates of your video, which will be used as a config.

Make sure you have the virtualenv package in your global Python environment.

```
python -m pip install virtualenv
```

Move this project to its own folder and setup a virtual environment inside of it.

```
python -m venv env
```

Activate your virtual environment.

```
env/Scripts/activate
```

Install the project's dependencies into your virtual environment.

```
pip install -r requirements.txt
```

Modify the [`configs/config.json`](configs/config.json) file to adjust your settings and point to your relevant video and data files. I have placed example files in the resources folder.

Run your program!

```
python focus_analyzer.py
```


