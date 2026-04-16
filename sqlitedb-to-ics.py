# iOS calendar db to ics
# Author: Mr Kaos

# This script extracts calendar items from an iOS calendar sqlite database and converts them into a readable .ics file for importing into a calendar.

import sqlite3
import os
from time import strftime, gmtime, localtime, timezone
from sqlite3 import Connection

file = "./Calendar.sqlitedb"
local_timezone = "Australia/Melbourne"
cocoa_core_data_time_difference = 978307200

def open_file(file: str):
	conn = None
	if (os.path.exists(file)):
		conn = sqlite3.connect(file)
		
	else:
		print("The calendar file \"" + file + "\" does not exist!")

	return conn

def calendar_item_to_ics(item):
	event = "\nBEGIN:VEVENT"

	epoch_start = item[2] + cocoa_core_data_time_difference
	start_timezone = item[3]
	if start_timezone == "_float":
		start_timezone = local_timezone

	epoch_end = item[4] + cocoa_core_data_time_difference
	end_timezone = item[5]
	if end_timezone == "_float":
		end_timezone = local_timezone

	epoch_modified = None
	if item[8] != None:
		epoch_modified = item[8] + cocoa_core_data_time_difference

	epoch_created = None
	if item[10] != None:
		epoch_created = item[10] + cocoa_core_data_time_difference

	event += "\nCREATED:" + strftime("%Y%m%dT%H%M%SZ", localtime(epoch_created))
	event += "\nDTEND;TZID=" + start_timezone + ":" +strftime("%Y%m%dT%H%M%S", localtime(epoch_end))
	event += "\nDTSTAMP:" + strftime("%Y%m%dT%H%M%SZ", gmtime(epoch_created))
	event += "\nDTSTART;TZID=" + end_timezone + ":" + strftime("%Y%m%dT%H%M%S", localtime(epoch_start))
	event += "\nLAST-MODIFIED:" + strftime("%Y%m%dT%H%M%SZ", localtime(epoch_modified))
	# event += "\nRRULE:FREQ=DAILY;UNTIL:" + item[]
	# event += "\nSEQUENCE:" + str(item[11])
	event += "\nSUMMARY:" + str(item[0])
	event += "\nDESCRIPTION:" + str(item[1] or "").replace("\n", "\\n")
	event += "\nURL:" + str(item[7] or "")
	event += "\nUID:" + str(item[9] or "")

	event += "\nEND:VEVENT"
	return str(event.encode("utf-8"))

def extract_calendar_items(conn: Connection, calendar_id: int, name: str):
	cur = conn.cursor()
	where = ""
	if calendar_id != 0:
		where = " WHERE calendar_id = " + str(calendar_id)

	query = "SELECT `summary`, `description`, `start_date`, `start_tz`, `end_date`, `end_tz`, `all_day`, `url`, `last_modified`, `unique_identifier`, `creation_date`, `display_order`" \
		"FROM CalendarItem" + where
	res = cur.execute(query)

	filename = "calendar_" + name + ".ics"
	file = open(filename, "w")

	file.write("BEGIN:VCALENDAR")

	for item in res.fetchall():
		file.write(calendar_item_to_ics(item))

	file.write("\nEND:VCALENDAR")

	file.close()
	cur.close()
	print("Successfully exported to \"" + filename + "\"")

def get_calendars(conn: Connection):
	cur = conn.cursor()
	res = cur.execute("SELECT c.ROWID, title, COUNT(ci.ROWID) items FROM Calendar c JOIN CalendarItem ci ON ci.calendar_id = c.ROWID GROUP BY c.ROWID, title")

	calendars = res.fetchall()

	print("There are " + str(len(calendars)) + " calendars that can be extracted. Options:")
	print("0: [ALL CALENDARS]")
	for i in range(len(calendars)):
		print(str(i + 1) + ": " + calendars[i][1] + " (" + str(calendars[i][2]) + " items)")

	selection = input("Enter a calendar number to export: ")
	while selection.isnumeric() and (int(selection) > len(calendars) or int(selection) < 0) or not selection.isnumeric():
		selection = input("Enter a calendar number to export: ")
		
	if int(selection) == 0:
		# combine = input("Would you like to combine all calendars into one .ics file? [y/N]: ")
		print("NOT AVAILABLE YET, SORRY")
	else:
		extract_calendar_items(conn, calendars[int(selection) - 1][0], calendars[int(selection) - 1][1])

conn = open_file(file)

if (conn != None):
	get_calendars(conn)
	# extract_calendar_items(conn, 0)
