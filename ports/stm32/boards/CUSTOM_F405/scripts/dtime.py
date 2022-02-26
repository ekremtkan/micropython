import time as _time
import math as _math


def split_date_fmt(fmt):
    # "%4d-%02d-%02d %02d:%02d:%02d"
    # mktime_fmt=time.mktime((2020,5,15,23,56,55,0,0,0))
    # y,m,d,H,M,S,z,c,f=map(int,(2020,05,15,23,56,55,0,0,0))
    # for f in '%Y-%m-%d %H:%M:%S'.split('%'):
    fmt_list={}
    key_list=[]
    for f in fmt.split('%'):
        if not f:continue
        sep="" if f == f[-1] else f[-1]
        if 'Y' in f:
            fmt_list['Y']=['%4d', sep]
        elif 'm' in f:
            fmt_list['m']=['%02d', sep]
        elif 'd' in f:
            fmt_list['d']=['%02d', sep]
        elif 'H' in f:
            fmt_list['H']=['%02d', sep]
        elif 'M' in f:
            fmt_list['M']=['%02d', sep]
        elif 'S' in f:
            fmt_list['S']=['%02d', sep]
        elif 'y' in f:
            fmt_list['y']=['%02d', sep]
        elif 's' in f:
            fmt_list['s']=['%02d', sep]
        key_list.append(f[0])
    return key_list,fmt_list

def date_len(fmt):
    return 4 if fmt == 'Y' else 9 if fmt == 's' else 2
    
def split_date_str(date_time:str):
    d_l=[] #values
    s_l=[] #seperators
    s=""
    for i in date_time:
        if i.isdigit():
            s='%s%s'%(s,i)
        else:
            d_l.append(int(s))
            s=""
            s_l.append(i)
    if s:
        d_l.append(int(s))
    return d_l,s_l

def strftime(time_t:tuple,fmt:str):
    # ('%4d', '-', '%02d', '-', '%02d', ' ', '%02d', ':', '%02d', ':', '%02d', '', '', '', '', '')
    if not time_t:
        time_t=_time.localtime()
    y,m,d,H,M,S=0,0,0,0,0,0
    if len(time_t) == 8:
        y,m,d,H,M,S,z,x=time_t
    elif len(time_t) == 9:
        y,m,d,H,M,S,z,x,t=time_t
    else:
        for i,v in enumerate(time_t):
            if i == 0:y=v
            elif i==1:m=v
            elif i==2:d=v
            elif i==3:H=v
            elif i==4:M=v
            elif i==5:S=v
    rets=''
    key_list,fmt_list=split_date_fmt(fmt)
    for k in key_list:
        if k == 'Y' :rets='%s%s%s'%(rets,fmt_list[k][0]%(y),fmt_list[k][1])
        elif k == 'y' :rets='%s%s%s'%(rets,fmt_list[k][0]%(y%100),fmt_list[k][1])
        elif k == 'd' :rets='%s%s%s'%(rets,fmt_list[k][0]%d,fmt_list[k][1])
        elif k == 'm' :rets='%s%s%s'%(rets,fmt_list[k][0]%(m),fmt_list[k][1])
        elif k == 'H' :rets='%s%s%s'%(rets,fmt_list[k][0]%(H),fmt_list[k][1])
        elif k == 'M' :rets='%s%s%s'%(rets,fmt_list[k][0]%(M),fmt_list[k][1])
        elif k == 'S' :rets='%s%s%s'%(rets,fmt_list[k][0]%(S),fmt_list[k][1])
        elif k == 's' :rets='%s%s%s'%(rets,fmt_list[k][0]%(_time.mktime(time_t)),fmt_list[k][1])
    return rets




def strptime(time_t:str,fmt:str):
    Y,y,m,d,H,M,S,s=0,0,0,0,0,0,0,0
    t1,t2=0,0
    d_l,sp_l=split_date_str(time_t)
    no_separator=False
    if len(d_l) ==1:
        no_separator=True
    key_list,fmt_list=split_date_fmt(fmt)
    begin=0
    for i,k in enumerate(key_list):
        step=date_len(k)
        if no_separator:
            val=int(str(d_l[0])[begin:begin+step])
        else:
            val=d_l[i]
        if k == 'Y' :Y=val if len(str(val))==4 else 2000
        elif k == 'y' :y=val if len(str(val))==2 else val%100
        elif k == 'd' :d=val
        elif k == 'm' :m=val
        elif k == 'H' :H=val
        elif k == 'M' :M=val
        elif k == 'S' :S=val
        elif k == 's' :s=val
        begin+=step
    if Y :
        t1=_time.mktime((Y,m,d,H,M,S,0,0,0))
    if y :
        t1=_time.mktime((y+2000,m,d,H,M,S,0,0,0))
    if s:
        ret=_time.localtime(s)
    else:
        ret=_time.localtime(t1)
    return ret
