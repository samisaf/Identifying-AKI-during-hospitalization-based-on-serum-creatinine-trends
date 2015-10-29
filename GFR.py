# -*- coding: utf-8 -*-
"""
@author: Sami Safadi
The ckdepi functions calculates an estimated serum creatinine based on the patient's
serum creatinine, age, gender, and race per CKD EPI equation
"""


def ckdepi(cr, age, gender, race):
    """
    141 × min(cr/κ, 1)**α × max(cr/κ, 1)**(-1.209) × 0.993**age × g × r 
    Scr is serum creatinine in mg/dL,
    κ is 0.7 for females and 0.9 for males,
    α is -0.329 for females and -0.411 for males,  
    g is 1.018 for females and 1 for males,
    r is 1.159 for blacks and 1 for other races
    """    
    if gender == "MALE" or gender == "M" or gender == 1: k, a, g = 0.9, -0.411, 1.0
    elif gender == "FEMALE" or gender == "F" or gender == 2: k, a, g = 0.7, -0.329, 1.018
    else: raise Exception("equation undefined for gender:", gender)
    
    r = 1.0
    if race == "BLACK" or race == "B" or race == "AA" or race == 1: r = 1.159

    egfr = 141 * min(cr/k, 1)**a * max(cr/k, 1)**(-1.209) * 0.993**age * g * r
    return egfr

def test():
    print("\n20 year old white male with cr 1.0")
    print("CKD-EPI")
    print("Expect: 107.9 ml/min. Actual:", ckdepi(1.0, 20, 1, 1))
    
    print("\n40 year old black male with cr 1.5")
    print("CKD-EPI")
    print("Expect: 66.4 ml/min. Actual:", ckdepi(1.5, 40, 1, 2))
    
    print("\n80 year old white female with cr 2.0")
    print("CKD-EPI")
    print("Expect: 23.1 ml/min. Actual:", ckdepi(2, 80, 2, 1))
    
    print("\n50 year old black female with cr 1.1")
    print("CKD-EPI")
    print("Expect: 67.6 ml/min. Actual:", ckdepi(1.1, 50, 2, 2))

if __name__ == "__main__":
    print("Some tests...")
    test()