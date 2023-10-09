import datetime

now = datetime.datetime.now()


def log(date, time, temp, ph, salinity):
    data = f"{date}x{time}x{temp}x{ph}x{salinity}"

    try:
        with open("log.txt", 'a') as logFile:
            logFile.write(data + "\n")
    except IOError:
        with open("log.txt", "w") as logFile:
            logFile.write("LOG\n")
            logFile.write(data + "\n")


def fetch():
    with open("log.txt", "r") as logFile:
        readlines = logFile.read().splitlines()
        log1 = readlines[-1].split('x')
        log2 = readlines[-2].split('x')
        log3 = readlines[-3].split('x')
        log4 = readlines[-4].split('x')
        log5 = readlines[-5].split('x')

        log = [log1, log2, log3, log4, log5]

        return log


def fetchAll():
    logFull = []

    with open("log.txt", "r") as logFile:
        readlines = logFile.read().splitlines()
        for line in readlines:
            parts = line.split('x')
            logFull.append(parts)

    return logFull


def get():
    temp = 28
    ph = 7.1
    salinity = 1234

    data = [temp, ph, salinity]

    log(now.date(), now.time(), temp, ph, salinity)

    return data
