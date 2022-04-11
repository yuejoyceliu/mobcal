#!/usr/bin/python

import os, sys, glob, shutil
nCORES = 28
NAME = "sample.mfj"

def checkcommand():
    options = ["He", "N2", "Both", "Either"]
    assert len(sys.argv) == 2, "Usage: python mobcal.py {}".format('/'.join(options))
    assert sys.argv[1] in options, "{} not in [{}]".format(sys.argv[1], ' '.join(options))
    return sys.argv[1]


def create_task(fl, key):
    dfolders = []
    if key == "Either":
        while key != "He" and key != "N2":
            key = raw_input("Choose the version for " + fl + " : [He or N2] ")
    elif key == "Both":
        dfolders.append(create_task(fl, "He")[0])
        key =  "N2"
    flname = fl.split(".")[0]
    dirname = "d_" + flname + "_" + key
    dfolders.append(dirname)
    os.mkdir(dirname)
    shutil.copyfile(fl, dirname + "/" + NAME) 
    shutil.copyfile(os.path.expanduser('~')+ "/mobcal/mobcal_" + key + ".f", dirname + "/mobcal_" + key + ".f")
    with open(dirname+"/mobcal.in", "w") as fo:
        fo.write(NAME + "\n")
        fo.write("sample_" + key + ".out\n")
        fo.write("5013489\n")
    return dfolders

def cpfile(env):
    mfjs = glob.glob("*.mfj")
    tasks = []
    for mfj in mfjs:
        tasks.extend(create_task(mfj, env))
    return tasks


def parallel_run(dmfj_tasks):
    pwd = os.path.abspath(".")
    with open("tasklists.sh", "w") as fo:
        for d in dmfj_tasks:
            if d[-2:] == "He":
                fo.write("cd "+pwd+"/"+d+"; gfortran -o mn mobcal_He.f -w; ./mn\n")
            else:
                fo.write("cd "+pwd+"/"+d+"; gfortran -o mn mobcal_N2.f -w; ./mn\n")
    ntasks = len(dmfj_tasks)
    p1 = '#!/bin/bash\n#SBATCH --job-name=mobcal\n#SBATCH --nodes=1\n#SBATCH --ntasks-per-node='+str(nCORES)+'\n#SBATCH --time=40:00:00\n#SBATCH --mem=200G\n'
    p2 = '#SBATCH --chdir='+pwd+'\n'
    p3 = '#SBATCH --partition=chem\n#SBATCH --account=chem\n\n'                                                                                              
    p4 = 'module load parallel-20170722\n'                                                                                           
    p5 = 'cat tasklists.sh | parallel -j '+str(min(ntasks,nCORES))+'\n'
    with open('parallel_run.sh','w') as fo:
        fo.write(p1)
        fo.write(p2)
        fo.write(p3)
        fo.write('#set up time\nbegin=$(date +%s)\n\n')
        fo.write(p4)
        fo.write(p5)
        fo.write('end=$(date +%s)\nlet "etime=($end-$begin)/60"\necho \'Elapsed Time: \'$etime\' min\'')

def main():
    key = checkcommand()
    tasks = cpfile(key)
    parallel_run(tasks)
    reminders = [(160, 23.5), (231, 55.2)]
    print("Reminder:")
    for reminder in reminders:
        print("%5d atoms in N2: %3.1fh" % (reminder[0], reminder[1]))

if __name__=="__main__":
    main()
