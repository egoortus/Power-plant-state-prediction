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
