# -*- coding: utf-8 -*-
"""
@author: Sami Safadi
The Patient class represents a patient along with his/her demographic information (number, age, gender, and race)
as well as serum creatinine values. The creatinine values are oganized chornologically. 

Baseline creatinine is calculated based on the creatinines before the admission date. Two variables can be tweaked:
WINDOW: timeframe in days within which creatinine values are used
MEASUREFUNC: is how the baseline creatinine is estimated
For example, if baseline creatinine is defined as the median creatinine within 6 months before hospitalization, 
then WINDOW = 180, and MEASUREFUNC = median.

Peak creatinine is defiend as the highest creatinine during the patient's hospitalization.
AKI during hospitalization can the be easily calculated via comparing the baseline creatinine, and the peak creatinine.
"""

import GFR
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

WINDOW = pd.DateOffset(days = 6 * 30) # 180 days
MEASUREFUNC = np.median

class Patient(object):
    """
    Represents a patient along with his/her demographic information and serum creatinine values
    mrn: medical record number (number)
    age: age in years (ca)
    gender: gender (character or integer)
    race: race (character or integer)
    admissiondate : Date of admission (string)
    dischargedate: Date of discharge (string)
    crs: dictionary containing serum creatinines, the key is the date on which the test was done     
    """
    def __init__(self, mrn, age = 0, gender = 0, race = 0, admissionDate = None, dischargeDate = None, crs = {}):
        self.mrn = mrn
        self.age = age
        self.gender = gender
        self.race = race
        self.admissionDate = pd.to_datetime(admissionDate)
        self.dischargeDate = pd.to_datetime(dischargeDate)
        
        temp = DataFrame(Series(crs), columns=['value'])
        temp.index = pd.to_datetime(temp.index)
        indexDate = self.admissionDate - WINDOW
        self.crsAll = temp.value               
        self.crsBeforeAdmission = self.crsAll.ix[(self.crsAll.index < admissionDate) & (self.crsAll.index > indexDate)]
        self.crsDuringAdmission = self.crsAll.ix[(self.crsAll.index >= admissionDate) & (self.crsAll.index <= dischargeDate)]
        if self.crsAll.size > 0: self.initialize()
        
    def initialize(self): 
        self.baseCr = self.__calcBaseCr__() # calculate the baseline creatiniine 
        self.peakCr = self.__calcPeakCr__() # calculate the peak creatinine during the patient's admission
        
        try: self.admitCr = self.crsAll[self.admissionDate] # calculate creatinine value on admission       
        except: self.admitCr = np.NaN
        
        try: self.egfr = GFR.ckdepi(self.baseCr, self.age, self.gender, self.race)
        except: self.egfr = np.NaN
        
    def __str__(self): 
        temp = "<MRN {}, Age {}, Gender {}, Race {}, Hosp. {},  Num CRS {}>"\
            .format(self.mrn, self.age, self.gender, self.race, self.admissionDate, self.crsAll.size)
        return temp

    def __repr__(self): 
        return self.__str__()
    
    def __calcBaseCr__(self):
        try: self.minCr = np.min(self.crsBeforeAdmission) # calculate the minimum creatinine ever      
        except: self.minCr = np.NaN
        
        try: self.cr25 = np.percentile(self.crsBeforeAdmission, 25) # calculate the 25% creatinine
        except: self.cr25 = np.NaN
        
        try: self.baseCr = MEASUREFUNC(self.crsBeforeAdmission)
        except: self.baseCr = np.NaN
        
        return self.baseCr
    
    def __calcPeakCr__(self):
        return np.max(self.crsDuringAdmission)
        
    def plot(self):
        plt.hlines(self.baseCr, self.crsAll.index.min(), self.crsAll.index.max(), linestyles='dotted')
        plt.plot(self.crsAll.index, self.crsAll.values)        
        plt.plot(self.crsAll.index, self.crsAll.values, 'g.')
        plt.title(str(self))
        plt.xlabel("Date")
        plt.ylabel("Creatinine")

def testPatient():
    print ("Running some tests")
       
    values = [ 1.8,  2.2,  2. ,  2.8,  3. ,  3.3,  3.4,  3.4,  3.5,  3.7,  4., 
        3.7,  3.7,  3.9,  4.1,  4. ,  3.8,  3.9,  3.9,  4.1,  3.9,  3.9, 
        4.3,  4.5,  4.8,  5. ,  5.2,  5. ,  3.8,  4.2,  4.7,  5.1,  4.6, 
        5.2,  5.2,  4.9,  4.7,  4.7,  5.1,  4.6,  5.5,  5.5,  5.3,  5.3, 
        5.9,  6.1,  6.1,  6.1,  6. ,  5.9,  6.8,  6.3,  7. ,  6.9,  7.9, 
        7.9,  6.8,  6.3,  6.4,  6.6,  6.9,  6.6,  7. ,  7.7,  7.5,  8.3, 
        6.8,  6.9,  6.6,  6.8,  6.6,  6.9,  6.9,  7. ,  6.5,  8. ,  8.3, 
        8.2,  8.7,  8.5,  8. ,  8.1,  7.6,  8.4,  8.9,  7.3,  9.5,  6.8, 
        9.5,  8.2,  8. ,  8.2,  8.5,  8.4,  7.6,  8.1,  9.5] 
    
    dates = ['2009-02-02', '2009-06-30', '2009-07-01', '2009-10-15',
               '2010-01-13', '2010-11-08', '2010-11-09', '2010-11-10',
               '2010-11-12', '2010-11-13', '2010-11-14', '2010-11-15',
               '2010-11-16', '2010-11-17', '2010-11-18', '2010-11-19',
               '2010-11-20', '2010-11-21', '2010-11-22', '2010-11-23',
               '2010-11-24', '2010-11-25', '2010-11-26', '2010-11-27',
               '2010-11-28', '2010-11-29', '2010-11-30', '2010-12-01',
               '2010-12-16', '2011-01-19', '2011-05-02', '2011-06-01',
               '2011-06-23', '2011-07-07', '2011-08-16', '2011-09-22',
               '2011-10-24', '2011-11-23', '2011-12-21', '2012-01-03',
               '2012-01-04', '2012-01-05', '2012-01-06', '2012-01-07',
               '2012-01-09', '2012-01-11', '2012-01-13', '2012-01-16',
               '2012-01-18', '2012-02-06', '2012-03-07', '2012-04-10',
               '2012-05-01', '2012-05-02', '2012-05-14', '2012-06-11',
               '2012-06-25', '2012-06-27', '2012-06-28', '2012-06-29',
               '2012-06-30', '2012-07-01', '2012-07-02', '2012-07-09',
               '2012-07-18', '2012-08-28', '2012-09-20', '2012-10-18',
               '2012-11-15', '2012-12-20', '2013-01-17', '2013-02-21',
               '2013-03-21', '2013-04-18', '2013-05-16', '2013-06-20',
               '2013-07-18', '2013-08-22', '2013-09-19', '2013-10-17',
               '2013-11-21', '2013-12-19', '2014-01-23', '2014-02-20',
               '2014-03-20', '2014-04-02', '2014-04-03', '2014-04-04',
               '2014-04-17', '2014-05-22', '2014-06-19', '2014-07-17',
               '2014-08-21', '2014-09-18', '2014-10-16', '2014-11-20',
               '2014-12-18']        
    data = {}
    for i in range(len(values)): data[dates[i]] = values[i]    
    mrn = 1 
    age = 55
    gender = 'M'
    race = 'C'
    admissionDate = '2014-04-01'
    dischargeDate = '2014-04-04'
    demoPt1 = Patient(mrn, age, gender, race, admissionDate, dischargeDate, data)
    
    values = [ 0.9,  0.8,  0.9,  0.9,  0.8,  0.8,  1.1,  0.8,  0.8,  0.8,  1. ,
        1. ,  0.7,  0.7,  0.7,  0.7,  0.6,  0.6,  0.6,  0.7,  0.6,  0.6,
        0.6,  0.7,  0.9,  0.9,  1. ,  1. ,  0.9,  0.9,  0.8,  0.8,  0.9,
        0.6,  0.6,  0.6,  0.6,  0.6]
        
    dates = ['2009-09-30', '2010-01-29', '2010-11-24', '2011-03-03',
               '2012-06-13', '2012-06-14', '2012-06-15', '2012-06-16',
               '2012-06-17', '2012-06-18', '2012-06-19', '2012-06-20',
               '2012-06-21', '2012-06-22', '2012-06-23', '2012-06-24',
               '2012-06-25', '2012-06-30', '2012-07-01', '2012-07-02',
               '2012-07-03', '2012-07-05', '2012-07-06', '2012-08-02',
               '2012-09-27', '2012-12-20', '2013-03-14', '2013-07-25',
               '2013-12-05', '2014-03-06', '2014-04-10', '2014-07-17',
               '2014-08-04', '2014-08-06', '2014-08-08', '2014-08-26',
               '2014-09-25', '2014-10-01']
    data = {}
    for i in range(len(values)): data[dates[i]] = values[i]
    mrn = 2
    age = 64
    gender = 'F'
    race = 'C'
    admissionDate = '2014-08-04'
    dischargeDate = '2014-08-08'
    demoPt2 = Patient(mrn, age, gender, race, admissionDate, dischargeDate, data)
    
    values = [ 1.2,  1.1,  1.1,  1.1,  1.1,  1.1,  1. ,  1.1,  0.9,  1. ,  0.8,
        0.9,  0.8,  1.2,  0.9,  0.9,  1.1,  1.1,  0.9,  0.9,  0.9,  1.2,
        1.1,  1.1,  1. ,  1. ,  1.1,  1.2,  1. ,  0.8,  1. ,  0.9,  0.9,
        1. ,  0.9,  1. ,  0.9,  0.9,  0.8,  0.7,  0.8,  0.8,  0.9,  2. ,
        3.1,  3.3,  4. ]
        
    dates = ['2012-06-26', '2012-07-16', '2012-08-08', '2012-08-24',
               '2012-09-17', '2012-10-17', '2012-11-01', '2012-11-29',
               '2012-12-27', '2013-01-05', '2013-01-07', '2013-01-08',
               '2013-02-14', '2013-05-01', '2013-05-31', '2013-06-13',
               '2013-07-17', '2013-08-16', '2013-08-29', '2013-09-12',
               '2013-09-30', '2013-10-10', '2013-11-04', '2013-11-25',
               '2013-12-30', '2014-04-03', '2014-05-12', '2014-05-19',
               '2014-06-09', '2014-07-01', '2014-07-08', '2014-07-22',
               '2014-08-21', '2014-09-02', '2014-09-09', '2014-09-18',
               '2014-09-29', '2014-10-23', '2014-11-03', '2014-11-04',
               '2014-11-05', '2014-11-06', '2014-11-11', '2014-11-14',
               '2014-11-25', '2014-11-26', '2014-11-29']
    data = {}
    for i in range(len(values)): data[dates[i]] = values[i]
    mrn = 3
    age = 43
    gender = 'M'
    race = 'C'
    admissionDate = '2014-11-29'
    dischargeDate = '2014-11-30'
    demoPt3 = Patient(mrn, age, gender, race, admissionDate, dischargeDate, data)
    
    print(demoPt1)
    print(demoPt2)
    print(demoPt3)
    print(demoPt2.plot())
    
if __name__ == "__main__":
    testPatient()