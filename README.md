# iOS Calendar Extractor

This is a simple tool that helps you restore your calendar items from an iOS calendar database.

## How To Use

This is a Python-based command-line tool. The following prerequisites are required:

- Python (3.7 or higher recommended)

To run:

1. Get your `calendar.sqlitedb` database file.  
	*If you don't have the `calendar.sqlitedb` file but only the backup of your iOS device, you will need to extract the calendar from your backup using a tool like [iTunes Backup Explorer](https://github.com/MaxiHuHe04/iTunes-Backup-Explorer).*
2. Download `sqlitedb-to-ics.py` and place it in the folder where your `calendar.sqlitedb` is.
3. Open a command line or terminal window in the folder with your calendar database and the downloaded python file.  
	- For Windows, press `Win` + `R` and type "cmd" in the Run box and press enter.
	- For Linux, press `Ctrl` + `Alt` + `T`.
4. Type `python sqlitedb-to-ics.py` and hit enter.
5. You will be prompted with all the calendars in the database that contain calendar items. Enter the number of the calendar you wish to export and press enter.  
	*If you enter `0`, you can export all your calendars at once into one file or separate files.*
6. Your calendar items will be exported and saved as *`<name_of_selected_calendar>.ics`* in the same folder as the database and python file.

## What is Extracted

This tool currently extracts the following fields from calendar items:

- Summary (event title)
- Description
- Start date/time
- End date/time
- URL
- Creation date
- All-Day event flag