'''
A simple logging library.
Made with python on 11/21/21
'''
import pylogger.operators as op
def init(lf: str, prcsname: str) -> None:
    """Add global variables

    Args:
        lf (str): _description_
        prcsname (str): _description_
        overflowlines (int): _description_
    """
    import os
    import inspect
    cls = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    global logfile
    global processname
    global rtrns
    rtrns = []
    processname = prcsname
    logfile = lf
    global filename
    if __name__ != '__main__':
        for frame in inspect.stack()[1:]:
            if frame.filename[0] != '<':
                path = frame.filename
                break
    filename = path.rsplit("\\")
    filename = filename[len(filename)-1]

def logdec(func) -> None:
    '''
    Decorator that logs function name and return
    '''
    from functools import wraps
    @wraps(func)
    def wrapperl(*args, **kwargs):
        lastprcsname = processname
        init(logfile, f"{processname} | {func.__name__}")
        log(f"Executing function '{func.__name__}'")
        func(*args, **kwargs)
        rtrn = func(*args, **kwargs)
        log(f"Function completed with return '{rtrn}'")
        init(logfile, lastprcsname)
        return rtrn
    return wrapperl

def log(*_log: object) -> None:
    __log = ""
    for i in _log:
        __log += i
    __log = __log.replace("\n", "")
    if ':' in logfile:
        # import time
        from time import strftime
        # create time string
        logtime = strftime("[%I:%M:%S %p %B %d %Y %A]")
        # open file for log
        with open(logfile, "a") as logging:
            # write log with formatting
           logging.write(f"{logtime} | {__log}                  {filename} | {processname}\n")

def clear(ask: bool, logornot: bool | None = False, log__ = "") -> None:
    """Clear the log file

    Args:
        ask (bool): Ask for user confirmation.
        log__ (str, optional): What to log after clearing.
        logornot (bool, optional): Log clear or not.
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
            with open(logfile, "w") as logging:
                logtime = strftime("[%Y %A %B %d %I:%M:%S %p]")
                # write reason
                if "Y" in logornot or "y" in logornot:
                    logging.write(f"File cleared at {logtime} with clear reason: {log__}\n")
                else:
                    logging.write("")
                    os.system("cls")
                    print("Cleared.")
                    time.sleep(2.5)
                    os.system("cls")
        else:
            # did not clear
            os.system("cls")
            with open(logfile, "a") as logging:
                log("Did not clear")
                print("Did not clear.")
                exit()
    else:
        # open file for clear
        with open(logfile, "w") as logging:
            # write reason
            logging.write(f"")

def seperate(amount="Amount of seperations") -> None:
    'Adds newlines to inputted file.'
    # open file for seperation
    with open(logfile, "a") as logging:
        # get amount of seperations
        a=amount
        # for loop through seperations
        for i in range(a):
            logging.write("\n")

def clearlastline() -> None:
        'Clears last line of log file.'
        # list to store file lines
        lines = []
        # read file
        with open(logfile, 'r') as fp:
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
