#!/usr/bin/env python

import os,sys, copy

# Number of coordinate sets to be averaged over (50 in a10A1.mfj). Multiple coordinate sets are used to average a conformation over an MD run. We've found that 50 coordinate sets gives a good average.
NumCoord = "1"
# "ang" to specify coordinates in Angstroms, "au" to specify atomic units.
UNIT = "ang"
# This parameter defines the charge on the atoms. "calc" to specify a charge distribution that is to be read in; "equal" to specify a uniform charge distribution; and "none" to specify no charge.
ChargeForm = "calc"
# A scaling factor for the coordinates. Usually 1.0000.
SCALOR = "1.0000"

XYZ = "Standard orientation"
MULLIKEN = ["Mulliken charges:", "Mulliken atomic charges:", "Mulliken charges and spin densities:"]
NPA = "Natural Population"
# periodic table of the element (proton_numer: mass)
MASS_TABLE = {1:1, 2:4, 3:7, 4:9, 5:11, 6:12, 7:14, 8:16, 9:19, 10:20,
             11:23, 12:24, 13:27, 14:28, 15:31, 16:32, 17:35, 18:40, 19: 30, 20: 40,
             26:56, 35:80, 53:127}


def checkcommand():
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python glog2mfj.py *.log")
    if os.path.isfile(sys.argv[1]):
        return sys.argv[1]
    raise SystemExit("Error: %s not exists" % sys.argv[1])


def readlog(flog):
    fo = open(flog, "r")
    lines = fo.readlines()
    fo.close()
    # find where are the keywords representing start of orientation and charge
    xyzstarts = []
    pop = -1
    npa = -1
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith(XYZ):
            xyzstarts.append(i)
        elif line.startswith(MULLIKEN[0]) or line.startswith(MULLIKEN[1]) or line.startswith(MULLIKEN[2]):
            pop = i
        elif npa==-1 and line.startswith(NPA):
            npa = i
    if not xyzstarts:
        raise SystemExit("Error: Not found \"%s\" in %s" % (XYZ, flog))
    if pop == -1 and npa == -1:
        raise SystemExit("Error: Not found \"%s\" or \"%s\" in %s" % (MULLIKEN, NPA, flog))
    # keep the last orientation
    i = xyzstarts[-1] + 5
    xyz = []
    while True:
        s = lines[i].split()
        if len(s) != 6: break
        xyz.append(s[3:] + [s[1]])
        i += 1
    natoms = len(xyz)
    # keep the mullicken charges:
    charges_mlk = []
    if pop != -1:
        i = pop + 2
        for j in range(natoms):
            charges_mlk.append(lines[i+j].split()[2])
    # keep the natural populatioin anaylysis result:
    charges_npa = []
    if npa != -1:
        i = npa + 4
        for j in range(natoms):
            charges_npa.append(lines[i+j].split()[2])
    return xyz, charges_mlk, charges_npa

def reformat(xyz, charges):
    data  = copy.deepcopy(xyz)
    for i, c in enumerate(charges):
        data[i][-1] = MASS_TABLE[int(data[i][-1])]
        data[i].append(c)
    return data

def wrmfj(name, data):
    with open(name+".mfj", "w") as fo:
        fo.writelines([name[:min(15, len(name))]+"\n", NumCoord+"\n", str(len(data))+"\n", UNIT+"\n", ChargeForm+"\n", SCALOR+"\n"])
        for x,y,z,mass,chg in data: 
            fo.write("{:>14}{:>14}{:>14}{:>4}{:>15}".format(x, y, z, mass, chg) + "\n")
    print("**\(^O^)/** Please check %s.mfj" % name)

def main():
    flog = checkcommand()
    xyz, charge_mlk, charge_npa = readlog(flog)
    if charge_mlk:
        name = flog.split(".")[0] + '_mlk'
        data = reformat(xyz, charge_mlk)
        wrmfj(name, data)
    if charge_npa:
        name = flog.split(".")[0] + '_npa'
        data = reformat(xyz, charge_npa)
        wrmfj(name, data)


if __name__=="__main__":
    main()         
    
    
