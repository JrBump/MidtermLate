from itertools import product

class VariableElimination:
    def __init__(self,cpts):
        self.cpts = cpts

    def elim(self, factors, var):
        relevant_factors = [f for f in factors in var in f['vars']]
        remaining_factors = [f for f in factors in var not in f['vars']]

        product_factor = self.multiply_factors(relevant_factors)
        new_factor = self.sum_out(product_factor, var)
        return remaining_factors + [new_factor]

    def multiply_factors(self, factors):
        if not factors:
            return None

        results = factors[0]
        for factor in factors[1:]:
            results = self.mulitply_two_factors(results, factor)
        return results

    def mulitply_two_factors(self,f1,f2):
        common_vars = list(set(f1['vars']) & set(f2['vars']))
        new_vars = list(set(f1['vars'] + f2['vars']))

        new_factor = {'vars': new_vars, 'table': {}}
        assignments = product(*[range(2) for _ in new_vars])

        for assignment in assignments:
            assign_dict = dcit(zip(new_vars, assignment))
            val1 = self.get_factor_value(f1, assign_dict)
            val2 = self.get_factor_value(f2, assign_dict)
            new_factor['table'][tuple(assignment)] = val1 * val2
        return new_factor

    def sum_out(self, factor, var):
        var_index = factor['vars'].index(var)
        new_vars = [v for v in factor['vars'] if v != var]
        new_factor = {'vars': new_vars, 'table': {}}
        sums = {}

        for assignment,value in factor['table'].items():
            key = tuple(v for i,v in enumerate(assignment) if i != var_index)
            sums[key] = sums.get(key, 0) + value

        new_factor['table'] = sums
        return new_factor

    def query(self, query_vars, evidence={}, elimination_order=None):
        factors = []
        for var, cpt in self.cpts.items():
            if var in evidence:
                new_cpt = {'vars': cpt['vars'], 'table': {}}
                for assignment, prob in cpt['table'].items():
                    if assignment[cpt['vars'].index(var)] == evidence[var]:
                        new_assignment = tuple(v for i, v in enumerate(assignment)
                                            if cpt['vars'][i] != var)
                        new_cpt['table'][new_assignment] = prob
                factors.append(new_cpt)
            else:
                factors.append(cpt.copy())

        if elimination_order is None:
            all_vars = set()
            for factor in factors:
                all_vars.update(factor['vars'])
            query_vars_set= set(query_vars)
            elimination_order = [var for var in all_vars if var not in query_vars_set]

        for var in elimination_order:
            factors = self.eliminate(factors, var)

        result_factor = self.multiply_factors(factors)
        total = sum(result_factor['table'].values())
        normalized_table = {k: v/total for k,v in result_factor['table'].items()}

        return {'vars': result_factor['vars'], 'table': normalized_table}

    def get_factor_value(self, factor, assignment):
        key = tuple(assignment[var] for var in factor['vars'])
        return factor['table'].get(key,0)
    