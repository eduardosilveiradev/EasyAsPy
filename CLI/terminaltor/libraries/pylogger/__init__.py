'''
A simple logging library.
Made with python on 11/21/21
'''
import pylogger.operators as op
import traceback
import sys
from io import StringIO
from colorama import Fore, init
init(autoreset=True)

class Logger():
    def __init__(self, lf: str, prcsname: str) -> None:
        """
        Creates global variables for your logger

        Args:
            lf (str): Log file for logger
            prcsname (str): Process name for logger
        """
        import os
        import inspect
        cls = lambda: os.system('cls' if os.name == 'nt' else 'clear')
        self.rtrns = []
        self.processname = prcsname
        self.logfile = lf
        if __name__ != '__main__':
            for frame in inspect.stack()[1:]:
                if frame.filename[0] != '<':
                    path = frame.filename
                    break
        self.filename = path.rsplit("\\")
        self.filename = self.filename[len(self.filename)-1]

    def logdec(self, func) -> str:
        """
        Decorator for logging output of functions

        Args:
            func (function): Function for logging

        Returns:
            str: Output of `func`
        """
        from functools import wraps
        @wraps(func)
        def wrapperl(*args, **kwargs):
            self.log(f"Executing function '{func.__name__}'")
            try:
                rtrn = func(*args, **kwargs)
                self.log(f"Function completed with return '{rtrn}'")
                return rtrn
            except Exception as e:
                error_type = type(e).__name__
                error_message = str(e)
                tb_str = ''.join(traceback.format_exception(e))
                self.log(f"Error\n\n--- START ERROR BLOCK ---\n\nFunction `{func.__name__}` errored \n\n{error_type}: {error_message}\n\n{tb_str}\n\n--- END ERROR BLOCK ---\n")
                print(f"{Fore.RED}Error: \n")
                print(f"{Fore.GREEN}Type: {Fore.RED}{error_type}")
                print(f"{Fore.GREEN}Message: {Fore.RED}{error_message}\n")
                print(f"{Fore.GREEN}Traceback: \n" + Fore.RED + tb_str.replace(f"{error_type}: {error_message}", "\r"))
                exit()
        return wrapperl

    def log(self, *_log: object) -> None:
        '''
        Function for logging.                                

        Usage(example):                                
        log("Example log")
        Uses predetermined time code.
        Example of time code: [07:23:22 PM January 09      2024 Tuesday]
        '''
        __log = ""
        for i in _log:
            __log += i
        if ':' in self.logfile:
            # import time
            from time import strftime
            # create time string
            logtime = strftime("[%I:%M:%S %p %B %d      %Y %A]")
            # open file for log
            with open(self.logfile, "a") as logging:
                # write log with formatting
                logging.write(f"From '{self.filename} | {self.processname}' at {logtime}               {__log}\n")
        else:
            import os
            os.system("cls")
            print("ERROR CODE: 543. Warning log file will not enter the desired directory as you did not include the full file path inside of 'LOGFILE'")
            exit()

    def clear(self, log: str, logornot: bool | None=True, ask: bool | None=True) -> None:
        """Clears logfile

        Args:
            log (str, optional): _description_..
            logornot (bool): Log or not. Defaults to True
            ask (bool): Ask for user input. Defaults to True.
        """
        from time import strftime
        logtime = strftime("[%Y %A %B %d %I:%M:%S %p]")
        # neccesary librarys
        import os
        from time import strftime
        import time
        if ask == True:
            # ask for clear
            os.system("cls")
            yesorno = input(f"Do you really want to clear the log file({logfile})?: ")
            if yesorno == "Y" or yesorno == "y":
                # open file for clear
                with open(self.logfile, "w") as logging:
                    logtime = strftime("[%Y %A %B %d %I:%M:%S %p]")
                    # write reason
                    if "Y" in logornot or "y" in logornot:
                        logging.write(f"File cleared manually at {logtime} with clear reason: {log}\n")
                    else:
                        logging.write("")
                        os.system("cls")
                        print("Cleared.")
                        time.sleep(2.5)
                        os.system("cls")
            else:
                # did not clear
                os.system("cls")
                with open(self.logfile, "a") as logging:
                    logging.write(f"[Clear] {logtime}               Did not clear.\n")
                    print("Did not clear.")
                    exit()
        else:
            # open file for clear
            with open(self.logfile, "w") as logging:
                # write reason
                logging.write(f"")

    def seperate(self, amount: "Amount of seperations") -> None:
        'Adds newlines to inputted file. Example: seperate(LOGFILE="C:/example/example.log", amount=5)'
        # open file for seperation
        with open(self.logfile, "a") as logging:
            # get amount of seperations
            a=amount
            # for loop through seperations
            for i in range(a):
                logging.write("\n")

    def clearlastline(self) -> None:
            'Clears last line of inputted file. Example: clearlastline()'
            # list to store file lines
            lines = []
            # read file
            with open(self.logfile, 'r') as fp:
                # read an store all lines into list
                lines = fp.readlines()
                  # Write file
                with open(logfile, 'w') as fp:
                    # iterate each line
                    for number, line in enumerate(lines):
                        # note list index starts from 0
                        length=len(lines)
                        if number not in [length-1]:
                            fp.write(line)