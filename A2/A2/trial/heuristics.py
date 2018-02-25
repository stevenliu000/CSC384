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
    unasgn_vars = csp.get_all_unasgn_vars()
    vars_degree = []
    for var in unasgn_vars:
        var_degree = 0
        for c in csp.get_cons_with_var(var):
            if c.get_n_unasgn()>1:
                var_degree +=1
        vars_degree.append(var_degree)
    return unasgn_vars[vars_degree.index(max(vars_degree))]
    #pass

def ord_mrv(csp):
    # TODO! IMPLEMENT THIS!
    unasgn_vars = csp.get_all_unasgn_vars()
    domain_size = [size.cur_domain_size() for size in unasgn_vars]
    return unasgn_vars[domain_size.index(min(domain_size))]
    #pass

def val_lcv(csp, var):
    # TODO! IMPLEMENT THIS!    
    vals = var.cur_domain().copy()
    flexibility_list = []
    
    for val in vals:
        var.assign(val)
        GAC_queue = csp.get_cons_with_var(var)
        prune_list = []
        while not len(GAC_queue)==0:
            c = GAC_queue.pop(0)
            for v in c.get_scope():
                if v.is_assigned():
                    continue
                else:
                    current_domain = deepcopy(v.cur_domain())
                    for d in current_domain:
                        if not c.has_support(v,d):
                            v.prune_value(d)
                            prune_list.append((v,d))
                            for cp in csp.get_cons_with_var(v):
                                if not cp in GAC_queue:
                                    GAC_queue.append(cp)
        flexibility_list.append(len(prune_list))
        for variable, values in prune_list:
            variable.unprune_value(values)
        var.unassign()
    result = []    
    while len(flexibility_list) != 0:
        result.append(vals.pop(flexibility_list.index(min(flexibility_list))))
        flexibility_list.remove(min(flexibility_list))
    return result
    #pass