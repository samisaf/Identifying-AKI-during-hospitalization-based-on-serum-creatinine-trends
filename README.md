# AKI Calculator
This program analyses a series of creatinine laboratory values and calculates the number of AKI, and their dates. It also has the ability to plot the results. The porgram is meant to assess a patient's baseline creatinine based on values before hospitalization, and the patient's peak creatinine during hospitalization. 

Baseline creatinine is calculated based on the creatinines before the admission date. Two variables can be tweaked in the `Patient.py` file:
`WINDOW`: timeframe in days within which creatinine values are used
`MEASUREFUNC`: is how the baseline creatinine is estimated
For example, if baseline creatinine is defined as the median creatinine within 6 months before hospitalization, 
then `WINDOW = 180`, and `MEASUREFUNC = median`.

Peak creatinine is defiend as the highest creatinine during the patient's hospitalization. AKI during hospitalization can be calculated via comparing the baseline creatinine, and the peak creatinine.

## How to use the program
The program is written in Python 3. It requires `Python 3.x`, and the following packages installed: `numpy`, `scipy`, `matplotlib`, and `pandas`. In order to use the program, you have to include patients creatinine values in the input folder as `Labsxx.csv` files. If you also want the estimated glomerular filtration rate, then a `Demographics.csv` file is needed with patients identifiers, age, gender, and race, as these variables are used in the GER equation.  

## Input
Please see the current files in the `input` folder as an example of how the files are structured. 

## Output
Upon running `Main.py`, the information in the `Input` folder is proccessed, and the following files are written in the `Output` folder:
- `AKI.csv`: This files contains a list of all patients, their estimated baseline creatinine, and baseline GFR, as well as their peak creatinine levels during their hospitalization.
- `Graphs` folder: This folder contains a list of `.png` names by patients MRNs, and illustrate the patients creatinine trend. 