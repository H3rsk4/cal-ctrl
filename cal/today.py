from typing import Annotated
import typer
import datetime
from pathlib import Path

from rich import print
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

@app.command("test")
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
		if repeat_number == 0:
			continue
		match repeat_type:
			case "d":
				x = today_date - task_date
				if x.days % repeat_number == 0:
					fetch_list.append(i)
			case "m":
				pass
			case _:
				continue

	return fetch_list 
		# print(task_date.strftime("%d-%m-%Y"))


def show_tasks():
	pass

def fetch_entries():
	pass

def fetch():
	entries = []
	if fileExist(paths.task_path):
		entries = fetch_tasks()
	f = open(paths.today_path, "a")
	for entry in entries:
		f.write(f"{entry}\n")
	f.close()

def read_today():
	f_today = open(paths.today_path, "r")
	f_task = open(paths.task_path, "r")
	task_lines = f_task.readlines()
	for entry in f_today:
		entry = int(entry.rstrip("\n"))
		print(task_lines[entry].rstrip("\n"))
	f_today.close()
	f_task.close()

# Function that invokes when no command is given
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
	if ctx.invoked_subcommand is None:
		#filereading.showEntries(str(datetime.date.today()))
		fetch()
		read_today()
		
@app.command("done")
@app.command("complete")
@app.command("c")
def complete_task(index: int):
	pass

if __name__ == "__main__":
    app()
