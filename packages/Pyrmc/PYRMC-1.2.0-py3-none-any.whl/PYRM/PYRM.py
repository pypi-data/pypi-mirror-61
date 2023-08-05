import os
import sys
import sqlite3
import getpass
import PYRM.logs as logs

class PYRM:
    #initialisation of the class
    def __init__(self, mode="debug", dump_path="cache"):
        try:
            os.mkdir(dump_path)
        except:
            pass
        self.sqldb=f'{dump_path}/info.db3'
        self.logger=logs.logger(mode=mode, path=dump_path)
        try:
            conn = sqlite3.connect(self.sqldb)
            c = conn.cursor()
            c.execute('CREATE TABLE info (pseudo text, info text)')
            conn.commit()
            conn.close()
        except:
            os.remove(self.sqldb)
            conn = sqlite3.connect(self.sqldb)
            c = conn.cursor()
            c.execute('CREATE TABLE info (pseudo text, info text)')
            conn.commit()
            conn.close()
        
        self.logger.write(0,"initialisation...")

        self.username = getpass.getuser()
        self.commands={

        }
        super().__init__()
        self.__last_func_exe=""
    def log(self,level:int, text:str):
        self.logger.write(level, text)
        
    def Print(self,what:str):
        print(f"{self.__last_func_exe}: {what}")
    #reset username to default value
    def reset_username(self):
        self.__username=getpass.getuser()
        self.logger.write(1,"username set to default: "+self.username)
        return self.__username
        
    #set username
    def set_username(self, new_username:str):
        self.username=new_username
        self.logger.write(1,"username have been set to: "+self.username)
        return self.__username
    #return username
    def return_username(self):
        return self.__username
    #return user input as if it was native to the "pyrm" program
    def get_user_input(self, what=""):
        if what=="":
            ans=input(f"{self.username}:>  ")
        else:
            ans=input(f"{what}\n{self.username}:>  ")
        return ans
    #return the path for the Database
    def get_DB_file_path(self):
        return self.sqldb
    #add function!
    def add_func(self,path_call, pseudo:str, info=""):
        self.commands[pseudo]= path_call
        conn = sqlite3.connect(self.sqldb)
        c = conn.cursor()
        c.execute(f"INSERT INTO info VALUES ('{pseudo}','{info}')")
        conn.commit()
        conn.close()
        self.logger.write(0, f"function: {pseudo} : {str(path_call)} with info: {info} has been added")
    #execute the fonction that was pass as parameter
    def __execute_func(self,pseudo, *args):
        aa=self.commands[pseudo]
        self.__last_func_exe=pseudo
        try:
            aa(*args)
        except Exception as e:
            self.logger.write(2,f"{pseudo} crash! with error: {e}")
            print(f"{pseudo} crash! with error: {e}")
        
    #print all info that you need for knowing what the func do!
    def __print_info(self):
        conn = sqlite3.connect(self.sqldb)
        c = conn.cursor()
        c.execute('SELECT * FROM info')
        c=c.fetchall()
        for i in c:
            print("command: \""+str(i[0])+"\"  |  info: "+str(i[1]))
        conn.commit()
        conn.close()
        
    #post init mean that the program will run on the framework
    def post_init(self):
        print("enter \"help;;\" to get help")
        print("enter \"exit;;\" to exit")
        self.logger.write(0,"commander start!")
        while True:
            try:
                
                command=input(f"{self.username}:>  ")
                if "exit;;" in command:
                    os.remove(self.sqldb)
                    exit()
                elif "help;;" in command:
                    self.__print_info()   
                else:
                    self.__execute_func(command)
                self.logger.write(0,f"{command}")
            except Exception as e:
                self.logger.write(1,f"{e}")
                print(f"command {e} do not exist!")
                pass






        



        
        
