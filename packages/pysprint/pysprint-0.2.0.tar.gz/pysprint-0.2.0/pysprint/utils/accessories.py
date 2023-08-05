from functools import wraps

import numpy as np
from scipy.interpolate import interp1d
import scipy.stats as st

__all__ = ['scipy_disp', 'lmfit_disp', 'findNearest', 'find_closest',
           '_handle_input', 'print_disp', 'fourier_interpolate',
           'between', 'get_closest', 'run_from_ipython',
           'calc_envelope', 'measurement']



def calc_envelope(x, ind, mode='u'):
    '''Source: https://stackoverflow.com/a/39662343/11751294
    '''
    x_abs = np.abs(x)
    if mode == 'u':
    	loc = np.where(np.diff(np.sign(np.diff(x_abs))) < 0)[0] + 1
    elif mode == 'l':
    	loc = np.where(np.diff(np.sign(np.diff(x_abs))) > 0)[0] + 1
    else:
    	raise ValueError('mode must be u or l.')
    peak = x_abs[loc]
    envelope = np.interp(ind, loc, peak)
    return envelope, peak, loc

def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def get_closest(xValue, xArray, yArray):
	idx = (np.abs(xArray - xValue)).argmin()
	value = xArray[idx]
	return value, yArray[idx], idx

def between(val, except_around):
	if except_around is None:
		return False
	elif len(except_around) != 2:
		raise ValueError(f'Invalid interval. Try [start, end] instead of {except_around}')
	else:
		lower = float(min(except_around))
		upper = float(max(except_around))
	if val <= upper and val >= lower:
		return True
	return False

def scipy_disp(r):
	for idx in range(len(r)):
		dispersion[idx] = dispersion[idx] * factorial(idx+1)
		dispersion_std[idx] = dispersion_std[idx] * factorial(idx+1)
	return dispersion, dispersion_std


def lmfit_disp(r):
	dispersion, dispersion_std = [], []
	for name, par in r:
		dispersion.append(par.value)
		dispersion_std.append(par.stderr)
	return dispersion, dispersion_std


def measurement(array, confidence=0.95):
	"""
	Give the measurement results with condifence interval
	assuming the standard deviation is unknown.

	Parameters
	----------

	array : ndarray
		The array containing the measured values

	confidence : float
		The desired confidence level. Must be between 0 and 1.

	Returns
	-------

	mean: float
	The mean of the given array

	conf: tuple-like (interval)
	The confidence interval

	Example(s)
	---------
	>>> import numpy as np
	>>> from pysprint import measurement
	>>> a = np.array([123.783, 121.846, 122.248, 125.139, 122.569])
	>>> mean, interval = measurement(a, 0.99)
	123.117000 ± 2.763022
	>>> mean
	123.117
	>>> interval
	(120.35397798230359, 125.88002201769642)

	Notes
	-----

	I decided to print the results immediately, because people often don't use
	it for further code. Of course, they are also returned if needed.

	"""
	mean = np.mean(array)
	conf = st.t.interval(confidence, len(array)-1, loc=mean, scale=st.sem(array))
	print(f'{mean:5f} ± {(mean-conf[0]):5f}')
	return mean, conf


def findNearest(array, value):
	#Finds the nearest element to the given value in the array
	#returns tuple: (element, element's index)
	
    array = np.asarray(array)
    idx = (np.abs(value - array)).argmin()
    return array[idx], idx


def _handle_input(initSpectrumX, initSpectrumY, referenceArmY, sampleArmY):
	"""
	Instead of handling the inputs in every function, there is this private method.

	Parameters
	----------

	initSpectrumX: array-like
	x-axis data

	initSpectrumY: array-like
	y-axis data

	referenceArmY, sampleArmY: array-like
	reference and sample arm spectrum evaluated at initSpectrumX

	Returns
	-------
	initSpectrumX: array-like
	unchanged x data

	Ydata: array-like
	the transformed y data

	"""
	if (len(initSpectrumX) > 0) and (len(referenceArmY) > 0) and (len(sampleArmY) > 0):
		Ydata = (initSpectrumY - referenceArmY - sampleArmY) / (2 * np.sqrt(referenceArmY * sampleArmY))
	elif (len(referenceArmY) == 0) or (len(sampleArmY) == 0):
		Ydata = initSpectrumY
	elif len(initSpectrumX) == 0:
		raise ValueError('Please load the spectrum!\n')
	elif len(initSpectrumY) == 0:
		raise ValueError('Please load the spectrum!\n')
	else:
		raise TypeError('Input types are wrong.\n')
	return initSpectrumX,  Ydata


def find_closest(xValue, xArray, yArray):
	idx = (np.abs(xArray - xValue)).argmin()
	value = xArray[idx]
	return value, yArray[idx]


def print_disp(f):
    @wraps(f)
    def wrapping(*args, **kwargs):
        disp, disp_std, stri = f(*args, **kwargs)
        labels = ('GD', 'GDD','TOD', 'FOD', 'QOD')
        for i, (label, disp_item, disp_std_item) in enumerate(zip(labels, disp, disp_std)):
             print(f'{label} = {disp_item:.5f} ± {disp_std_item:.5f} fs^{i+1}')
        return disp, disp_std, stri
    return wrapping


def fourier_interpolate(x, y):
    ''' Simple linear interpolation for FFTs'''
    xs = np.linspace(x[0], x[-1], len(x))
    intp = interp1d(x, y, kind='linear', fill_value='extrapolate')
    ys = intp(xs)
    return xs, ys
