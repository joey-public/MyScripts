import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

from my_ofdm import * 

def my_psd(x):
    dft = np.fft.fft(x)
    return dft*np.conjugate(dft)

def sim1(CP_LEN, FIG_NUM1, FIG_NUM2, FILE_NAME1, FILE_NAME2, SUPTITLE):
    N = 32 #fft length 
    L = 1000  #number of ofdm frames
    alphabet = [-1+1j, 1+1j, 
                -1-1j, 1-1j] #QPSK subchannels
    
    h = np.zeros(N)
    h[0] = 1
    h[N//2-1] = -1
    
    tx_f_syms = gen_rand_symbols((N,L), alphabet)
    tx_t_samp = modulate_ofdm(tx_f_syms)
    tx_t_samp_cp = add_cp(tx_t_samp, CP_LEN)
    tx_signal = p2s_conv(tx_t_samp_cp)
    
    #shifted_tx_signal = np.zeros(tx_signal.size)
    #shifted_tx_signal[tx_signal.size//2:tx_signal.size] = tx_signal[0:tx_signal.size//2]
    #rx2 = tx_signal + shifted_tx_signal
    
    rx_signal = sp.signal.lfilter(h, (1), tx_signal)
    #rx_signal = np.convolve(h, tx_signal, 'same')
    #rx_signal = np.convolve(h, tx_signal)[0:tx_signal.size]
    
    rx_t_samp_cp = s2p_conv(rx_signal, N, L, CP_LEN)
    rx_t_samp = remove_cp(rx_t_samp_cp, CP_LEN)
    rx_f_syms = demodulate_ofdm(rx_t_samp)
#    rx_f_syms = equalize(rx_f_syms, np.fft.fft(h))
    
    plt.figure(FIG_NUM1)
    plt.suptitle(SUPTITLE)
    plt.subplot(211)
    plt.plot(my_psd(tx_signal))
    plt.title('Transmitted Signal PSD')
    plt.xlabel('k')
    plt.ylabel('Magnitude')
    plt.subplot(212)
    plt.plot(my_psd(rx_signal))
    plt.title('Received Signal PSD')
    plt.xlabel('k')
    plt.ylabel('Magnitude')
    plt.tight_layout()
    plt.savefig(FILE_NAME1)
    
    plt.figure(FIG_NUM2)
    plt.suptitle(SUPTITLE)
    ch = 0
    spl = 1
    for i in range(32):
        temp = rx_f_syms[ch,:]
        plt.subplot(4,8,spl)
        plt.scatter(np.real(temp), np.imag(temp))
        plt.text(-3,3,'Sub Ch: {}'.format(ch))
        ch += 1
        spl+= 1
        plt.xlim(-4,4)
        plt.ylim(-4,4)
    plt.tight_layout()
    plt.savefig(FILE_NAME2)
#    plt.subplot(221)
#    temp = rx_f_syms[0,:]
#    plt.scatter(np.real(temp), np.imag(temp))
#    plt.title('Channel 0 RX Constellation')
#    plt.xlabel('Real')
#    plt.ylabel('Imag')
#    plt.subplot(222)
#    temp = rx_f_syms[5,:]
#    plt.scatter(np.real(temp), np.imag(temp))
#    plt.title('Channel 5 RX Constellation')
#    plt.xlabel('Real')
#    plt.ylabel('Imag')
#    plt.subplot(223)
#    temp = rx_f_syms[24,:]
#    plt.scatter(np.real(temp), np.imag(temp))
#    plt.title('Channel 24 RX Constellation')
#    plt.xlabel('Real')
#    plt.ylabel('Imag')
#    plt.subplot(224)
#    temp = rx_f_syms[16,:]
#    plt.scatter(np.real(temp), np.imag(temp))
#    plt.title('Channel 16 RX Constellation')
#    plt.xlabel('Real')
#    plt.ylabel('Imag')
#    plt.tight_layout()
#    plt.savefig(FILE_NAME2)

#part a
CP_LEN = 0
SUPTITLE = 'No Cyclic Prefix Constellations' 
sim1(CP_LEN, 1, 2, './images/sim1_1.jpeg','./images/sim1_2.jpeg', SUPTITLE)
#part b 1
CP_LEN = 24 
SUPTITLE = 'L=24 Cyclic Prefix Contellations' 
sim1(CP_LEN, 3, 4, './images/sim1_3.jpeg','./images/sim1_4.jpeg', SUPTITLE)
#part b 2
CP_LEN = 8 
SUPTITLE = 'L=8 Cyclic Prefix Constellations' 
sim1(CP_LEN, 5, 6, './images/sim1_5.jpeg','./images/sim1_6.jpeg', SUPTITLE)
plt.show()
