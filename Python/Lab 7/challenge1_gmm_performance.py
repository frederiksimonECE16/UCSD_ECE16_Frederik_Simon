# Import for searching a directory
import glob

#import scipy for Band Altman plot
from scipy import stats

# The usual suspects
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt

# The GMM Import
from sklearn.mixture import GaussianMixture as GMM

# Import for Gaussian PDF
from scipy.stats import norm

# Retrieve a list of the names of the subjects
def get_subjects(directory):
  filepaths = glob.glob(directory + "/*")
  return [filepath.split("\\")[-1] for filepath in filepaths]

# Retrieve a data file, verifying its FS is reasonable
def get_data(directory, subject, trial, fs):
  search_key = "%s/%s/%s_%02d_*.csv" % (directory, subject, subject, trial)
  print(search_key)
  filepath = glob.glob(search_key)[0]
  t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
  t = (t-t[0])/1e3
  hr = get_hr(filepath, len(ppg), fs)

  fs_est = estimate_fs(t)
  if(fs_est < fs-1 or fs_est > fs):
    print("Bad data! FS=%.2f. Consider discarding: %s" % (fs_est,filepath))

  return t, ppg, hr, fs_est

# Estimate the heart rate from the user-reported peak count
def get_hr(filepath, num_samples, fs):
  count = int(filepath.split("_")[-1].split(".")[0])
  seconds = num_samples / fs
  return count / seconds * 60 # 60s in a minute

# Estimate the sampling rate from the time vector
def estimate_fs(times):
  return 1 / np.mean(np.diff(times))

# Filter the signal (as in the prior lab)
def process(x):
  x = filt.detrend(x, 25)
  x = filt.moving_average(x, 5)
  x = filt.gradient(x)
  return filt.normalize(x)

# Plot each component of the GMM as a separate Gaussian
def plot_gaussian(weight, mu, var):
  weight = float(weight)
  mu = float(mu)
  var = float(var)

  x = np.linspace(0, 1)
  y = weight * norm.pdf(x, mu, np.sqrt(var))
  plt.plot(x, y)

# Estimate the heart rate given GMM output labels
def estimate_hr(labels, num_samples, fs):
  peaks = np.diff(labels, prepend=0) == 1
  count = sum(peaks)
  seconds = num_samples / fs
  hr = count / seconds * 60 # 60s in a minute
  return hr, peaks

# Run the GMM with Leave-One-Subject-Out-Validation
if __name__ == "__main__":
  fs = 50
  directory = "./data"
  subjects = get_subjects(directory)

  # Leave-One-Subject-Out-Validation
  # 1) Exclude subject
  # 2) Load all other data, process, concatenate
  # 3) Train the GMM
  # 4) Compute the histogram and compare with GMM
  # 5) Test the GMM on excluded subject
  for exclude in subjects:
    print("Training - excluding subject: %s" % exclude)
    train_data = np.array([])
    for subject in subjects:
      for trial in range(1,6):
        t, ppg, hr, fs_est = get_data(directory, subject, trial, fs)

        if subject != exclude:
          train_data = np.append(train_data, process(ppg))

    # Train the GMM
    train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
    gmm = GMM(n_components=2).fit(train_data)

    # Compare the histogram with the GMM to make sure it is a good fit
    plt.hist(train_data, 100, density=True)
    plot_gaussian(gmm.weights_[0], gmm.means_[0], gmm.covariances_[0])
    plot_gaussian(gmm.weights_[1], gmm.means_[1], gmm.covariances_[1])
    plt.show()

    #create variables for plotting the error and computing the RMSE 
    sum_diff = 0
    number_of_samples = 0
    error_array = []
    number_array =[]

    #ground_truth and estimates array for Bland Altman plot
    ground_truth  = np.array([])
    estimates = np.array([])

    # Test the GMM on excluded subject
    print("Testing - all trials of subject: %s" % exclude)
    for trial in range(1,6):
      t, ppg, hr, fs_est = get_data(directory, exclude, trial, fs)
      test_data = process(ppg)

      labels = gmm.predict(test_data.reshape(-1,1))

      hr_est, peaks = estimate_hr(labels, len(ppg), fs)
      print("File: %s_%s: HR: %3.2f, HR_EST: %3.2f" % (exclude,trial,hr,hr_est))

      #calculate error and append to array to plot the error to later plot it 
      error = (hr-hr_est)**2
      error_array.append(error)

      #calculate the sum term from the RMSE
      sum_diff += (hr-hr_est)**2
      
      #count the number of samples 
      number_of_samples += 1
      number_array.append(number_of_samples)

      #create arrays for Bland Altman plot 
      estimates = np.append(estimates, hr_est)
      ground_truth = np.append(ground_truth, hr)
      


      #plt.plot(t, test_data)
      #plt.plot(t, peaks)
      #plt.show()

    RMSE = ((1/number_of_samples)*sum_diff)**(1/2)
    print("RMSE: ", RMSE)

    plt.plot(number_array, error_array)
    plt.show()

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
    
    break