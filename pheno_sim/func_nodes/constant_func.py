""" Function nodes that generate values representing constants 
and broadcast them to some shape.
"""

from typing import Union

import numpy as np

from pheno_sim.base_nodes import AbstractBaseFunctionNode


class Constant(AbstractBaseFunctionNode):
	""" Class that generates constant values.
	
	The constant for this function is either:
		- A single value, which is broadcast to the shape of the input.
		- A list of values (one per feature dim), which are broadcast to the
			shape of the input.
	
	Args:
		alias: The alias of the node.
		input_match_size: The alias of the input node for values used to
			determine the size of the output array. Output will be the same
			size as this input.
		constant: The constant value(s) to generate.
		
	Examples:
		>>> match_size = np.array([[1, 2, 3], [4, 5, 6]])
		>>> Constant("const", "match_size", 1)(match_size)
		array([[1, 1, 1],
			   [1, 1, 1]])
		>>> Constant("const", "match_size", [1, 2])(match_size)
		array([[1, 1, 1],
			   [2, 2, 2]])
	"""
	
	def __init__(
		self,
		alias: str,
		input_match_size: str,
		constant: Union[int, float, list]
	):
		super().__init__(alias)
		self.inputs = input_match_size
		self.constant = constant

	def run(self, input_match_size):
		""" Generate the constant value(s). """
		if isinstance(self.constant, list):
			return np.broadcast_to(
				np.array(self.constant)[:, np.newaxis],
				input_match_size.shape
			)
		else:
			return np.broadcast_to(
				self.constant,
				input_match_size.shape
			)
		

class RandomConstant(AbstractBaseFunctionNode):
	""" Class that generates constant values, where constant
	values are drawn from a distribution.

	Any distribution that can be sampled from using numpy.random.Generator
	can be used. The parameters for the distribution (see numpy docs
	https://numpy.org/doc/stable/reference/random/generator.html#distributions)
	are passed as the dist_kwargs argument. 'size' should not be passed in
	dist_kwargs.

	If by_feat is False, a single value is drawn from the distribution and
	broadcast to the shape of the input. If by_feat is True, a value is drawn
	from the distribution for each feature dim and broadcast to the shape of
	the input.

	Args:
		alias: The alias of the node.
		input_match_size: The alias of the input node for values used to
			determine the size of the output array. Output will be the same
			size as this input. If by_feat is True, this input will also be
			used to determine the number of feature dimensions.
		dist_name: The name of the distribution to draw from.
		dist_kwargs: The keyword arguments for the distribution.
		by_feat: Whether to draw a value for each feature dim. Default is False.
	
	Examples:
		>>> match_size = np.array([[1, 2, 3], [4, 5, 6]])

		>>> RandomConstant(
			"const", "match_size", "uniform", {"low": 0, "high": 1}
		)(match_size)
		array([[0.37454012, 0.37454012, 0.37454012],
			   [0.37454012, 0.37454012, 0.37454012]])

		>>> RandomConstant(
			"const", "match_size", "uniform", {"low": 0, "high": 1}, by_feat=True
		)(match_size)
		array([[0.37454012, 0.37454012, 0.37454012],
			   [0.95071431, 0.95071431, 0.95071431]])
	"""

	def __init__(
		self,
		alias: str,
		input_match_size: str,
		dist_name: str,
		dist_kwargs: dict,
		by_feat: bool = False
	):
		super().__init__(alias)
		self.inputs = input_match_size
		self.dist_name = dist_name
		self.dist_kwargs = dist_kwargs
		self.by_feat = by_feat

		self.constant = None

	def _draw_constant(self, input_match):
		""" Draw constant value(s) from the distribution. """
		dist = getattr(np.random.default_rng(), self.dist_name)
		if self.by_feat:
			if input_match.ndim == 1:
				return dist(size=1, **self.dist_kwargs)
			else:
				return dist(size=input_match.shape[0], **self.dist_kwargs)
		else:
			return dist(size=1, **self.dist_kwargs)

	def run(self, input_match):
		""" Generate the constant value(s). """
		if self.constant is None:
			self.constant = self._draw_constant(input_match)

		if self.by_feat:
			return np.broadcast_to(
				self.constant[:, np.newaxis],
				input_match.shape
			)
		else:
			return np.broadcast_to(
				self.constant,
				input_match.shape
			)

		



if __name__ == "__main__":

	# Test Constant
	match_size = np.array([[1, 2, 3], [4, 5, 6]])

	const = Constant("const", "match_size", 1)
	print(const(match_size))

	const = Constant("const", "match_size", [1, 2])
	print(const(match_size))

	# Test RandomConstant
	rand_const = RandomConstant(
		"const", "match_size", "uniform", {"low": 0, "high": 1}
	)
	print(rand_const(match_size))
	print(rand_const(match_size))
	rand_const = RandomConstant(
		"const", "match_size", "uniform", {"low": 0, "high": 1},
		by_feat=True
	)
	print(rand_const(match_size))
	print(rand_const(match_size))
