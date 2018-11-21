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


def _nsga2(random_state, parents_nsga, parents, tournament_size, greater_is_better):
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
        """
        # [[parent0, domination-list1, dominated by counter2, rank3, dist4, index5], [...]]
        if parents_nsga is None:
            parents_nsga = [[parents[i], [], 0,-1, 0, i] for i in range(len(parents))]
            firstfront = []
            for A in parents_nsga:
                for B in parents_nsga:
                    # check domination
                    if round(B[0].fitness_, 4) > round(A[0].fitness_, 4):
                        if B[0].length_ > A[0].length_:
                            # A dominates B
                            A[1].append(B)
                    elif round(A[0].fitness_, 4) > round(B[0].fitness_, 4):
                        if A[0].length_ > B[0].length_:
                            # B dominates A
                            A[2] = A[2] + 1

                if A[2] == 0:
                    A[3] = 0
                    firstfront.append(A)
            prfronts = []
            prfronts.append(firstfront)
            i = 0
            while len(prfronts[i]) != 0:
                nextfront = []
                for A in prfronts[i]:
                    for B in A[1]:
                        B[2] = B[2] - 1
                        if B[2] == 0:
                            B[3] = i + 1
                            nextfront.append(B)
                i = i + 1
                prfronts.append(nextfront)   
            prfronts.pop()
            """
            ### 2. crowding distance
            for front in prfronts:
                for obj in objectives:
                    front = front.sort(obj)
                    front[0] = front[-1] = MAX_FLOAT
                    for i in range(1, len(pop)):
                        front[i].dist = front[i].dist + (front[i+1].obj-front[i-1].obj) / (np.argmax(front.obj) - np.argmin(front.obj))
            """
            for front in prfronts:
                front = sorted(front, key=lambda A: A[0].fitness_)
                front[0][4] = np.finfo(np.float).max
                front[-1][4] = np.finfo(np.float).max
                normalizer = 1
                if front[-1][0].fitness_ - front[0][0].fitness_ != 0:
                    normalizer = front[-1][0].fitness_ - front[0][0].fitness_
                for i in range(1, len(front)-1):
                    front[i][4] = front[i][4] + (front[i+1][0].fitness_ - front[i-1][0].fitness_) / normalizer

                front = sorted(front, key=lambda A: A[0].length_)
                front[0][4] = np.finfo(np.float).max
                front[-1][4] = np.finfo(np.float).max
                normalizer = 1
                if front[-1][0].length_ - front[0][0].length_ != 0:
                    normalizer = front[-1][0].length_ - front[0][0].length_
                for i in range(1, len(front)-1):
                    front[i][4] = front[i][4] + (front[i+1][0].length_ - front[i-1][0].length_) / normalizer


        ### 3. select parents by rank, or rank & distance
        contenders = random_state.randint(0, len(parents), tournament_size)

        parents_contenders = [parents_nsga[p] for p in contenders]
        parents_contenders = sorted(parents_contenders, key=lambda A: A[3])
        selected = []
        for p in parents_contenders:
            if p[3] == parents_contenders[0][3]:
                selected.append(p)
            else:
                break
        if len(selected) > 1:
            selected = sorted(selected, key=lambda A: A[4], reverse=True)
        parent_index = selected[0][5]
        return parents[parent_index], parent_index, parents_nsga


_selection_map = {  'tournament': _tournament,
                    'nsga2': _nsga2}