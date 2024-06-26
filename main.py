from typing import Annotated
import typer
import datetime

from rich import print

# today typer
from cal import today

# paths
from cal import paths

import os

app = typer.Typer()
app.add_typer(today.app, name="today")

"""

main today ch 1 -> complete todays 1. task

main task a <title> <date> --tf <timeframe> --r <cycle> -> add new task
main entry a <title> <date> --tf <timeframe> --r <cycle> -> add new entry


SYSTEMS
cc today -> create or read today file
cc today c <number> -> complete task from today file
cc a -> create an entry

cc <number>

"""



def fileExist(path) -> bool:
	if path.is_file():
		return True
	else:
		print("[bold yellow] file not found", path)
		return False

@app.command()
def pathtest():
	print(paths.application_path)

# Example for day repeat logic
@app.command()
def p():
	# a = datetime.date(2024,4,10)
	# b = datetime.date.today()
	# c = a - b
	# print(c.days)

	# for getting another dates from one single date
	# today + datetime.timedelta(days=1)

	# today = datetime.date.today()
	# for i in range(60):
	# 	x = today + datetime.timedelta(days=1)
	# 	print(x)
	# 	today = x
	today = datetime.date.today()
	startdate = datetime.date(2024,4,4)
	repeat = 7
	# x = today - startdate
	# if x.days % repeat == 0:
	# 	print("yes")
	# else:
	# 	print("no")

	for i in range(30):
		x = today - startdate
		if x.days % repeat == 0:
			print(today.strftime("%d-%m-%Y") + ": YES")
		else:
			print(today.strftime("%d-%m-%Y") + ": no")
		today = today + datetime.timedelta(days=1)
	

# Example for month repeat logic
@app.command()
def m():
	today = datetime.date.today()
	startdate = datetime.date(2024,5,5)
	repeat = 12
	# x = today.month - startdate.month
	# print(x)
	for i in range(365 * 2):
		x = today.month - startdate.month
		if x % repeat == 0:
			if today.day == startdate.day:
				print(today.strftime("%d-%m-%Y") + ": [green]Yes")
			else:
				print(today.strftime("%d-%m-%Y") + ": [red]no")
		else:
			print(today.strftime("%d-%m-%Y") + ": [red]no")
		today = today + datetime.timedelta(days=1)

# name: Annotated[str, typer.Argument(default_factory=get_name)]
# def main(user_name: Annotated[str, typer.Option("--name")]):

# Parse the date input
def parse_date(date_string):

	default_date = datetime.date.today()
	date_data = [
		default_date.day,
		default_date.month,
		default_date.year
	]

	# Default keywords
	if date_string == "today":
		return str(datetime.date.today())

	date_values = date_string.split("-")
	date_length = len(date_values)
	# Check if list too large
	if date_length > 3:
		return None
	
	for i in range(date_length):
		try:
			date_data[i] = int(date_values[i])
		except:
			return None

	# try to make a date
	try:
		return str(datetime.date(date_data[2], date_data[1], date_data[0]).strftime("%d-%m-%Y"))
	except:
		return None


# Parse the repeat input
def parse_repeat(repeat):
	repeat_type = str(repeat[-1])
	repeat_number = 0

	match repeat_type:
		case "d":
			pass
		case "m":
			pass
		case _:
			return None

	# Check if the other part is int
	try:
		repeat_number = int(repeat[:-1])
	except:
		return None
	return f"{repeat_number}{repeat_type}"

def write_to_file(path, entry):
	if not fileExist(path):
		return
	
	f = open(path, "a")
	f.write(entry + "\n")
	f.close()

@app.command("a")
@app.command("add")
def add_entry(
	entry: Annotated[str, typer.Argument()],
	title: Annotated[str, typer.Argument()],
	start: Annotated[str, typer.Argument()] = str(datetime.date.today().strftime("%d-%m-%Y")),
	repeat: Annotated[str, typer.Option("-r")] = "0d",
	# start: Annotated[str, typer.Option("--date", "-d")] = str(datetime.date.today()),
	):
	# if entry != "task":
	# 	print("[bold red]Invalid entry type")
	parsed_date = parse_date(start)
	if parsed_date == None:
		print("[bold red]Invalid date value")
		return
	
	parsed_repeat = parse_repeat(repeat)
	if parsed_repeat == None:
		print("[bold red]Invalid repeat value")
		return
	#print(entry,title,parsed_date,repeat)
	
	# today + datetime.timedelta(days=1)

	#yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%d-%m-%Y")
	

	if entry == "task":
		complete_entry = f"{title}@{parsed_date}@{parsed_repeat}@not completed"
		write_to_file(paths.task_path,complete_entry)
		print(f"'{title}' added to [deep_sky_blue1]task[/deep_sky_blue1] list")
		return
	if entry == "entry":
		complete_entry = f"{title}@{parsed_date}@{parsed_repeat}"
		write_to_file(paths.entry_path,complete_entry)
		print(f"'{title}' added to [yellow]entry[/yellow] list")
		return

	print("[bold red]Invalid entry type")

#@app.command()
#def a(title: str, due: str = str(datetime.date.today())):
#	if not fileExist():
#		return
#	f = open(tasks, "a")
#	#title = input("title: ")
#	#due = input("date(YYYY-MM-DD)(leave blank for today)\n: ")
#	#if due == "":
#	#	due = str(datetime.date.today())
#	f.write(title + "@" + due + "@0" +"\n")
#	f.close()

if __name__ == "__main__":
    app()
