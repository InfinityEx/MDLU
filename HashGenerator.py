# !/usr/bin/python
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
def interia(path):
    list={
        "data":[]
    }
    # list.update({"data":[]})
    for root,dirs,files in os.walk(path):
        for file in files:
            file_patht=os.path.join(root,file)
            file_pathr=os.path.join(root)
            file_name=os.path.basename(file)
            # print(f" {Fore.YELLOW}path:{file_patht} || name:{file_name}{Fore.RESET}")
            # list.update({file_name:hashlib.md5(open(file_patht,'rb').read()).hexdigest()},{"version":"0.4.5"})
            # list["data"].append([{file_name:hashlib.md5(open(file_patht,'rb').read()).hexdigest(),"version":"0.4.5"}])
            litdetial={
                "filename":file_name,
                "path":os.path.join(root,file).replace('\\','/').split(path)[1],
                "md5":hashlib.md5(open(file_patht,'rb').read()).hexdigest(),
                "version":"0.4.5"
                }
            print("os path join: "+os.path.join(root,file))
            print("path: "+path)
            print("file_pathr"+file_pathr)
            print("file_patht"+file_patht)
            print(litdetial["path"])
            list["data"].append(litdetial)
    with open(f"{path}/hash.json",'w',encoding='utf-8') as hf:
        json.dump(list,hf,indent=2,ensure_ascii=False)
    pass

def welcome():
    print("="*45)
    print(f"{Fore.LIGHTGREEN_EX} Hash Generator v0.1\n{Fore.LIGHTMAGENTA_EX} Program for generate hash file of MiniDL{Fore.RESET}")
    print("="*45)

if __name__ == '__main__':
    welcome()
    # print(os.path.abspath("HashGenerator.py").split(os.path.basename("HashGenerator.py"))[0])
    # pathWalk()
    parser = argparse.ArgumentParser(prog='hashGen.exe',usage=f'{Fore.LIGHTYELLOW_EX}%(prog)s {Fore.LIGHTRED_EX}[-p] <print_type> {Fore.LIGHTCYAN_EX}[-g] <path>{Fore.LIGHTWHITE_EX} ',description='')
    parser.add_argument('-p',default='',nargs='?',help='Get game path and print as text/json,like "hashGen.exe -p text" or "hashGen.exe -p json"')
    parser.add_argument('-g',nargs='?',help=f'Generate hash file from game path[need specified],like "hashGen.exe -g "D:/Games/MiniDL/MiniDL_Data"{Fore.RESET}')

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
            print(f"{Fore.LIGHTGREEN_EX} Info: path is available\n{Fore.RESET}")
            interia(args.g)
        elif os.path.exists(args.g)==False:
            print(f"\n{Fore.LIGHTRED_EX} Warning: path is unavailable\n{Fore.RESET}")
            parser.print_help()
    
    if args.p not in ('json','text',' ') and args.g==None:
        parser.print_help()
    pass
