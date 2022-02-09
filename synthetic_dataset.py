import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from riverdata import RiverData
import netCDF
import math


class SyntheticDataset:

    def __init__(self, root, time_steps, Tref, C, Tao, ey, ez, er):

        self.time_steps = time_steps

        self.root = root
        self.C = C
        self.Tao = Tao
        self.ey = ey
        self.ez = ez
        self.er = er
        self.X1 = list(np.zeros(15))
        self.X2 = list(np.zeros(15))
        self.X3 = list(np.zeros(15))
        self.X4 = list(np.zeros(15))
        self.X5 = list(np.zeros(15))
        self.X6 = list(np.zeros(15))
        self.X7 = list(np.zeros(15))
        self.X8 = list(np.zeros(15))
        self.X9 = list(np.zeros(15))
        self.X10 = list(np.zeros(15))

    def normalize(self, var):
        nvar = (np.array(var) - np.mean(var)) / np.std(var)
        return nvar

    def down_sample(self, data, win_size):
        agg_data = []
        monthly_data = []
        for i in range(len(data)):
            monthly_data.append(data[i])
            if (i % win_size) == 0:
                agg_data.append(sum(monthly_data) / win_size)
                monthly_data = []
        return agg_data

    def generate_data(self):

        for t in range(10, self.time_steps):

            self.X1.append(self.root[t])
            self.X2.append(C.get('c1') * self.X1[t - Tao.get('t1')] + ey[t])
            self.X3.append(C.get('c2') ** ((self.X1[t - Tao.get('t2')]) / 2 + ez[t]))
            self.X4.append(C.get('c3') * self.X3[t - Tao.get('t3')] + C.get('c4') * self.X2[t - Tao.get('t4')] + er[t])

        return self.X1, self.X2, self.X3, self.X4

    def SNR(self, s, n):

        Ps = np.sqrt(np.mean(np.array(s)**2))
        Pn = np.sqrt(np.mean(np.array(n)**2))
        SNR = Ps/Pn
        return 10*math.log(SNR, 10)        # 10*math.log(((Ps-Pn)/Pn), 10)


if __name__ == '__main__':

    # River data as base
    dataobj = RiverData()
    data = dataobj.get_data()
    xts = data['Kempten']
    yts = data['Dillingen']
    zts = data['Lenggries']

    Fs = 10000
    f = 25
    sample = 10000
    t = np.arange(sample)
    pattern = 0.5 * np.sin(np.pi * 3 * f * t * t / Fs)
    signal = 2 * np.sin(2 * np.pi * f * t / Fs)
    intrinsic_noise = np.random.normal(0, 0.10, 10000)
    roots = np.abs(signal) + pattern + intrinsic_noise
    # roots = xts + root[0: len(xts)]

    time_steps, Tref = round(len(roots)), 15
    ey = np.random.normal(0, 0.05, time_steps)
    ez = np.random.normal(0, 0.15, time_steps)
    er = np.random.normal(0, 0.10, time_steps)

    C = {'c1': 0.75, 'c2': 0.25, 'c3': 0.75, 'c4': 0.90, 'c5': 0.80}          # c2:1.75, c5:1.85
    Tao = {'t1': 2, 't2': 1, 't3': 4, 't4': 3, 't5': 5, 't6': 6}
    data_obj = SyntheticDataset(roots, time_steps, Tref, C, Tao, ey, ez, er)
    X1, X2, X3, X4 = data_obj.generate_data()

    corr1 = np.corrcoef(ey, ez)

    print("Correlation Coefficient (ey, ez): ", corr1)
    # print("SNR (Temperature)", data_obj.SNR(Yts, ez))

    data = {'Z1': X1[150:], 'Z2': X2[150:], 'Z3': X3[150:], 'Z4': X4[150:]}
    df = pd.DataFrame(data, columns=['Z1', 'Z2', 'Z3', 'Z4'])
    df.to_csv(r'/home/ahmad/PycharmProjects/deepCause/datasets/ncdata/synthetic_data.csv', index_label=False, header=True)
    print(df.head(100))

    fig = plt.figure()
    ax1 = fig.add_subplot(411)
    ax1.plot(X1[15:1500])
    ax1.set_ylabel('X1')

    ax2 = fig.add_subplot(412)
    ax2.plot(X2[15:1500])
    ax2.set_ylabel("X2")

    ax3 = fig.add_subplot(413)
    ax3.plot(X3[15:1500])
    ax3.set_ylabel("X3")

    ax4 = fig.add_subplot(414)
    ax4.plot(X4[15:1500])
    ax4.set_ylabel("X4")
    plt.show()