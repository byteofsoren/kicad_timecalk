import re
from datetime import datetime

target_file='main.sch'
FMT = '%H:%M'


def min_to_hm(mins):
    h = int(mins/60)
    m = int(mins)%60
    #print(f'Minuts={mins}, hours={h}, mins={m}')
    return h, m

def sum_time(data):
    pars_for_time_stamps = re.compile("((2[0-3]|[01][0-9]):[0-5][0-9]\s*-\s*(2[0-3]|[01][0-9]):[0-5][0-9])")
    pars_for_time = re.compile("((2[0-3]|[01][0-9]):[0-5][0-9])")
    minuts=0
    timedata=list()
    fstamps = pars_for_time_stamps.findall(data)
    for stamp in fstamps:
        ts = stamp[0]
        hts = pars_for_time.findall(ts)
        start:str = hts[0][0]
        stop:str = hts[1][0]
        t1 = [int(x) for x in start.split(':')]
        t2 = [int(x) for x in stop.split(':')]
        h1=t1[0];m1=t1[1]
        h2=t2[0];m2=t2[1]
        if h2 < h1:
            h2+=24
        #tdiff = (h2)*60+(m2) - (h1)*60+(m1)
        # Create time objects
        time_from = datetime.strptime(f'{h1}:{m1}',FMT)
        time_to   = datetime.strptime(f'{h2}:{m2}',FMT)
        # Calculate the difference an create an time delta
        tdiff = time_to - time_from
        tdiff_sec= tdiff.total_seconds()

        minuts+=int(int(tdiff_sec)/60)
        tdiff = min_to_hm(int(tdiff_sec)/60)
        actime = min_to_hm(minuts)
        print(f'{h1}:{m1:02d} to {h2}:{m2:02d} = {tdiff[0]}h,{tdiff[1]:02d}m and acumelated time: {actime[0]}h,{actime[1]:02d}m')

    tt = min_to_hm(minuts)
    print(f'Totaly {tt[0]}hours {tt[1]:02d}minuts')
    return tt

def sum_charged_time(data):
    print("Sum all sum_charged_time")
    # pars_for_bill = re.compile("(#[Bb]illed\s+(for\s+|)\d+(\s+|)[hH]ours)")
    pars_for_bill = re.compile("(#[Bb]illed\s+(for\s+|)\d+(\s+|)([hH]ours|[hH]))")
    pars_for_hour = re.compile("(\d+(\s+|)[Hh](ours|))")

    fbills = pars_for_bill.findall(data)
    hours=0
    # print(fbills)
    for bill in fbills:
        fbill = pars_for_hour.findall(bill[0])[0][0]
        try:
            nbill = int(re.sub("((\s+|)([hH]ours|[hH]))", "", fbill))
        except ValueError as e:
            print("There is a wrong in the int conversion")
            raise e
        hours+=nbill
        print(f'Billed for {nbill}hours to a total of {hours}hours')
    print(f'Totaly billed for {hours}hours')
    return hours, 0

def time_diff(spent, billed):
    ''' Calculate the time diffrense for time spent and time billed'''
    b = (billed[0]*60 + billed[1])
    s = (spent[0]*60 + spent[1])
    minuts = s-b
    if s < b:
        t = min_to_hm(minuts)
        return -t[0], 60-t[1]
    else:
        return min_to_hm(minuts)


def main():
    data=0
    with open(target_file, 'r') as fd:
        data=fd.read()
    print("==========[ Tim summation of work done ]==========")
    time_spent = sum_time(data)
    print("\n===========[ Summation of billed time ]===========")
    time_billed = sum_charged_time(data)
    diff = time_diff(time_spent,time_billed)
    print("\n==================[ Result ]======================")
    if diff[0] < 0:
        print(f'Over billed by {diff[0]}hours and {diff[1]}minuts')
    else:
        print(f'Time left to bill is {diff[0]}hours and {diff[1]}minuts')



def calc_proj(path:str):
    data=0
    with open(path, 'r') as fd:
        data=fd.read()
    # print("==========[ Tim summation of work done ]==========")
    time_spent = sum_time(data)
    # print("\n===========[ Summation of billed time ]===========")
    time_billed = sum_charged_time(data)
    diff = time_diff(time_spent,time_billed)
    # print("\n==================[ Result ]======================")
    # if diff[0] < 0:
    #     print(f'Over billed by {diff[0]}hours and {diff[1]}minuts')
    # else:
    #     print(f'Time left to bill is {diff[0]}hours and {diff[1]}minuts')
    return time_spent,time_billed,diff


if __name__ == '__main__':
    main()
