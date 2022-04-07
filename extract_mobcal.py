#!/usr/bin/env python

import glob,os
import csv

def findfiles():
    files = glob.glob("d_*/*.out")
    if not files:
        raise SystemExit("Warning: not found mobal.out")
    fo = open("mobcal_summary.csv", "w")
    wrcsv = csv.writer(fo)
    wrcsv.writerow(["struct", "He/N2", "PA", "EHS", "TM"])
    for f in files:
        data = extract(f)
        name = f.split("/")[0]
        name = name.split("_")
        wrcsv.writerow(["_".join(name[1:-1]), name[-1]] + data)
    print("**\(^O^)/** Please check mobcal_summary.csv!")

def extract(f):
    pa =  ehs = tm = None
    with open(f, "r") as fo:
        lines = fo.readlines()
    for line in lines:
        if "average PA cross section" in line:
            pa = getdata(line)
        elif "average EHS cross section" in line:
            ehs = getdata(line)
        elif "average TM cross section" in line:
            tm = getdata(line)
            return [pa, ehs, tm]
    print("Warning: Not Finish:", f.split("/")[0])
    return [pa, ehs, tm]

def getdata(s):
    return float(s.split()[-1])


if __name__ == "__main__":
    findfiles()
    
    
