"""Operators that add noise in the phenotype simulation.

Classes:

	* GaussianNoise: A node that adds Gaussian noise to the input.

	* Heritability: Contols what fraction of the information output by
		the node is a function of the input vs. Gaussian noise. The output is
		a weighted average of the input and Gaussian noise. The Gaussian noise
		is scaled so that the output has the same variance as the input.

TODO:
	* Correlated noise.	
"""

import numpy as np

from pheno_sim.base_nodes import AbstractBaseFunctionNode


class GaussianNoise(AbstractBaseFunctionNode):
	"""Operator node that adds Gaussian noise to the input.
	
	Noise is added element-wise to the input.

	Example:
	```python
		>>> vals = np.vstack([
			np.random.randint(0, 10, size=10000),
			np.ones(10000),
			np.zeros(10000),
		])
		>>> gn = GaussianNoise("gn", "vals", 1)

		>>> out_vals = gn(vals)
		>>> out_vals
		array([[ 7.260, -0.843, ...,  8.977, -0.345],
			[ 0.260,  1.012, ...,  1.766,  3.573],
			[-0.107,  0.222, ..., -0.526,  1.615]])
		>>> out_vals.mean(1)
		array([ 4.532,  1.013, -0.013])
		>>> out_vals.std(1)
		array([3.056, 1.008, 0.998])
	```
	"""
	
	def __init__(self, alias: str, input_alias: str, noise_std: float):
		"""Initialize GaussianNoise node.
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
			noise_std: The standard deviation of the Gaussian noise.
		"""
		super().__init__(alias)
		self.inputs = input_alias
		self.noise_std = noise_std
		
	def run(self, input_vals):
		"""Return the input with Gaussian noise added."""
		return input_vals + np.random.normal(
			loc=0, scale=self.noise_std, size=input_vals.shape
		)
	

class Heritability(AbstractBaseFunctionNode):
	"""Operator node that caps heritability of it's output values.

	Contols what fraction of the information output by the node is a
	function of the input vs. Gaussian noise. The output is a weighted
	average of the input and Gaussian noise. The Gaussian noise is
	scaled so that the output has the same variance as the input.

	The output distribution of values is roughly scaled to have a mean
	of 0 and a standard deviation of 1.

	Heritability (h^2) ranges from 0 (all noise) to 1 (all input signal).

	Implements the following equation:

	```
	for heritability (h^2) in [0, 1] and input values vector x:

	output(x_i) = sqrt(h^2) * (x_i - mean(x)) / std(x)	# signal
			+ sqrt(1 - h^2) * N(0,1)		# noise
	```

	Example:
	```python
		>>> vals = np.vstack([
			np.random.randint(0, 10, size=10000),
			np.ones(10000),
			np.zeros(10000),
		])
		>>> highly_heritable = Heritability("herit_cap", "vals", 0.99)
		>>> medium_heritable = Heritability("herit_cap", "vals", 0.5)
		>>> low_heritable = Heritability("herit_cap", "vals", 0.05)

		>>> high_herit_out = highly_heritable(vals)
		>>> med_herit_out = medium_heritable(vals)
		>>> low_herit_out = low_heritable(vals)

		>>> vals
		array([[8., 0., ..., 8., 0.],
			[1., 1., ..., 1., 1.],
			[0., 0., ..., 0., 0.]])
		>>> high_herit_out
		array([[ 1.382, -1.623, ...,  1.243, -1.495],
			[ 0.138,  0.156, ...,  0.122,  0.141],
			[ 0.2  , -0.108, ..., -0.053,  0.094]])
		>>> med_herit_out
		array([[ 0.917, -0.257, ...,  0.732, -2.233],
			[ 0.271, -0.228, ...,  0.712, -0.722],
			[-0.333,  0.565, ...,  1.331, -0.708]])
		>>> low_herit_out
		array([[ 0.319, -0.15 , ...,  1.397, -1.249],
			[-0.572, -0.124, ...,  2.178,  1.469],
			[-0.631, -1.017, ..., -1.227, -1.187]])

		>>> high_herit_out.mean(1)
		array([ 0.001,  0.001, -0.001])
		>>> high_herit_out.std(1)
		array([1.001, 0.099, 0.099])

		>>> low_herit_out.mean(1)
		array([ 0.001, -0.002,  0.002])
		>>> low_herit_out.std(1)
		array([1.005, 0.978, 0.975])
	```
	"""

	def __init__(self, alias: str, input_alias: str, heritability: float):
		"""Initialize GaussianNoiseRatio node.

		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
			heritability: Used to calculate the ratio of signal to noise.
		"""
		super().__init__(alias)
		self.inputs = input_alias
		self.heritability = heritability

	def run(self, input_vals):
		"""Return the input with noise added to achieve some heritability."""

		if input_vals.ndim == 1:
			# Vector input
			return np.sqrt(self.heritability) * np.divide(
				input_vals - np.mean(input_vals), 
				np.std(input_vals),
				out=np.zeros_like(input_vals),
				where=np.std(input_vals) != 0,
				casting='unsafe'
			) + np.sqrt(1 - self.heritability) * np.random.normal(
				loc=0, scale=1, size=input_vals.shape
			)
		elif input_vals.ndim == 2:
			# Apply to each row of matrix
			return np.apply_along_axis(
				func1d=lambda x: np.sqrt(self.heritability) * np.divide(
					x - np.mean(x), 
					np.std(x),
					out=np.zeros_like(x),
					where=np.std(x) != 0,
					casting='unsafe'
				) + np.sqrt(1 - self.heritability) * np.random.normal(
					loc=0, scale=1, size=x.shape
				),
				axis=1, arr=input_vals
			)
		else:
			raise ValueError(
				"Input must be a vector or 2D matrix. "
				f"Input has {input_vals.ndim} dimensions."
			)
		

if __name__ == "__main__":
	
	# Test GaussianNoise

	single_vals = np.array([1, 1, 1, 1, 5, 10, 10, 10, 10])
	vals = np.vstack([
		np.random.randint(0, 10, size=10000),
		np.ones(10000),
		np.zeros(10000),
	])

	gn = GaussianNoise("gn", "vals", 1)
	out_vals = gn(vals)
	print(out_vals.mean(1))
	print(out_vals.std(1))
	print(gn(single_vals))

	# Test Heritability

	highly_heritable = Heritability("herit_cap", "vals", 0.99)
	medium_heritable = Heritability("herit_cap", "vals", 0.5)
	low_heritable = Heritability("herit_cap", "vals", 0.05)

	high_herit_out = highly_heritable(vals)
	med_herit_out = medium_heritable(vals)
	low_herit_out = low_heritable(vals)

	print(high_herit_out.mean(1))
	print(high_herit_out.std(1))

	print(med_herit_out.mean(1))
	print(med_herit_out.std(1))

	print(low_herit_out.mean(1))
	print(low_herit_out.std(1))
		