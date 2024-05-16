import colorama
from sys import stderr

# available text colors
class text:
    def __init__(self):
        self.red = colorama.Fore.RED
        self.cyan = colorama.Fore.CYAN
        self.blue = colorama.Fore.BLUE
        self.green = colorama.Fore.GREEN
        self.white = colorama.Fore.WHITE
        self.black= colorama.Fore.BLACK
        self.yellow = colorama.Fore.YELLOW
        self.magenta = colorama.Fore.MAGENTA
        self.RESET = colorama.Fore.RESET

# available background colors
class background:
    def __init__(self):
        self.red = colorama.Back.RED
        self.blue = colorama.Back.BLUE
        self.cyan = colorama.Back.CYAN
        self.green = colorama.Back.GREEN
        self.white = colorama.Back.WHITE
        self.black = colorama.Back.BLACK
        self.yellow = colorama.Back.YELLOW
        self.magenta = colorama.Back.MAGENTA
        self.reset = colorama.Back.RESET

# class that abstracts all colorama syntax to functions
class log():
    def __init__(self):
        self.text = text()
        self.background = background()
        self.reset = colorama.Style.RESET_ALL

    def error(self, msg):
        print(self.text.white + self.background.red + "[!] " + msg + " " + self.reset, file=stderr)

    def alert(self, msg):
        print(self.text.yellow + self.background.blue + "[~] " + msg + " " + self.reset)

    def comment(self, msg):
        print(colorama.Style.DIM + msg + self.reset, end="")

    def acknowledge(self, msg):
        print(self.text.green + self.background.black + "[✓] " + msg + " " + self.reset)

    def highlight(self, msg):
        print(self.text.black + self.background.white + msg + self.reset, end="")
# driver program for testing
if __name__ == "__main__":
    log = log()
    print("This module is written by Ahmed Mamdouh (DeaDude)")
    log.highlight("[LinkedIn]")
    log.comment("  https://www.linkedin.com/in/ahmed-mamdouh-b563081b6/)\n")
    log.highlight("[GitHub]")
    log.comment("    https://github.com/DeadDude-glitch/)\n")
    print()
    print("ERROR MESSAGE: " , end='\t')
    log.error("error")

    print("NOTICE MESSAGE: " , end='')
    log.alert("notice")

    print("ACK MESSAGE: " , end='\t')
    log.acknowledge("acknowledgement")
