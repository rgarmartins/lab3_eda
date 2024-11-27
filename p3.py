import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#import csv file id-v-microled and create dataframe 
df = pd.read_csv('id-v-microled.csv')

#only plot id-v curve between 10nA and 3uA
df = df[(df['/I2/p1 Y'] > 10e-9) & (df['/I2/p1 Y'] < 3e-6)]

#plot
plt.figure(1, figsize=(10,6))
plt.plot(df['/I2/p1 X'], df['/I2/p1 Y']*1e6, 'ro')
plt.xlabel('Vgs (V)')
plt.ylabel('Id (uA)')
plt.title('Id-V curve')
plt.grid()

ut = 0.026

def obtainId1(vgs,Is, vt):
    return Is * (np.exp((vgs-vt)/ut) - 1)

#curve fitting
[Is,vt], pcov = curve_fit(obtainId1, df['/I2/p1 X'], df['/I2/p1 Y'],p0=(1e-3,1))

print('-------------------------ESTIMATION 1 -------------------------')
print('Is = ', Is)
print('vt = ', vt)

#plot
plt.figure(2, figsize=(10,6))
plt.plot(df['/I2/p1 X'], df['/I2/p1 Y']*1e6, 'ro', label='Experimental')
plt.plot(df['/I2/p1 X'], obtainId1(df['/I2/p1 X'], Is, vt)*1e6, 'b-', label  = 'Theoretical')
plt.legend(loc='best')
plt.xlabel('Vgs (V)')
plt.ylabel('Id (uA)')
plt.title('Id-V curve')
plt.grid()


def obtainId2(vgs,Is, vt, n):
    return Is * (np.exp((vgs-vt)/(n*ut)) - 1)

#curve fitting
#[Is,vt,n], pcov = curve_fit(obtainId2, df['/I2/p1 X'], df['/I2/p1 Y'], bounds=  ([0,0,0],[1e-10,1.7,1.5]))
[Is,vt,n], pcov = curve_fit(obtainId2, df['/I2/p1 X'], df['/I2/p1 Y'], p0=(1e-3,1,1))

print('-------------------------ESTIMATION 2 -------------------------')
print('Is = ', Is)
print('vt = ', vt)
print('n = ', n)

#plot
plt.figure(3, figsize=(10,6))
plt.plot(df['/I2/p1 X'], df['/I2/p1 Y']*1e6, 'ro', label='Experimental')
plt.plot(df['/I2/p1 X'], obtainId2(df['/I2/p1 X'], Is, vt, n)*1e6, 'b-', label  = 'Theoretical')
plt.legend(loc='best')
plt.xlabel('Vgs (V)')
plt.ylabel('Id (uA)')
plt.title('Id-V curve')
plt.grid()


def obtainId3(vgs,Is, vt, n, rs):
    return Is * (np.exp((vgs-vt-rs*Is)/(n*ut)) - 1) 

#curve fitting
[Is,vt,n,rs], pcov = curve_fit(obtainId3, df['/I2/p1 X'], df['/I2/p1 Y'])

print('-------------------------ESTIMATION 3 -------------------------')
print('Is = ', Is)
print('vt = ', vt)
print('n = ', n)
print('rs = ', rs)

#plot
plt.figure(4, figsize=(10,6))
plt.plot(df['/I2/p1 X'], df['/I2/p1 Y']*1e6, 'ro', label='Experimental')
plt.plot(df['/I2/p1 X'], obtainId3(df['/I2/p1 X'], Is, vt, n, rs)*1e6, 'b-', label  = 'Theoretical')
plt.legend(loc='best')
plt.xlabel('Vgs (V)')
plt.ylabel('Id (uA)')
plt.title('Id-V curve')
plt.grid()
plt.show()
