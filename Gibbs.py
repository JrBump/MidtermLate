import random

class GibbsSampling:
    def __init__(self,cpts):
        self.cpts = cpts
        self.variables = list(cpts.keys())

    def sample(self, query_vars, evidence={}, num_samples=10000, burn_in=1000):
        state = {}
        for var in self.variables:
            if var in evidence:
                state[var] = evidence[var]
            else:
                state[var] = random.randint(0,1)

        non_evidence_vars = [var for var in self.variables if var not in evidence]
        counts = {tuple([0]* len(query_vars)): 0, tuple([1] * len(query_vars)): 0}

        for i in range(num_samples + burn_in):
            random.shuffle(non_evidence_vars)

            for var in non_evidence_vars:
                prob = self.compute_conditional(var, state)
                state[var] = 1 if random.random() < prob else 0

            if i >= burn_in:
                query_values = tuple(state[var] for var in query_vars)
                counts[query_values] = counts.get(query_values, 0) + 1
        
        total = sum(counts.values())
        probs = {k: v/total for k,v in counts.items()}
        return probs

    def compute_conditional(self,var,state):
        parents = self.cpts[var]['vars'][:-1]
        children = []
        for child_var, cpt in self.cpts.items():
            if var in cpt['vars'][:-1]:
                children.append(child_var)

        parent_values = tuple(state[p] for p in parents)
        key = parent_values + (1,)
        p_var1 = self.cpts[var]['table'].get(key, 0)
        key = parent_values + (0,)
        p_var0 = self.cpts[var]['table'].get(key, 0)

        for child in children:
            child_parents = self.cpts[child]['vars'][:-1]
            child_parents_values = tuple(state[p] if p != var else 1 for p in child_parents)
            key = child_parents_values + (state[child],)
            p_var *= self.cpts[child]['table'].get(key, 0)
            child_parents_values = tuple(state[p] if p != var else 0 for p in child_parents)
            key = child_parents_values + (state[child],)
            p_var0 *= self.cpts[child]['table'].get(key, 0)

        total = p_var1 + p_var0
        if total == 0:
            return 0.5
        return p_var1 / total
