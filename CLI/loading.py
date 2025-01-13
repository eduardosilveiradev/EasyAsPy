# from easyaspy import rprint
class Loading:

    def __init__(self, name: str, unit: str, maxtime: float) -> None:
        self.name = name
        self.unit = unit
        self.maxtime = maxtime

    def render(self, time: int) -> str:
        """
        Render the loader

        Args:
            time (int): 0 - 100

        Returns:
            str: Print the return

        Usage:
            print(myLoader.render(0))
        """
        from colorama import Fore, init

        init()
        filler = "━"
        colorfiller = "-"
        time = time + 1
        timedisp = ((time) / 100) * self.maxtime
        # str(filler * round((time * 3)/(self.maxtime / 2))) + "".center(120 - round((time * 3)/(self.maxtime / 2)))
        built = (
            Fore.WHITE
            + self.name
            + " | "
            + Fore.BLUE
            + "".center(time, filler)
            + Fore.LIGHTBLACK_EX
            + "".center(100 - time, colorfiller)
            + Fore.WHITE
            + " |       "
            + Fore.GREEN
            + f"{timedisp:0.2f}"
            + "/"
            + f"{self.maxtime:0.2f}"
            + " "
            + self.unit
        )
        return built

    def prender(self, time: int) -> None:
        """Print a rendered loader

        Args:
            time (int): 0 - 100
        """
        import shutil

        columns = shutil.get_terminal_size().columns
        print("".center(columns), end="\r", flush=True)
        print(self.render(time), end="\r", flush=True)


if __name__ == "__main__":
    import time, shutil

    columns = shutil.get_terminal_size().columns
    print("TESTING LOADING")
    testLoader = Loading("Testing", "mB", 5.0)
    for i in range(100):
        time.sleep(0.02)
        testLoader.prender(i)
    print()
