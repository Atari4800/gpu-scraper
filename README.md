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

## Release Notes 1

*Currently working:*
- Best Buy, B&H, and Newegg have been tested and succeed
- Firefox can open URL when product is in stock
- Build script installs dependencies
- Headless Selenium allows some bot evasion
- Beautiful Soup can parse HTML to find needed elements
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

**Code Milestone 1 Completion:**  
We feel we have achieved all our goals for this milestone, and we have started on future milestone goals along with continuously improving what we have done.

Our goals for Milestone 1 were:
- Implement Web Scraper Core
- Identify which Python modules are best suited to aid in task
- Create basic web scraper
- Research methods of bot-detection evasion
- Implement bot-detection evasion features
- Test web-scraper functionality on known websites.

----------------------------------

## Release Notes 2

*Currently Completed:*
- All functionality from Code Milestone 1 is still working
- Automatic testing suite for all modules and major functions
- 31 test cases to cover major functionality
- GUI is connected and operating with the backend
- GUI is populating displayed list from JSON data
- Reliability of connecting to sites is improved
- Modules have had all functions commented so that documentation can be generated

*Currently in Progress:*
- Fill out test cases with more edge cases
- Test Regex for increased speed over Beautiful Soup
- Connecting Notification component

*To Do:*
- Work on connecting more GUI functionality
- Keep increasing bot evasion
- Keep increasing speed
- Increase readability and maintainability of code
- Refactor into proper PEP8 style formatting


**Code Milestone 2 Completion:**  
We have achieved all our goals for this milestone and have made great headway into Milestone 3.

Our goals for Milestone 2 were:  
- Identify which Python modules are best suited to aid in task
- Identify keywords, and web-code sections that contain product status information
- Determine if cookies need to be stored and used, or JavaScript information needs to be dynamically interpreted to retrieve product status information
- Create web-code parser
- Test web-code parser to ensure functionality

Goals completed from Milestone 3 are:
 - Tie GUI into web scraper and parser components
 - Have everyone create a sketch of GUI


## Release Notes 3

*Currently Completed*
- All goals from Milestone 1 and Milestone 2
- GUI is fully connected to backend
- Test suite tests all major functionality
- Speed is improved with Regex
- Code is refactored and commented adequately

*Currently in Progress*
- Polishing code for consistant results

*To Do*
- Generate final documentation

**Code Milestone 3 Completion**  
We have achieved all of our goals set out for this milestone and are now in the process of polishing up the final deliverable.

Our goals for Milestone 3 were:
- Brainstorm items user may want control over
- Brainstorm useful GUI components (text input fields, buttons, etc.)
- Have everyone create a sketch of GUI
- Create best hybrid GUI among the three variations
- Tie GUI into web scraper and parser components
- Test GUI among 3 non-developer users and get feedback

## Release Notes 4

*Currently Completed*  
- All goals from Milestone 1, Milestone 2, and Milstone 3
- GUI is fully connected to all backend functions
- Code comments are up finalized
- Final documentation generated
- Website is live

*Currently in Progress*  
- None

*To Do*  
- None

**Code Milestone 4 Completion**  
We have achieved all of our goals set out for this milestone and were ahead of schedule on delivering this project. 

Our goals for Milestone 4 were:
- Written reports of additional functionality (ie, specific websites, GUI refinement, additional bot detection evasion)
- Any additional bot detection evasion completed.
- Add any remaining unimplemented GUI sections
- Optimize code if possible
- Milestone 4 video and final code commits. 
- Any relevant documentation on the final code commits must be added, and previous documentation must be updated.


