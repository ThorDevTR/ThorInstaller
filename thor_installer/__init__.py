# Naber kodları karıştıran meraklı.

from rich.console import Console
from rich.panel import Panel
from rich.live_render import LiveRender
import sys, os, shutil
from pyrogram import __version__
console = Console()

# Birkaç kısaltma.

def hata(text):
   console.print(text, style="bold red")
def bilgi(text):
   console.print(text, style="blue")
def basarili(text):
   console.print(f"[bold green]{text}[/]")
def onemli(text):
   console.print(text, style="bold cyan")
def soru(soru):
   return console.input(f"[bold yellow]{soru}[/]")
def logo():
   surum = str(sys.version_info[0]) + "." + str(sys.version_info[1])
   console.print(Panel(f"[bold blue]@ThorUserBot Installer :hammer:[/]\n\nPython: [i]{surum}[/]\nPyrogram: [i]{__version__}[/]"), justify="center")
def tamamlandi(saniye):
   console.print(Panel(f"[bold green]Kurulum Tamamlandı!\n[i]Botu {round(saniye)} saniye içinde kurdunuz.[/]\n\n[bold green]Birkaç dakika sonra herhangi bir sohbette .alive yazarak test edebilirsiniz. \nKeyifli kullanımlar dileriz :)[/]"), justify="center")                  
def del_it(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)
    else:
        shutil.rmtree(path)
