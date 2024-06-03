# !/usr/bin/python
import hashlib
import os
import sys
import json
import argparse
from colorama import Fore,init,Back
import requests as rqs

init()
# getPath
def pathWalk(outType,output=''):
    if os.path.exists(os.getcwd()+"/preference.json"):
        # print(os.path.exists(os.getcwd()+"/preference.json"))
        with open(os.getcwd()+"/preference.json",'r',encoding='utf-8') as pf:
            try:
                settings=json.load(pf)
                options={}
                options['path']=settings['Game'][0]['path']
                options['data']=f"{options['path']}{settings['Game'][0]['data']}"
                options['hashlist']=f"{options['path']}{settings['Game'][0]['hashlist']}"
                # print(os.path.exists(options['data']))
                if outType=='json':
                    if output=='':
                        return print(options)
                    if output=='real':
                        return options
                elif outType=='text':
                    return print(f"path:{options['path']}\ndata:{options['data']}\nhash:{options['hashlist']}")
                else:
                    exit
            except:
                print(f'{Fore.LIGHTRED_EX}Fatal Error: Incorrect JSON structure{Fore.RESET}')
                createPreference()
                print(f"preference file restored")
                
    else:
        print(f'{Fore.LIGHTRED_EX}Error: preference file not found{Fore.RESET}')
        createPreference()
        print(f"preference file restored")

def createPreference():
    pfs={
        "Updater":
            [{
                "version":"0.1",
                "":""
                }],
        "Game":
            [{
                "currentVersion":None,
                "previousVersion":None,
                "path":None,
                "data":None,
                "hashlist":None
            }],
            "showUpdate":False
        }
    with open(f"{os.getcwd()}/preference.json",'w',encoding='utf-8') as pf:
        json.dump(pfs,pf,indent=2,ensure_ascii=False)

# getHash
def getHash(path):
    md5=hashlib.md5(open(path,'rb').read()).hexdigest()
    return md5


# fileWalk
def interia(data,path=''):
    with open(f"{data}/version.json",'r',encoding='utf-8') as vs:
        da=json.load(vs)
        ver=da['version']
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
                "md5":getHash(file_patht),
                "version":ver
                }
            # print("os path join: "+os.path.join(root,file))
            # print("path: "+path)
            # print("file_pathr"+file_pathr)
            # print("file_patht"+file_patht)
            # print(litdetial["path"])
            list["data"].append(litdetial)
    with open(f"{path}/list.json",'w',encoding='utf-8') as hf:
        json.dump(list,hf,indent=2,ensure_ascii=False)
    pass

def welcome():
    print("="*45)
    print(f"{Fore.LIGHTGREEN_EX} Hash Generator v0.1\n{Fore.LIGHTMAGENTA_EX} Program for generate hash file of MiniDL{Fore.RESET}")
    print("="*45)

if __name__ == '__main__':
    # print(os.path.abspath("HashGenerator.py").split(os.path.basename("HashGenerator.py"))[0])
    # pathWalk()
    parser = argparse.ArgumentParser(prog='hashGen.exe',usage=f'{Fore.LIGHTYELLOW_EX}%(prog)s {Fore.LIGHTRED_EX}[-p] <print_type> {Fore.LIGHTCYAN_EX}[-g] <path> {Fore.LIGHTMAGENTA_EX}[--version]{Fore.RESET} ',description='',add_help=False)
    parser.add_argument('-h','--help',action="store_true",help=f'{Fore.LIGHTWHITE_EX}show this help message and exit{Fore.RED}')
    parser.add_argument('-p','-print',choices=['json','text'],nargs='?',help=f'{Fore.LIGHTRED_EX}Get game path and print as text/json,like "hashGen.exe -p text" or "hashGen.exe -p json"{Fore.CYAN}')
    parser.add_argument('-g','-gen',nargs='?',help=f'{Fore.LIGHTCYAN_EX}Generate hash file from game path[need specified],like "hashGen.exe -g "D:/Games/MiniDL/MiniDL_Data"{Fore.MAGENTA}')
    parser.add_argument('--version',help=f'{Fore.LIGHTMAGENTA_EX}Print program version{Fore.RESET}',action="store_true")
    parser.add_argument('-mini',action="store_true")
    parser.add_argument('-update',action="store_true")


    # merge parser
    args = parser.parse_args()

    # print path
    if args.p=='json':
        pathWalk('json')
    elif args.p=='text':
        pathWalk('text')

    if args.version:
        welcome()
        sys.exit()

    if args.mini:
        realpath=pathWalk('json','real')
        # print(realpath)
        print(f" data_path: {realpath['data']}\n launcher_path: {realpath['path']}\n")
        interia(realpath['data'],realpath['path'])
        print(f'{Fore.LIGHTCYAN_EX} JSON file is generated in {Fore.LIGHTGREEN_EX}"{realpath["path"]}"{Fore.RESET}')
        pass

    if args.update:
        realpath=pathWalk('json','real')
        path=realpath['path']
        url="http://127.0.0.1:99/minidl"
        head="/list.json"
        response=rqs.get(url+head)
        if os.path.exists(f"{path}/patch")==False:
            os.mkdir(f"{path}/patch")
        if response.status_code==200:
            with open(f"{path}/patch/list.json",'w',encoding='utf-8') as hf:
                hf.write(response.text)
        new={}
        local={}
        with open(f"{path}/list.json",'r',encoding='utf-8') as nw:
            new=json.load(nw)
        with open(f"{path}/patch/list.json",'r',encoding='utf-8') as lc:
            local=json.load(lc)
        for i in range(0,len(new['data'])):
            for j in range(0,len(local['data'])):  
                if new['data'][i]['filename']==local['data'][j]['filename']:
                    if new['data'][i]['md5']!=local['data'][j]['md5']:
                        res=rqs.get(f"{url}/{new['data'][i]['path']}")
                        with open(f"{path}/{new['data'][i]['path']}",'wb') as file1:
                            file1.write(res.content)
                        local['data'][j].update(new['data'][i])
                        print(f"{local['data'][j]}, {new['data'][i]}\n")
                elif new['data'][i]['filename']!=local['data'][j]['filename']:
                    resa=rqs.get(f"{url}/{new['data'][i]['path']}")
                    with open(f"{path}/{new['data'][i]['path']}",'wb') as file2:
                        file2.write(resa.content)
                    local['data'].append(new['data'][i])
                    print(f"{new['data'][i]}, {local['data']}\n")
                
        # print(local["data"][0])
        pass


    # get Hash
    if args.g!=None:
        if os.path.exists(args.g)==True:
            print(f"{Fore.LIGHTGREEN_EX} Info: path is available\n{Fore.RESET}")
            interia(args.g)
        elif os.path.exists(args.g)==False:
            print(f"\n{Fore.LIGHTRED_EX} Warning: path is unavailable\n{Fore.RESET}")
            parser.print_help()
    
    if args.p==None and args.g==None and args.mini==False and args.update==False:
        parser.print_help()
    pass
