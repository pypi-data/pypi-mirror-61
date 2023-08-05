UVFlag Parameters
=================
These are the standard attributes of UVFlag objects.

Under the hood they are actually properties based on UVParameter objects.

Required
----------------
These parameters are required to have a sensible UVFlag object and 
are required for most kinds of uv data files.

**Nants_data**
     Number of antennas with data present. Only available for "baseline" or "antenna" type objects.May be smaller than the number of antennas in the array

**Nants_telescope**
     Number of antennas in the array. Only available for "baseline" type objects. May be larger than the number of antennas with data.

**Nbls**
     Number of baselines. Only Required for "baseline" type objects.

**Nblts**
     Number of baseline-times (i.e. number of spectra). Not necessarily equal to Nbls * Ntimes

**Nfreqs**
     Number of frequency channels

**Npols**
     Number of polarizations

**Nspws**
     Number of spectral windows (ie non-contiguous spectral chunks). More than one spectral window is not currently supported.

**Ntimes**
     Number of times

**ant_1_array**
     Array of first antenna indices, shape (Nblts). Only available for "baseline" type objects. type = int, 0 indexed

**ant_2_array**
     Array of second antenna indices, shape (Nblts). Only available for "baseline" type objects. type = int, 0 indexed

**baseline_array**
     Array of baseline indices, shape (Nblts). Only available for "baseline" type objects. type = int; baseline = 2048 * (ant1+1) + (ant2+1) + 2^16

**freq_array**
     Array of frequencies, center of the channel, shape (Nspws, Nfreqs), units Hz

**history**
     String of history, units English

**label**
     String used for labeling the object (e.g. 'FM'). Default is empty string.

**lst_array**
     Array of lsts, center of integration, shape (Nblts), units radians

**metric_array**
     Floating point metric information, only availble in metric mode. shape (Nblts, Nspws, Nfreq, Npols).

**mode**
     The mode determines whether the object has a floating point metric_array or a boolean flag_array. Options: {"metric", "flag"}. Default is "metric".

**polarization_array**
     Array of polarization integers, shape (Npols). AIPS Memo 117 says: pseudo-stokes 1:4 (pI, pQ, pU, pV);  circular -1:-4 (RR, LL, RL, LR); linear -5:-8 (XX, YY, XY, YX). NOTE: AIPS Memo 117 actually calls the pseudo-Stokes polarizations "Stokes", but this is inaccurate as visibilities cannot be in true Stokes polarizations for physical antennas. We adopt the term pseudo-Stokes to refer to linear combinations of instrumental visibility polarizations (e.g. pI = xx + yy).

**time_array**
     Array of times, center of integration, shape (Nblts), units Julian Date

**type**
     The type of object defines the form of some arrays  and also how metrics/flags are combined. Accepted types:"waterfall", "baseline", "antenna"

**weights_array**
     Floating point weight information, shape (Nblts, Nspws, Nfreq, Npols).

Optional
----------------
These parameters are defined by one or more  type but are not always required.
Some of them are required depending on the type (as noted below).

**ant_array**
     Array of antenna numbers, shape (Nants_data), Only available for "antenna" type objects. type = int, 0 indexed

**flag_array**
     Boolean flag, True is flagged, only availble in flag mode. shape (Nblts, Nspws, Nfreq, Npols).

**x_orientation**
     Orientation of the physical dipole corresponding to what is labelled as the x polarization. Options are "east" (indicating east/west orientation) and "north" (indicating north/south orientation)

last updated: 2020-01-31