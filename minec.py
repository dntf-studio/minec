from typing import Text
import pydirectinput as direct
import time
import clr
import sys
import os
import re
clr.AddReference('components1_cs')
from components1_cs import Class1

# -*- coding: utf-8 -*-

# grammer: <key>,loop,!loop,wait:<time>,keep(<key>):<time>
def main():
    try:
        print("マインクラフトのウィンドウ名を入力してください")
        r1 = input(">> Minecraft ")
        activeWindow("Minecraft "+r1)
        ask()

    except KeyboardInterrupt:
        print("\nプログラムを終了します...")

def activeWindow(n):
    try:
        cs = Class1(n)
        cs.SetWindowActive()
        #direct.keyDown('esc')
        #direct.keyUp('esc')
        step()

    except:
        print("なにか問題が発生しました。")
        print('....')
        main()

def ask():
    r2 = input("プログラムを終了しますか？(Y/N)")
    if r2.strip().upper() == 'Y' :
        sys.exit()
    elif r2.strip().upper() == 'N' :
        main()
    else:
        ask()

def step():
    file_ = open('order.txt', 'r', encoding='UTF-8') 
    data = file_.readlines()
    d = []
    j=0
    #なぜか普通に動かない配列操作。。
    for i in data:
        if i == '\n':
            data.pop(j)
        elif i.startswith('@') or len(i) >= 20:
            data.pop(j)
        else:
            d.append(i)
        j+=1

    print("指示数:",len(d))
    print(d)

    for i in range(len(d)):
        f = False
        loop = []
        if d[i].strip() == "loop":
            dd=i
            global eol
            while True:
                if dd >= len(d):
                    print('order.txt : loop処理が終了していません。\nプログラムを終了します。')
                    sys.exit()
                elif d[dd].strip() == "!loop":
                    f = True
                    eol = dd+i
                    print("ループされる処理:",loop)
                    loop_(loop)
                    break
                else :
                    if not dd == i:
                        loop.append(d[dd])
                dd+=1
        elif d[i].strip() == 'click':
            direct.click()
        elif d[i].strip() == 'rclick':
            direct.rightClick()
        elif d[i].strip().startswith('wait'):
            wait(d[i])
        elif d[i].strip().startswith('keep'):
            keep(d[i].strip())
        else :
            direct.press(d[i].strip())

def loop_(l):
    try:
        while True:
            for i in l:
                if i.startswith('wait'):
                    wait(i)
                elif i.startswith('keep'):
                    print('i')
                    keep(i)
                elif i.strip() == 'click':
                    direct.click()
                elif i.strip() == 'rclick':
                    direct.rightClick()
                else:
                    direct.press(i.strip())
    except KeyboardInterrupt:
        ask()

def keep(s):
    print('a')
    if s[4] == '(':
        i = 5
        while True:
            if len(s) <= i:
                print('keep命令文に ) がありません')
                raise
            elif s[i] == ')':
                print('b')
                break
            i+=1
        key = s[5:i]
        if s[i+1] == ':':
            print("k",key)
            num = s[i+1:]
            f = decimal(num)
            print('num',f)
            direct.keyDown(key)
            time.sleep(f)
            direct.keyUp(key)
        else: 
            print('b2')
    else :
        raise "keep error"
        

def wait(s):
    f = decimal(s)
    print('待機:',f)
    time.sleep(f)

def decimal(f):
    ma = re.search(r'([0-9]+)?\.[0-9]+|[0-9]+\.|([0-9]+|([0-9]+)?\.[0-9]+|[0-9]+\.)[eE][-+][0-9]+',f)
    return float(ma.group(0))


if __name__ == "__main__":
    main()