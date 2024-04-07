from typing import Annotated
import typer
import datetime

from rich import print
from rich.console import Console
from rich.table import Table

from . import paths

app = typer.Typer()


today_date = datetime.date.today()

""" EXAMPLE FETCH
def getAllEntries():
	entryList = []
	if not fileExist():
		return entryList
	f = open(tasks, "r")
	for dataline in f:
		dataline = dataline.rstrip("\n")
		splitData = dataline.split("@")
		entryList.append(Entry(splitData[0], splitData[1]))
	f.close()
	return entryList


x = today - startdate
if x.days % repeat == 0:
	print(today.strftime("%d-%m-%Y") + ": YES")
else:
	print(today.strftime("%d-%m-%Y") + ": no")
today = today + datetime.timedelta(days=1)
"""

def fileExist(path) -> bool:
	if path.is_file():
		return True
	else:
		print("[bold yellow] file not found", path)
		return False

# Check entries with day cycle
def day_check(entry_date, repeat):
	x = today_date - entry_date
	if x.days % repeat == 0:
		return True
	else:
		return False

# Check entries with month cycle
def month_check(entry_date, repeat):
	x = today_date.month - entry_date.month
	if x % repeat == 0:
		if today_date.day == entry_date.day:
			return True
		else:
			return False
	else:
		return False

#@app.command("test")
def fetch_tasks():
	fetch_list = []
	f = open(paths.task_path,"r")
	lines = f.readlines()
	for i in range(len(lines)):
		task_data = lines[i].rstrip("\n").split("@")

		# get date
		task_date_list = [int(i) for i in task_data[1].split("-")]
		task_date_list.reverse()
		task_date = datetime.date(task_date_list[0],task_date_list[1],task_date_list[2])

		# get repeat
		repeat_type = str(task_data[2][-1])
		repeat_number = int(task_data[2][:-1])

		# check if not repeatable
		if repeat_number == 0:
			continue

		match repeat_type:
			case "d":
				if day_check(task_date, repeat_number) == True:
					fetch_list.append(i)
			case "m":
				if month_check(task_date, repeat_number) == True:
					fetch_list.append(i)
			case _:
				continue

	return fetch_list 
		# print(task_date.strftime("%d-%m-%Y"))


def fetch_entries():
	pass

def write_today():
	entries = []
	if fileExist(paths.task_path):
		entries = fetch_tasks()
	f = open(paths.today_path, "w")
	f.write(today_date.strftime("%d-%m-%Y")+"\n")
	for entry in entries:
		f.write(f"{entry}\n")
	f.close()

def is_completed(task_data):
	if task_data[-1] == today_date.strftime("%d-%m-%Y"):
		return True
	else:
		return False

def read_today(title:str="[bold yellow]What's for today?"):
	table = Table(title=title)
	table.add_column("",no_wrap=True)
	table.add_column("title")
	table.add_column("started")

	f_today = open(paths.today_path, "r")
	today_lines = f_today.readlines()
	f_task = open(paths.task_path, "r")
	task_lines = f_task.readlines()
	for i in range(len(today_lines)):
		if i == 0:
			continue
		entry = int(today_lines[i].rstrip("\n"))
		task_data = task_lines[entry].rstrip("\n").split("@")
		if is_completed(task_data):
			table.add_row(f"{i}.","\uf14a " + task_data[0], task_data[1], style="light_green")
		else:
			table.add_row(f"{i}.","\ue640 " + task_data[0], task_data[1])
		# print(f"{i}.",task_lines[entry].rstrip("\n"))
		
	f_today.close()
	f_task.close()
	console = Console()
	console.print(table)

# Function that invokes when no command is given
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
	if ctx.invoked_subcommand is None:
		#filereading.showEntries(str(datetime.date.today()))
		write_today()
		read_today()
		
@app.command("done")
@app.command("complete")
@app.command("c")
def complete_task(today_index: int):
	if today_index <= 0:
		print("[bold red]Invalid number")
		return

	# fetch todays lines
	f_today = open(paths.today_path, "r")
	today_lines = f_today.readlines()
	f_today.close()

	if today_index > len(today_lines):
		print("[bold red]Invalid number")
		return

	f_task = open(paths.task_path,"r")
	task_lines = f_task.readlines()
	f_task.close()

	task_index = int(today_lines[today_index])
	task_data = task_lines[task_index].rstrip("\n").split("@")
	task_data[-1] = today_date.strftime("%d-%m-%Y")
	task_lines[task_index] = f"{task_data[0]}@{task_data[1]}@{task_data[2]}@{task_data[3]}" + "\n"

	f_task = open(paths.task_path, "w")
	f_task.writelines(task_lines)
	f_task.close()
	read_today(f"[light_green]Completed: {task_data[0]}")


@app.command("undone")
@app.command("clear")
@app.command("uncheck")
@app.command("u")
def uncheck_task(today_index: int):
	if today_index <= 0:
		print("[bold red]Invalid number")
		return

	# fetch todays lines
	f_today = open(paths.today_path, "r")
	today_lines = f_today.readlines()
	f_today.close()

	if today_index > len(today_lines):
		print("[bold red]Invalid number")
		return

	f_task = open(paths.task_path,"r")
	task_lines = f_task.readlines()
	f_task.close()

	task_index = int(today_lines[today_index])
	task_data = task_lines[task_index].rstrip("\n").split("@")
	task_data[-1] = "not completed"
	task_lines[task_index] = f"{task_data[0]}@{task_data[1]}@{task_data[2]}@{task_data[3]}" + "\n"

	f_task = open(paths.task_path, "w")
	f_task.writelines(task_lines)
	f_task.close()
	read_today(f"[indian_red1]Unchecked: {task_data[0]}")

if __name__ == "__main__":
    app()
