# iragnsep

iragnsep performs IR (i.e. 8--1000 microns) SED fits to separate the AGN and the galaxy contributions allowing to measure the host galaxy properties (e.g. SFRs) free of AGN contamination. The advantage of iragnsep is that, in addition to fit observed photometric fluxes, it allows to incorporate spectra which improves the robustness at separating the AGN and the galaxy IR emission. For the galaxy component iragnsep uses a library of templates that are representative of local star-forming galaxies. For the AGN contribution, should the input dataset contains a mixed of a spectral and photometric data, iragnsep uses a combination of power-laws for the AGN continuum and some broad features for the silicate emissions. If the dataset contains photometric data only, the AGN contribution is accounted for by using a fixed library of AGN templates representative of typical AGN emission at IR wavelengths. The advanced fitting techniques used by iragnsep (i.e. MLE optimised with MCMC) combined with powerful model comparison tests (e.g. AIC) allow iragnsep to provide a statistically robust interpretation of the data in terms of AGN--galaxy separation for the IR emission of galaxies harbouring AGNs at their centre.

The aim of this README is to show how to use iragnsep and to present the various modules used throughout. Further information concerns the limitations of iragnsep as well as future work expected to improve iragnsep. These are important to consider while using iragnsep. Any use of iragnsep out of those defined boundaries are to be taken with care and is at the users risk.

For a detailed description on the templates and the models see Bernhard et al. (in prep.).

Contacts: e.p.bernhard[at]sheffield.ac.uk

## Getting Started
These instructions should assist you in getting iragnsep running on your machine. iragnsep is written in python 3 and is available on PyPI.

### Prerequisites
iragnsep requires various non-standard libraries (dependencies) to run. These should automatically get installed when downloading and installing iragnsep. If not, these can be manually installed using the pip3 command. The dependencies are as follow,

* [NumPy](https://numpy.org) - NumPy is the fundamental package for scientific computing with Python.
* [Matplotlib](https://matplotlib.org) - Matplotlib is a Python 2D plotting library.
* [Astropy](https://www.astropy.org) - The Astropy Project is a community effort to develop a common core package for Astronomy in Python and foster an ecosystem of inter-operable astronomy packages.
* [SciPy](https://www.scipy.org) - SciPy is a Python-based ecosystem of open-source software for mathematics, science, and engineering.
* [pandas](https://pandas.pydata.org) - pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
* [emcee](https://emcee.readthedocs.io/en/stable/#) - emcee is an MIT licensed pure-Python implementation of Goodman & Weare’s Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler.
* [Numba](http://numba.pydata.org) - Numba translates Python functions to optimized machine code at runtime using the industry-standard LLVM compiler library. Numba-compiled numerical algorithms in Python can approach the speeds of C or FORTRAN.

### Installation
We recommend to install iragnsep and its dependencies using pip,

```
pip3 install iragnsep
```
The project is also publicly available on bitbucket at https://bitbucket.org/ebernhard/iragnsep/src/master/ .

## Quick start

In this section we show how to infer the SFR of the galaxy mrk1066 using iragnsep.

### Step 1: Get the data and the script

You can download the data at https://bitbucket.org/ebernhard/iragnsepex/src/master/. The file data_mrk1066.csv contains the Herschel fluxes of mrk1066 and the file data_mrk1066_spec.csv contains the IRS spectrum of mrk1066. The file main.py is the main script. Once downloaded, create a folder with all of these files.

### Step 2: Run the script

In a terminal simply cd to the folder that contains the files and run,

```
python3 main.py
```

iragnsep is now fitting mrk1066, first using a combination of the IRS spectra and Herschel photometry, then using photometry only as if the IRS spectra was not available. The user can open the file main.py which is commented and can be used as a template for future use of iragnsep.

### Step 3: Output

Once the fit is performed the plots and tables are generated and saved in the same folder. 

* **mrk1066_fitRes_spec.csv** - contains the results of the fits for all possible combinations of models. Each line corresponds to a specific model. This file is for fits based on data which include the IRS spectrum. The best model is flagged by a value of 1.0 in the column 'bestModelFlag'. See the section ** Description of the tables** for a full description of each of the columns.
* **mrk1066_fitResAll_spec.pdf** - shows each of the models fit to the data which include the IRS spectrum.
* **mrk1066_fitResBM_spec.pdf** -  shows the best fit to the data which include the IRS spectrum. The best fit corresponds to a weighted average of all the different models.
* **mrk1066_fitRes_photo.csv** - contains the results of the fits for all possible combinations of models. Each line corresponds to a specific model. This file is for fits based on photometric data. The best model is flagged by a value of 1.0 in the column 'bestModelFlag'. See the section ** Description of the tables** for a full description of each of the columns.
* **mrk1066_fitResAll_photo.pdf** - shows each of the models fit to the photometric data.
* **mrk1066_fitResBM_photo.pdf** - shows the best fit to the photometric data. The best fit corresponds to a weighted average of all the different models.

(Important notice: for this example the number of steps for the MCMC is set to 1000. This is way too short and should be increased to get a more reliable fit. We use 1000 here so it is not too much time consuming and the fits appear to be OK.)

## Preparing your data
As this is the first version of iragnsep it is important to make sure that the data in input are compatible with the code. Future versions will allow more flexibility in the format of the input data. The main input are the wavelengths of the SED (or combined spectrum and photometry) and the corresponding fluxes and their uncertainties. Here is a (non-exhaustive) check list of points that are required to ensure a robust behaviour of iragnsep.

* the wavelengths are in microns, the fluxes and the uncertainties are in Jy.
* the vector wavelength is in monotonically increasing order.
* their is no negative or undefined (e.g. nan) values in the fluxes and their uncertainties (upper-limits can be passed via the keyword UL).
* the vectors fed in the keywords 'wavToFit', 'filters' and 'UL' are of the same length. The later is defined by the number of photometric points in the SED.
* if any of the keywords 'wavToFit', 'filters' and 'UL' are changed, they all need to be changed accordingly (see the example of mrk1066 where there is no flux at 500 micron).
* if using iragnsep with a combination of spectrum and photometry, make sure that no photometric points are overlapping with the spectral data (e.g. IRS spectra and MIPS 24 micron would be overlapping).
* from practice, a good value for Nmc (the number of steps in the MCMC) is at least >10000 steps.
* do not forget to set the redshift of the source using the keyword z.
* make sure that you do not have any data points below roughly 5 microns rest-frame as iragnsep has not been designed to account for emissions below this value.

Should you find anything non-intuitive missing from the above list, contact us at: e.p.bernhard[at]sheffield.ac.uk

## Description of the tables

The output of the fits can be saved using the keyword saveRes as shown in the main.py of the Quick Start example on mrk1066. In particular two types of tables can be generated whether using the version of the code with spectra or that of with photometry only.

The table sourceName_fitRes_spec.csv is a comma separated values table which contains the results of the fits performed on data which includes spectra (i.e. using the full model for AGN emission). Each line of the table is a possible model that has been fit to the data. Columns are as follow,

* **tplName** - the name of the template for the galaxy emission.
* **AGNon** - if set to 0.0 the fit was performed assuming no AGN and if set to 1.0 the AGN was included in the fit.
* **logNormGal_dust, elogNormGal_dust** - the log-normalisation of the galaxy dust continuum emission and its uncertainties.
* **logNormGal_PAH, elognNormGal_PAH** - the log-normalisation of the PAH emission template and its uncertainties.
* **logNormAGN_PL, elogNormAGN_PL** - the overall normalisation of the continuum emission for AGN (combination of power-laws) and its uncertainties.
* **lBreak_PL, elBreak_PL** - the position of the main break for the AGN emission and its uncertainties.
* **alpha1_PL, ealpha1_PL** - the slope of the AGN power-law below 15 micron and its uncertainties.
* **alpha2_PL, ealpha2_PL** - the slope of the AGN power-law above 15 micron and below lbreak_PL and its uncertainties.
* **logNorm_Si11, elogNorm_Si11** - the log-normalisation of the silicate emission at 11 micron and its uncertainties.
* **logNorm_Si19, elogNorm_Si19** - the log-normalisation of the silicate emission at 19 micron and its uncertainties.
* **loglumIR_host, eloglumIR_host** - the IR (8--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumMIR_host, eloglumMIR_host** - the MIR (5--35 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumFIR_host, eloglumFIR_host** - the FIR (40--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumIR_AGN, eloglumIR_AGN** - the IR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumMIR_AGN, eloglumMIR_AGN** - the MIR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumFIR_AGN, eloglumFIR_AGN** - the FIR luminosity of the AGN free of host contamination, and its uncertainties.
* **AGNfrac_IR** - the fraction of the total IR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_MIR** - the fraction of the total MIR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_FIR** - the fraction of the total FIR luminosity which is attributed to the AGN, and its uncertainties.
* **SFR, eSFR** - the star formation rate free of AGN contamination, and its uncertainties.
* **wSFR, ewSFR** - the weighted star formation rate free of AGN contamination, and its uncertainties.
* **logl** - the loglikelihood of the fit given the model.
* **Aw** - the Akaike weight of the model.
* **tau9p7** - the total extinction at 9.7 micron.
* **bestModelFlag** - a value of 1.0 indicates the best model.

The table sourceName_fitRes_photo.csv is a comma separated values table which contains the results of the fits performed on data with photometry only (i.e. using the templates for the AGN emission). Each line is a possible model that has been fit to the data. Columns are as follow,

* **tplName_gal** - the name of the template for the galaxy emission.
* **AGNon** - if set to 0.0 the fit was performed assuming no AGN and if set to 1.0 the AGN was included in the fit.
* **tplName_AGN** - the name of the template for the AGN emission.
* **logNormGal_dust, elogNormGal_dust** - the log-normalisation of the galaxy dust continuum emission and its uncertainties.
* **logNormGal_PAH, elogNormGal_PAH** - the log-normalisation of the PAH emission template and its uncertainties.
* **logNormAGN, elogNormAGN** - the log-normalisation of the template for the AGN emission and its uncertainties.
* **logNormSiem, elogNormSiem** - the log-normalisation of the template for the silicate emission and its uncertainties.
* **loglumIR_host, eloglumIR_host** - the IR (8--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumMIR_host, eloglumMIR_host** - the MIR (5--35 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumFIR_host, eloglumFIR_host** - the FIR (40--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumIR_AGN, eloglumIR_AGN** - the IR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumMIR_AGN, eloglumMIR_AGN** - the MIR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumFIR_AGN, eloglumFIR_AGN** - the FIR luminosity of the AGN free of host contamination, and its uncertainties.
* **AGNfrac_IR** - the fraction of the total IR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_MIR** - the fraction of the total MIR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_FIR** - the fraction of the total FIR luminosity which is attributed to the AGN, and its uncertainties.
* **SFR, eSFR** - the star formation rate free of AGN contamination, and its uncertainties.
* **wSFR, ewSFR** - the weighted star formation rate free of AGN contamination, and its uncertainties.
* **logl** - the loglikelihood of the fit given the model.
* **Aw** - the Akaike weight of the model.
* **bestModelFlag** - a value of 1.0 indicates the best model.

## iragnsep: modules

--

### SEDanalysis

--

The module SEDanalysis is the main module which runs the fits (yet see the **run_all** module for an end-to-end use of iragnsep, including generating plots and tables). SEDanalysis contains two main functions. **runSEDspecFit** is for dataset which combines spectral and photometric fluxes and **runSEDphotFit** is for dataset which contains photometric data only.

-- --

**res, resBM = SEDanalysis.runSEDspecFit(lambdaObs, fluxObs, efluxObs,
z = 0.01,
filters = ['PACS70', 'PACS100', 'PACS160', 'SPIRE250ps', 'SPIRE350ps', 'SPIRE500ps'],
wavToFit = [70., 100., 160., 250., 350., 500.],
UL = [0., 0., 0., 0., 0., 0.],
IRSobsCorr = True,
Nmc = 10000, pgrbar = 1,
Pdust = [10, 2.5], PPAH = [9., 2.5], Ppl = [0., 5.], Pbreak = [50., 0.01], Pslope1 = [0., 5.], Pslope2 = [0., 5.],
Plsg = [0., 5.], Pllg = [0., 5.],
templ = '')**

INPUT:

* **lambdaObs** - observed wavelengths in microns.
* **fluxObs** - observed fluxes in Jy.
* **efluxObs** - uncertainties on the observed fluxes in Jy.

OUTPUT:

* **res** - dataframe which contains all the results of the fits for each of the models (see section **Description of the tables**).
* **resBM** - same as res but for the best model only.

KEYWORDS:

* **z** - redshift of the source. Default: 0.01.
* **filters** - name of the broad band filters used in the fit. Default: ['PACS70', 'PACS100', 'PACS160', 'SPIRE250ps', 'SPIRE350ps', 'SPIRE500ps'].
* **wavToFit** - observed wavelengths of the broad band filters used in the fit. Default: [70., 100., 160., 250., 350., 500.].
* **UL** - if any of the value in the list is set to 1, the flux is treated as an upper limit. Default: [0., 0., 0., 0., 0., 0.].
* **IRSobsCorr** - if True, performs polynomial fits of the continuum around the 9.7micron absorption feature to correct for obscuration. Default: True.
* **Nmc** - numbers of steps in the MCMC. Default: 10000 (a bit too low. However runs fast for end-to-end tests).
* **pgrbar** - if set to 1, displays a progress bar. Default: 1.
* **Pdust** - normal prior on the log-normalisation of the galaxy dust continuum component ([mu, sigma]). Default: [10., 1.].
* **PPAH** - normal prior on the log-normalisation of the galaxy PAH emission component ([mu, sigma]). Default: [9., 1.].
* **Ppl** - normal prior on the log-normalisation of power-laws for the AGN continuum ([mu, sigma]). Default: [-1., 1.].
* **Pbreak** - normal prior on the position of the break for the AGN component ([mu, sigma]). Default: [40., 3.].
* **Pslope1** - normal prior on the slope of the AGN power-law below 15 micron ([mu, sigma]). Default: [1., 0.1].
* **Pslope2** - normal prior on the slope of the AGN power-law above 15 micron and below the main break ([mu, sigma]). Default: [1., 0.1].
* **Plsg** - normal prior on the log-normalisation of the silicate emission at 11 micron ([mu, sigma]). Default: [-1., 1.]. 
* **Pllg** - normal prior on the log-normalisation of the silicate emission at 19 micron ([mu, sigma]). Default: [-1., 1.].
* **templ** - templates to be used. Default: '' (B18 templates as described in Bernhard et al., in prep.).

-- --

**res, resBM = SEDanalysis.runSEDphotFit(lambdaObs, fluxObs, efluxObs,
z = 0.01,
filters = ['MIPS24', 'PACS70', 'PACS100', 'PACS160', 'SPIRE250ps', 'SPIRE350ps', 'SPIRE500ps'],
wavToFit = [24., 70., 100., 160., 250., 350., 500.],
UL = [0., 0., 0., 0., 0., 0., 0.],
Nmc = 10000, pgrbar = 1,
NoSiem = False,
Pdust = [10., 2.5], PPAH = [9., 2.5], PnormAGN = [10., 10.], PSiEm = [10., 10.],
templ = '')**

INPUT:

* **lambdaObs** - observed wavelengths in microns.
* **fluxObs** - observed fluxes in Jy.
* **efluxObs** - uncertainties on the observed fluxes in Jy.

OUTPUT:

* **res** - dataframe which contains all the results of the fits for each of the models (see section **Description of the tables**).
* **resBM** - same as res but for the best model only.

KEYWORDS:

* **z** - redshift of the source. Default: 0.01.
* **filters** - name of the broad band filters used in the fit. Default: ['MIPS24', 'PACS70', 'PACS100', 'PACS160', 'SPIRE250ps', 'SPIRE350ps', 'SPIRE500ps'].
* **wavToFit** - observed wavelengths of the broad band filters used in the fit. Default: [24., 70., 100., 160., 250., 350., 500.].
* **UL** - if any of the value in the list is set to 1, the flux is treated as an upper limit. Default: [0., 0., 0., 0., 0., 0., 0.].
* **Nmc** - numbers of steps in the MCMC. Default: 10000 (a bit too low. However runs fast for end-to-end tests).
* **pgrbar** - if set to 1 displays a progress bar. Default: 1.
* **Pdust** - normal prior on the log-normalisation of the galaxy dust continuum component ([mu, sigma]). Default: [10., 1.].
* **PPAH** - normal prior on the log-normalisation of the galaxy PAH emission component ([mu, sigma]). Default: [9., 1.].
* **PnormAGN** - normal prior on the log-normalisation of the AGN template component  ([mu, sigma]). Default: [10., 1.]
* **PSiEm** - normal prior on the log-normalisation of the silicate emission template component. Default: [10., 1.]
* **templ** - templates to be used. Default: '' (B18 templates as described in Bernhard et al., in prep.).

-- --

--


### toolplot

--

The module toolplot generates plots based on the results of the fits. toolplot contains two functions. plotFitSpec generates a plot showing all of the possible combinations of models and generates a plot showing that of the best model for dataset which combines spectral and photometric data. plotFitPhoto is the same as plotFitSpec but for photometric datasets.

-- --

**toolplot.plotFitSpec(df, data,
z = 0.01,
UL = np.array([]),
pathFig = './',
sourceName = 'NoName',
templ = '',
saveRes = True)**

INPUT:

* **df** - dataframe containing the output of SEDanalysis.runSEDspecFit (defined as "res" in this manual).
* **data** - a list of 3xNobs, where Nobs is the number of observed fluxes, and the first, second and third dimensions are the observed wavelengths, the observed fluxes and the uncertainties on the fluxes, respectively (i.e. [lambdaObs, fluxObs, efluxObs]).

KEYWORDS:

* **z** - redshift of the source. Default: 0.01.
* **UL** - if any of the value in the list is set to 1, the flux is treated as an upper limit. Default: np.array([]).
* **pathFig** - if the figures are to be saved, pathFig specifies the location. Default: './'.
* **sourceName** - if the figures are to be saved, sourceName specifies the name to be given. Default: 'NoName'.
* **templ** - templates to be used. Default: '' (B18 templates as described in Bernhard et al., in prep.).
* **saveRes** - if set to True the figures are saved as pathFig/sourceName_fitResAll_spec.pdf (all possible models) and pathFig/sourceName_fitResBM_spec.pdf (best model). Default = True.

-- --

**toolplot.plotFitPhoto(df, data,
z = 0.01,
UL = np.array([]),
pathFig = './',
sourceName = 'NoName',
templ = '',
saveRes = True)**

INPUT:

* **df** - dataframe containing the output of SEDanalysis.runSEDphotFit (defined as "res" in this manual).
* **data** - a list of 3xNobs, where Nobs is the number of observed points, and the first, second and third dimensions are the observed wavelengths, the observed fluxes and the uncertainties on the fluxes, respectively (i.e. [lambdaObs, fluxObs, efluxObs]).

KEYWORDS:

* **z** - redshift of the source. Default: 0.01.
* **UL** - if any of the value in the list is set to 1, the flux is treated as an upper limit. Default: np.array([]).
* **pathFig** - if the figures are to be saved pathFig specifies the location. Default: './'.
* **sourceName** - if the figures are to be saved sourceName specifies the name to be given. Default: 'NoName'.
* **templ** - templates to be used. Default: '' (B18 templates as described in Bernhard et al., in prep.).
* **saveRes** - if set to True the figures are saved as pathFig/sourceName_fitResAll_spec.pdf (all possible models) and pathFig/sourceName_fitResBM_spec.pdf (best model). Default = True.

-- --

--

### run_all

--

The module run_all eases the use of iragnsep by running everything from the fits to the plots and give the possibility to save the results as tables. run_all contains two functions. fitSpec performs everything on datasets which combine spectral and photometric data and fitPhoto does the same but on photometric datasets.

-- --

**res, resBM = run_all.fitSpec(wav, flux, eflux,
z = 0.01,
filters = ['PACS70', 'PACS100', 'PACS160', 'SPIRE250ps', 'SPIRE350ps', 'SPIRE500ps'],
wavToFit = [70., 100., 160., 250., 350., 500.],
UL = [0., 0., 0., 0., 0., 0.],
IRSobsCorr = True,
Nmc = 10000, pgrbar = 1,
Pdust = [10, 1.], PPAH = [9., 1.], Ppl = [-1., 1.], Pbreak = [40., 1.], Pslope1 = [1., 0.1], Pslope2 = [1., 0.1],
Plsg = [-1., 1.], Pllg = [-1., 1.],
sourceName = 'NoName', pathTable = './', pathFig = './',
redoFit = True, saveRes = True)**

INPUT:

* **wav** - observed wavelengths in microns.
* **flux** - observed fluxes in Jy.
* **eflux** - uncertainties on the observed fluxes in Jy.

OUTPUT:

* **res** - dataframe which contains all the results of the fits for each of the models (see the section **Description of the tables**).
* **resBM** - same as res but for the best model only.

KEYWORDS:

* **z** - redshift of the source. Default: 0.01.
* **filters** - name of the broad band filters used in the fit. Default: ['PACS70', 'PACS100', 'PACS160', 'SPIRE250ps', 'SPIRE350ps', 'SPIRE500ps'].
* **wavToFit** - observed wavelengths of the broad band filters used in the fit. Default: [70., 100., 160., 250., 350., 500.].
* **UL** - if any of the value in the list is set to 1, the flux is treated as an upper limit. Default: [0., 0., 0., 0., 0., 0.].
* **IRSobsCorr** - if True, performs polynomial fits of the continuum around the 9.7micron absorption feature to correct for obscuration. Default: True.
* **Nmc** - numbers of steps in the MCMC. Default: 10000 (a bit too low. However runs fast for end-to-end tests).
* **pgrbar** - if set to 1, displays a progress bar. Default: 1.
* **Pdust** - normal prior on the log-normalisation of the galaxy dust continuum component ([mu, sigma]). Default: [10., 1.].
* **PPAH** - normal prior on the log-normalisation of the galaxy PAH emission component ([mu, sigma]). Default: [9., 1.].
* **Ppl** - normal prior on the log-normalisation of power-laws for the AGN continuum ([mu, sigma]). Default: [-1., 1.].
* **Pbreak** - normal prior on the position of the break for the AGN component ([mu, sigma]). Default: [40., 3.].
* **Pslope1** - normal prior on the slope of the AGN power-law below 15 micron ([mu, sigma]). Default: [1., 0.1].
* **Pslope2** - normal prior on the slope of the AGN power-law above 15 micron and below the main break ([mu, sigma]). Default: [1., 0.1].
* **Plsg** - normal prior on the log-normalisation of the silicate emission at 11 micron ([mu, sigma]). Default: [-1., 1.]. 
* **Pllg** - normal prior on the log-normalisation of the silicate emission at 19 micron ([mu, sigma]). Default: [-1., 1.].
* **sourceName** - if the results are to be saved sourceName specifies the name to be given to the files. Default: 'NoName'.
* **pathTable** - if the results are to be saved pathTable specifies the location. Default: './'.
* **pathFig** - if the figures are to be saved pathFig specifies the location. Default: './'.
* **redoFit** - if set to True re-performs the fits. If set to False, get the results saved in pathTable/SourceName_fitRes_spec.csv to only produce the plots and the analysis. Default: True.
* **saveRes** - if set to True, saves the resulting tables as pathTable/SourceName_fitRes_spec.csv and plots as pathFig/SourceName_fitResAll_spec.pdf (all the possible models) and pathFig/SourceName_fitResBM_spec.pdf (best model).

----

**res, resBM = run_all.fitPhoto(wav, flux, eflux,
z = 0.01,
filters = ['PACS70', 'PACS100', 'PACS160', 'SPIRE250ps', 'SPIRE350ps', 'SPIRE500ps'],
wavToFit = [70., 100., 160., 250., 350., 500.],
UL = [0., 0., 0., 0., 0., 0.],
Nmc = 10000, nthreads = 1, pgrbar = 1,
NoSiem = False,
Pdust = [10., 1.], PPAH = [9., 1.], PnormAGN = [10., 1.], PSiEm = [10., 1.],
sourceName = 'NoName', pathTable = './', pathFig = './',
redoFit = True, saveRes = True)**

INPUT:

* **wav** - observed wavelengths in microns.
* **flux** - observed fluxes in Jy.
* **eflux** - uncertainties on the observed fluxes in Jy.

OUTPUT:

* **res** - dataframe which contains all the results of the fits for each of the models (see the section **Description of the tables**).
* **resBM** - same as res but for the best model only.

KEYWORDS:

* **z** - redshift of the source. Default: 0.01.
* **filters** - name of the broad band filters used in the fit. Default: ['MIPS24', 'PACS70', 'PACS100', 'PACS160', 'SPIRE250ps', 'SPIRE350ps', 'SPIRE500ps'].
* **wavToFit** - observed wavelengths of the broad band filters used in the fit. Default: [24., 70., 100., 160., 250., 350., 500.].
* **UL** - if any of the value in the list is set to 1, the flux is treated as an upper limit. Default: [0., 0., 0., 0., 0., 0., 0.].
* **Nmc** - numbers of steps in the MCMC. Default: 10000 (a bit too low. However runs fast for end-to-end tests).
* **pgrbar** - if set to 1 displays a progress bar. Default: 1.
* **Pdust** - normal prior on the log-normalisation of the galaxy dust continuum component ([mu, sigma]). Default: [10., 1.].
* **PPAH** - normal prior on the log-normalisation of the galaxy PAH emission component ([mu, sigma]). Default: [9., 1.].
* **PnormAGN** - normal prior on the log-normalisation of the AGN template component  ([mu, sigma]). Default: [10., 1.]
* **PSiEm** - normal prior on the log-normalisation of the silicate emission template component. Default: [10., 1.].
* **sourceName** - if the results are to be saved sourceName specifies the name to be given to the files. Default: 'NoName'.
* **pathTable** - if the results are to be saved pathTable specifies the location. Default: './'.
* **pathFig** - if the figures are to be saved pathFig specifies the location. Default: './'.
* **redoFit** - if set to True re-performs the fits. If set to False, get the results saved in pathTable/SourceName_fitRes_photo.csv to only produce the plots and the analysis. Default: True.
* **saveRes** - if set to True save the resulting tables as pathTable/SourceName_fitRes_photo.csv and plots as pathFig/SourceName_fitResAll_photo.pdf (all the possible models) and pathFig/SourceName_fitResBM_photo.pdf (best model).

----

--

### func

--

The module func contains a bunch of functions used to run the fits, the best model selection and the analysis.

-- --

**get_prop(df, z = 0.01, specOn = True, templ = '')**

Description:

This function runs the analysis to derive various properties (see OUTPUT) based on the fits of the IR SEDs.

INPUT:

* **df** - dataframe that contains the results of the fits as output of any SEDanalysis modules.

OUTPUT:

* **loglum_hostIR** - the IR (8--1000 microns) luminosity of the host free of AGN contamination.
* **eloglum_hostIR** - uncertainties on the IR luminosity of the host free of AGN contamination.
* **loglum_hostMIR** - the MIR (5--35 microns) luminosity of the host free of AGN contamination.
* **eloglum_hostMIR** - uncertainties on the MIR luminosity of the host free of AGN contamination.
* **loglum_hostFIR** - the FIR (40--1000 microns) luminosity of the host free of AGN contamination.
* **eloglum_hostFIR** - uncertainties on the FIR luminosity of the host free of AGN contamination.
* **loglum_AGNIR** - the IR luminosity of the AGN free of host contamination.
* **eloglum_AGNIR** - uncertainties on the IR luminosity of the AGN free of host contamination.
* **loglum_AGNMIR** - the MIR luminosity of the AGN free of host contamination.
* **eloglum_AGNMIR** - uncertainties on the MIR luminosity of the AGN free of host contamination.
* **loglum_AGNFIR** - the FIR luminosity of the AGN free of host contamination.
* **eloglum_AGNFIR** - uncertainties on the FIR luminosity of the AGN free of host contamination.
* **AGNfrac_IR** - the fraction of the total IR luminosity which is attributed to the AGN.
* **AGNfrac_MIR** - the fraction of the total MIR luminosity which is attributed to the AGN.
* **AGNfrac_FIR** - the fraction of the total FIR luminosity which is attributed to the AGN.
* **SFR** - the star formation rate free of AGN contamination.
* **eSFR** - uncertainties on the star formation rate free of AGN contamination.
* **wSFR** - the weighted star formation rate free of AGN contamination.
* **ewSFR** - uncertainties on the weighted star formation rate free of AGN contamination.

KEYWORDS:

* **z** - redshift of the source. Default: 0.01.
* **specOn** - if set to True the data are a combination of spectrum and photometry. If set to False the data are photometry only. Default: True.
* **templ** - templates to be used. Default: '' (B18 templates as described in Bernhard et al., in prep).

-- --

**basictests(wav, flux, eflux, filters, wavToFit, UL, z, specOn = True)**

Description:

This function runs some basic tests to check that everything is ready to be fed to the various modules of iragnsep.

INPUT:

* **wav** - observed wavelengths in microns.
* **flux** - observed fluxes in Jy.
* **eflux** - uncertainties on the observed fluxes in Jy.
* **filters** - name of the broad band filters.
* **wavToFit** - observed wavelengths of the broad band filters used in the fit.
* **UL** - vector of length equal to wavToFit. If any of the values in the list is set to 1, the flux is treated as an upper limit.
* **z** - redshift of the source.

OUTPUT:

Pass or crash with error messages.

KEYWORDS:

* **specOn** - if set to True the data are a combination of spectrum and photometry. If set to False the data are photometric only. Default: True.

-- --

**exctractBestModel(logl, k, n, corrected = True)**

Description:

This function finds the best model across the various possible combinations of models accounting for the differences in the numbers of degrees of freedom by using the AIC or the corrected AIC.

INPUT:

* **logl** - the log-likelihood of the fit.
* **k** - the total numbers of free parameters in the models.
* **n** - the total numbers of data points.

OUTPUT:

* **bestModelInd** - the index of the best model.
* **Awi** - the Akaike weight of each individual model.

KEYWORDS:

* **corrected** - if set to true applies the corrected AIC (AICc). Default: True.

-- --

**nuLnuToFnu(spec_wav, nuLnu, z)**

Description:

This function takes the model nuLnu and transforms it to observed fluxes at the given redshift.

INPUT:

* **spec_wav** - the wavelengths in microns.
* **nuLnu** - the model nuLnu.
* **z** - the redshift of the source.

OUTPUT:

* **Fnu** - observed flux in Jy.

-- --

**getFluxInFilt(filt_wav, filt_QE, spec_wav, nuLnu, z)**

Description:

This function calculates the observed flux within a given filter from the model nuLnu located at a redshift z.

INPUT:

* **filt_wav** - passband of the filter.
* **filt_QE** - quantum efficiency of the filter.
* **spec_wav** - the wavelengths in microns.
* **nuLnu** - the model nuLnu.
* **z** - the redshift of the source.

OUTPUT:

* **flux_Obs** - the observed flux.

-- --

**Gauss(x, mu, sigma)**

Description:

This function returns a simple Gaussian centred on mu and of width sigma.

INPUT:

* **x** - wavelengths in microns.
* **mu** - central location of the Gaussian.
* **sigma** - width of the Gaussian.

OUTPUT:

* **Bnu** - Gaussian normalised to the peak value.
__ __

**AGNmodel(x, lambdab1, lambdab2, alpha1, alpha2, alpha3)**

Description:

This function calculates the shape of the model for the AGN emission as described in Bernhard et al. (in prep).

INPUT:

* **x** - wavelengths in microns.
* **lambda1** - position of the break for the first broken power-law.
* **lambda2** - position of the break for the second broken power-law.
* **alpha1** - slope of the first power-law below lambda1.
* **alpha2** - slope of the first power-law above lambda1. Also, slope of the second power-law below lambda2.
* **alpha3** - slope of the second power-law above lambda2.

OUTPUT:

* **Bnu** - full model for AGN normalised at 15 microns.

-- --

**KVTextinctCurve(lambda_obs)**

Description:

This function calculates the extinction curve as presented in Kemper et al. (2004).

INPUT:

* **lambda_obs** - the observed wavelengths in microns.

OUTPUT:

* **tau** - the value of the extinction at any given wavelengths.

-- --

**drude(x, gamma_r, lambda_r, normed = True)**

Description:

This function calculates a Drude profile given a central wavelengths gamma_r and a fractional FWHM lambda_r.

INPUT:

* **x** - wavelengths in microns.
* **gamma_r** - central wavelengths.
* **lambda_r** - fractional FWHM.

OUTPUT:

* **drudeVal** - the corresponding drude model at wavelength x.

KEYWORDS:

* **normed** - if set to True the drude profile is normalised to its maximum value. Default: true.

-- --

**corrIRSobs(IRSwavRest, IRSflux, eIRSflux):**

Description:

This function takes an observed flux and corrects for extinction as described in Bernhard et al. (in prep).

INPUT:

* **IRSwavRest** - rest-wavelengths in microns of the observed SED.
* **IRSflux** - observed (attenuated) fluxes in Jy.
* **eIRSflux** - uncertainties on the observed fluxes in Jy.

OUTPUT:

* **IRSflux_corr** - de-attenuated fluxes in Jy.
* **eIRSflux_corr** - uncertainties on the de-attenuated fluxes in Jy.
* **_tau9p7** - total absorption at 9.7 microns.

-- --

**mod_black_body_norm(x, T, beta)**

Description:

This function calculates the modified black-body curve at a temperature T and with beta index beta.

INPUT:

* **x** - wavelengths in microns.
* **T** - temperature in K.
* **beta** - beta index of the source.

OUTPUT:

* **Bnu** - normalised modified black body curve.

-- --

--

### classes

--

The module classes contains one class called 'modelToSED' which calls various functions to return the photometric point at a given wavelengths in a given filters for a model nuLnu. The available filters are as follow:

* **IRAC1** - Spitzer IRAC, 3.6 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **IRAC2** - Spitzer IRAC, 4.5 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **IRAC3** - Spitzer IRAC, 5.8 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **IRAC4** - Spitzer IRAC, 8.0 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **WISE_W1** - WISE, 3.4 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **WISE_W2** - WISE, 4.6 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **WISE_W3** - WISE, 12 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **WISE_W4** - WISE, 22 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **IRAS12** - IRAS, 12 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=IRAS
* **IRAS60** - IRAS, 60 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=IRAS
* **IRAS100** - IRAS, 100 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=IRAS
* **MIPS24** - Spitzer MIPS, 24 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer&gname2=MIPS
* **MIPS70** - Spitzer MIPS, 70 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer&gname2=MIPS
* **MIPS160** - Spitzer MIPS, 160 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer&gname2=MIPS
* **PACS70** - Herschel PACS, 70 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel
* **PACS100** - Herschel PACS, 100 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel
* **PACS160** - Herschel PACS, 160 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel
* **SPIRE250ps** - Herschel SPIRE, 250 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel&gname2=SPIRE
* **SPIRE350ps** - Herschel SPIRE, 350 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel&gname2=SPIRE
* **SPIRE500ps** - Herschel SPIRE, 500 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel&gname2=SPIRE

Note: to add filter please contact e.p.bernhard[at]sheffield.ac.uk.

-- --

## Cautionary notes

As this is the first version of iragnsep we suggest the user to check carefully the results and to report anything that is possibly a bug. To do this, please contact us at: e.p.bernhard[at]sheffield.ac.uk.

The templates and models built for iragnsep are based on observations out to z=0.3 . As a consequence there is no proof that these are valid at higher redshifts. We are currently testing this and early results suggest that iragnsep can be used for sources at higher redshifts i.e. z=0.3 . However, this is at the user's own risk.

The templates have been derived on moderate luminosity AGNs 41.6 erg/s<Log10(Lx2-10kev)<45.2 erg/s. As a consequence, using iragnsep for let's say bright QSOs is at the User's own risks.

## Future work

Future version will allow a more flexible input for the observed data. In addition it will be possible for the user to choose a complete different set of templates if necessary and to use iragnsep as a fitting and analysis routine only. We also plan to increase to even higher level the robustness of the model selection by using different model testing methods.

For this version we use Numba to speed up the code. This python dependency pre-compiles the meaty bit of the code allowing iragnsep to run faster. Using Numba we have sped up iragnsep by a factor of 10. Since MCMC are time expensive, we are planning to further incorporate multi-threading for a possible increase in the speed.

So far we have tested iragnsep using data from the IRS spectra and Herschel photometric data only. We are currently testing the possibility to incorporate other spectral data such as future JWST data.

## Versioning

We use three numbers for the versions defined as x.y.z. If only y and z are changed the output of iragnsep is unchanged and minor patches are applied. If x changes it means that major changes has been applied and results are likely to differ from the x-1 version.

The first released version starts at x=3.

## Authors

* **Emmanuel Bernhard** - *Initial work*
* James Mullaney
* Clive Tadhunter

The associated paper can be found at Bernhard et al. (in prep).

## Citation

Please cite Bernhard et al. (in prep) when using iragnsep.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details