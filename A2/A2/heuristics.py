'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy

def ord_dh(csp):
    # TODO! IMPLEMENT THIS!
    unasgns = csp.get_all_unasgn_vars()
    degrees = []
    for unasgn in unasgns:
        degree = 0
        for c in csp.get_cons_with_var(unasgn):
            if c.get_n_unasgn() > 1:
                degree += 1
        degrees.append(degree)
    return unasgns[degrees.index(max(degrees))]

def ord_mrv(csp):
    # TODO! IMPLEMENT THIS!
    unasgns = csp.get_all_unasgn_vars()
    domSize = [(unasgn.cur_domain_size()) for unasgn in unasgns]
    return unasgns[domSize.index(min(domSize))]

def val_lcv(csp, var):
    # TODO! IMPLEMENT THIS!
    vals = var.cur_domain().copy()
    inflexs = {}

    for val in vals:
        var.assign(val)
        cs = csp.get_cons_with_var(var)
        prunes = []
        flag = False

        while len(cs) != 0:
            c = cs.pop(0)
            for v in c.get_scope():
                if not v.is_assigned():
                    curDom = deepcopy(v.cur_domain())
                    for d in curDom:
                        if not c.has_support(v,d):
                            prunes.append((v,d))
                            v.prune_value(d)
                            if v.cur_domain_size() == 0:
                                flag = True
                                break
                            else:
                                for cPrime in csp.get_cons_with_var(v):
                                    if cPrime not in cs:
                                        cs.append(cPrime)
                if flag:
                	break
        inflexs[val] = len(prunes)

        for a, b in prunes:
            a.unprune_value(b)
        var.unassign()

    return sorted(inflexs, key = inflexs.__getitem__, reverse = True)



