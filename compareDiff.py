import hashlib
import os
import sys
import json
import argparse
from colorama import Fore,init,Back
# should i init download at this file?
import requests

init()

# load different json file from different version
def readJson(r1="./h1.json",r2="./h2.json"):
    with open(r1,'r') as f1, open(r2,'r') as f2:
        data1=json.load(f1)['data']
        data2=json.load(f2)['data']
    return data1,data2

# check diff between two json file
def checkDiff(a,b):
    # set1 = {item['filename'] for item in a}  
    # set2 = {item['filename'] for item in b} 
    # pack value to set_1 and set_2
    # why use path? easy to joint text as a download link
    set1 = {item['path'] for item in a}  
    set2 = {item['path'] for item in b} 

    # unique_in_1 is what file will deleted in future version
    unique_in_1 = set1 - set2  
    # unique_in_2 is what file will add in future version
    unique_in_2 = set2 - set1  

    # transfer set to list
    if len(unique_in_1)==0:
        unique_in_1={"Empty"}
    else:
        ilist1=[]
        for item in unique_in_1:
            ilist1.append(item)
        unique_in_1=ilist1
            
    if len(unique_in_2)==0:
        unique_in_2={"Empty"}
    else:
        ilist2=[]
        for item in unique_in_2:
            ilist2.append(item)
        unique_in_2=ilist2

    # print file
    print(f"file deleted: {unique_in_1}\n")
    print(f"file update: {unique_in_2}\n")

    ultraLlist=[]
    for item1 in a:
        for item2 in b:
            # check if file name is same and md5 is different
            if item1['filename'] == item2['filename'] and item1['md5'] != item2['md5']: 
                # print path and diff md5 between two version
                print(f"{Fore.LIGHTYELLOW_EX}filename: {item1['path']} \n{Fore.LIGHTCYAN_EX}previous: {item1['md5']} | newest: {item2['md5']}\n")
                ultraLlist.append({"filename":item1['path'],"previous":item1['md5'],"newest":item2['md5']})
                pass
                break
    return ultraLlist
    pass

def getDiff(jsonList):
    print(jsonList)
    with open("./update.json",'w') as f:
        json.dump({"update":jsonList},f)
    pass

if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='compareDiff',usage=f'-c <path1> <path2>',description='',add_help=False)
    parser.add_argument('-c',nargs=2,metavar=('PATH1', 'PATH2'))
    args = parser.parse_args()
    print(args.c[0])
    if args.c!=None:
        data1,data2=readJson(args.c[0],args.c[1])
        getDiff(checkDiff(data1,data2))
    pass