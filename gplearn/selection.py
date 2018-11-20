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

    def __call__(self, *args):
        return self.function(*args, **self.kwargs)


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


def _tournament(random_state, parents, tournament_size, greater_is_better):
        """Find the fittest individual from a sub-population."""
        contenders = random_state.randint(0, len(parents), tournament_size)
        fitness = [parents[p].fitness_ for p in contenders]
        if greater_is_better:
            parent_index = contenders[np.argmax(fitness)]
        else:
            parent_index = contenders[np.argmin(fitness)]
        return parents[parent_index], parent_index


def _nsga2(random_state, parents, tournament_size, greater_is_better):
        """Find the fittest individual from a sub-population."""
        """
        ### 1. fast non-dominated sorting
        for A in parents:
            for B in parents:
                if A dominates B:
                    A.doms.append(B)
                elif B dominates A:
                    A.dombycount = A.dombycount + 1
            if A.dombycount == 0:
                A.rank = 0
                firstfront.append(A)
        prfronts = []
        prfronts.append(firstfront)
        i = 0
        while len(prfronts[i]) != 0:
            nextfront = []
            for A in prfronts[i]:
                for B in A.doms:
                    B.dombycount = B.dombycount - 1
                    if B.dombycount == 0:
                        B.rank = i + 1
                        nextfront.append(B)
            i = i +1
            pfronts.append(nextfront)

        ### 2. crowding distance
        for front in prfronts:
            for obj in objectives:
                front = front.sort(obj)
                pfrontop[0] = front[-1] = MAX_FLOAT
                for i in range(1, len(pop)-1):
                    front[i].dist = front[i].dist + (front[i+1].obj-front[i-1].obj) / (np.argmax(front.obj) - np.argmin(front.obj))
        """
        # 2. select parents by rank
        contenders = random_state.randint(0, len(parents), tournament_size)
        parent_index = contenders[0]
        return parents[parent_index], parent_index


_selection_map = {  'tournament': _tournament,
                    'nsga2': _nsga2}