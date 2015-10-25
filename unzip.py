__author__ = 'hai'

import argparse
import os
import zipfile
import traceback, sys
from glob import glob
import re
import subprocess

parser = argparse.ArgumentParser(description='Unzip and Compile Java Files.')
parser.add_argument('--path',default='./Hw1',help='path to directory to be unzip')
args = parser.parse_args()

class unzip:
    def __init__(self, path, student_file):
        self.counter = 0
        self.total_success = 0;
        self.path = path
        self.student_file = student_file
        self.total_fail = []
        self.unzip()
        self.print_()


    def unzip(self):
        '''
        unzip file and compile
        '''
        found_jar = False
        for i in os.listdir(self.path):
            tmp_fold = os.path.join(self.path,i)
            if os.path.isdir(tmp_fold):
                for j in os.listdir(tmp_fold):
                    tmp_file = os.path.join(tmp_fold, j)
                    print(tmp_file)
                    if os.path.isfile(tmp_file) and tmp_file.endswith('.zip'):
                        try:
                            with zipfile.ZipFile(tmp_file, 'r') as z:
                                z.extractall(tmp_fold)
                                tmp_path = os.getcwd()
                                p = os.path.abspath(tmp_fold)
                                self.compile(p)
                        except:
                            traceback.print_exc()
                            print("Failed to unzip/compile {0}".format(tmp_file))
                            self.total_fail.append(tmp_file)

                        finally:
                            os.chdir(tmp_path)

    def print_(self):
        '''
        print summary
        '''
        print("\nSummary:\n")
        #print("Total zip files found: {0}".format(self.total_success + len(self.total_fail)))
        print("Success: {0}\n".format(self.total_success))
        print("Failed: {0}\n".format(len(self.total_fail)))
        for i in self.total_fail:
            print("{0}\n".format(i))


    def compile(self, path):
        '''
        compile java files
        '''
        os.chdir(path)
        cur_dir = os.getcwd()
        if not os.listdir(path):
            return False

        found_jar = False
        for k in os.listdir(cur_dir):
            k_file = os.path.abspath(k)
            #dirty way to handle ._ MAC folder
            if k_file.endswith('.java') and not '._' in k_file:
                found_jar = True
                break

        if found_jar is True:
            subprocess.check_output("javac *.java", shell=True)
            self.total_success = self.total_success + 1
            return True

        else:
            for k in os.listdir(cur_dir):
                j = os.path.join(cur_dir,k)
                if os.path.isdir(j):
                    if self.compile(j):
                        return True
        return False


if __name__ == "__main__":
    unzip(args.path, None)