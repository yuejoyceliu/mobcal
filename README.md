# Ion Mobility Calculation (MobCal)
Calculate ion mobility (cross section) in helium and nitrogen on Hyak.
- atoms supported in N2: H, C, N, O, F, Na, Si, P, S, F, Cl, Fe, Br and I.
- atoms supported in He: H, C, N, O, F, Na, Si, S and Fe.
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
# References
- Campuzano, I. D. G.;* Bush, M. F.;* Robinson, C. V.; Beaumont, C.; Richardson, K.; Kim, H.; Kim, H. I. “Structural Characterization of Drug-like Compounds by Ion Mobility Mass Spectrometry: Comparison of Theoretical and Experimentally Derived Nitrogen Collision Cross-sections” Anal. Chem. 2012, 84, 1026-1033.
- Mesleh, M. F.; Hunter, J. M.; Shvartsburg, A. A.; Schatz, G. C.; Jarrold, M. F. “Structural Information from Ion Mobility Measurements: Effects of the Long Range Potential" J. Phys. Chem. 1996, 100, 16082-16086.
- Kim, H; Kim, H. I.; Johnson, P. V.; Beegle, L. W.; Beauchamp J.L.; Goddard, W.A.; Kanik, I. “Experimental and theoretical investigation into the correlation between mass and ion mobility for choline and other ammonium cations in N2” Anal. Chem. 2008, 80, 1928-1936.
- Lee, J. W.; Lee, H. H. L.; Davidson, K. L.; Bush, M. F.; Kim, H. I. "Structural Characterization of Small Molecular Ions by Ion Mobility Mass Spectrometry in Nitrogen Drift Gas: Improving the Accuracy of Trajectory Method Calculations" Analyst, 2018, 143, 1786-1796.
- Lee, J. W.; Davidson, K. L.; Bush, M. F.; Kim, H. I. "Collision Cross Sections and Ion Structures: Development of a General Calculation Method via High-quality Ion Mobility Measurements and Theoretical Modeling" Analyst, 2017, 142, 4289-4298.
