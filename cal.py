from typing import Annotated
import typer
import datetime
from pathlib import Path

from rich import print

app = typer.Typer()


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

task_path = Path("./tasks.txt")
entry_path = Path("./entries.txt")


def fileExist(path) -> bool:
	if path.is_file():
		return True
	else:
		print("[bold yellow] file not found", path)
		return False

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
		write_to_file(task_path,complete_entry)
		return
	if entry == "entry":
		complete_entry = f"{title}@{parsed_date}@{parsed_repeat}"
		write_to_file(entry_path,complete_entry)
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
