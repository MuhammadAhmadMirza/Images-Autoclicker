# Image-Autoclicker

A simple lightweight tool to automatically detect and click specified images on the screen

## Description

This is a Python-based application that automates mouse clicks on specific images displayed on your screen. It uses the `pyautogui` library to locate images and perform clicks. The application provides a graphical user interface (GUI) built with `tkinter` for easy configuration and control. This probably already exists but i couldn't find an open source one exactly for my needs so i made this.

## Features

- Add multiple images to search for on the screen.
- Choose between "Parallel" (clicks the first found image) or "Sequential" (clicks images in order) modes.
- Adjustable delay between image checks.
- Configurable confidence threshold for image matching.
- Supports left, right, middle, and double clicks.
- Drag-and-drop reordering of image paths.

## Requirements

- Python 3.x
- Libraries:
  - `Tkinter` (included with Python)
  - `PyAutoGUI`
  - `json` (included with Python)
  - `os` (included with Python)

## Installation

Go to the releases page and download the latest release containing the .exe

OR

Run Source Code:

1. Install Python 3.x from <https://www.python.org/>.
2. Download or clone the project files.
3. Install the required libraries using pip:

     ```sh
     pip install -r requirements.txt
     ```

## Usage

1. Run the script:

     ```sh
     python Image_clicker.py / Image_AutoClicker.exe
     ```

2. Add image paths using the "+ Add Images" button.
3. Configure the settings:
     - Choose the click type (Left, Right, Middle, Double).
     - Set the delay between checks.
     - Adjust the confidence threshold for image matching.
     - Select the mode (Parallel or Sequential).
4. Click "Start" to begin the automation.
5. Click "Stop" to pause the automation.

## Configuration

- The application saves settings (image paths, mode, etc.) to a `settings.json` file in the same directory as the script.
- You can manually edit this file if needed.

## Notes

- Ensure the images you want to click are visible on the screen.
- The application works best with static images (e.g., buttons, icons).
- For dynamic content, you may need to adjust the confidence threshold or use more distinct images.

## Troubleshooting

- If the application cannot find images:
  - Increase the confidence threshold.
  - Ensure the images are exactly the same as those on the screen (size, color, etc.).
- If the GUI looks incorrect:
  - Ensure you are using a compatible operating system (Windows only is tested)
  - Update your Python and library versions (i used 3.11.9)

## License

This project is open-source and available under the MIT License. Feel free to modify and distribute it as needed.
