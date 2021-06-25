# GPU Hunter
## Overview
GPU Hunter is a Linux app designed to help a user keep track of a store's stock of GPU products and will notify the user when the wanted item is in stock and available to purchase.

-----

## How to install
*Linux*:  
1. Clone this repo with `git clone https://github.com/Atari4800/gpu-scraper.git`  
2. Make sure `build.sh` is executable: if not, run `chmod +x build.sh`   
2. Run `sudo ./build.sh` (sudo is needed to install dependancies properly) 

-----------

## How to use
*Linux*:
After building:
1. Run `python3 scheduler.py`to start an instance of GPU Hunter
2. Use the command `crontab -l` to check if the cronjob is currently running.
4. Use the command `crontab -r` to stop the cron job. 

---------

## Release Notes

*Currently working:*
- Best Buy, B&H, and Newegg have been tested and succeed
- Firefox is able to open URL when product is in stock
- Build script installs dependancies
- Headless Selenium allows some bot evasion
- Beautiful Soup is able to parse HTML to find needed elements
- Crontab allows program to be called every minute to not be constantly running in the background

*Currently in Progress:*
- GUI is started
- GUI can interact with command line
- GUI can create popup notification
- GUI has text field entry

*To Do:*
- Make the program use resources more effeciently as it currently is running slow if more than one thing is searched for at a time
- Increase bot evasion measures
- Integrate GUI with backend
- Research if Windows is a viable platform


**Code Milestone 1:**  
We feel we have achieved all our goals for this milestone and we have started on future milestone goals along with continuously improving what we have done.

Our goals for Milestone 1 were:
- Implement Web Scraper Core
- Identify which Python modules are best suited to aid in task
- Create basic web scraper
- Research methods of bot-detection evasion
- Implement bot-detection evasion features
- Test web-scraper functionality on known websites.
