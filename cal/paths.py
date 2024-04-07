from pathlib import Path

import sys, os

application_path = ""

if getattr(sys, 'frozen', False):
	application_path = os.path.dirname(sys.executable)
else:
	application_path = "."

# path for all entries
task_path: Path = Path(application_path + "/appdata/tasks.txt")
entry_path: Path = Path(application_path + "/appdata/entries.txt")

# temp paths
today_path: Path = Path(application_path + "/appdata/today.txt")
