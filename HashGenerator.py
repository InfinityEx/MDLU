#!/usr/bin/python
import hashlib
import os
import json
import argparse
from colorama import Fore,init,Back

init()
# getPath
def pathWalk(outType):
    if os.path.exists(os.getcwd()+"/preference.json"):
        # print(os.path.exists(os.getcwd()+"/preference.json"))
        with open(os.getcwd()+"/preference.json",'r',encoding='utf-8') as pf:
            settings=json.load(pf)
            options={}
            options['path']=settings['Game'][0]['path']
            options['data']=f"{options['path']}{settings['Game'][0]['data']}"
            options['hashlist']=f"{options['path']}{settings['Game'][0]['hashlist']}"
            # print(os.path.exists(options['data']))
            if outType=='json':
                return print(options)
            elif outType=='text':
                return print(f"path:{options['path']}\ndata:{options['data']}\nhash:{options['hashlist']}")
            else:
                exit
    else:
        print('error')


# getHash
def getHash():
    pass


# fileWalk
def interia():
    pass


if __name__ == '__main__':
    # print(os.path.abspath("HashGenerator.py").split(os.path.basename("HashGenerator.py"))[0])
    # pathWalk()
    parser = argparse.ArgumentParser(prog='hashGen.exe',usage='%(prog)s [-p] <print_type> [-g] <path> ',description="Hash Generator")
    parser.add_argument('-p',default='',nargs='?',help='Get game path and print as text/json,like "hashGen.exe -p text" or "hashGen.exe -p json"')
    parser.add_argument('-g',nargs='?',help='Generate hash file from game path[need specified],like "hashGen.exe -g "D:/Games/MiniDL/MiniDL_Data""')

    # merge parser
    args = parser.parse_args()

    # print path
    if args.p=='json':
        pathWalk('json')
    elif args.p=='text':
        pathWalk('text')

    # get Hash
    if args.g!=None:
        if os.path.exists(args.g)==True:
            print(f"{Fore.LIGHTGREEN_EX}path is available\n")
            parser.print_help()
        elif os.path.exists(args.g)==False:
            print(f"\n{Fore.LIGHTRED_EX} Warning: path is unavailable\n{Fore.RESET}")
            parser.print_help()
    
    if args.p=='' and args.g==None:
        parser.print_help()
    pass
