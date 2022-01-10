from datetime import datetime
from datetime import date

class Logger():

    @property
    def logFile(self):
        return self.__logFile
    
    @logFile.setter
    def logFile(self,file):
        self.__logFile=file

    def __init__(self):
        self.__createLogFile()
        self.write("Inicio do log")
    
    def __del__(self):
        self.write("Execução finalizada normalmente")
        self.logFile.close()

    def error(self):
        self.write("Execução finalizada com erro")
        self.logFile.close()

    def write(self,message):
        self.logfile.write(self.__getTimeNow()+": "+message+"\n")

    def __createLogFile(self):
        self.logfile=open("log"+self.__currentDate(),"a")

    def __getTimeNow(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def __currentDate(self):
        today = date.today()
        return today.strftime("%b-%d-%Y")