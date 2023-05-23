""" Functions that reduce a Values matrix to one value per sample using
the specified operation.
"""

import numpy as np

from pheno_sim.base_nodes import AbstractBaseFunctionNode


class SumReduce(AbstractBaseFunctionNode):
	""" For a Values matrix (num_feats, num_samples), return a vector of
	the sum of the feature values for each sample (a num_samples length array).
	
	Examples:
		>>> SumReduce("sum_reduce", "vals")(np.array([[1, 2, 3], [4, 5, 6]]))
		array([ 5,  7,  9])
	"""

	def __init__(self, alias: str, input_alias: str):
		super().__init__(alias)
		self.inputs = input_alias

	def run(self, input_vals):
		return np.sum(input_vals, axis=0)
	

class MinReduce(AbstractBaseFunctionNode):
	""" For a Values matrix (num_feats, num_samples), return a vector of
	the minimum of the feature values for each sample (a num_samples length
	array).

	Examples:
		>>> MinReduce("min_reduce", "vals")(np.array([[1, 2, 3], [4, 5, 6]]))
		array([1, 2, 3])
	"""
	
	def __init__(self, alias: str, input_alias: str):
		super().__init__(alias)
		self.inputs = input_alias

	def run(self, input_vals):
		return np.min(input_vals, axis=0)
	

class MaxReduce(AbstractBaseFunctionNode):
	""" For a Values matrix (num_feats, num_samples), return a vector of
	the maximum of the feature values for each sample (a num_samples length
	array).

	Examples:
		>>> MaxReduce("max_reduce", "vals")(np.array([[1, 2, 3], [4, 5, 6]]))
		array([4, 5, 6])
	"""
	
	def __init__(self, alias: str, input_alias: str):
		super().__init__(alias)
		self.inputs = input_alias

	def run(self, input_vals):
		return np.max(input_vals, axis=0)
	

class MeanReduce(AbstractBaseFunctionNode):
	""" For a Values matrix (num_feats, num_samples), return a vector of
	the mean of the feature values for each sample (a num_samples length
	array).

	Mean is either arithmetic (default), geometric, or harmonic.

	Args:
		alias: The alias of the node.
		input_alias: The alias of the input.
		mean_type: The type of mean to use. One of 'arithmetic' (default),
			'geometric', or 'harmonic'.

	Examples:
		>>> MeanReduce("mean_reduce", "vals")(np.array([[1, 2, 3], [4, 5, 6]]))
		array([2.5, 3.5, 4.5])
		>>> MeanReduce("mean_reduce", "vals", mean_type="geometric")(
			np.array([[1, 2, 3], [4, 5, 6]])
		)
		array([2., 3.16227766, 4.24264069])
		>>> MeanReduce("mean_reduce", "vals", mean_type="harmonic")(
			np.array([[1, 2, 3], [4, 5, 6]])
		)
		array([1.6, 2.85714286, 4])
	"""

	def __init__(self, alias: str, input_alias: str, mean_type: str = "arithmetic"):
		super().__init__(alias)
		self.inputs = input_alias
		self.mean_type = mean_type

	def run(self, input_vals):
		if self.mean_type == "arithmetic":
			return np.mean(input_vals, axis=0)
		elif self.mean_type == "geometric":
			return np.exp(np.mean(np.log(input_vals), axis=0))
		elif self.mean_type == "harmonic":
			return 1 / np.mean(np.divide(1, input_vals), axis=0)
		else:
			raise ValueError(
				"mean_type must be one of 'arithmetic', 'geometric', or 'harmonic'"
			)


class AnyReduce(AbstractBaseFunctionNode):
	""" For a Values matrix (num_feats, num_samples), return a num_samples
	length vector that is 1 if the sample has any feature values meet some
	comparison with a threshold value, and 0 otherwise.

	Comparison function may be greater that (gt), greater than or equal (ge),
	less than (lt), less than or equal (le), equal (eq), or not equal (ne).

	Args:
		alias: The alias of the node.
		input_alias: The alias of the input.
		threshold: The threshold to use for determining if a sample has any
			feature values past the threshold. Default is 1.
		comparison: The comparison operator to use. One of 'ge' (default),
			'le', 'gt', 'lt', 'eq', or 'ne'.

	Examples:
		>>> vals = np.array([[0, -1, 3], [.5, 1, 1]])
		>>> AnyReduce("any_reduce", "vals")(vals)
		array([0, 1, 1])
		>>> AnyReduce("any_reduce", "vals", threshold=0, comparison="lt")(vals)
		array([0, 1, 0])
	"""

	def __init__(
		self,
		alias: str,
		input_alias: str,
		threshold: float = 1,
		comparison: str = "ge"
	):
		super().__init__(alias)
		self.inputs = input_alias
		self.threshold = threshold
		self.comparison = comparison

	def run(self, input_vals):
		if self.comparison == "ge":
			return np.any(input_vals >= self.threshold, axis=0).astype(int)
		elif self.comparison == "le":
			return np.any(input_vals <= self.threshold, axis=0).astype(int)
		elif self.comparison == "gt":
			return np.any(input_vals > self.threshold, axis=0).astype(int)
		elif self.comparison == "lt":
			return np.any(input_vals < self.threshold, axis=0).astype(int)
		elif self.comparison == "eq":
			return np.any(input_vals == self.threshold, axis=0).astype(int)
		elif self.comparison == "ne":
			return np.any(input_vals != self.threshold, axis=0).astype(int)
		else:
			raise ValueError(
				"comparison must be one of 'ge', 'le', 'gt', 'lt', 'eq', or 'ne'"
			)
		

class AllReduce(AbstractBaseFunctionNode):
	""" For a Values matrix (num_feats, num_samples), return a num_samples
	length vector that is 1 if the sample has all feature values meet some
	comparison with a threshold value, and 0 otherwise.

	Comparison function may be greater that (gt), greater than or equal (ge),
	less than (lt), less than or equal (le), equal (eq), or not equal (ne).

	Args:
		alias: The alias of the node.
		input_alias: The alias of the input.
		threshold: The threshold to use for determining if a sample has all
			feature values past the threshold. Default is 1.
		comparison: The comparison operator to use. One of 'ge' (default),
			'le', 'gt', 'lt', 'eq', or 'ne'.

	Examples:
		>>> vals = np.array([[0, -1, 3], [.5, 1, 1]])
		>>> AllReduce("all_reduce", "vals")(vals)
		array([0, 0, 1])
		>>> AllReduce("all_reduce", "vals", threshold=0, comparison="lt")(vals)
		array([0, 0, 0])
	"""

	def __init__(
		self,
		alias: str,
		input_alias: str,
		threshold: float = 1,
		comparison: str = "ge"
	):
		super().__init__(alias)
		self.inputs = input_alias
		self.threshold = threshold
		self.comparison = comparison

	def run(self, input_vals):
		if self.comparison == "ge":
			return np.all(input_vals >= self.threshold, axis=0).astype(int)
		elif self.comparison == "le":
			return np.all(input_vals <= self.threshold, axis=0).astype(int)
		elif self.comparison == "gt":
			return np.all(input_vals > self.threshold, axis=0).astype(int)
		elif self.comparison == "lt":
			return np.all(input_vals < self.threshold, axis=0).astype(int)
		elif self.comparison == "eq":
			return np.all(input_vals == self.threshold, axis=0).astype(int)
		elif self.comparison == "ne":
			return np.all(input_vals != self.threshold, axis=0).astype(int)
		else:
			raise ValueError(
				"comparison must be one of 'ge', 'le', 'gt', 'lt', 'eq', or 'ne'"
			)



if __name__ == "__main__":
	
	# Test SumReduce
	sum_reduce = SumReduce("sum_reduce", "vals")
	print(sum_reduce(np.array([[1, 2, 3], [4, 5, 6]])))

	# Test MinReduce
	min_reduce = MinReduce("min_reduce", "vals")
	print(min_reduce(np.array([[1, 2, 3], [4, 5, 6]])))

	# Test MaxReduce
	max_reduce = MaxReduce("max_reduce", "vals")
	print(max_reduce(np.array([[1, 2, 3], [4, 5, 6]])))

	# Test MeanReduce
	vals = np.array([[1, 2, 3], [4, 5, 6]])
	hap_vals = (vals, vals)

	mean_reduce = MeanReduce("mean_reduce", "vals")
	gmean_reduce = MeanReduce("gmean_reduce", "vals", mean_type="geometric")
	hmean_reduce = MeanReduce("hmean_reduce", "vals", mean_type="harmonic")

	print(mean_reduce(vals))
	print(gmean_reduce(vals))
	print(hmean_reduce(vals))

	print(mean_reduce(hap_vals))
	print(gmean_reduce(hap_vals))
	print(hmean_reduce(hap_vals))

	# Test AnyReduce and AllReduce
	vals = np.array([[0, -1, 3], [.5, 1, 1]])
	any_reduce = AnyReduce("any_reduce", "vals")
	all_reduce = AllReduce("all_reduce", "vals")
	print(any_reduce(vals))
	print(all_reduce(vals))

	any_reduce = AnyReduce("any_reduce", "vals", threshold=0, comparison="lt")
	all_reduce = AllReduce("all_reduce", "vals", threshold=0, comparison="lt")
	print(any_reduce(vals))
	print(all_reduce(vals))
	

