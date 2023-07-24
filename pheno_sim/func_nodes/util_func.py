""" Utility functions for simulations.

Includes:

- Concatenate: A node that concatenates some inputs into a single array.
"""

import numpy as np

from pheno_sim.base_nodes import AbstractBaseFunctionNode


class Concatenate(AbstractBaseFunctionNode):
	""" A node that concatenates some inputs into a single array.

	The inputs are concatenated in the order they are given in the input list.

	Examples:
	```python
		>>> Concatenate("concat", ["arrs"])(
			[np.array([1, 2, 3]), np.array([4, 5, 6])]
		)
		array([[1, 2, 3],
			   [4, 5, 6]])

		>>> Concatenate("concat", ["arrs"])(
			[np.array([[1, 2, 3], [4, 5, 6]]), np.array([[7, 8, 9]])]
		)
		array([[1, 2, 3],
			   [4, 5, 6],
			   [7, 8, 9]])
	```
	"""

	def __init__(self, alias: str, input_aliases: list):
		"""Initialize Concatenate node.

		Args:
			alias: The alias of the node.
			input_aliases (list): The aliases of the inputs to be concatenated.
		"""
		super().__init__(alias)
		self.inputs = input_aliases

	def run(self, *input_vals):
		"""Return concatenated array of input values."""
		return np.vstack(input_vals)
	

if __name__ == "__main__":

	# Test Concatenate
	input_dict = {
		"i1": np.array([1, 2, 3]),
		"i2": np.array([[1, 2, 3], [4, 5, 6]]),
		"i3": np.array([[7, 8, 9]])
	}

	concat_node = Concatenate("concat", ["i1", "i2", "i3"])(
		[input_dict["i1"], input_dict["i2"], input_dict["i3"]]
	)
