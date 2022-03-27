import json, urllib.request, os, zipfile, sys, time
from rich.console import Console
from rich.table import Table

def clear():
    print('\n' * 100)

console = Console()
try:
    args = sys.argv[1]
except:
    args = None

def main():
    console.print('[bold blue] Welcome [bold red] to [bold green] FDPFE[bold white]!\n')
    with console.status('  Requesting to github...', spinner="line"):
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
        with console.status(f'  Downloading https://nightly.link/UnlegitMC/FDPClient/actions/runs/{id}/FDPClient.zip', spinner="line"):
                urllib.request.urlretrieve(f'https://nightly.link/UnlegitMC/FDPClient/actions/runs/{id}/FDPClient.zip', f'FDPClient-{id}.zip')
        with console.status(f'  Unpacking FDPClient-{id}.zip', spinner="line"):
            with zipfile.ZipFile(f'FDPClient-{id}.zip',"r") as zip_ref:
                zip_ref.extractall(".")
                time.sleep(1)
                os.remove(f'FDPClient-{id}.zip')
        console.print(f'[bold green] FDPClient (Build: {id}) has been downloaded. Thanks for using!')
    except KeyboardInterrupt:
        clear()
        try:
            os.remove(f'FDPClient-{id}.zip')
        except:
            pass
        console.print('[bold red] Downloading has been stopped.')
    except PermissionError:
            with console.status(f'  Deleting FDPClient-{id}.zip', spinner="line"):
                time.sleep(1)
                os.remove(f'FDPClient-{id}.zip')
            console.print(f'[bold green] FDPClient (Build: {id}) has been downloaded. Thanks for using!')
    except Exception as e:
        clear()
        try:
            os.remove(f'FDPClient-{id}.zip')
        except:
            pass
        console.print(f'[bold red] {e}. Try again later.')

def latest():
    console.print('[bold blue] Welcome [bold red] to [bold green] FDPFE[bold white]!\n')
    with console.status('  Requesting to github...', spinner="line"):
        data = json.loads(urllib.request.urlopen('https://api.github.com/repos/UnlegitMC/FDPClient/actions/runs').read().decode())
    for i in range(len(data['workflow_runs'])):
        if data['workflow_runs'][i]['conclusion'] == 'success' and data['workflow_runs'][i]['head_branch'] == 'main' and data['workflow_runs'][i]['name'] == 'build' and data['workflow_runs'][i]['head_commit']['author']['name'] != 'dependabot[bot]':
            id = str(data['workflow_runs'][i]['id'])
            console.print(f"""[bold white] Finded build: [bold green]{id}\n[bold white]Message build: {str(data['workflow_runs'][i]['head_commit']['message'])}\nAuthor: {data['workflow_runs'][i]['head_commit']['author']['name']}\n""")
        try:
            with console.status(f'  Downloading https://nightly.link/UnlegitMC/FDPClient/actions/runs/{id}/FDPClient.zip', spinner="line"):
                urllib.request.urlretrieve(f'https://nightly.link/UnlegitMC/FDPClient/actions/runs/{id}/FDPClient.zip', f'FDPClient-{id}.zip')
            with console.status(f'  Unpacking FDPClient-{id}.zip', spinner="line"):
                with zipfile.ZipFile(f'FDPClient-{id}.zip',"r") as zip_ref:
                    zip_ref.extractall(".")
                    time.sleep(1)
                    os.remove(f'FDPClient-{id}.zip')
            console.print(f'[bold green] FDPClient (Build: {id}) has been downloaded. Thanks for using!')
            sys.exit(0)
        except KeyboardInterrupt:
            try:
                os.remove(f'FDPClient-{id}.zip')
            except:
                pass
            console.print('[bold red] Downloading has been stopped.')
            sys.exit(0)
        except PermissionError:
            with console.status(f'  Deleting FDPClient-{id}.zip', spinner="line"):
                time.sleep(1)
                os.remove(f'FDPClient-{id}.zip')
            console.print(f'[bold green] FDPClient (Build: {id}) has been downloaded. Thanks for using!')
            sys.exit(0)
        except Exception as e:
            try:
                os.remove(f'FDPClient-{id}.zip')
            except:
                pass
            console.print(f'[bold red] {e}. Try again later.')

if __name__ == '__main__':
    if args == 'latest':
        latest()
    else:
        main()