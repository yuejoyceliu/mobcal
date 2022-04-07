# Ion Mobility Calculation (MobCal)
Calculate the mobilities (cross section) of molecular ions in helium and nitrogen

## Prepare Input File
1. Complete Gaussian population analysis and get the output file ("example.log").
2. Make MobCal input file ("example.mfj") based on the Gaussian output file by running `python glog2mfj.py example.log`.
## Calcualte Multiple Ion Mobilities in Parallel
1. Stay in/Go to the directory containing one or more MobCal input files ("\*.mfj"). 
2. Generate ion mobility tasks using python file mobcal.py
    - If compute ion mobility in Nitrogen: `python mobcal.py N2`;
    - If compute ion mobility in Helium: `python mobcal.py He`;
    - If compute ion mobility in both gases: `python mobcal.py Both`;
    - If some in N2 and the others in He: `python mobcal.py Either` and the specific environment gas will be obtained from the input.
3. Modify the job time and/or partition defined in "parallel_run.sh" if needed.
4. Submit the tasks: `sbatch parallel_run.sh`. 
5. Wait until the tasks complete.
## Obtain the Result
1. Go to the same directory that has MobCal input files.
2. Extract cross sections for all molecular ions: `python extract_mobcal.py`.
3. Save the output file "mobcal_summary.csv"!
