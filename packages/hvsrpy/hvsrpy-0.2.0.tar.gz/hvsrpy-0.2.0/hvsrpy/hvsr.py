# This file is part of hvsrpy a Python module for horizontal-to-vertical
# spectral ratio processing.
# Copyright (C) 2019-2020 Joseph P. Vantassel (jvantassel@utexas.edu)
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https: //www.gnu.org/licenses/>.

"""File for Horizontal-to-Vertical Spectral Ratio (Hvsr) class."""

import numpy as np
import scipy.signal as sg
import logging
logger = logging.getLogger(__name__)


class Hvsr():
    """Class for creating and manipulating horizontal-to-vertical
    spectral ratio objects.

    Attributes
    ----------
    amp : ndarray
        Array of H/V amplitudes. Each row represents an individual
        curve and each column a frequency.
    frq : ndarray
        Vector of frequencies corresponds to each column.
    n_windows : int
        Number of windows in `Hvsr` object.
    valid_window_indices : ndarray
        Array of indices indicating valid windows.
    rejected_window_indices : ndarray
        Array of indices indicating rejected windows.
    peak_frq : ndarray
        Frequency peaks, one per valid time window.
    peak_amp : ndarray
        Amplitude(s) which correspond to `peak_frq`.
    """
    @staticmethod
    def _check_input(name, value):
        """Basic check on input values.

        Specifically;
            1. `value` must be of type `list`, `tuple`, `ndarray`.
            2. If `value` is not `ndarray`, convert to `ndarray`.
            3. `value` must be >=0.

        Parameters
        ----------
        name : str
            Name of `value` to be checked, used solely for
            meaningful error messages.
        value : any
            Value to be checked.

        Returns
        -------
        ndarray
            `values` in correct format.

        Raises
        ------
        TypeError
            If `value` is not one of the types specified.
        ValueError
            If `value` contains a negative values.
        """

        if type(value) not in [list, tuple, np.ndarray]:
            msg = f"{name} must be of type `ndarray`, not `{type(value)}`."
            raise TypeError(msg)
        if type(value) in [list, tuple]:
            value = np.array(value)
        if np.sum(value < 0):
            raise ValueError(f"{name} must be >= 0.")
        return value

    def __init__(self, amplitude, frequency, find_peaks=True, meta=None):
        """Initialize a `Hvsr` oject from an amplitude and frequency
        vector.

        Parameters
        ----------
        amplitude : ndarray
            Array of H/V amplitudes. Each row represents an individual
            curve and each column a frequency.
        frequency : ndarray
            Vector of frequencies, corresponding to each column.
        find_peaks : bool, optional
            Indicates whether peaks of Hvsr will be found when created,
            default is True.
        meta : dict, optional
            Meta information about the object, default is None.

        Returns
        -------
        Hvsr
            Initialized with `amplitdue` and `frequency`.
        """
        self.amp = self._check_input("amplitude", amplitude)
        self.frq = self._check_input("frequency", frequency)
        self.n_windows = self.amp.shape[0] if len(self.amp.shape) > 1 else 1
        self.valid_window_indices = np.arange(self.n_windows)
        self._master_peak_frq = np.zeros(self.n_windows)
        self._master_peak_amp = np.zeros(self.n_windows)
        self._initialized_peaks = find_peaks
        self.meta = meta
        if find_peaks:
            self.update_peaks()

    @property
    def rejected_window_indices(self):
        """Rejected window indices."""
        return np.array([cwindow for cwindow in range(self.n_windows) if cwindow not in self.valid_window_indices])

    @property
    def peak_frq(self):
        """Valid peak frequency vector."""
        if not self._initialized_peaks:
            self.update_peaks()
        return self._master_peak_frq[self.valid_window_indices]

    @property
    def peak_amp(self):
        """Valid peak amplitude vector."""
        if not self._initialized_peaks:
            self.update_peaks()
        return self._master_peak_amp[self.valid_window_indices]

    @staticmethod
    def find_peaks(amp, **kwargs):
        """Indices of all peaks in `amp`.

        Wrapper method for scipy.signal.find_peaks function.

        Parameters
        ----------
        amp : ndarray
            Vector or array of amplitudes. See `amp` attribute for
            details.
        **kwargs : dict
            Refer to
            `scipy.signal.find_peaks <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html>`_
            documentation.

        Returns
        -------
        Tuple
            Of the form (peaks, settings)

            peaks : ndarray or list
                `ndarray` or `list` of `ndarrays` (one per window) of
                peak indices.

            settings : dict
                Refer to
                `scipy.signal.find_peaks <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html>`_
                documentation.
        """
        if len(amp.shape) == 1:
            peaks, settings = sg.find_peaks(amp, **kwargs)
            return (peaks, settings)
        else:
            peaks = []
            for c_amp in amp:
                peak, settings = sg.find_peaks(c_amp, **kwargs)
                peaks.append(peak)
            return (peaks, settings)

    def update_peaks(self, **kwargs):
        """Update `peaks` attribute with the lowest frequency, highest
        amplitude peak.

        Properties
        ----------
        **kwargs : dict
            Refer to :meth:`find_peaks <Hvsr.find_peaks>` documentation.

        Returns
        -------
        None
            Updates `peaks` attribute.
        """
        if not self._initialized_peaks:
            self._initialized_peaks = True

        if self.n_windows == 1:
            peak_indices, _ = self.find_peaks(self.amp, **kwargs)
            c_index = np.where(self.amp == np.max(self.amp[peak_indices]))
            self._master_peak_amp = self.amp[c_index]
            self._master_peak_frq = self.frq[c_index]
            return

        peak_indices, _ = self.find_peaks(self.amp[self.valid_window_indices],
                                          **kwargs)
        valid_indices = []
        for c_window, c_window_peaks in zip(self.valid_window_indices, peak_indices):
            try:
                c_index = np.where(self.amp[c_window] == np.max(
                    self.amp[c_window, c_window_peaks]))
                self._master_peak_amp[c_window] = self.amp[c_window, c_index]
                self._master_peak_frq[c_window] = self.frq[c_index]
                valid_indices.append(c_window)
            except:
                assert(c_window_peaks.size == 0)
                logger.warning(f"No peak found in window #{c_window}.")
        self.valid_window_indices = np.array(valid_indices)

    def mean_f0_frq(self, distribution='log-normal'):
        """Mean `f0` of valid time windows.

        Parameters
        ----------
        distribution : {'normal', 'log-normal'}
            Assumed distribution of `f0`, default is 'log-normal'.

        Returns
        -------
        float
            Mean value of `f0` according to the distribution specified.

        Raises
        ------
        KeyError
            If `distribution` does not match the available options.
        """
        if distribution == "normal":
            return np.mean(self.peak_frq)
        elif distribution == "log-normal":
            return np.exp(np.mean(np.log(self.peak_frq)))
        else:
            msg = f"distribution type {distribution} not recognized."
            raise KeyError(msg)

    def mean_f0_amp(self, distribution='log-normal'):
        """Mean amplitude of `f0` of valid time windows.

        Parameters
        ----------
        distribution : {'normal', 'log-normal'}
            Assumed distribution of `f0`, default is 'log-normal'.

        Returns
        -------
        float
            Mean amplitude of `f0` according to the distribution
            specified.

        Raises
        ------
        KeyError
            If `distribution` does not match the available options.
        """
        if distribution == "normal":
            return np.mean(self.peak_amp)
        elif distribution == "log-normal":
            return np.exp(np.mean(np.log(self.peak_amp)))
        else:
            msg = f"distribution type {distribution} not recognized."
            raise KeyError(msg)

    def std_f0_frq(self, distribution='log-normal'):
        """Sample standard deviation of `f0` of valid time windows.

        Parameters
        ----------
            distribution : {'normal', 'log-normal'}, optional
                Assumed distribution of `f0`, default is 'log-normal'.

        Returns
        -------
            Sample standard deviation of `f0` according to the
            distribution specified.

        Raises
        ------
        KeyError
            If `distribution` does not match the available options.
        """
        if distribution == "normal":
            return np.std(self.peak_frq, ddof=1)
        elif distribution == "log-normal":
            return np.std(np.log(self.peak_frq), ddof=1)
        else:
            raise KeyError(f"distribution type {distribution} not recognized.")

    def std_f0_amp(self, distribution='log-normal'):
        """Sample standard deviation of amplitude of `f0` of valid
        time windows.

        Parameters
        ----------
        distribution : {'normal', 'log-normal'}, optional
            Assumed distribution of `f0`, default is 'log-normal'.

        Returns
        -------
        float
            Sample standard deviation of the amplitude of f0 according
            to the distribution specified.

        Raises
        ------
        KeyError
            If `distribution` does not match the available options.
        """
        if distribution == "normal":
            return np.std(self.peak_amp, ddof=1)
        elif distribution == "log-normal":
            return np.std(np.log(self.peak_amp), ddof=1)
        else:
            raise KeyError(f"distribution type {distribution} not recognized.")

    def mean_curve(self, distribution='log-normal'):
        """Return mean H/V curve.

        Parameters
        ----------
            distribution : {'normal', 'log-normal'}, optional
                Assumed distribution of mean curve, default is
                'log-normal'.

        Returns
        -------
        ndarray
            Mean H/V curve according to the distribution specified.

        Raises
        ------
        KeyError
            If `distribution` does not match the available options.
        """
        if self.n_windows == 1:
            return self.amp

        if distribution == "normal":
            return np.mean(self.amp[self.valid_window_indices], axis=0)
        elif distribution == "log-normal":
            return np.exp(np.mean(np.log(self.amp[self.valid_window_indices]), axis=0))
        else:
            raise KeyError(f"distribution type {distribution} not recognized.")

    def std_curve(self, distribution='log-normal'):
        """Sample standard deviation associated with the mean H/V curve.

        Parameters
            distribution : {'normal', 'log-normal'}, optional
                Assumed distribution of H/V curve, default is
                'log-normal'.

        Returns
        -------
        ndarray
            Sample standard deviation of H/V curve according to the
            distribution specified.

        Raises
        ------
        ValueError
            If only single time window is defined.
        KeyError
            If `distribution` does not match the available options.
        """
        if self.n_windows == 1:
            msg = "The standard deviation of the mean curve is not defined for a single window."
            raise ValueError(msg)

        if distribution == "normal":
            return np.std(self.amp[self.valid_window_indices], axis=0, ddof=1)
        elif distribution == "log-normal":
            return np.std(np.log(self.amp[self.valid_window_indices]), axis=0, ddof=1)
        else:
            raise KeyError(f"distribution type {distribution} not recognized.")

    def mc_peak_frq(self, distribution='log-normal'):
        """Frequency of the peak of the mean H/V curve.

        Parameters
        ----------
        distribution : {'normal', 'log-normal'}, optional
            Refer to :meth:`mean_curve <Hvsr.mean_curve>` for details.

        Returns
        -------
        float
            Frequency associated with the peak of the mean H/V curve.
        """
        mc = self.mean_curve(distribution)
        return float(self.frq[np.where(mc == np.max(mc[self.find_peaks(mc)[0]]))])

    def mc_peak_amp(self, distribution='log-normal'):
        """Amplitude of the peak of the mean H/V curve.

        Parameters
        ----------
        distribution : {'normal', 'log-normal'}, optional
            Refer to :meth:`mean_curve <Hvsr.mean_curve>` for details.

        Returns
        -------
        float
            Ampltiude associated with the peak of the mean H/V curve.
        """
        mc = self.mean_curve(distribution)
        return np.max(mc[self.find_peaks(mc)[0]])

    def reject_windows(self, n=2, max_iterations=50,
                       distribution_f0='log-normal',
                       distribution_mc='log-normal'):
        """Perform rejection of H/V windows using the method proposed by
        Cox et al. (in review).

        Parameters
        ----------
        n : float, optional
            Number of standard deviations from the mean, default
            value is 2.
        max_iterations : int, optional
            Maximum number of rejection iterations, default value is
            50.
        distribution_f0 : {'log-normal', 'normal'}, optional
            Assumed distribution of `f0` from time windows, the
            default is 'log-normal'.
        distribution_mc : {'log-normal', 'normal'}, optional
            Assumed distribution of mean curve, the default is
            'log-normal'.

        Returns
        -------
        int
            Number of iterations required for convergence.
        """
        if isinstance(self.meta, dict):
            self.meta["n"] = n
            self.meta["Performed Rejection"] = "True"
        else:
            self.meta = {"n": n, "Performed Rejection": "True"}

        if not self._initialized_peaks:
            self.update_peaks()

        for c_iteration in range(max_iterations):

            logger.debug(f"c_iteration: {c_iteration}")
            logger.debug(f"valid_window_indices: {self.valid_window_indices}")

            mean_f0_before = self.mean_f0_frq(distribution_f0)
            std_f0_before = self.std_f0_frq(distribution_f0)
            mc_peak_frq_before = self.mc_peak_frq(distribution_mc)
            d_before = abs(mean_f0_before - mc_peak_frq_before)

            logger.debug(f"\tmean_f0_before: {mean_f0_before}")
            logger.debug(f"\tstd_f0_before: {std_f0_before}")
            logger.debug(f"\tmc_peak_frq_before: {mc_peak_frq_before}")
            logger.debug(f"\td_before: {d_before}")

            lower_bound = self.nstd_f0_frq(-n, distribution_f0)
            upper_bound = self.nstd_f0_frq(+n, distribution_f0)
            keep_indices = []
            for c_window, c_peak in zip(self.valid_window_indices, self.peak_frq):
                if c_peak > lower_bound and c_peak < upper_bound:
                    keep_indices.append(c_window)
            old_indices = np.array(self.valid_window_indices)
            self.valid_window_indices = np.array(keep_indices)

            mean_f0_after = self.mean_f0_frq(distribution_f0)
            std_f0_after = self.std_f0_frq(distribution_f0)
            mc_peak_frq_after = self.mc_peak_frq(distribution_mc)
            d_after = abs(mean_f0_after - mc_peak_frq_after)

            logger.debug(f"\tmean_f0_after: {mean_f0_after}")
            logger.debug(f"\tstd_f0_after: {std_f0_after}")
            logger.debug(f"\tmc_peak_frq_after: {mc_peak_frq_after}")
            logger.debug(f"\td_after: {d_after}")

            if d_before == 0 or std_f0_before == 0 or std_f0_after == 0:
                logger.warning(
                    f"Performed {c_iteration} iterations, returning b/c 0 values.")
                return c_iteration

            d_diff = abs(d_after - d_before)/d_before
            s_diff = abs(std_f0_after - std_f0_before)

            logger.debug(f"\td_diff: {d_diff}")
            logger.debug(f"\ts_diff: {s_diff}")

            if (d_diff < 0.01) and (s_diff < 0.01):
                self.valid_window_indices = old_indices
                logger.info(
                    f"Performed {c_iteration} iterations, returning b/c rejection converged.")
                return c_iteration

    def nstd_f0_frq(self, n, distribution):
        """Return nth standard deviation of `f0`.

        Parameters
        ----------
        n : float
            Number of standard deviations away from the mean `f0`
            from the valid time windows.
        distribution : {'log-normal', 'normal'}, optional
            Assumed distribution of `f0`, the default is
            'log-normal'.

        Returns
        -------
        float
            nth standard deviation of `f0`.
        """
        if distribution == "normal":
            return (self.mean_f0_frq(distribution) + n*self.std_f0_frq(distribution))
        elif distribution == "log-normal":
            return (np.exp(np.log(self.mean_f0_frq(distribution)) + n*self.std_f0_frq(distribution)))
        else:
            raise KeyError(f"distribution type {distribution} not recognized.")

    def nstd_f0_amp(self, n, distribution):
        """nth sample standard deviation of amplitude of `f0` from time
        windows.

        Parameters
        ----------
        n : float
            Number of standard deviations away from the mean
            amplitude of `f0` from valid time windows.
        distribution : {'log-normal', 'normal'}, optional
            Assumed distribution of `f0`, the default is
            'log-normal'.

        Returns
        -------
        float
            nth standard deviation of ampltiude of `f0`.
        """
        if distribution == "normal":
            return (self.mean_f0_amp(distribution) + n*self.std_f0_amp(distribution))
        elif distribution == "log-normal":
            return (np.exp(np.log(self.mean_f0_amp(distribution)) + n*self.std_f0_amp(distribution)))
        else:
            raise KeyError(f"distribution type {distribution} not recognized.")

    def nstd_curve(self, n, distribution):
        """Return nth standard deviation curve.

        Parameters
        ----------
        n : float
            Number of standard deviations away from the mean curve.
        distribution : {'log-normal', 'normal'}, optional
            Assumed distribution of mean curve, the default is
            'log-normal'.

        Returns
        -------
        ndarray
            nth standard deviation curve.
        """
        if distribution == "normal":
            return (self.mean_curve(distribution) + n*self.std_curve(distribution))
        elif distribution == "log-normal":
            return (np.exp(np.log(self.mean_curve(distribution)) + n*self.std_curve(distribution)))
        else:
            raise KeyError(f"distribution type {distribution} not recognized.")

    # def print_stats(self, distribution_f0):
    #     """Print basic statistics of `Hvsr` instance."""

    #     if distribution_f0 == "log-normal":
    #         f0 = f"|    f0     |  Log-normal  |    -    | {str(self.mean_f0_frq(distribution_f0))[:4]} Hz |        {str(self.std_f0_frq(distribution_f0))[:4]}        |"
    #     else:
    #         f0 = f"|    f0     |    Normal    | {str(self.std_f0_frq(distribution_f0))[:4]} Hz |    -    |      {str(self.std_f0_frq(distribution_f0))[:4]} Hz       |"

    #     if distribution_f0 == "log-normal":
    #         T0 = f"|    T0     |  Log-normal  |    -    | {str(1/self.mean_f0_frq(distribution_f0))[:4]} s  |       {str(-1*self.std_f0_frq(distribution_f0))[:5]}        |"
    #     else:
    #         T0 = f"|    T0     |    Normal    |    -    |    -    |         -          |"

    #     stats = [
    #         "| Parameter | Distribution |   Mean  |  Median | Standard Deviation |",
    #         "|-----------+--------------+---------+---------+--------------------|",
    #         f0,
    #         T0
    #     ]
    #     for stat in stats:
    #         print(stat)

    def print_stats(self, distribution_f0):
        """Print basic statistics of `Hvsr` instance."""

        if distribution_f0 == "log-normal":
            upper = "                                 | Log-Normal |     Log-Normal     |"
            lower = "|              Name              |   Median   | Standard Deviation |"

            f0 = (f"|   {str(self.mean_f0_frq(distribution_f0))[:4]} Hz  " +
                  f"|        {str(self.std_f0_frq(distribution_f0))[:4]}        |")
            T0 = (f"|   {str(1/self.mean_f0_frq(distribution_f0))[:4]} s   " +
                  f"|       {str(-1*self.std_f0_frq(distribution_f0))[:5]}        |")

        elif distribution_f0 == "normal":
            upper = ""
            lower = "|              Name              |    Mean    | Standard Deviation |"

            f0 = (f"|   {str(self.mean_f0_frq(distribution_f0))[:4]} Hz  " +
                  f"|      {str(self.std_f0_frq(distribution_f0))[:4]} Hz       |")
            T0 = (f"|     -      |         -          |")

        else:
            msg = f"`distribution_f0` of {distribution_f0} is not implemented."
            raise NotImplementedError(msg)

        stats = [
            upper,
            lower,
            "|--------------------------------+------------+--------------------|",
            "| Fundemental Site Frequency, f0 "+f0,
            "|   Fundemental Site Period, T0  "+T0
        ]
        for stat in stats:
            if stat != "":
                print(stat)

    def to_file_like_geopsy(self, fname, distribution_f0, distribution_mc):
        """Save H/V data to file in Geopsy format.

        Parameters
        ----------
        fname : str
            Name of file to save the results, may be a full or
            relative path.
        distribution_f0 : {'log-normal', 'normal'}, optional
            Assumed distribution of `f0` from the time windows, the
            default is 'log-normal'.
        distribution_mc : {'log-normal', 'normal'}, optional
            Assumed distribution of mean curve, the default is
            'log-normal'.

        Returns
        -------
        None
            Writes file to disk.
        """
        # f0 from windows
        mean = self.mean_f0_frq(distribution_f0)
        lower = self.nstd_f0_frq(-1, distribution_f0)
        upper = self.nstd_f0_frq(+1, distribution_f0)

        # mean curve
        mc = self.mean_curve(distribution_mc)
        mc_peak_frq = self.mc_peak_frq(distribution_mc)
        mc_peak_amp = self.mc_peak_amp(distribution_mc)
        _min = self.nstd_curve(-1, distribution_mc)
        _max = self.nstd_curve(+1, distribution_mc)

        lines = [
            f"# hvsrpy output version 0.2.0",
            f"# Number of windows = {len(self.valid_window_indices)}",
            f"# f0 from average\t{mc_peak_frq}",
            f"# Number of windows for f0 = {len(self.valid_window_indices)}",
            f"# f0 from windows\t{mean}\t{lower}\t{upper}",
            f"# Peak amplitude\t{mc[np.where(self.frq == mc_peak_frq)][0]}",
            f"# Position\t{0} {0} {0}",
            f"# Category\tDefault",
            f"# Frequency\tAverage\tMin\tMax",
        ]
        with open(fname, "w") as f:
            for line in lines:
                f.write(line+"\n")
            for f_i, a_i, n_i, x_i in zip(self.frq, mc, _min, _max):
                f.write(f"{f_i}\t{a_i}\t{n_i}\t{x_i}\n")

    def to_file(self, fname, distribution_f0, distribution_mc):
        """Save H/V data to file in hvsrpy format.

        Parameters
        ----------
        fname : str
            Name of file to save the results, may be a full or
            relative path.
        distribution_f0 : {'log-normal', 'normal'}, optional
            Assumed distribution of `f0` from the time windows, the
            default is 'log-normal'.
        distribution_mc : {'log-normal', 'normal'}, optional
            Assumed distribution of mean curve, the default is
            'log-normal'.

        Returns
        -------
        None
            Writes file to disk.
        """
        # f0 from windows
        mean_f = self.mean_f0_frq(distribution_f0)
        sigm_f = self.std_f0_frq(distribution_f0)

        # mean curve
        mc = self.mean_curve(distribution_mc)
        mc_peak_frq = self.mc_peak_frq(distribution_mc)
        mc_peak_amp = self.mc_peak_amp(distribution_mc)
        _min = self.nstd_curve(-1, distribution_mc)
        _max = self.nstd_curve(+1, distribution_mc)

        n_rejected = self.n_windows - len(self.valid_window_indices)
        rejection = self.meta.get('Performed Rejection')
        lines = [
            f"# hvsrpy output version 0.2.0",
            f"# File Name (),{self.meta.get('File Name')}",
            f"# Window Length (s),{self.meta.get('Window Length')}",
            f"# Total Number of Windows,{self.n_windows}",
            f"# Frequency Domain Rejetion Performed,{'False' if rejection is None else rejection}",
            f"# Number of Standard Deviations Used for Rejection () [n],{self.meta.get('n')}",
            f"# Number of Accepted Windows,{self.n_windows-n_rejected}",
            f"# Number of Rejected Windows,{n_rejected}",
            f"# Distribution of f0,{distribution_f0}"]

        if distribution_f0 == "log-normal":
            mean_t = 1/mean_f
            sigm_t = -1*sigm_f
            ci_68_lower_t = np.exp(np.log(mean_t) + sigm_t)
            ci_68_upper_t = np.exp(np.log(mean_t) - sigm_t)

            lines += [
                f"# Median f0 (Hz) [LMf0],{mean_f}",
                f"# Log-normal standard deviation f0 () [SigmaLNf0],{sigm_f}",
                f"# 68 % Confidence Interval f0 (Hz),{ci_68_lower_f},to,{ci_68_upper_f}",
                f"# Median T0 (s) [LMT0],{mean_t}",
                f"# Log-normal standard deviation T0 () [SigmaLNT0],{sigm_t}",
                f"# 68 % Confidence Interval T0 (s),{ci_68_lower_t},to,{ci_68_upper_t}",
            ]

        else:
            ci_68_lower_f = self.nstd_f0_frq(-1, distribution_f0)
            ci_68_upper_f = self.nstd_f0_frq(+1, distribution_f0)

            lines += [
                f"# Mean f0 (Hz),{mean_f}",
                f"# Standard deviation f0 (Hz) [Sigmaf0],{sigm_f}",
                f"# 68 % Confidence Interval f0 (Hz),{ci_68_lower_f},to,{ci_68_upper_f}",
                f"# Mean T0 (s) [LMT0],NA",
                f"# Standard deviation T0 () [SigmaT0],NA",
                f"# 68 % Confidence Interval T0 (s),NA",
            ]

        c_type = "Median" if distribution_mc == "log-normal" else "Mean"
        lines += [
            f"# {c_type} Curve Distribution,{distribution_mc}",
            f"# {c_type} Curve Peak Frequency (Hz) [f0mc],{mc_peak_frq}",
            f"# {c_type} Curve Peak Amplitude (),{mc_peak_amp}",
            f"# Frequency (Hz),{c_type} Curve,1 STD Below {c_type} Curve,1 STD Above {c_type} Curve",
        ]

        with open(fname, "w") as f:
            for line in lines:
                f.write(line+"\n")
            for f_i, mean_i, bel_i, abv_i in zip(self.frq, mc, _min, _max):
                f.write(f"{f_i},{mean_i},{bel_i},{abv_i}\n")
