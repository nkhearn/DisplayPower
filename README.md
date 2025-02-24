# EmonPi Display Script

This Python script retrieves data from an EmonPi server and displays it on a Waveshare 1.54 inch e-Paper display. It shows voltage, balance (or a positive sign if balance is 0), and a smiley/sad face based on the voltage level, along with the current time.

## Features

* **EmonPi Data Retrieval:** Fetches voltage and balance data from an EmonPi server via HTTP requests.
* **IP Address Validation:** Checks if the EmonPi IP address is valid.
* **Error Handling:** Handles cases where the EmonPi server is unreachable or returns non-200 status codes.
* **e-Paper Display:** Displays the retrieved data on a Waveshare 1.54 inch e-Paper display.
* **Visual Feedback:** Shows a smiley face if the voltage is above a threshold, and a sad face if it's below.
* **Time Display:** Shows the current time on the e-Paper display.
* **External Script Handling:** If the IP address is invalid, or the EmonPi is unreachable, the script executes an external `notfound.py` script.

## Prerequisites

* Raspberry Pi
* Waveshare 1.54 inch e-Paper display
* EmonPi server
* Python 3
* `requests` library (`pip install requests`)
* `waveshare_epd` library (install as described in the waveshare documentation)
* DejaVuSans-Bold font (usually installed on linux systems)
* nmap for emonip.sh

## Installation

1.  **Clone the Repository (or copy the script):**
    ```bash
    # If using git
    git clone https://github.com/nkhearn/DisplayPower.git
    cd DisplayPower
    
    # or just copy the python script to your raspberry pi
    ```
2.  **Install Dependencies:**
    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip
    sudo pip3 install requests
    # Install the waveshare_epd library as described in their documentation.
    ```
3.  **Configure EmonPi IP Address:**
    * Create a file named `emonpi` in the `/home/pi/` directory.
    * Add the EmonPi server's IP address to this file. (e.g., `192.168.1.100`)
    * Ensure there are no trailing whitespace characters.
4.  **`notfound.py` script:**
    * This script will be executed if the EmonPi IP address is invalid or the server is unreachable.
    *  `notfound.py` executes emonip.sh
  
5.  **`emonip.sh` script:**
    * This script runs nmap to find the server called emonpi and outputs it's IP address.

## Script Description

* The script reads the EmonPi IP address from the `/home/pi/emonpi` file.
* It validates the IP address using a regular expression.
* If the IP address is valid, it sends an HTTP request to the EmonPi server to retrieve voltage and balance data.
* If the request is successful, it processes the data and displays it on the e-Paper display.
* It displays the current time, balance, voltage, and a smiley/sad face based on the voltage level.
* If the IP address is invalid or the EmonPi server is unreachable, it executes the `notfound.py` script.
* The script uses the `waveshare_epd` library to interact with the e-Paper display.
* Error handling is implemented for network issues and keyboard interrupts.

## Notes

* Ensure the EmonPi server is running and accessible from the Raspberry Pi.
* Adjust the voltage threshold for the smiley/sad face as needed.
* The script assumes the EmonPi server returns data in JSON format with specific IDs (32 and 9). Adjust the request URL and data processing as needed.
* The script uses a hardcoded font path. You may need to adjust this path based on your system.
* The display rotates the image 0 degrees, this can be changed in the display section of the code.
