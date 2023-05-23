""" General function nodes for the simulation. 

Includes:

	IdentityNode: A node that returns the input.
	
	SumNode: A node that sums some inputs element-wise.

	GeneLevelAndNode

	GeneLevelOrNode

	MaskNode
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

# class GeneLevelAND(AbstractBaseFunctionNode): 

# 	""" A node that takes the element-wise mean of the two haplotypes.
	
# 	Mean is either arithmetic, geometric, or harmonic.

# 	Examples:
# 		>>> hap = (np.array([1, 2, 3]), np.array([4, 5, 6]))
# 		>>> GeneLevelANDCombine("mean", "hap")(hap)
# 		array([2.5, 3.5, 4.5])
		
# 		>>> hap = (
# 				np.array([[1, 2, 3],
# 				          [4, 5, 6]]),
# 				np.array([[ 7,  8,  9],
# 						  [10, 11, 12]])
# 			)
# 		>>> MeanCombine("mean", "hap")(hap)
# 		array([[4. , 5. , 6. ],
# 			   [7. , 8. , 9]])
# 		>>> MeanCombine("mean", "hap", mean_type="geometric")(hap)
# 		array([[2.64575131, 4.        , 5.19615242],
#        		   [6.32455532, 7.41619849, 8.48528137]])
# 		>>> MeanCombine("mean", "hap", mean_type="harmonic")(hap)
# 		array([[1.75      , 3.2       , 4.5       ],
#        		   [5.71428571, 6.875     , 8.        ]])
# 	"""

# 	def __init__(
# 		self,
# 		alias: str,
# 		input_alias: str,
# 		mean_type: str = "arithmetic"
# 	):
		
# 	def run(self, hap_vals: HaplotypeValues):

# 		return np.multiply(hap_vals[0], hap_vals[1])


if __name__ == "__main__":
	from pheno_sim.pheno_simulation import PhenoSimulation
	
	# Test IdentityNode
	vals = np.array([1, 2, 3])
	hap_vals = (np.array([1, 2, 3]), np.array([4, 5, 6]))

	identity_node = Identity("identity", "arr")

	print(identity_node(vals))
	print(identity_node(hap_vals))

	# Test AddNode
	# what does arr1d and 2d correspond to 
	arr1d = np.array([[1, 2, 3]])
	arr2d = np.array([[1, 2, 3], [4, 5, 6]])

	arrs = [arr1d, arr2d]

	print(np.sum(np.array(arrs, dtype=object), axis=0))