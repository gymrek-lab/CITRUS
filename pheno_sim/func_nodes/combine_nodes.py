""" Function nodes for combining HaplotypeValues into a single Value. """

import numpy as np

from pheno_sim.data_types import HaplotypeValues
from pheno_sim.base_nodes import AbstractBaseCombineFunctionNode


class AdditiveCombine(AbstractBaseCombineFunctionNode):
	""" A node that sums the two haplotypes element-wise.
	
	Examples:
		>>> hap = (np.array([1, 2, 3]), np.array([4, 5, 6]))
		>>> AdditiveCombine("add", "hap")(hap)
		array([5, 7, 9])

		>>> hap = (
				np.array([[1, 2, 3],
				          [4, 5, 6]]),
				np.array([[ 7,  8,  9],
						  [10, 11, 12]])
			)
		>>> AdditiveCombine("add", "hap")(hap)
		array([[ 8, 10, 12],
			   [14, 16, 18]])
	"""

	def __init__(self, alias: str, input_alias: str):
		""" Initialize the node. 
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
		"""
		super().__init__(alias)
		self.inputs = input_alias

	def run(self, hap_vals: HaplotypeValues):
		return hap_vals[0] + hap_vals[1]
	

class MaxCombine(AbstractBaseCombineFunctionNode):
	""" A node that takes the element-wise maximum of the two haplotypes. 
	
	Examples:
		>>> hap = (np.array([1, 2, 3]), np.array([4, 5, 6]))
		>>> MaxCombine("max", "hap")(hap)
		array([4, 5, 6])

		>>> hap = (
				np.array([[1, 2, 3],
				          [4, 5, 6]]),
				np.array([[ 7,  8,  9],
						  [10, 11, 12]])
			)
		>>> MaxCombine("max", "hap")(hap)
		array([[ 7,  8,  9],
			   [10, 11, 12]])
	"""

	def __init__(self, alias: str, input_alias: str):
		""" Initialize the node.

		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
		"""
		super().__init__(alias)
		self.inputs = input_alias

	def run(self, hap_vals: HaplotypeValues):
		return np.maximum(hap_vals[0], hap_vals[1])
	

class MinCombine(AbstractBaseCombineFunctionNode):
	""" A node that takes the element-wise minimum of the two haplotypes.
	
	Examples:
		>>> hap = (np.array([1, 2, 3]), np.array([4, 5, 6]))
		>>> MinCombine("min", "hap")(hap)
		array([1, 2, 3])

		>>> hap = (
				np.array([[1, 2, 3],
				          [4, 5, 6]]),
				np.array([[ 7,  8,  9],
						  [10, 11, 12]])
			)
		>>> MinCombine("min", "hap")(hap)
		array([[1, 2, 3],
			   [4, 5, 6]])
	"""

	def __init__(self, alias: str, input_alias: str):
		""" Initialize the node.

		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
		"""
		super().__init__(alias)
		self.inputs = input_alias

	def run(self, hap_vals: HaplotypeValues):
		return np.minimum(hap_vals[0], hap_vals[1])
	

class MeanCombine(AbstractBaseCombineFunctionNode):
	""" A node that takes the element-wise mean of the two haplotypes.
	
	Mean is either arithmetic, geometric, or harmonic.

	Examples:
		>>> hap = (np.array([1, 2, 3]), np.array([4, 5, 6]))
		>>> MeanCombine("mean", "hap")(hap)
		array([2.5, 3.5, 4.5])
		>>> MeanCombine("mean", "hap", mean_type="geometric")(hap)
		array([2.        , 3.16227766, 4.24264069])
		>>> MeanCombine("mean", "hap", mean_type="harmonic")(hap)
		array([1.6       , 2.85714286, 4.        ])

		>>> hap = (
				np.array([[1, 2, 3],
				          [4, 5, 6]]),
				np.array([[ 7,  8,  9],
						  [10, 11, 12]])
			)
		>>> MeanCombine("mean", "hap")(hap)
		array([[4. , 5. , 6. ],
			   [7. , 8. , 9]])
		>>> MeanCombine("mean", "hap", mean_type="geometric")(hap)
		array([[2.64575131, 4.        , 5.19615242],
       		   [6.32455532, 7.41619849, 8.48528137]])
		>>> MeanCombine("mean", "hap", mean_type="harmonic")(hap)
		array([[1.75      , 3.2       , 4.5       ],
       		   [5.71428571, 6.875     , 8.        ]])
	"""

	def __init__(
		self,
		alias: str,
		input_alias: str,
		mean_type: str = "arithmetic"
	):
		""" Initialize the MeanCombine node.
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
			mean_type: The type of mean to take. Can be "arithmetic",
				"geometric", or "harmonic".
		"""
		super().__init__(alias)
		self.inputs = input_alias
		self.mean_type = mean_type

	def run(self, hap_vals: HaplotypeValues):
		if self.mean_type == "arithmetic":
			return np.mean(hap_vals, axis=0)
		elif self.mean_type == "geometric":
			return np.exp(np.mean(np.log(hap_vals), axis=0))
		elif self.mean_type == "harmonic":
			return 1 / np.mean(np.divide(1, hap_vals), axis=0)
		else:
			raise ValueError(
				f"mean_type {self.mean_type} not supported."
				" Must be 'arithmetic', 'geometric', or 'harmonic'."
			)



