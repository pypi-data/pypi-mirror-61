"""
Utility functions for creating synthetic (geochemical) data.
"""
import numpy as np
import pandas as pd
from ..comp.codata import ilr, inverse_ilr


def random_cov_matrix(dim, sigmas=None, validate=False, seed=None):
    """
    Generate a random covariance matrix which is symmetric positive-semidefinite.

    Parameters
    -----------
    dim : :class:`int`
        Dimensionality of the covariance matrix.
    sigmas : :class:`numpy.ndarray`
        Optionally specified sigmas for the variables.
    validate : :class:`bool`
        Whether to validate output.

    Returns
    --------
    :class:`numpy.ndarray`
        Covariance matrix of shape :code:`(dim, dim)`.

    Todo
    -----
        * Implement a characteristic scale for the covariance matrix.
    """
    if seed is not None:
        np.random.seed(seed)
    # create a matrix of correlation coefficients
    corr = (np.random.rand(dim, dim) - 0.5) * 2  # values between -1 and 1
    corr[np.tril_indices(dim)] = corr.T[np.tril_indices(dim)]  # lower=upper
    corr[np.arange(dim), np.arange(dim)] = 1.0

    if sigmas is None:
        sigmas = np.ones(dim).reshape(1, dim)
    else:
        sigmas = np.array(sigmas)
        sigmas = sigmas.reshape(1, dim)

    cov = sigmas.T @ sigmas  # multiply by ~ variance
    cov *= corr
    cov = np.sign(cov) * np.sqrt(np.abs(cov) / dim)
    cov = cov @ cov.T

    if validate:
        try:
            assert (cov == cov.T).all()
            # eig = np.linalg.eigvalsh(cov)
            for i in range(dim):
                assert np.linalg.det(cov[0:i, 0:i]) > 0.0  # sylvesters criterion
        except:
            cov = random_cov_matrix(dim, validate=validate)
    return cov


def random_composition(
    size=1000,
    D=4,
    mean=None,
    cov=None,
    propnan=0.1,
    missingcols=None,
    missing=None,
    seed=None,
):
    """
    Generate a simulated random unimodal compositional dataset,
    optionally with missing data.

    Parameters
    -----------
    size : :class:`int`
        Size of the dataset.
    D : :class:`int`
        Dimensionality of the dataset.
    mean : :class:`numpy.ndarray`, :code:`None`
        Optional specification of mean composition.
    cov : :class:`numpy.ndarray`, :code:`None`
        Optional specification of covariance matrix (in log space).
    propnan : :class:`float`, [0, 1)
        Proportion of missing values in the output dataset.
    missingcols : :class:`int` | :class:`tuple`
        Specification of columns to be missing. If an integer is specified,
        interpreted to be the number of columns containin missing data (at a proportion
        defined by `propnan`). If a tuple or list, the specific columns to contain
        missing data.
    missing : :class:`str`, :code:`None`
        Missingness pattern.
        If not :code:`None`, a string in :code:`{"MCAR", "MAR", "MNAR"}`.

            * If :code:`missing = "MCAR"``, data will be missing at random.
            * If :code:`missing = "MAR"``, data will be missing with some relationship to other parameters.
            * If :code:`missing = "MNAR"``, data will be thresholded at some lower bound.

    Returns
    --------
    :class:`numpy.ndarray`
        Simulated dataset with missing values.

    Todo
    ------
        * Add feature to translate rough covariance in D to logcovariance in D-1
        * Update the `:code:`missing = "MAR"`` example to be more realistic/variable.
    """
    data = None
    # dimensions
    if mean is None and cov is None:
        pass
    elif mean is None:
        D = cov.shape[0] + 1
    elif cov is None:
        mean = np.array(mean)
        D = mean.size
    else:  # both defined
        mean, cov = np.array(mean), np.array(cov)
        assert mean.size == cov.shape[0] + 1
        D = mean.size
        mean = mean.reshape(1, -1)

    if seed is not None:
        np.random.seed(seed)
    # mean
    if mean is None:
        if D > 1:
            mean = np.random.randn(D - 1).reshape(1, -1)
        else:  # D == 1, return a 1D series
            data = np.exp(np.random.randn(size).reshape(size, D))
            data /= np.nanmax(data)
            return data
    else:
        mean = ilr(mean.reshape(1, D)).reshape(
            1, -1
        )  # ilr of a (1, D) mean to (1, D-1)

    # covariance
    if cov is None:
        if D != 1:
            cov = random_cov_matrix(D - 1, sigmas=np.abs(mean) * 0.1, seed=seed)  # 10% sigmas
        else:
            cov = np.array([[1]])

    assert cov.shape in [(D - 1, D - 1), (1, 1)]

    if size == 1:  # single sample
        data = inverse_ilr(mean).reshape(size, D)

    # if the covariance matrix isn't for the logspace data, we'd have to convert it
    if data is None:
        data = inverse_ilr(
            np.random.multivariate_normal(mean.reshape(D - 1), cov, size=size)
        ).reshape(size, D)

    if missingcols is None:
        nancols = (
            np.random.choice(
                range(data.shape[1] - 1), size=int(data.shape[1] - 1), replace=False
            )
            + 1
        )
    elif isinstance(missingcols, int):  # number of columns specified
        nancols = (
            np.random.choice(range(data.shape[1] - 1), size=missingcols, replace=False)
            + 1
        )
    else:  # tuples, list etc
        nancols = missingcols

    if missing is not None:
        if missing == "MCAR":
            for i in nancols:
                data[np.random.randint(size, size=int(propnan * size)), i] = np.nan
        elif missing == "MAR":
            thresholds = np.percentile(data[:, nancols], propnan * 100, axis=0)[
                np.newaxis, :
            ]
            # should update this such that data are proportional to other variables
            # potentially just by rearranging the where statement
            data[:, nancols] = np.where(
                data[:, nancols]
                < np.tile(thresholds, size).reshape(size, len(nancols)),
                np.nan,
                data[:, nancols],
            )
        elif missing == "MNAR":
            thresholds = np.percentile(data[:, nancols], propnan * 100, axis=0)[
                np.newaxis, :
            ]
            data[:, nancols] = np.where(
                data[:, nancols]
                < np.tile(thresholds, size).reshape(size, len(nancols)),
                np.nan,
                data[:, nancols],
            )
        else:
            msg = "Provide a value for missing in {}".format(
                set(["MCAR", "MAR", "MNAR"])
            )
            raise NotImplementedError(msg)

    return data


def test_df(
    cols=["SiO2", "CaO", "MgO", "FeO", "TiO2"], index_length=10, mean=None, **kwargs
):
    """
    Creates a pandas.DataFrame with random data.
    """
    return pd.DataFrame(
        columns=cols,
        data=random_composition(size=index_length, D=len(cols), mean=mean, **kwargs),
    )


def test_ser(index=["SiO2", "CaO", "MgO", "FeO", "TiO2"], mean=None, **kwargs):
    """
    Creates a pandas.Series with random data.
    """
    return pd.Series(
        random_composition(size=1, D=len(index), mean=mean, **kwargs).flatten(),
        index=index,
    )
