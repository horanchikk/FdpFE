import json, urllib.request, logging, os, zipfile
from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table

def clear():
    print('\n' * 100)

console = Console()
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
console.print('[bold blue] Welcome [bold red] to [bold green] FDPDownloader[bold white]!\n')
log.info('Requesting to github...')
data = json.loads(urllib.request.urlopen('https://api.github.com/repos/UnlegitMC/FDPClient/actions/runs').read().decode())
clear()
table = Table(show_footer=False, title=f'[bold]Total builds -> [bold red]{data["total_count"]}')
table.add_column("ID", width=35)
table.add_column("Message", width=50)
table.add_column("Author", width=15)
for i in range(len(data['workflow_runs'])):
    if data['workflow_runs'][i]['conclusion'] == 'success' and data['workflow_runs'][i]['head_branch'] == 'main' and data['workflow_runs'][i]['name'] == 'build' and data['workflow_runs'][i]['head_commit']['author']['name'] != 'dependabot[bot]':
        table.add_row(str(data['workflow_runs'][i]['id']), str(data['workflow_runs'][i]['head_commit']['message']), str(data['workflow_runs'][i]['actor']['login']))
console.print(table)


try:
    id = input('\nEnter ID: ')
    print('\n')
    with console.status(f'Downloading https://nightly.link/UnlegitMC/FDPClient/actions/runs/{id}/FDPClient.zip', spinner="line"):
        urllib.request.urlretrieve(f'https://nightly.link/UnlegitMC/FDPClient/actions/runs/{id}/FDPClient.zip', f'FDPClient-{id}.zip')
        with zipfile.ZipFile(f'FDPClient-{id}.zip',"r") as zip_ref:
            zip_ref.extractall(".")
            os.remove(f'FDPClient-{id}.zip')
    clear()
    console.print(f'[bold green] FDPClient (Build: {id}) has been downloaded. Thanks for using!')
except KeyboardInterrupt:
    clear()
    try:
        os.remove(f'FDPClient-{id}.zip')
    except:
        pass
    console.print('[bold red] Downloading has been stopped.')
except Exception as e:
    clear()
    try:
        os.remove(f'FDPClient-{id}.zip')
    except:
        pass
    console.print(f'[bold red] {e}. Try again later.')