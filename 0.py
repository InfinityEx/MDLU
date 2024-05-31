#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:时无ShiWu
#Filename:DSE.py
#Version:1.0 448.37

import os
import sys
import csv
import time
import json
import argparse
import subprocess

# 脚本默认位置
default_path=os.path.split(os.path.realpath(__file__))[0]
# vgmstream 位置
vgm_path=default_path+r'\vgmstream\test.exe'
# 数据文件列表位置
sfs_path=default_path+r'\soundfile_seq.csv'
# 音频序列位置
seq_path=default_path+r'\acbseq'
# 源文件位置
osf_path=default_path+r'\osf'
# 输出位置 
output_path=default_path+r'\output'

respond=''
cir=0

def extract_files(a,b):

    print(default_path,vgm_path)

    # 加载数据文件列表
    with open(sfs_path,'r') as sfs:
        fsreader=dict(csv.reader(sfs))

    # 序列是否存在进行判断，存在则为其创建一个文件夹
    print(a)
    fn=fsreader.get(a,-1)
    if(fn==-1):
        print('seq not found')
        sys.exit(0)
    else:
        # Reference from sh0wer1ee/DLStories
        if not (os.path.exists(f'{output_path}/{fn}')):
            os.makedirs(f'{output_path}/{fn}')
    
    try:
        ib=int(b)
    except:
        print('wrong channel number,plz check argument')
        sys.exit(0)

    # 判断只导出单个声道还是导出全部声道
    # Reference from sh0wer1ee/DLStories（20221005）
    acbjson={}
    seqjson={}
    sn=0
    yb=str(ib)
    if os.path.exists(f'{osf_path}/{fn}.awb')==True and os.path.exists(f'{osf_path}/{fn}.acb')==True:
        acbjson=json.loads(subprocess.check_output(f'{vgm_path} -s {yb} -I -m {osf_path}/{fn}.awb'))
    elif os.path.exists(f'{osf_path}/{fn}.awb')==False and os.path.exists(f'{osf_path}/{fn}.acb')==True:
        acbjson=json.loads(subprocess.check_output(f'{vgm_path} -s {yb} -I -m {osf_path}/{fn}.acb'))
    sn=acbjson['streamInfo']['total']
    sstr=''

    if(ib!=0):
        outname=acbjson['streamInfo']['name']
        if(ib < sn):
        # cmd序列生成
            # subprocess.check_output(f'{vgm_path} -s {yb} -i -o {output_path}/{fn}/{outname}.wav {osf_path}/{fn}.awb').decode('utf-8')
            subprocess.check_call(f'{vgm_path} -s {yb} -i -o {output_path}/{fn}/{outname}.wav {osf_path}/{fn}.awb',bufsize=-1)
        else:
            print('channel id not in awb file')
        # print(f'{outname}')
        # print(sstr)
    elif(ib==0):
        for i in range(0,sn):
            y=str(i)
            if os.path.exists(f'{osf_path}/{fn}.awb')==True and os.path.exists(f'{osf_path}/{fn}.acb')==True:
                seqjson=json.loads(subprocess.check_output(f'{vgm_path} -s {y} -I -m {osf_path}/{fn}.awb'))
            elif os.path.exists(f'{osf_path}/{fn}.awb')==False and os.path.exists(f'{osf_path}/{fn}.acb')==True:
                seqjson=json.loads(subprocess.check_output(f'{vgm_path} -s {y} -I -m {osf_path}/{fn}.acb'))
            outname=seqjson['streamInfo']['name']
            # print(outname)
            # wav='.wav'
            # awb='.awb'
            # cmd序列生成
            # subprocess.check_output(f'{vgm_path} -s {y} -i -o {output_path}/{fn}/{outname}{wav} {osf_path}/{fn}{awb}').decode('utf-8')
            if os.path.exists(f'{osf_path}/{fn}.awb')==True and os.path.exists(f'{osf_path}/{fn}.acb')==True:
                subprocess.check_call(f'{vgm_path} -s {y} -o {output_path}/{fn}/{outname}.wav {osf_path}/{fn}.awb',bufsize=-2)
            elif os.path.exists(f'{osf_path}/{fn}.awb')==False and os.path.exists(f'{osf_path}/{fn}.acb')==True:
                subprocess.check_call(f'{vgm_path} -s {y} -o {output_path}/{fn}/{outname}.wav {osf_path}/{fn}.acb',bufsize=-2)
            print(f'{outname}')
    sfs.close()
    time.sleep(1)
    

if __name__=="__main__":
    # parser settings
    parser = argparse.ArgumentParser(prog='python dse.py',usage='%(prog)s [-fileid] <file_id> [-seqfile] <seqfile> ([-channel] <channel_id> [-ow <int>])',description="Python Program for Extract Sound Files")
    parser.add_argument('-fileid',default='empty',nargs='?',help='extract file from filelist sequence')
    parser.add_argument('-seqfile',default=sfs_path,nargs='?',help='specify a file instead of default sequence')
    parser.add_argument('-channel',default=0,nargs='?',help='extract channel N from file channels,set 0 or empty extract all single channel')
    parser.add_argument('-ow',default=0,nargs='?',help="""<unavailable> selected set 1 allow export file overwrite,
    default or set 0 refuse overwrite.""")

    # merge parser
    args = parser.parse_args()
    
    # print help with boot
    # parser.print_help()

    if(args.fileid=='empty'):
        print("You can't run prog without <fileid>\n")
        parser.print_help()
        sys.exit(0)


    if(args.fileid=='all'):
        # 加载数据文件列表
        if(args.seqfile==sfs_path):
            with open(sfs_path,'r') as psfs:
                fsreader=dict(csv.reader(psfs))
            psfi=len(fsreader)
            for s in range(1,psfi):
                    extract_files(str(s),args.channel) 
        else:
            sfs_path=default_path+"\\"+str(args.seqfile)
            with open(sfs_path,'r') as psfs:
                fsreader=dict(csv.reader(psfs))
            psfi=len(fsreader)
            for s in range(1,psfi):
                    extract_files(str(s),args.channel) 
    else:
        extract_files(args.fileid,args.channel)