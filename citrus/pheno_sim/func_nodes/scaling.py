"""Operators that scaling input distributions in the phenotype simulation.

Classes:

	* Clip: A node that clips the input to be greater than or equal to some
		minimum value and/or less than or equal to some maximum value.

	* MinMaxScaler: A node that scales the input to be between 0 and 1 using
		the minimum and maximum values of the input.
		
	* StandardScaler: A node that scales the input to have mean 0 and standard
		deviation 1 using the mean and standard deviation of the input.

	* RobustScaler: A node that scales the input to have median 0 and interquartile
		range 1 using the median and interquartile range of the input.
"""

import numpy as np
from scipy.stats import iqr

from ..base_nodes import AbstractBaseFunctionNode


class Clip(AbstractBaseFunctionNode):
	"""Operator node that clips the input based on a min and/or max value(s).

	If a minimum value is provided, then all values less than the minimum
	value are set to the minimum value. If a maximum value is provided, then
	all values greater than the maximum value are set to the maximum value.

	Example:
	```python
		>>> vals = np.array([
			[1, 2, 3],
			[4, 5, 6],
			[7, 8, 9]
		])

		>>> clip = Clip("clip", "vals", min_val=2, max_val=8)
		>>> clip(vals)
		array([[2, 2, 3],
			[4, 5, 6],
			[7, 8, 8]])

		>>> clip = Clip("clip", "vals", min_val=4)
		>>> clip(vals)
		array([[4, 4, 4],
			[4, 5, 6],
			[7, 8, 9]])

		>>> clip = Clip("clip", "vals", max_val=6)
		>>> clip(vals)
		array([[1, 2, 3],
			[4, 5, 6],
			[6, 6, 6]])
	```
	"""

	def __init__(
		self,
		alias: str,
		input_alias: str,
		min_val: float = None,
		max_val: float = None
	):
		"""Initialize Clip node.
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
			min_val (float, default None): The minimum value to clip to.
			max_val (float, default None): The maximum value to clip to.
		"""
		super().__init__(alias)
		self.inputs = input_alias
		self.min_val = min_val
		self.max_val = max_val

	def run(self, input_vals):
		"""Return the input clipped to the min and/or max value(s)."""
		vals = input_vals.copy()
		if self.min_val is not None:
			vals = np.maximum(vals, self.min_val)
		if self.max_val is not None:
			vals = np.minimum(vals, self.max_val)
		return vals


class MinMaxScaler(AbstractBaseFunctionNode):
	"""Operator node that scales the input to be between 0 and 1.
	
	The scaling is based on the minimum and maximum values of the input,
	such that the minimum value of the input is mapped to 0 and the maximum
	value of the input is mapped to 1. All other values are scaled linearly
	between 0 and 1.
	
	Scaling is done either by feature or among all features based on the
	'by_feat' argument.

	Example:
	```python
		>>> vals = np.array([
			[1, 2, 3],
			[4, 5, 6],
			[7, 8, 9]
		])

		>>> mms_by_feat = MinMaxScaler("mms", "vals", by_feat=True)
		>>> mms_all = MinMaxScaler("mms", "vals", by_feat=False)

		>>> print(mms_by_feat(vals))
		array([[0. , 0.5, 1. ],
			[0. , 0.5, 1. ],
			[0. , 0.5, 1. ]])
		>>> print(mms_all(vals))
		array([[0.   , 0.125, 0.25 ],
			[0.375, 0.5  , 0.625],
			[0.75 , 0.875, 1.   ]])
	```
	"""
	
	def __init__(self, alias: str, input_alias: str, by_feat: bool = True):
		"""Initialize MinMaxScaler node.
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
			by_feat (bool, default True): Whether to scale by feature or
			among all features.
		"""
		super().__init__(alias)
		self.inputs = input_alias
		self.by_feat = by_feat

	def run(self, input_vals):
		"""Return the input scaled to be between 0 and 1.
		
		Args:
			input_vals: The input values to scale.
		
		Returns:
			The input scaled to be between 0 and 1.
		"""
		if input_vals.ndim == 1:
			input_vals = input_vals.reshape(1, -1)
		if self.by_feat:
			min_vals = input_vals.min(1, keepdims=True)
			max_vals = input_vals.max(1, keepdims=True)
		else:
			min_vals = input_vals.min(keepdims=True)
			max_vals = input_vals.max(keepdims=True)
		
		# Avoid division by zero
		ranges = max_vals - min_vals
		if np.any(ranges == 0):
			return np.where(ranges == 0, 0.5, (input_vals - min_vals) / ranges)
		else:
			return (input_vals - min_vals) / ranges
	

class StandardScaler(AbstractBaseFunctionNode):
	"""Operator that scales input to have mean 0 and standard deviation 1.

	Scaling is either done by feature or among all features based on the
	'by_feat' argument.

	Example:
	```python
		>>> vals = np.array([
			[1, 2, 3],
			[4, 5, 6],
			[7, 8, 9]
		])
		>>> std_scaler_by_feat = StandardScaler(
			"std_scaler", "vals", by_feat=True
		)
		>>> std_scaler_all = StandardScaler(
			"std_scaler", "vals", by_feat=False
		)

		>>> by_feat_out = std_scaler_by_feat(vals)
		>>> all_out = std_scaler_all(vals)

		>>> by_feat_out
		array([[-1.225,  0.   ,  1.225],
			[-1.225,  0.   ,  1.225],
			[-1.225,  0.   ,  1.225]])
		>>> all_out
		array([[-1.549, -1.162, -0.775],
			[-0.387,  0.   ,  0.387],
			[ 0.775,  1.162,  1.549]])
		
		>>> by_feat_out.mean(1)
		array([0., 0., 0.])
		>>> by_feat_out.std(1)
		array([1., 1., 1.])

		>>> all_out.mean(1)
		array([-1.162,  0.   ,  1.162])
		>>> all_out.mean()
		0.0
		>>> all_out.std()
		1.0
	"""

	def __init__(self, alias: str, input_alias: str, by_feat: bool = True):
		"""Initialize StandardScaler node.
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
			by_feat (bool, default True): Whether to scale by feature or
			among all features.
		"""
		super().__init__(alias)
		self.inputs = input_alias
		self.by_feat = by_feat

	def run(self, input_vals):
		"""Scale the input to have mean 0 and standard deviation 1."""
		if input_vals.ndim == 1:
			input_vals = input_vals.reshape(1, -1)
		if self.by_feat:
			mean_vals = input_vals.mean(1, keepdims=True)
			std_vals = input_vals.std(1, keepdims=True)
		else:
			mean_vals = input_vals.mean(keepdims=True)
			std_vals = input_vals.std(keepdims=True)

		# Avoid division by zero
		if np.any(std_vals == 0):
			return np.where(
				std_vals == 0,
				0.,
				(input_vals - mean_vals) / std_vals
			)
		return (input_vals - mean_vals) / std_vals


class RobustScaler(AbstractBaseFunctionNode):
	"""Operator that scales input to have median 0 and interquartile range 1.

	Output interquartile range can be changed by using the 'out_iqr' argument.
	Output median can be changed by using the 'out_median' argument.

	Scaling is either done by feature or among all features based on the
	'by_feat' argument.

	Example:
	```python
		>>> vals = np.array([
			[1, 2, 3],
			[4, 5, 6],
			[7, 8, 9]
		])
		>>> robust_by_feat = RobustScaler("robust", "vals", by_feat=True)
		>>> robust_all = RobustScaler("robust", "vals", by_feat=False)

		>>> robust_by_feat(vals)
		array([[-1.,  0.,  1.],
			[-1.,  0.,  1.],
			[-1.,  0.,  1.]])
		>>> robust_all(vals)
		array([[-1.  , -0.75, -0.5 ],
			[-0.25,  0.  ,  0.25],
			[ 0.5 ,  0.75,  1.  ]])

		>>> extreme_vals = np.array(
			np.random.normal(0, 10, 1000).tolist() + [-1000000000000]
		)
		>>> robust_by_feat(extreme_vals)
		array([[-7.454e-01, -6.908e-01, ..., -1.848e+00, -7.676e+10]])

		>>> vals = np.random.uniform(0, 10, size=(1000, 5))
		>>> robust_scaled = RobustScaler(
			"robust", "vals", out_iqr=.5, out_median=1
		)
		>>> scaled_vals = robust_scaled(vals)
		>>> np.median(scaled_vals, axis=0)
		array([1., 1., 1., 1., 1.])
		>>> iqr(scaled_vals, axis=0)
		array([0.608, 0.546, 0.528, 0.483, 0.571])
	```
	"""

	def __init__(
		self,
		alias: str,
		input_alias: str,
		by_feat: bool = True,
		out_iqr: float = 1.0,
		out_median: float = 0.0
	):
		"""Initialize RobustScaler node.
		
		Args:
			alias: The alias of the node.
			input_alias: The alias of the input node.
			by_feat (bool, default True): Whether to scale by feature or
				among all features.
			out_iqr (float, default 1.0): The interquartile range of the
				output.
			out_median (float, default 0.0): The median of the output.
		"""
		super().__init__(alias)
		self.inputs = input_alias
		self.by_feat = by_feat
		self.out_iqr = out_iqr
		self.out_median = out_median

	def run(self, input_vals):
		"""Scale the input to have median 0 and interquartile range 1."""
		if input_vals.ndim == 1:
			input_vals = input_vals.reshape(1, -1)
		
		if self.by_feat:
			medians = np.median(input_vals, axis=1, keepdims=True)
			iqrs = iqr(input_vals, axis=1, keepdims=True)
		else:
			medians = np.median(input_vals, keepdims=True)
			iqrs = iqr(input_vals, keepdims=True)

		# To avoid division by zero, replace zero IQRs with 1
		iqrs = np.where(iqrs == 0, 1, iqrs)

		# Subtract the median and scale by the IQR
		return (input_vals - medians) / iqrs * self.out_iqr + self.out_median


if __name__ == "__main__":

	# Test MinMaxScaler
	vals = np.array([
		[1, 2, 3],
		[4, 5, 6],
		[7, 8, 9]
	])

	mms_by_feat = MinMaxScaler("mms", "vals", by_feat=True)
	mms_all = MinMaxScaler("mms", "vals", by_feat=False)

	print(mms_by_feat(vals))
	print(mms_all(vals))

	# Test StandardScaler
	std_scaler_by_feat = StandardScaler("std_scaler", "vals", by_feat=True)
	std_scaler_all = StandardScaler("std_scaler", "vals", by_feat=False)

	by_feat_out = std_scaler_by_feat(vals)
	all_out = std_scaler_all(vals)


	# Test RobustScaler
	robust_by_feat = RobustScaler("robust", "vals", by_feat=True)
	robust_all = RobustScaler("robust", "vals", by_feat=False)

	robust_by_feat_out = robust_by_feat(vals)
	robust_all_out = robust_all(vals)

	extreme_vals = np.array(
		np.random.normal(0, 10, 1000).tolist() + [-1000000000000]
	)
	extr_out = robust_by_feat(extreme_vals)

	vals = np.random.uniform(0, 10, size=(1000, 5))
	robust_scaled = RobustScaler(
		"robust", "vals", out_iqr=.5, out_median=1
	)
	scaled_vals = robust_scaled(vals)
	np.median(scaled_vals, axis=0)
	iqr(scaled_vals, axis=0)


	# Test Clip
	clip = Clip("clip", "vals", min_val=2, max_val=8)
	print(clip(vals))

	clip = Clip("clip", "vals", min_val=4)
	print(clip(vals))

	clip = Clip("clip", "vals", max_val=6)
	print(clip(vals))
