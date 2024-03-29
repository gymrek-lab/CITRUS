""" Abstrract class for input sources (e.i. input data files like a VCF),
which will be used to create input nodes for the simulation.
"""

from abc import ABC, abstractmethod

import numpy as np


class BaseInputSource(ABC):
	""" Abstract class for input sources (e.i. input data files like a VCF),
	which will be used to create input nodes for the simulation.
	
	The class implements two main functions:
		- load_inputs(): Loads the input data from the source file and sets
			the input_nodes and input_sample_ids attributes.
		- subset_and_order_samples(sample_ids): Subsets data in input_nodes
			and input_sample_ids to just the sample ids in sample_ids and in
			the same order as sample_ids. Used to get corresponding sample ids
			and data from multiple input sources.
			
	There is also a class method get_input_source(input_config) that returns
	the appropriate input source class based on the dict from the input config.
			
	Attributes:
		input_config: The dictionary from the input section of the simulation
			config file that defines this input source. Input sources with
			random selection update this to what is selected for
			reproducibility.
		input_nodes: A list of input nodes that use the input source.
		input_sample_ids: A list of sample ids from the input source.
		
	Methods:
		load_inputs(): Loads the input data from the source file and sets
			the input_nodes and input_sample_ids attributes.
		subset_and_order_samples(sample_ids): Subsets data in input_nodes
			and input_sample_ids to just the sample ids in sample_ids and in
			the same order as sample_ids. Used to get corresponding sample ids
			and data from multiple input sources.
		get_input_source(input_config): Returns the appropriate input source
			class based on the dict from the input config.
	"""
	
	def __init__(self, input_config):
		self.input_config = input_config
		self.input_nodes = None
		self.input_sample_ids = None
	
	@abstractmethod
	def load_inputs(self):
		""" Loads the input data from the source file and sets the input_nodes
		and input_sample_ids attributes.
		"""
		pass
	
	def subset_and_order_samples(self, sample_ids, input_node_vals):
		""" Subsets data in input_nodes and input_sample_ids to just the sample
		ids in sample_ids and in the same order as sample_ids. Used to get
		corresponding sample ids and data from multiple input sources.
		
		Args:
			sample_ids: A list of sample ids to subset to and match the
				order of.
			input_node_vals: Dict of input node values to subset. The last
				dimension of each value should be the same length as
				self.input_sample_ids with corresponding values.

		Returns:
			dict input_node_vals with the last dimension of each value subset
			to just the sample ids in sample_ids and in the same order as
			sample_ids.
		"""
		subset_idx = [
			np.where(self.input_sample_ids == sid)[0][0] for sid in sample_ids
		]

		for key in input_node_vals.keys():
			if isinstance(input_node_vals[key], np.ndarray):
				if input_node_vals[key].ndim == 1:
					input_node_vals[key] = input_node_vals[key][subset_idx]
				else:
					input_node_vals[key] = input_node_vals[key][:, subset_idx]
			elif isinstance(input_node_vals[key], tuple):
				original_vals = input_node_vals[key]

				if original_vals[0].ndim == 1:
					input_node_vals[key] = (
						original_vals[0][subset_idx],
						original_vals[1][subset_idx]
					)
				else:
					input_node_vals[key] = (
						original_vals[0][:, subset_idx],
						original_vals[1][:, subset_idx]
					)
			else:
				raise ValueError(
					'Invalid input node value type: ' + str(type(input_node_vals[key]))
				)
			
		return input_node_vals
