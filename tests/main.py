from pathlib import Path
import datetime
import typer

import today

import filereading

"""

main today ch 1 -> complete todays 1. task

main task a <title> <date> --tf <timeframe> --r <cycle> -> add new task
main entry a <title> <date> --tf <timeframe> --r <cycle> -> add new entry

main today -> return all entries for today
main -> return all entries for today
main -1 -> return all entries for yesterday

"""

app = typer.Typer()
app.add_typer(today.app, name="today")


# entryList = []

tasks = Path("./tasks.txt")

@app.command()
def a(title: str, due: str = str(datetime.date.today())):
	if not filereading.fileExist():
		return
	f = open(tasks, "a")
	#title = input("title: ")
	#due = input("date(YYYY-MM-DD)(leave blank for today)\n: ")
	#if due == "":
	#	due = str(datetime.date.today())
	f.write(title + "@" + due + "@0" +"\n")
	f.close()

# Function to complete task
@app.command()
def d(r: str = ""):
#	if not fileExist():
#		return
#	f = open(tasks, "r")
#	data = f.readlines
	if r != "":
		print(r)
	else:
		print("default")
	

def deleteEntry():
	pass

# @app.command()
# def today():
# 	showEntries(str(datetime.date.today()))

@app.command()
def all():
	entryList = filereading.getAllEntries()

	# Print result
	for i in range(len(entryList)):
		print(f"{str(i + 1)}. {entryList[i].date}: {entryList[i].title}")




if __name__ == "__main__":
    app()

#print(type(datetime.date.today()))
