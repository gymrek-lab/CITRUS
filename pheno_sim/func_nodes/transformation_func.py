"""Non-linear transformation function operator nodes.

Take some input values and apply some transformation function, like a
sigmoid, tanh, ReLU, 

Includes:

	* ReLU
	
	* Sigmoid
	
	* Softmax
	
	* Tanh
"""

import numpy as np

from pheno_sim.base_nodes import AbstractBaseFunctionNode


class ReLU(AbstractBaseFunctionNode):
	"""Operator node that applies the ReLU function to the input.
	
	User can specify:
		- The slope of the negative values.
		- The threshold at which the slope changes.

	Example:
	
	```python
		>>> vals = np.array([-2, -1, 0, 1, 2])

		>>> relu = ReLU("relu", "vals")
		>>> relu(vals)
		array([-0., -0.,  0.,  1.,  2.])

		>>> relu = ReLU("relu", "vals", neg_slope=0.5)
		>>> relu(vals)
		array([-1. , -0.5,  0. ,  1. ,  2. ])

		>>> relu = ReLU("relu", "vals", threshold=1.5)
		>>> relu(vals)
		array([-0., -0.,  0.,  0.,  2.])

		>>> relu = ReLU("relu", "vals", neg_slope=0.5, threshold=1.5)
		>>> relu(vals)
		array([-1. , -0.5,  0. ,  0.5,  2. ])

		>>> relu = ReLU("relu", "vals", neg_slope=-0.5)
		>>> relu(vals)
		array([ 1. ,  0.5, -0. ,  1. ,  2. ])
	```
	"""
	
	def __init__(
		self,
		alias: str,
		input_alias: str,
		neg_slope: float = 0.0,
		threshold: float = 0.0
	):
		"""Initialize ReLU node.
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
			neg_slope (float, default 0.0): The slope of the negative values.
			threshold (float, default 0.0): The threshold at which the slope
				changes.
		"""
		super().__init__(alias)
		self.inputs = input_alias
		self.neg_slope = neg_slope
		self.threshold = threshold
		
	def run(self, input_vals):
		"""Return the input with ReLU applied."""
		return np.where(
			input_vals > self.threshold,
			input_vals,
			input_vals * self.neg_slope
		)
	

class Sigmoid(AbstractBaseFunctionNode):
	"""Operator node that applies the sigmoid function to the input.
	
	Output is between 0 and 1.

	Example:
	```python
		>>> vals = np.array([-3, -2, -1, 0, 1, 2, 3])
		>>> sigmoid = Sigmoid("sigmoid", "vals")
		>>> sigmoid(vals)
		array([0.018, 0.047, 0.119, 0.269, 0.5  , 0.731, 0.881, 0.953, 0.982])
	```
	"""

	def __init__(self, alias: str, input_alias: str):
		"""Initialize Sigmoid node.
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
		"""
		super().__init__(alias)
		self.inputs = input_alias
		
	def run(self, input_vals):
		"""Return the input with sigmoid applied."""
		return 1 / (1 + np.exp(-input_vals))
	

class Softmax(AbstractBaseFunctionNode):
	"""Applies softmax to each sample's multiple values.

	Only use this function when the input is a matrix (there are multiple
	values in the input for each sample). Default behavior is to throw an
	error if the input is not a matrix.
	
	The output will be a matrix with the same dimension as the input. The
	softmax function is applied to each sample's values independently,
	so the columns of the output matrix will sum to 1.

	Example:

	```python
		>>> vals = np.array([
			[-1, 0, 3, 2],
			[0, 1, 3, -1],
			[1, 2, 3, -4]
		])
		>>> softmax = Softmax("softmax", "vals")
		>>> softmax(vals)
		array([
			[0.09 , 0.09 , 0.333, 0.95 ],
			[0.245, 0.245, 0.333, 0.047],
			[0.665, 0.665, 0.333, 0.002]
		])
	```
	"""

	def __init__(self, alias: str, input_alias: str):
		"""Initialize Softmax node.
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
		"""
		super().__init__(alias)
		self.inputs = input_alias
		
	def run(self, input_vals):
		"""Return the input with softmax applied."""
		if input_vals.ndim == 1:
			raise ValueError(
				"Input to Softmax node must be a matrix (2D array, "
				"multiple values per sample)."
			)

		exp_vals = np.exp(input_vals)
		return exp_vals / exp_vals.sum(0)


class Tanh(AbstractBaseFunctionNode):
	"""Operator node that applies the tanh function to the input.

	Output is between -1 and 1.

	Example:
	```python
		>>> vals = np.array([-3, -2, -1, 0, 1, 2, 3])
		>>> tanh = Tanh("tanh", "vals")
		>>> tanh(vals)
		array([-0.995, -0.964, -0.762,  0.   ,  0.762,  0.964,  0.995])
	```
	"""

	def __init__(self, alias: str, input_alias: str):
		"""Initialize Tanh node.
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
		"""
		super().__init__(alias)
		self.inputs = input_alias
		
	def run(self, input_vals):
		"""Return the input with tanh applied."""
		return np.tanh(input_vals)
	

if __name__ == "__main__":

	vals = np.array([
		[1, 2, 3, 0],
		[4, 5, 6, 1],
		[7, 8, 9, -1]
	])

	# Test ReLU
	vals = np.array([
		[-2, -1, 0, 1, 2],
		[-2, -1, 0, 1, 2],
	])
	vals = np.array([-2, -1, 0, 1, 2])

	relu = ReLU("relu", "vals")
	print(relu(vals))

	relu = ReLU("relu", "vals", neg_slope=0.5)
	print(relu(vals))

	relu = ReLU("relu", "vals", threshold=1.5)
	print(relu(vals))

	relu = ReLU("relu", "vals", neg_slope=0.5, threshold=1.5)
	print(relu(vals))

	relu = ReLU("relu", "vals", neg_slope=-0.5)
	print(relu(vals))


	# Test Sigmoid
	vals = np.array([-3, -2, -1, 0, 1, 2, 3])
	np.set_printoptions(precision=3)

	sigmoid = Sigmoid("sigmoid", "vals")
	print(sigmoid(vals))


	# Test Softmax
	vals = np.array([
		[-1, 0, 3, 2],
		[0, 1, 3, -1],
		[1, 2, 3, -4]
	])

	softmax = Softmax("softmax", "vals")
	print(softmax(vals))

	# Test Tanh
	vals = np.array([-3, -2, -1, 0, 1, 2, 3])
	tanh = Tanh("tanh", "vals")
	print(tanh(vals))