""" Abstrract class for input sources (e.i. input data files like a VCF),
which will be used to create input nodes for the simulation.
"""

from abc import ABC, abstractmethod

import numpy as np


class BaseInputSource(ABC):
	""" Abstract class for input sources (e.i. input data files like a VCF),
	which will be used to create input nodes for the simulation.
	
	Attributes:
		input_config: The dictionary from the input section of the simulation
			config file that defines this input source. Input sources with
			random selection update this to what is selected for
			reproducibility.
		input_node_ids: A list of input nodes that use the input source.
		input_sample_ids: A list of sample ids from the input source.
		
	Methods:
		load_input_node(): Loads data for a single input node from the 
		    source file. Optionally pass a list of sample_ids to subset and
		    reorder according to that sample list
	"""
	
	def __init__(self, input_config):
		self.input_config = input_config
		self.input_node_ids = self.input_config.keys()
		self.input_sample_ids = []
	
	@abstractmethod
	def load_input_node(self, input_node_config, sample_ids=None):
		""" Loads the input data from the source file for a single node.
		"""
		pass

	def subset_and_order_samples(self, input_node_vals, sample_ids):
		""" Subsets data ito just the sample
		ids in sample_ids and in the same order as sample_ids. Used to get
		corresponding sample ids and data from multiple input sources.
		
		Args:
			input_node_vals: Input node values for a single node. The last
				dimension of each value should be the same length as
				self.input_sample_ids with corresponding values.
			sample_ids: A list of sample ids to subset to and match the
				order of.

		Returns:
			dict input_node_vals with the last dimension of each value subset
			to just the sample ids in sample_ids and in the same order as
			sample_ids.
		"""
		subset_idx = [
			np.where(self.input_sample_ids == sid)[0][0] for sid in sample_ids
		]

		if isinstance(input_node_vals, np.ndarray):
			if input_node_vals.ndim == 1:
				input_node_vals = input_node_vals[subset_idx]
			else:
				input_node_vals = input_node_vals[:, subset_idx]
		elif isinstance(input_node_vals, tuple):
			original_vals = input_node_vals

			if original_vals[0].ndim == 1:
				input_node_vals = (
					original_vals[0][subset_idx],
					original_vals[1][subset_idx]
				)
			else:
				input_node_vals = (
					original_vals[0][:, subset_idx],
					original_vals[1][:, subset_idx]
				)
		else:
			raise ValueError(
				'Invalid input node value type: ' + str(type(input_node_vals[key]))
			)
			
		return input_node_vals