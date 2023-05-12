""" General function nodes for the simulation. 

Includes:

	IdentityNode: A node that returns the input.
	
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
	

# class SumNode(AbstractBaseFunctionNode):
# 	""" A node that sums some inputs element-wise.

# 	If all inputs
# 	"""
# 	pass

	

if __name__ == "__main__":
	from pheno_sim.pheno_simulation import PhenoSimulation
	
	# Test IdentityNode
	vals = np.array([1, 2, 3])
	hap_vals = (np.array([1, 2, 3]), np.array([4, 5, 6]))

	identity_node = Identity("identity", "arr")

	print(identity_node(vals))
	print(identity_node(hap_vals))

	# Test AddNode
	arr1d = np.array([[1, 2, 3]])
	arr2d = np.array([[1, 2, 3], [4, 5, 6]])

	arrs = [arr1d, arr2d]

	np.sum(np.array(arrs, dtype=object), axis=0)