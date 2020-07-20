"""Module containing some useful functions.
"""

from hmmlearn import hmm
import numpy as np
from sklearn import mixture

def bic_gmm(X):
    """Returns the best GMM with covariance type 'full' for fitting X"""
    lowest_bic = np.infty
    bic = []
    n_components_range = range(1, 7)
    cv_types = ['diag']
    for cv_type in cv_types:
        for n_components in n_components_range:
            # Fit a Gaussian mixture with EM
            gmm = mixture.GaussianMixture(n_components=n_components,
                                          covariance_type=cv_type)
            gmm.fit(X)
            bic.append(gmm.bic(X))
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm
    return (best_gmm, bic)

def bic_general(likelihood_fn, k, X):
    """likelihood_fn: Function. Should take as input X and give out the log likelihood
                      of the data under the fitted model.
       k - int. Number of parameters in the model. The parameter that we are trying to optimize.
                For HMM it is number of states.
                For GMM the number of components.
       X - array. Data that been fitted upon.
    """
    bic = np.log(len(X))*k - 2*likelihood_fn(X)
    return bic

def bic_hmmlearn(X):
    """Fits HMM with different number of states to the data X.
    Then calculates the BIC score for each of the HMMs and returns the one with the lowest score."""
    lowest_bic = np.infty
    bic = []
    n_states_range = range(1,7)
    for n_components in n_states_range:

        hmm_curr = hmm.GaussianHMM(n_components=n_components, covariance_type='diag')
        hmm_curr.fit(X)

        # Calculate number of free parameters
        # free_parameters = for_means + for_covars + for_transmat + for_startprob
        # for_means & for_covars = n_features*n_components
        n_features = hmm_curr.n_features
        free_parameters = 2*(n_components*n_features) + n_components*(n_components-1) + (n_components-1)

        bic_curr = bic_general(hmm_curr.score, free_parameters, X)
        bic.append(bic_curr)
        if bic_curr < lowest_bic:
            lowest_bic = bic_curr
            best_hmm = hmm_curr

    return (best_hmm, bic)

def get_esd_feature(frame_esd):
    """Estimate the features (center_frequency, narrowness)
    from an ESD array.1
    Input - Array. One dimensional of length self.FFT_OUTPUT_SIZE
    Return - List"""
    length_x = len(frame_esd)
    scale = 500

    center_freq = np.argmax(frame_esd)

    # If last two bins (24000 or 23000) or first two bins (0 or 1000)
    # reject it without considering further. It's most probably noise.
    if center_freq > length_x-3 or center_freq < 3:
        return [float('nan'), float('nan')]

    #narrowness = frame_esd[center_freq]/np.sum(frame_esd)
    narrowness = (frame_esd[center_freq]+frame_esd[center_freq+1]+frame_esd[center_freq-1])/np.sum(frame_esd)

    return [scale*center_freq, narrowness]

def naive_filtfilt(b, x):
    """Perform forward backward filtering using moving average coefficients.
    For using with Moving average filters. Not for IIR."""

    # Pad the input signal to reduce transient effects at edges
    pad_left = x[0]*np.ones(len(b)-1)
    pad_right = x[-1]*np.ones(len(b)-1)
    x = np.r_[pad_left, x, pad_right]
    x = np.array(x, dtype='float32')

    # Forward filter
    y0 = np.convolve(x, b, mode='same')
    y0 = np.flipud(y0)
    # Backward Filter
    y0 = np.convolve(y0, b, mode='same')
    y = np.flipud(y0)

    # Remove padding and return
    return y[len(b)-1:-(len(b)-1)]
