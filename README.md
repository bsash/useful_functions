# useful_functions
Various functions that are useful for signal processing and data science tasks.

Available functions:
- bic_gmm: Returns the best GMM, according to Bayesian information criteria, with covariance type 'full' for fitting X.
- bic_hmmlearn: Fits HMM with different number of states to the data X. 
                Then calculates the BIC score for each of the HMMs and returns the one with the lowest score.
- bic_general: Calculates the bayesian information criteria for a likelihood function, with parameters k for data X.
- get_esd_feature: Estimate features (center_frequency, narrowness) from an Energy spectral density array.
- naive_filtfilt: Perform forward backward filtering using moving average coefficients using numpy. 
                  For using with Moving average filters. Not for IIR.
- remove_outliers_iteratively:Gets the percentile of the featureVector and calculates the IQR. 
                              Then removes outliers by checking whether they are outside median+factorIQR*IQR
