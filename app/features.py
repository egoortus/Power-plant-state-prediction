import numpy as np
import pandas as pd

from scipy import signal

def get_delta(signal_df):
    wnd = [1.0, -1.0]
    return signal_df.apply(lambda s: np.convolve(s, wnd, mode='valid'))


def get_fft(signal_df):
    return signal_df.apply(
        lambda s: signal.spectrogram(
            s,
            nperseg=s.size,
            window='hann',
            scaling='spectrum',
            mode='magnitude'
        )[2].ravel(),
        result_type='expand'
    )


def get_filtered_fir(signal_df):
    window = np.ones(11) / 11
    return signal_df \
        .apply(lambda s: np.convolve(s, window, mode='valid'))


def get_filtered_iir(signal_df):
    a, b = signal.butter(1, 0.01)
    return signal_df.apply(lambda x: signal.filtfilt(a, b, x))
