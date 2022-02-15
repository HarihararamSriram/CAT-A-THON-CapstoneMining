import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from intropandas import X, Y, Y_threshold, s1, s2, s3, max_sev, cur_sev, candidate, event
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, accuracy_score

max_sev_list = list()
s1lis, s2lis, s3lis = list(), list(), list()
s = [s1, s2, s3]
#Preparing the constant value for to be plotted.
for i in range(len(X)):
    max_sev_list.append(Y_threshold)
    s1lis.append(s1)
    s2lis.append(s2)
    s3lis.append(s3)

max_sev_list = np.array(max_sev_list)
s1lis, s2lis, s3lis = np.array(s1lis), np.array(s2lis), np.array(s3lis),

# Visualizing the Polymonial Regression results
def viz_polymonial():
    #This function is used for drawing the prediction graph which is our units (Y) vs date (X) 
    X1 = list()
    for i in X:
        temp = np.array([i,])
        X1.append(temp)
    Y1 = Y
    try:
        X_train, X_test, Y_train, Y_test = train_test_split(X1, Y1, test_size=0.2, random_state=0)
    except:
        print("Insufficient number of samples for regression analysis.")
        return
    poly_reg = PolynomialFeatures(degree=4)
    X_poly1 = poly_reg.fit_transform(X1)
    pol_reg = LinearRegression()
    pol_reg.fit(X_poly1, Y1)
    score = r2_score(Y, pol_reg.predict(poly_reg.fit_transform(X1)))
    print(score)
    plt.scatter(X1, Y1, color='green')
    plt.plot(X1, pol_reg.predict(poly_reg.fit_transform(X1)), color='blue')
    
    plt.plot(X1, max_sev_list, color='red')
    for i in s1lis, s2lis, s3lis:
        plt.plot(X1, i, color='yellow')
    
    plt.title('Threshold prediction')
    plt.xlabel('date')
    plt.ylabel('weighted units')
    plt.show()
    
    fin_date = X1[len(X1)-1][0]
    i = fin_date
    reachdate_list = [None, None, None]
    end_list = [False, False, False]
    
    
    if(pol_reg.predict(poly_reg.fit_transform( [[ i ]]) )) > pol_reg.predict(poly_reg.fit_transform( [[ i+4 ]]) ):
        print("The candidate can be operated safely because the severity level is decreasing and replacement can be done after many dates.")
    else:
        while pol_reg.predict(poly_reg.fit_transform( [[ i ]]) )<Y_threshold:
            pred_val = pol_reg.predict(poly_reg.fit_transform( [[ i ]]) )
            for j in range(cur_sev-1):
                if(pred_val>s[j] and end_list[j]==False):
                    reachdate_list[j] = i
                    end_list[j] = True
            i+=4
        #print(r2_score(Y1, pol_reg.predict(poly_reg.fit_transform( X1)) ))   
        print("Candidate:", candidate)
        print("Event(sensor):", event)
        print("\n---------------------------------\n\
The date when threshold is hit: ", i)
        threshold_date = i
        for i in range(cur_sev-1): 
            if(i==0):
                print("")
            print("The date when severity level reaches {} : {}".format(i+1, reachdate_list[i]))
        print("The current severity level is:", cur_sev)
        print("Criticality:", end=" ")
        replace_within = threshold_date - fin_date
        if(cur_sev==3):
            print("Minor")
        if(cur_sev==2):
            print("Moderately critical")
            print("Replace the candidate within", replace_within, "dates")
        if(cur_sev==1):
            print("Highly critical")
            print("Replace the candidate within", replace_within, "dates")
    return

    

viz_polymonial() # -> Function call for regressional analysis.


