import typer
import filereading 
import datetime

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
	if ctx.invoked_subcommand is None:
		filereading.showEntries(str(datetime.date.today()))

def ch(index: int):
	pass

if __name__ == "__main__":
    app()
