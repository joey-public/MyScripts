import numpy as np

# beta = rolloff factor
# span = number of symbol periods
# sps = number of samples per symbol
def pulse_rcos(beta, span, sps, shape='sqrt'):
    N = span*sps #number of samples in the filter
    T = 1 #assumed symbol period of 1
    t = (1/sps)*np.arange(-N/2, N/2+1)
    if beta==0:
        h = np.sinc(t)
        if (shape=='sqrt'): h = np.sqrt(h)
        return h
    numerator = np.cos(np.pi*beta*t)*np.sinc(t)
    denominator = 1-np.power(2*beta*t,2) 
    h = numerator/denominator
    h[len(h)//2]=1
    for i,val in enumerate(t):
        if np.absolute(val) == 1/(2*beta):
            h[i] = (np.pi/4) * np.sinc(1/(2*beta)) 
    if (shape=='sqrt'): h = np.sqrt(np.absolute(h))
    return h

def pulse_rect():
    pass

def pulse_gause(bt, span, sps):
    pass

def pulse_delta():
    pass
