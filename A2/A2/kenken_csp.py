'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''

from cspbase import Variable, Constraint, CSP
from itertools import permutations, product
from functools import reduce
import operator


def binary_ne_grid(kenken_grid):
    # Initialize
    dim = kenken_grid[0][0]
    vars = []
    vars_1d = []
    cons = []

    # construct list of lists of Variable objects 
    for i in range(dim):
        vars.append([])
        for j in range(dim):
            var = Variable("Cell_r%i_c%i"%(i+1,j+1), domain = [z for z in range(1, dim+1)])
            vars_1d.append(var)
            vars[i].append(var)


    # construct csp
    for i in range(dim):
        for j in range(dim-1):
            for k in range(j+1, dim):

                #for row
                con = Constraint("ConstraintRow_r%i_c%i_c%i"%(i+1,j+1,k+1), [vars[i][j],vars[i][k]])
                tuples = []
                for Tuple in permutations(list(range(1,dim+1)),2):
                    tuples.append(Tuple)
                con.add_satisfying_tuples(tuples)
                cons.append(con)

                #for col
                con = Constraint("ConstraintCol_c%i_r%i_r%i"%(i+1,j+1,k+1), [vars[j][i],vars[k][i]])
                tuples = []
                for Tuple in permutations(list(range(1,dim+1)),2):
                    tuples.append(Tuple)
                con.add_satisfying_tuples(tuples)
                cons.append(con)

    csp = CSP("binary_ne_grid", vars_1d)
    for con in cons:
        csp.add_constraint(con)

    return csp, vars




def nary_ad_grid(kenken_grid):
    # Initialize
    dim = kenken_grid[0][0]
    vars = []
    vars_1d = []
    cons = []

    # construct list of lists of Variable objects 
    for i in range(dim):
        vars.append([])
        for j in range(dim):
            var = Variable("Cell_r%i_c%i"%(i+1,j+1), domain = [z for z in range(1, dim+1)])
            vars_1d.append(var)
            vars[i].append(var)

    # construct csp
    for i in range(dim):

        #for row
        con = Constraint("ConstraintRow_r%i"%i, vars[i])
        tuples = []
        for Tuple in permutations(list(range(1, dim+1))):
            tuples.append(Tuple)
        con.add_satisfying_tuples(tuples)
        cons.append(con)

        #for col
        con = Constraint("ConstraintCol_r%i"%i, [(vars[row][i]) for row in range(n)])
        tuples = []
        for Tuple in permutations(list(range(1, dim+1))):
            tuples.append(Tuple)
        con.add_satisfying_tuples(tuples)
        cons.append(con)

    csp = CSP("nary_ad_grid", vars_1d)
    for con in cons:
        csp.add_constraint(con)

    return csp, vars



def kenken_csp_model(kenken_grid):
    '''
    Use nary_ad_grid
    '''

    # Initialize
    dim = kenken_grid[0][0]
    vars = []
    vars_1d = []
    cons = []

    # construct list of lists of Variable objects 
    for i in range(dim):
        vars.append([])
        for j in range(dim):
            var = Variable("Cell_r%i_c%i"%(i+1,j+1), domain = [z for z in range(1, dim+1)])
            vars_1d.append(var)
            vars[i].append(var)

    # nary_ad_grid
    for i in range(dim):

        #for row
        con = Constraint("ConstraintRow_r%i"%i, vars[i])
        tuples = []
        for Tuple in permutations(list(range(1, dim+1))):
            tuples.append(Tuple)
        con.add_satisfying_tuples(tuples)
        cons.append(con)

        #for col
        con = Constraint("ConstraintCol_r%i"%i, [(vars[row][i]) for row in range(dim)])
        tuples = []
        for Tuple in permutations(list(range(1, dim+1))):
            tuples.append(Tuple)
        con.add_satisfying_tuples(tuples)
        cons.append(con)

    # construct kenken constraints
    for idx, val in enumerate(kenken_grid[1:]):
        if len(val) == 2:
            con = Constraint("KenKen_%i"%idx, [(vars[(val[0]//10)-1][(val[0]%10)-1])])
            tuples = [[val[1]]]

        else:
            con = Constraint("KenKen_%i"%idx, [(vars[(i//10)-1][(i%10)-1]) for i in val[:-2]])
            tuples = []

            for comb in product(list(range(1,dim+1)), repeat = (len(val)-2)):
                if val[-1] == 0: 
                    oper = operator.add
                elif val[-1] == 1: 
                    oper = operator.sub 
                elif val[-1] == 2: 
                    oper = operator.truediv 
                elif val[-1] == 3: 
                    oper = operator.mul

                if reduce(oper, comb) == val[-2]:
                    for permu in permutations(comb):
                        if permu not in tuples:
                            tuples.append(permu)

        con.add_satisfying_tuples(tuples)
        cons.append(con)

    csp = CSP("kenken_csp_model", vars_1d)
    for con in cons:
        csp.add_constraint(con)

    return csp, vars