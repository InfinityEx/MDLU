import hashlib
import os
import sys
import json
import argparse
from colorama import Fore,init,Back

init()

def readJson(r1="./h1.json",r2="./h2.json"):
    with open(r1,'r') as f1, open(r2,'r') as f2:
        data1=json.load(f1)['data']
        data2=json.load(f2)['data']
    return data1,data2

def checkDiff(a,b):
    set1 = {item['filename'] for item in a}  
    set2 = {item['filename'] for item in b} 

    unique_in_1 = set1 - set2  
    unique_in_2 = set2 - set1  

    print(f"file lost: {unique_in_1}")
    print(f"file new: {unique_in_2}")

    for item1 in a:  
        for item2 in b:  
            if item1['filename'] == item2['filename'] and item1['md5'] != item2['md5']: 
                print(f"{Fore.LIGHTYELLOW_EX}filename: {item1['path']} \n{Fore.LIGHTCYAN_EX}previous: {item1['md5']} | newest: {item2['md5']}")
                break
    pass

def getDiff():
    pass

if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='compareDiff',usage=f'-c <path1> <path2>',description='',add_help=False)
    parser.add_argument('-c',nargs=2,metavar=('PATH1', 'PATH2'))
    args = parser.parse_args()
    print(args.c[0])
    if args.c!=None:
        data1,data2=readJson(args.c[0],args.c[1])
        checkDiff(data1,data2)
    pass