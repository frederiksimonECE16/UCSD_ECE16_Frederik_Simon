from ECE16Lib.HRMonitor import HRMonitor
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

#instantiate HR object knowing that we have 1 minute of data at sampling rate of 50Hz
hr_monitor = HRMonitor(3000, 50)


def eval_hr_monitor():

    #initialize arrays
    estimates = np.array([])
    ground_truth = np.array([])

    index_samples = 0
    
    #list of the names of the data files 
    file_paths = [
        "./data/U10310072/U10310072_01_75.csv",
        "./data/U10310072/U10310072_02_72.csv",
        "./data/U10310072/U10310072_03_70.csv",
        "./data/U10310072/U10310072_04_93.csv",
        "./data/U10310072/U10310072_05_70.csv",
    ]

    for file_path in file_paths:

        #extract data from files
        data = np.genfromtxt(file_path, delimiter=",")
        t = data[:,0]
        t = (t - t[0])/1e3
        ppg = data[:,1]

        hr_monitor.add(t, ppg)
        hr, peaks, filtered = hr_monitor.process()

        estimates = np.append(estimates, hr)

        #reset for next file 
        hr_monitor.reset()


    ground_truth = np.array([75,72,70,93,70]) # reference heart rates
    
    #fake data
    #ground_truth = np.array([63, 56, 96, 79, 63, 120, 152, 111, 95, 57])
    #estimates =    np.array([65, 54, 96, 71, 63, 127, 159, 115, 104, 54])

    [R,p] = stats.pearsonr(ground_truth, estimates) # correlation coefficient

    plt.figure(1)
    plt.clf()

    # Correlation Plot
    plt.subplot(211)
    plt.plot(estimates, estimates)
    plt.scatter(ground_truth, estimates)

    plt.ylabel("Estimated HR (BPM)")
    plt.xlabel("Reference HR (BPM)")
    plt.title("Correlation Plot: Coefficient (R) = {:.2f}".format(R))

    # Bland-Altman Plot
    avg = (ground_truth+estimates)/2 # take the average between each element of the ground_truth and
                                     # estimates arrays and you should end up with another array
    dif = ground_truth - estimates # take the difference between ground_truth and estimates
    std = np.std(dif) # get the standard deviation of the difference (using np.std)
    bias = np.mean(dif)# get the mean value of the difference
    upper_std = bias + 1.96*std # the bias plus 1.96 times the std
    lower_std = bias - 1.96*std # the bias minus 1.96 times the std

    plt.subplot(212)
    plt.scatter(avg, dif)

    plt.plot(avg, len(avg)*[bias])
    plt.plot(avg, len(avg)*[upper_std])
    plt.plot(avg, len(avg)*[lower_std])

    plt.legend(["Mean Value: {:.2f}".format(bias),
    "Upper bound (+1.96*STD): {:.2f}".format(upper_std),
    "Lower bound (-1.96*STD): {:.2f}".format(lower_std)
    ])

    plt.ylabel("Difference between estimates and ground_truth (BPM)")
    plt.xlabel("Average of estimates and ground_truth (BPM)")
    plt.title("Bland-Altman Plot")
    plt.show()
    print(estimates)


eval_hr_monitor()