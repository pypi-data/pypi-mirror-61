#import matplotlib
#matplotlib.use('Agg')

import numpy as np
import pymc3 as pm
import warnings
from .plotting import plotting

class peakbag(plotting):
    """
    Class for PBjam peakbagging.

    This class allows for simple manipulation of the data, the fitting of a
    PyMC3 model to the data, and some plotting of results functionality.

    Examples
    --------
    Star API interaction (recommended)

    >>> from pbjam import star
    >>> star = pb.star(kic, pg, numax, dnu, teff, bp_rp, store_chains=True, nthreads=4)
    >>> star.run_epsilon()
    >>> star.run_asy_peakbag(norders=7)
    >>> star.run_peakbag()

    Lower level API interaction.

    >>> import PBjam
    >>> pbag = pbjam.peakbag(frequency, snr, asy_result)
    >>> pbag.sample(model_type='simple', cores=4)
    >>> pbag.plot_fit()

    Parameters
    ----------
    f : float, array
        Array of frequency bins of the spectrum (muHz). Truncated to the range
        around numax.
    snr : float, array
        Array of SNR values for the frequency bins in f (dimensionless).
    asy_result : asy_result
        The result from the asy_peakbag method.
    init : bool
        If true runs make_start and trim_ladder to prepare starting
        guesses for sampling and transforms the data onto a ladder.

    Attributes
    ----------
    f : float, ndarray
        Array of frequency bins of the spectrum (muHz). Truncated to the range
        around numax.
    snr : float, ndarray
        Array of SNR values for the frequency bins in f (dimensionless).
    asy_result : asy_result
        The result from the asy_peakbag method.
        This is a dictionary of 'modeID' and 'summary'.
        'modeID' is a DataFrame with a list of modes and basic properties.
        'summary' are summary statistics from the asymptotic_fit.
        See asy_peakbag asymptotic_fit for more details.

    """

    def __init__(self, starinst, asyinst, init=True, path=None,
                       verbose=False):

        self.pg = starinst.pg
        self.f = starinst.f
        self.s = starinst.s
        self.asy_result = asyinst
        self.norders = asyinst.norders
        if init:
            self.make_start()
            self.trim_ladder(verbose=verbose)
        self.gp0 = [] # Used for gp linewidth info.

        starinst.peakbag = self


    def make_start(self):
        """
        Function uses the information in self.asy_result (the result of the
        asymptotic peakbagging) and builds a dictionary of starting values
        for the peakbagging methods.

        """

        idxl0 = self.asy_result.modeID.ell == 0
        idxl2 = self.asy_result.modeID.ell == 2

        l0 = self.asy_result.modeID.loc[idxl0, 'nu_med'].values.flatten()
        l2 = self.asy_result.modeID.loc[idxl2, 'nu_med'].values.flatten()

        l0, l2 = self.remove_outsiders(l0, l2)

        width = 10**(np.ones(len(l0)) * self.asy_result.summary.loc['mode_width', 'mean']).flatten()
        height =  (10**self.asy_result.summary.loc['env_height', 'mean'] * \
                 np.exp(-0.5 * (l0 - 10**self.asy_result.summary.loc['numax', 'mean'])**2 /
                 (10**self.asy_result.summary.loc['env_width', 'mean'])**2)).flatten()
        back = np.ones(len(l0))

        self.parnames = ['l0', 'l2', 'width0', 'width2', 'height0', 'height2',
                         'back']

        pars = [l0, l2, width, width, height, 0.7*height, back]

        self.start ={x:y for x,y in zip(self.parnames, pars)}
#        self.start = {'l0': l0, 'l2': l2, 'width0': width, 'width2': width,
#                      'height0': height, 'height2': height*0.7,
#                      'back': np.ones(len(l0))}
        self.n = np.linspace(0.0, 1.0, len(self.start['l0']))[:, None]

    def remove_outsiders(self, l0, l2):
        """ Drop outliers

        Drops modes where the guess frequency is outside of the supplied
        frequency range.

        """

        sel = np.where(np.logical_and(l0 < self.f.max(), l0 > self.f.min()))
        return l0[sel], l2[sel]

    def trim_ladder(self, lw_fac=10, extra=0.01, verbose=False):
        """
        This function makes ladders and then selects only the orders
        in the ladders that have modes that are to be fitted,
        i.e, it trims the ladder.

        Each ladder rung is constructed so that the central frequency is
        the mid point between the l=0 and l=2 modes as determined by the
        info in the asy_result dictionary.

        The width of the rung is determined by d02, line width, and some
        parameters lw_fac and extra.  The basic calculation is the width is:
        d02 + (lw_fac * line_width) + (extra * dnu)

        Parameters
        ----------
        lw_fac: float
            The factor by which the mode line width is multiplied in order
            to contribute to the rung width.
        extra: float
            The factor by which dnu is multiplied in order to contribute to
            the rung width.

        """

        d02 = 10**self.asy_result.summary.loc['d02','mean']
        d02_lw = d02 + lw_fac * 10**self.asy_result.summary.loc['mode_width', 'mean']
        w = d02_lw + (extra * 10**self.asy_result.summary.loc['dnu', 'mean'])
        bw = self.f[1] - self.f[0]
        w /= bw
        if verbose:
            print(f'w = {int(w)}')
            print(f'bw = {bw}')
        ladder_trim_f = np.zeros([len(self.start['l0']), int(w)])
        ladder_trim_s = np.zeros([len(self.start['l0']), int(w)])
        for idx, freq in enumerate(self.start['l0']):
            loc_mid_02 = np.argmin(np.abs(self.f - (freq - d02/2.0)))
            if loc_mid_02 == 0:
                warnings.warn('Did not find optimal rung location')
            if verbose:
                print(f'loc_mid_02 = {loc_mid_02}')
                print(f'w/2 = {int(w/2)}')
            ladder_trim_f[idx, :] = \
                self.f[loc_mid_02 - int(w/2): loc_mid_02 - int(w/2) + int(w)]
            ladder_trim_s[idx, :] = \
                self.s[loc_mid_02 - int(w/2): loc_mid_02 - int(w/2) + int(w) ]
        self.ladder_f = ladder_trim_f
        self.ladder_s = ladder_trim_s

    def lor(self, freq, w, h):
        """
        This function calculates a lorentzian for each rung of the frequency
        ladder.  The ladder is a 2D array.  freq, w, and h should be 1D arrays
        of length that matches the height of the ladder.  No checks are made
        for this so as to reduce overheads.

         Parameters
         ----------
         freq : float, ndarray
            A length H array of Lorentzian central frequencies where H is the
            height of self.ladder_f .
         w : float, ndarray
            A length H array of Lorentzian width where H is the
            height of self.ladder_f .
         h : float, ndarray
            A length H array of Lorentzian heightswhere H is the
            height of self.ladder_f .

        Returns
        -------
        lorentzians : float, ladder
           A ladder containing one Lorentzian per rung.

        """

        norm = 1.0 + 4.0 / w**2 * (self.ladder_f.T - freq)**2
        return h / norm

    def model(self, l0, l2, width0, width2, height0, height2, back):
        """
        Calcuates a simple model of a flat backgroud plus two lorentzians
        for each rung of self.ladder_f .

        Parameters
        ----------
        l0 : float, ndarray
            A length H array of l=0 mode central frequencies where H is the
            height of self.ladder_f .
        l2 : float, ndarray
            A length H array of l=2 mode central frequencies where H is the
            height of self.ladder_f .
        width0 : float, ndarray
            A length H array of l=0 mode widths where H is the
            height of self.ladder_f .
        width2 : float, ndarray
            A length H array of l=2 mode widths where H is the
            height of self.ladder_f .
        height0 : float, ndarray
            A length H array of l=0 mode heights where H is the
            height of self.ladder_f .
        height2 : float, ndarray
            A length H array of l=2 mode heights where H is the
            height of self.ladder_f .
        back : float, ndarray
            A length H array of background values where H is the
            height of self.ladder_f .

        Returns
        -------
        mod : float, ndarray
            A 2D array (or 'ladder') containing the calculated model.

        """

        mod = np.ones(self.ladder_f.shape).T * back
        mod += self.lor(l0, width0, height0)
        mod += self.lor(l2, width2, height2)
        return mod.T

    def init_model(self, model_type):
        """
        TODO - Need to describe what is happening here.
        Complete docs when model is settled on.  Probably quiet a
        long docs needed to explain.

        """

        dnu = 10**self.asy_result.summary.loc['dnu', 'mean']
        dnu_fac = 0.03 # Prior on mode frequency has width 3% of Dnu.
        height_fac = 0.4 # Lognorrmal prior on height has std=0.4.
        width_fac = 1.0 # Lognorrmal prior on width has std=1.0.
        back_fac = 0.5 # Lognorrmal prior on back has std=0.5.
        N = len(self.start['l2'])

        with self.pm_model:

            if model_type != 'model_gp':
                if model_type != 'simple': # defaults to simple if bad input
                    warnings.warn('Model not defined - using simple model')
                width0 = pm.Lognormal('width0', mu=np.log(self.start['width0']),
                                  sigma=width_fac, shape=N)
                width2 = pm.Lognormal('width2', mu=np.log(self.start['width2']),
                                  sigma=width_fac, shape=N)

                self.init_sampler = 'adapt_diag'
                self.target_accept = 0.9

            elif model_type == 'model_gp':
                warnings.warn('This model is developmental - use carefully')
                # Place a GP over the l=0 mode widths ...
                m0 = pm.Normal('gradient0', 0, 10)
                c0 = pm.Normal('intercept0', 0, 10)
                sigma0 = pm.Lognormal('sigma0', np.log(1.0), 1.0)
                ls = pm.Lognormal('ls', np.log(0.3), 1.0)
                mean_func0 = pm.gp.mean.Linear(coeffs=m0, intercept=c0)
                cov_func0 = sigma0 * pm.gp.cov.ExpQuad(1, ls=ls)
                self.gp0 = pm.gp.Latent(cov_func=cov_func0, mean_func=mean_func0)
                ln_width0 = self.gp0.prior('ln_width0', X=self.n)
                width0 = pm.Deterministic('width0', pm.math.exp(ln_width0))
                # and on the l=2 mode widths
                m2 = pm.Normal('gradient2', 0, 10)
                c2 = pm.Normal('intercept2', 0, 10)
                sigma2 = pm.Lognormal('sigma2', np.log(1.0), 1.0)
                mean_func2 = pm.gp.mean.Linear(coeffs=m2, intercept=c2)
                cov_func2 = sigma2 * pm.gp.cov.ExpQuad(1, ls=ls)
                self.gp2 = pm.gp.Latent(cov_func=cov_func2, mean_func=mean_func2)
                ln_width2 = self.gp2.prior('ln_width2', X=self.n)
                width2 = pm.Deterministic('width2', pm.math.exp(ln_width2))

                self.init_sampler = 'advi+adapt_diag'
                self.target_accept = 0.99


            l0 = pm.Normal('l0', self.start['l0'], dnu*dnu_fac, shape=N)

            l2 = pm.Normal('l2', self.start['l2'], dnu*dnu_fac, shape=N)

            height0 = pm.Lognormal('height0', mu=np.log(self.start['height0']),
                                    sigma=height_fac, shape=N)
            height2 = pm.Lognormal('height2', mu=np.log(self.start['height2']),
                                    sigma=height_fac, shape=N)
            back = pm.Lognormal('back', mu=np.log(1.0), sigma=back_fac, shape=N)

            limit = self.model(l0, l2, width0, width2, height0, height2, back)
            pm.Gamma('yobs', alpha=1, beta=1.0/limit, observed=self.ladder_s)



    def __call__(self, model_type='simple', tune=1500, nthreads=1, maxiter=4,
                     advi=False):
        """
        Function to perform the sampling of a defined model.

        Parameters
        ----------
        model_type : str
            Defaults to 'simple'.
            Can be either 'simple' or 'model_gp' which sets the type of model
            to be fitted to the data.
        tune : int
            Numer of tuning steps passed to pym3.sample
        nthreads : int
            Number of cores to use - passed to pym3.sample
        maxiter : int
            Number of times to attempt to reach convergence
        advo : bool
            Whether or not to fit using the fullrank_advi option in pymc3

        """

        self.pm_model = pm.Model()

        self.init_model(model_type=model_type)

        if advi:
            with self.pm_model:
                cb = pm.callbacks.CheckParametersConvergence(every=1000,
                                                             diff='absolute',
                                                             tolerance=0.01)

                mean_field = pm.fit(n=200000, method='fullrank_advi',
                                    start=self.start,
                                    callbacks=[cb])
                self.samples = mean_field.sample(1000)
        else:
            Rhat_max = 10
            niter = 1
            while Rhat_max > 1.05:
                if niter > maxiter:
                    warnings.warn('Did not converge!')
                    break
                with self.pm_model:
                    self.samples = pm.sample(tune=tune * niter, cores=nthreads,
                                             start=self.start,
                                             init=self.init_sampler,
                                             target_accept=self.target_accept,
                                             progressbar=False)
                Rhat_max = np.max([v.max() for k, v in pm.diagnostics.gelman_rubin(self.samples).items()])
                niter += 1

        self.summary = pm.summary(self.samples)
        self.par_names = self.summary.index


#    def simple(self):
#        """
#        Creates a simple peakbagging model in PyMC3's self.pm_model which is
#        an instance of pm.Model().
#
#        The simple model has three parameters per mode (freq, w, h) and one
#        back parameter per rung of the frequency ladder.
#
#        All parameters are independent.  For a model with additional constraints
#        see model_gp.
#
#        Priors on parameters are defined as follows:
#            lX ~ Normal(log(start[lX]), dnu*0.1)
#            widthX ~ Lognormal(log(start[widthX]), 1.0)
#            heightX ~ Lognormal(log(start[height0]), 0.4)
#            back ~ Lognormal(log(1), 0.5)
#
#        The equivalent likelihood function of the observed data is dealt with
#        using a Gamma distribution where alpha=1 and beta=1/limit where limit
#        is the model of the spectrum proposed.  Using this gamma distirbution
#        is the equivalent of stating that observed/model is distributed as
#        chi squared two degrees of freedom (see Anderson 1990 for more details).
#        The use of the Gamma distribution is much more in line with the ethos of
#        probabistic programming languages.
#        """
#
#        dnu = 10**self.asy_result.summary.loc['dnu', 'mean']
#        dnu_fac = 0.03 # Prior on mode frequency has width 3% of Dnu.
#        width_fac = 1.0 # Lognorrmal prior on width has std=1.0.
#        height_fac = 0.4 # Lognorrmal prior on height has std=0.4.
#        back_fac = 0.4 # Lognorrmal prior on back has std=0.4.
#        N = len(self.start['l2'])
#
#        with self.pm_model:
#
#            width0 = pm.Lognormal('width0', mu=np.log(self.start['width0']),
#                                  sigma=width_fac, shape=N)
#            width2 = pm.Lognormal('width2', mu=np.log(self.start['width2']),
#                                  sigma=width_fac, shape=N)
#
#            l0 = pm.Normal('l0', self.start['l0'], dnu*dnu_fac, shape=N)
#
#            l2 = pm.Normal('l2', self.start['l2'], dnu*dnu_fac, shape=N)
#
#            height0 = pm.Lognormal('height0', mu=np.log(self.start['height0']),
#                                    sigma=height_fac, shape=N)
#            height2 = pm.Lognormal('height2', mu=np.log(self.start['height2']),
#                                    sigma=height_fac, shape=N)
#            back = pm.Lognormal('back', mu=np.log(1.0), sigma=back_fac, shape=N)
#
#            limit = self.model(l0, l2, width0, width2, height0, height2, back)
#
#            pm.Gamma('yobs', alpha=1, beta=1.0/limit, observed=self.ladder_s)
