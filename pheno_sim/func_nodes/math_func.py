""" General math function nodes for the simulation. 

Includes:

	IdentityNode: A node that returns the input. Mainly for testing.
	
	SumNode: A node that sums some inputs element-wise.
"""

import numpy as np

from pheno_sim.data_types import HaplotypeValues, Values, ValuesDict
from pheno_sim.base_nodes import AbstractBaseFunctionNode


class Identity(AbstractBaseFunctionNode):
	""" A node that returns the input. 
	
	Examples:
		>>> Identity("identity", "arr")(np.array([1, 2, 3]))
		array([1, 2, 3])
		>>> Identity("identity", "hap")(
			(np.array([1, 2, 3]), np.array([4, 5, 6]))
		)
		(array([1, 2, 3]), array([4, 5, 6]))
	"""
	
	def __init__(self, alias: str, input_alias: str):
		super().__init__(alias)
		self.inputs = input_alias

	def run(self, input_vals):
		return input_vals
	

class Sum(AbstractBaseFunctionNode):
	""" A node that sums some inputs element-wise.

	If all inputs are vectors (num_samples length arrays), then the output
	is a vector that is the element-wise sum of the inputs.

	If all inputs are all matrices (num_feats x num_samples arrays), then
	the output is a matrix (with the same dimensions) that is the 
	element-wise sum.

	If the input is a mix of vectors and matrices:
		- All matrices must have the same dimensions.
		- Matrices are summed element-wise.
		- Vectors are summed element-wise over each of the num_feats of
			the matrices.

	Args:
		alias: The alias of the node.
		input_aliases (list): The aliases of the inputs to be summed.

	Examples:
		>>> Sum("sum", ["arrs"])([np.array([1, 2, 3]), np.array([4, 5, 6])])
		array([5, 7, 9])

		>>> Sum("sum", ["arrs"])([
			np.array([[1, 2, 3], [4, 5, 6]]),
			np.array([[7, 8, 9], [10, 11, 12]])
		])
		array([[ 8, 10, 12],
		       [14, 16, 18]])
		
		>>> Sum("sum", ["arrs"])([
			np.array([1, 2, 3]),
			np.array([[1, 1, 1], [2, 2, 2]]),
			np.array([[1, 1, 1], [2, 2, 2]])
		])
		array([[3, 4, 5],
		       [5, 6, 7]])			
	"""

	def __init__(self, alias: str, input_aliases: list):
		super().__init__(alias)
		self.inputs = input_aliases

	def run(self, input_vals):
		return np.sum(np.array(input_vals, dtype=object), axis=0)

	
if __name__ == "__main__":
	from pheno_sim.pheno_simulation import PhenoSimulation
	
	# Test Identity
	vals = np.array([1, 2, 3])
	hap_vals = (np.array([1, 2, 3]), np.array([4, 5, 6]))

	identity_node = Identity("identity", "arr")

	print(identity_node(vals))
	print(identity_node(hap_vals))


	# Test Sum
	sum_node = Sum("sum", ["arrs"])

	print(sum_node([np.array([1, 2, 3]), np.array([4, 5, 6])]))
	print(sum_node([
		np.array([[1, 2, 3], [4, 5, 6]]),
		np.array([[7, 8, 9], [10, 11, 12]])
	]))
	print(sum_node([	
		np.array([1, 2, 3]),
		np.array([[1, 1, 1], [2, 2, 2]]),
		np.array([[1, 1, 1], [2, 2, 2]])
	]))

	vals = [	
		np.array([1, 2, 3]),
		np.array([[1, 1, 1], [2, 2, 2]]),
		np.array([[1, 1, 1], [2, 2, 2]])
	]
	hap_vals = (vals, vals)

	print(sum_node(vals))
	print(sum_node(hap_vals))
