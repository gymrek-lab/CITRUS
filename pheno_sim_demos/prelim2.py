""" Preliminary testing """

import os
import inspect

import numpy as np

from pheno_sim import PhenoSimulation
from pheno_sim import func_nodes

# define custom class and pass to PhenoSimulation 

if __name__ == "__main__":
    
    # Create an input ValuesDict
	input_vals = {
		"SNP1": (
			np.array([0] * 10 + [1] * 10),
			np.array([0] * 5 + [1] * 5 + [0] * 5 + [1] * 5)
		),
		"SNP2": (np.ones(20), np.zeros(20)),
		"SNP3": (np.zeros(20), np.ones(20))
	}

