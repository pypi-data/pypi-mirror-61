import getpass
import os
import platform
if platform.system()!="windows":
    import readline
import shutil
import sqlite3
import subprocess
import sys
import time

import PYRM.logs as logs

false = False
true = True


class PYRM:
    # initialisation of the class
    def __init__(self, mode="debug", dump_path="cache", arg_spliter=',', can_exe_func_with_sysargv=False, can_exe_os_command=True, use_base_command=True):
        self.__ceos = can_exe_os_command
        self.__ubc = use_base_command
        self.__cefws = can_exe_func_with_sysargv
        self.arg_spliter = arg_spliter
        self.mode = mode
        try:
            os.mkdir(dump_path)
        except:
            pass
        self.cache = dump_path
        self.__sqldb = f'{dump_path}/info.db3'
        self.logger = logs.logger(mode=mode, path=dump_path)
        try:
            conn = sqlite3.connect(self.__sqldb)
            c = conn.cursor()
            c.execute(
                'CREATE TABLE info (pseudo text, info text, have_arg INTEGER)')
            conn.commit()
            conn.close()
        except:
            os.remove(self.__sqldb)
            conn = sqlite3.connect(self.__sqldb)
            c = conn.cursor()
            c.execute(
                'CREATE TABLE info (pseudo text, info text, have_arg INTEGER)')
            conn.commit()
            conn.close()

        self.logger.write(0, "initialisation...")

        self.username = getpass.getuser()
        self.commands = {

        }
        self.__last_func_exe = "System"
        if self.__ubc:
            self.add_func(self.__help, "helping",
                          "helping command", take_arg=false)
            self.add_func(self.__cls, "cls",
                          "clear screen like \"clear;;\"", take_arg=false)
            self.add_func(self.__cls, "clear",
                          "clear screen like \"cls;;\"", take_arg=false)
            self.add_func(self.__help1, "help",
                          "helping command for a specific func", take_arg=true)
            self.add_func(self.__read_log, "readlog",
                          "readlog with a specific number", take_arg=true)
            self.add_func(self.__read_log_up, "readlogup",
                          "readlog with a specific number and up", take_arg=true)
    # clear the terminal

    def clear(self):
        subprocess.Popen("cls" if platform.system() ==
                         "Windows" else "clear", shell=True)
        time.sleep(0.01)
    # get the last function executed (your fonction that actualy run)

    def get_last_func(self):
        return self.__last_func_exe
    # to log something!

    def log(self, level: int, text: str):
        self.logger.write(level, text)
    # get args that you want

    def get_sys_argv(self, number: int):
        return sys.argv[number]
    # print function to make your app more "native" to mine

    def Print(self, *args):
        ans = ""
        for a in args:
            ans += str(a)
        print(f"{self.__last_func_exe}: "+ans)
    # reset username to default value

    def reset_username(self):
        self.__username = getpass.getuser()
        self.logger.write(1, "username set to default: "+self.username)
        return self.__username

    # set username
    def set_username(self, new_username: str):
        self.username = new_username
        self.logger.write(1, "username have been set to: "+self.username)
        return self.__username
    # return username

    def return_username(self):
        return self.__username
    # return user input as if it was native to the "pyrm" program

    def get_user_input(self, *args):
        ask = ""
        for a in args:
            ask += str(a)
        ans = input(f"{ask}\n{self.username}?:>  ")
        return ans
    # return the path for the Database

    def get_DB_file_path(self):
        return self.__sqldb
    # add function!

    def add_func(self, path_call, pseudo: str, info: str, take_arg: bool):
        self.commands[pseudo] = path_call
        conn = sqlite3.connect(self.__sqldb)
        c = conn.cursor()
        if take_arg == False:
            take_ar = '0'
        elif take_arg == True:
            take_ar = '1'
        c.execute(
            f"INSERT INTO info VALUES ('{pseudo.lower()}','{info}','{take_ar}')")
        conn.commit()
        conn.close()
        self.logger.write(
            0, f"function: {pseudo} : {str(path_call)} with info: {info} has been added")
    # execute the fonction that was pass as parameter

    def __execute_func(self, pseudo, *args):
        aa = self.commands[pseudo]
        self.__last_func_exe = pseudo
        conn = sqlite3.connect(self.__sqldb)
        c = conn.cursor()
        c.execute(f'SELECT * FROM info where pseudo=\'{pseudo}\'')
        c = c.fetchall()
        try:
            for i in c:
                if i[2] == 0:
                    aa()
                elif i[2] == 1:
                    aa(tuple(*args))
            if self.mode == "debug":
                for i in args:
                    print(i)

        except Exception as e:
            self.logger.write(2, f"{pseudo} crash! with error: {e}")
            if self.mode != "debug":
                print(f"{pseudo} crash! with error: {e}")
    # read log with a specific level

    def read_log(self, force: int):
        print(self.logger.read(force))
    # read log with the specific level and up

    def read_log_up(self, force: int):
        print(self.logger.read_up(force))
    # that make you ablr to get user input whitout showing the content

    def get_user_input_password(self, *args):
        passe = ""
        for i in args:
            passe += str(i)

        ans = str(getpass.getpass(f"{passe}\n{self.username}?:>  "))
        return ans
    # print all info that you need for knowing what the func do!

    def __print_info(self):
        conn = sqlite3.connect(self.__sqldb)
        c = conn.cursor()
        c.execute('SELECT * FROM info')
        c = c.fetchall()
        for i in c:
            if i[2] == 0:
                nei = "False"
            elif i[2] == 1:
                nei = "True"
            print("command: \""+str(i[0])+"\"  |  info: " +
                  str(i[1]+"  |  take args?: "+str(nei)))
        conn.commit()
        conn.close()
    # print all the information that you need to know on a func

    def __print_info_for_a_func(self, co):
        conn = sqlite3.connect(self.__sqldb)
        c = conn.cursor()
        c.execute(f'SELECT * FROM info where pseudo=\"{co}\"')
        c = c.fetchall()
        for i in c:
            if i[2] == 0:
                nei = "False"
            elif i[2] == 1:
                nei = "True"
            print("command: \""+str(i[0])+"\"  |  info: " +
                  str(i[1]+"  |  take args?: "+str(nei)))
        conn.commit()
        conn.close()
    # helping command

    def __help(self):
        self.__print_info()
    # another one for specific command

    def __help1(self, *args):
        an = ""
        for i in args:
            if i == "help;":
                continue
            else:
                an += str(i[0])
        self.__print_info_for_a_func(an)
    # clear screen

    def __cls(self):
        self.clear()
    # that make you able to read logs

    def __read_log(self, *args):
        try:
            an = ""
            for i in args:
                an += str(i[0])
            self.read_log(int(an))
        except:
            print("please enter a number!")
    # this also make you able to read log but with a number and up

    def __read_log_up(self, *args):
        try:
            an = ""
            for i in args:
                an += str(i[0])
            self.read_log_up(int(an))
        except:
            print("please enter a number!")
    # that is the func to call when your program as add all is function

    def post_init(self):
        self.logger.write(0, "commander start!")

        if self.__cefws == True:
            cbe = True
            try:
                self.commands[sys.argv[1]]
            except:
                cbe = False
            if cbe == True:
                argstp = []
                ccpc = 2
                while True:
                    try:
                        nte = sys.argv[ccpc]
                        ccpc += 1
                    except:
                        break
                    argstp.insert(ccpc-2, nte)
                self.__execute_func(sys.argv[1], tuple(argstp))

        while True:
            try:
                raw_command = input(f"{self.username}:>  ")
                command = raw_command.lower()
                try:
                    try:
                        raa = command.split(' ')
                        aa = command.replace(raa[0], "")
                        ab = ""
                        for i in aa:
                            ab += i

                        ab = ab[1:]
                        ab = ab.split(",")

                        self.__execute_func(str(raa[0]), ab[0:])
                    except:
                        raa = command
                        self.__execute_func(raa)
                except:
                    if self.__ceos:
                        print(raw_command)
                        print(os.system(raw_command))

                self.logger.write(0, f"{command}")
            except Exception as e:
                self.logger.write(1, f"{e}")
                print(f"command {e} do not exist!")
                pass

