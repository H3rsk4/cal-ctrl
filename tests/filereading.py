from pathlib import Path
from entry import Entry

tasks = Path("./tasks.txt")

def fileExist() -> bool:
	if tasks.is_file():
		return True
	else:
		print("task file not found")
		return False

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


def showEntries(date):
	currentList = []
	entryList = getAllEntries()
	for e in entryList:
		if(e.date == date):
			currentList.append(e)
	if len(currentList) > 0:
		print("found", len(currentList), "entries for", str(date))
		for i in range(len(currentList)):
			print(str(i + 1) + ". " + currentList[i].title)
	else:
		print("no entries found")
