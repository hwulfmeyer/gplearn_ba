"""Selection methods to choose programs from the population

The :mod:`gplearn.selection` module contains some selection method 
with  which to choose from the computer programs created by 
the :mod:`gplearn.genetic` module.
"""

# Author: Hans-Martin Wulfmeyer <wulfmeyer.me>
#
# License: BSD 3 clause

import numpy as np

__all__ = ['make_selection']


class _Selection(object):

    """A selection method to get suitable individuals from the population

        TODO: Description

    Parameters
    ----------
    function : callable
        TODO: Description
    """

    def __init__(self, function, **kwargs):
        self.function = function
        self.kwargs = kwargs
        self.save = None

    def __call__(self, *args):       
        parent, parent_index, self.save = self.function(*args, **self.kwargs, save=self.save)
        return parent, parent_index


def make_selection(function, **kwargs):
    """Make a selection method

    This factory function creates a selection method object which takes the
    population of programs and selects suitable candiadtes for the evolution
    process.

    Parameters
    ----------
    function : callable
        TODO: description

    *args : TODO: datatype
        TODO: description

    """

    """
        TODO: some tests
        1. Test **kwargs contains all the default parameters needed by
            the provided function (or simply the same number of arguments)
        1. Test that function works with the **kwargs provided and returns
            an indivdual from the population
    """

    return _Selection(function, **kwargs)


def _tournament(random_state, parents, greater_is_better, tournament_size, save):
        """Find the fittest individual from a sub-population."""
        contenders = random_state.randint(0, len(parents), tournament_size)
        fitness = [parents[p].fitness_ for p in contenders]
        if greater_is_better:
            parent_index = contenders[np.argmax(fitness)]
        else:
            parent_index = contenders[np.argmin(fitness)]
        return parents[parent_index], parent_index, save


def _paretogp(random_state, paretofront, save):
        parent_index = random_state.randint(0, len(paretofront))
        return paretofront[parent_index], parent_index, save
        

def _eplex(random_state, parents, greater_is_better, X, y, save):
    survivors = np.arange(len(parents))
    cases = random_state.permutation(len(y))

    if save is None:
        errorsall = np.zeros((len(parents), len(y)))   
        for i, p in enumerate(parents):
            penalty = p.parsimony_coefficient * p.complexity()
            errorsall[i] = np.abs(p._y_pred - y) + penalty
        save = errorsall
    else:
        errorsall = save

    for case in cases:
        if len(survivors) == 1:
            break
        curerrorsall = errorsall[:,case]
        errors = [curerrorsall[k] for k in survivors]
        MAD = np.median(np.abs(errors - np.median(errors)))
        treshold = min(errors) + MAD
        survivors = [k for i, k in enumerate(survivors) if errors[i] <= treshold]
    
    parent_index = random_state.choice(survivors)
    return parents[parent_index], parent_index, save


_selection_map = {'tournament': _tournament,
                    'eplex': _eplex}