import os
import sys
import sqlite3
import getpass
import PYRM.logs as logs
import shutil
import subprocess
import platform
import time
class PYRM:
    #initialisation of the class
    def __init__(self, mode="debug", dump_path="cache", arg_spliter=','):
        self.arg_spliter=arg_spliter
        self.mode=mode
        self.basec="""
        enter \"help;;\" to get help
        enter \"help;+function_name\" to get info about a specifical function
        enter \"exit;;\" to exit
        enter \"cls;;\" or \"clear;;\" to clear the terminal
        """
        try:
            os.mkdir(dump_path)
        except:
            pass
        self.cache=dump_path
        self.__sqldb=f'{dump_path}/info.db3'
        self.logger=logs.logger(mode=mode, path=dump_path)
        try:
            conn = sqlite3.connect(self.__sqldb)
            c = conn.cursor()
            c.execute('CREATE TABLE info (pseudo text, info text)')
            conn.commit()
            conn.close()
        except:
            os.remove(self.__sqldb)
            conn = sqlite3.connect(self.__sqldb)
            c = conn.cursor()
            c.execute('CREATE TABLE info (pseudo text, info text)')
            conn.commit()
            conn.close()
        
        self.logger.write(0,"initialisation...")

        self.username = getpass.getuser()
        self.commands={

        }
        super().__init__()
        self.__last_func_exe="System"
    def clear(self):
        subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)
        time.sleep(0.01)
    def get_last_func(self):
        return self.__last_func_exe
    def log(self,level:int, text:str):
        self.logger.write(level, text)
        
    def Print(self,*args):
        ans=""
        for a in args:
            ans+=str(a)
        print(f"{self.__last_func_exe}: "+ans)
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
    def get_user_input(self, *args):
        ask=""
        for a in args:
            ask+=str(a)
        ans=input(f"{ask}\n{self.username}?:>  ")
        return ans
    #return the path for the Database
    def get_DB_file_path(self):
        return self.__sqldb
    #add function!
    def add_func(self,path_call, pseudo:str, info:str):
        self.commands[pseudo]= path_call
        conn = sqlite3.connect(self.__sqldb)
        c = conn.cursor()
        c.execute(f"INSERT INTO info VALUES ('{pseudo}','{info}')")
        conn.commit()
        conn.close()
        self.logger.write(0, f"function: {pseudo} : {str(path_call)} with info: {info} has been added")
    #execute the fonction that was pass as parameter
    def __execute_func(self,pseudo, *args):
        aa=self.commands[pseudo]
        self.__last_func_exe=pseudo
        if self.mode=="debug":
            for i in args:
                print(i)
        try:
            aa(tuple(*args))
        except Exception as e:
            self.logger.write(2,f"{pseudo} crash! with error: {e}")
            if self.mode!="debug":
             print(f"{pseudo} crash! with error: {e}")
    def read_log(self, force:int):
        self.logger.write(6,"test")
        print(self.logger.read(force))
    #print all info that you need for knowing what the func do!
    def __print_info(self):
        conn = sqlite3.connect(self.__sqldb)
        c = conn.cursor()
        c.execute('SELECT * FROM info')
        c=c.fetchall()
        for i in c:
            print("command: \""+str(i[0])+"\"  |  info: "+str(i[1]))
        conn.commit()
        conn.close()
    def __print_info_for_a_func(self, co):
        conn = sqlite3.connect(self.__sqldb)
        c = conn.cursor()
        c.execute(f'SELECT * FROM info where pseudo=\"{co}\"')
        c=c.fetchall()
        for i in c:
            print("command: \""+str(i[0])+"\"  |  info: "+str(i[1]))
        conn.commit()
        conn.close()
    #post init mean that the program will run on the framework
    def post_init(self):
        print(self.basec)
        self.logger.write(0,"commander start!")
        while True:
            try:
                command=input(f"{self.username}:>  ")
                command=command.lower()
                if "exit;;" in command:
                    os.remove(self.__sqldb)
                    exit()
                elif "help;;" in command:
                    self.__print_info()
                elif "cls;;" in command or "clear;;" in command:
                    self.clear()
                    
                elif "help;" in command:
                    an=""
                    aa=command.split(" ")
                    for i in aa:
                        if i=="help;":
                            continue
                        else:
                            an+=i
                    self.__print_info_for_a_func(an)
                elif "readlog;" in command:
                    raa=command.split(' ')
                    ab=str(raa[-1])
                    self.read_log(int(ab))
                elif "readlogup," in command:
                    raa=command.split(' ')
                    ab=str(raa[-1])
                    self.read_log(int(ab))
            

                else:
                    try:
                        raa=command.split(' ')
                        aa=command.replace(raa[0], "")
                        ab=""
                        for i in aa:
                            ab+=i

                        ab=ab[1:]
                        ab=ab.split(",")

                        self.__execute_func(str(raa[0]), ab[0:])
                    except:
                        raa=command
                        self.__execute_func(raa)
                    
                self.logger.write(0,f"{command}")
            except Exception as e:
                self.logger.write(1,f"{e}")
                print(f"command {e} do not exist!")
                pass