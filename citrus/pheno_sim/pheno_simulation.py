""" Object that runs the simulation. It is constructed from a JSON
configuration file. The configuration file contains definitions of the
inputs, the function nodes, and the output.

Attributes:
	input_step (InputStep): The input step of the simulation. Loads input
		genotype values as a ValuesDict.
	simulation_steps (List[SimulationStep]): List of the steps that when
		ran sequentially will run the simulation.
	output_step (OutputStep): The output step of the simulation. TODO.
	input_file_map (Dict[str, str]): A mapping from input file aliases to
		their paths. This is only used if 'input_file_map' is a key in the
		simulation configuration dict.
		
Methods:
	__init__(self, config_dict: Dict) -> None
		Initializes the PhenoSimulation object. This object will create the
			input step, the simulation steps, and the output step from the
			simulation configuration dict.
			
	from_JSON_file(cls, file_path: str) -> PhenoSimulation
		Alternative constructor. Creates a PhenoSimulation object from a
			simulation configuration JSON file. Class method.
			
	run_input_step(self) -> ValuesDict
		Run the input step and return the ValuesDict to be passed to the
			simulation steps.
			
	run_simulation_steps(
		self, input_values: ValuesDict, run_output_step=True
	) -> ValuesDict
		Run the simulation steps and optionally the output step. Returns
			whatever is returned by the last step run.
	
	run_simulation(
		self, input_file_map: None (default) or Dict[str, str]
	) -> ValuesDict
		Run the simulation. Returns whatever is returned by the last step.
"""

import copy
import json
import os
from typing import Dict, List

import numpy as np
import pandas as pd

from .data_types import ValuesDict
from .base_nodes import AbstractBaseFunctionNode
from .func_nodes import FunctionNodeBuilder
from .input_nodes import InputRunner

class PhenoSimulation:
	""" Object that runs the simulation. Also handles creating function nodes.
	
	Designed to be constructed from a JSON/dict simulation configuration.
	"""
	
	def __init__(self, config_dict: Dict, custom_func_node_classes=[]) -> None:
		""" Initializes the PhenoSimulation object. This object will create the
		input step, the simulation steps, and the output step from the
		simulation configuration dict.
		
		Args:
			config_dict: A dict containing the simulation configuration.
				See the documentation for the simulation configuration
				format.
			custom_func_node_classes (default []): A list of custom function
				node classes that can be used in the simulation.
		"""
		self._setup_input(config_dict)
		self._setup_simulation_steps(config_dict, custom_func_node_classes)

	@classmethod
	def from_JSON_file(cls, file_path: str, custom_func_node_classes=[]):
		""" Alternative constructor. Creates a PhenoSimulation object from a
		simulation configuration JSON file. Class method.
		
		Args:
			file_path: Path to the simulation configuration JSON file.
			custom_func_node_classes (default []): A list of custom function
				node classes to be used in the simulation.
			
		Returns:
			A PhenoSimulation object.
		"""
		
		# Load JSON file as dict.
		with open(file_path, 'r') as f:
			config_dict = json.load(f)
		
		# Create PhenoSimulation object from dict.
		return cls(config_dict, custom_func_node_classes)
	
	@classmethod
	def from_sim_steps_list(
		cls,
		sim_steps: List[AbstractBaseFunctionNode],
		input_config: Dict = None,
		output_config: Dict = None
	):
		""" Alternative constructor. Creates a PhenoSimulation object from a
		list of simulation steps. Class method.
		
		Args:
			sim_steps: A list of simulation steps.
			input_config (default {}): A dict containing the input configuration.
			output_config (default {}): A dict containing the output
				configuration.
			
		Returns:
			A PhenoSimulation object.
		"""
		
		# Create PhenoSimulation object from dict.
		sim_obj = cls({
			'input': input_config,
			'output': output_config
		})

		# Set the simulation steps.
		sim_obj.simulation_steps = sim_steps

		return sim_obj
	
	def _setup_input(self, config_dict: Dict) -> None:
		""" Sets up the input step from the simulation configuration dict.
		
		Args:
			config_dict: A dict containing the simulation configuration.
				See the documentation for the simulation configuration
				format.
		"""
		
		self.input_config = config_dict['input']

		self.input_runner = InputRunner(self.input_config)

	def _setup_simulation_steps(
		self,
		config_dict: Dict,
		custom_func_node_classes=[]
	) -> None:
		""" Sets up the simulation steps from the simulation configuration
		dict.
		
		Args:
			config_dict: A dict containing the simulation configuration.
				See the documentation for the simulation configuration
				format.
			custom_func_node_classes (default []): A list of custom function
				node classes that can be used in the simulation.
		"""
		self.simulation_steps = []
		self.sim_config = config_dict['simulation_steps']

		if 'simulation_steps' in config_dict:
			self.func_node_builder = FunctionNodeBuilder(custom_func_node_classes)

			for step_config in config_dict['simulation_steps']:
				step_config = step_config.copy()
				node_type = step_config.pop('type')
				self.simulation_steps.append(
					self.func_node_builder.create_node(node_type, **step_config)
				)

		# Track whether the simulation has been run and self.sim_config has
		# been updated.
		self.sim_config_updated = False

	def run_input_step(self) -> ValuesDict:
		""" Run the input step and return the ValuesDict to be passed to the
		simulation steps.

		Sets the sample_ids attribute to the sample IDs from the input step.

		Returns:
			A ValuesDict containing the input values.
		"""	
		if self.input_config is None:
			self.sample_ids = None
			return dict()
		else:
			self.sample_ids, input_node_vals = self.input_runner()
			return input_node_vals

	@staticmethod
	def run_function_node(
		function_node: AbstractBaseFunctionNode,
		vals_dict: ValuesDict
	):
		""" Run a function node and return the output.
		
		Performs following steps:
			1. Get input values to function_node from vals_dict.
			2. Run function node.
			3. Add output to vals_dict.
			4. Return vals_dict.

		Args:
			function_node: The function node to run.
			vals_dict: A ValuesDict containing the input values.

		Returns:
			vals_dict, with the output of the function node added.

		"""
		# Run function node
		if function_node.inputs is None:
			# Run function node with no inputs
			node_output = function_node()
		elif isinstance(function_node.inputs, str):
			# Run function node with one input
			node_output = function_node(vals_dict[function_node.inputs])
		elif isinstance(function_node.inputs, list):
			# Run with positional arguments
			node_output = function_node(*[
				vals_dict[input_alias] for input_alias in function_node.inputs
			])
		elif isinstance(function_node.inputs, dict):
			# Run with keyword arguments
			node_output = function_node(**{
				input_name: vals_dict[input_alias]
				for input_name, input_alias in function_node.inputs.items()
			})
		else:
			raise ValueError(
				"Function node attribute inputs must be None, str, list, or dict."
			)
		
		# Add output to vals_dict
		vals_dict[function_node.alias] = node_output

		return vals_dict

	def run_simulation_steps(
			self, val_dict: ValuesDict
	):
		""" Run the simulation steps and optionally the output step. Returns
		whatever is returned by the last step run.
		
		Args:
			val_dict: A ValuesDict containing the input values.
			
		Returns:
			Whatever is returned by the last step run.
		"""
		
		# Run simulation steps.
		for step in self.simulation_steps:
			val_dict = self.run_function_node(step, val_dict)

		# Update self.sim_config if it has not been updated.
		if not self.sim_config_updated:
			for i in range(len(self.simulation_steps)):
				self.sim_config[i].update(
					self.simulation_steps[i].get_config_updates()
				)

			# Update self.sim_config_updated
			self.sim_config_updated = True
		
		return val_dict
	
	def run_simulation(self):
		""" Run phenotype simulation. """

		# Run input step.
		val_dict = self.run_input_step()

		# Run simulation steps.
		return self.run_simulation_steps(val_dict)
	
	@staticmethod
	def vals_dict_to_dataframe(vals_dict: ValuesDict) -> pd.DataFrame:
		""" Convert a ValuesDict to a pandas DataFrame. 
		
		Values in Values dict are either 1D or 2D numpy arrays, or a two
		length tuple of 1D or 2D numpy arrays. Keys with values that are:

			1D numpy arrays: Converted to a single column with the key as
				the column name.

			2D numpy arrays: Converted to multiple columns with names that
				are '{key}*-*{row_index}'.

			Two length tuple of 1D arrays: Converted to two columns with
				names that are '{key}*-*a' and '{key}*-*b'. 'a' will always
				correspond to the first element in the tuple, and 'b' will
				always correspond to the second element in the tuple.

			Two length tuple of 2D arrays: Converted to 2*n_rows columns
				with names that are '{key}*-*{a/b}*-*{row_index}'.
		"""
		df_dict = dict()

		for key, vals in vals_dict.items():
			# 1D or 2D array
			if isinstance(vals, np.ndarray):
				if vals.ndim == 1:
					df_dict[key] = vals
				elif vals.ndim == 2:
					for i in range(vals.shape[0]):
						df_dict[f'{key}*-*{i}'] = vals[i]
				else:
					raise ValueError(
						"Numpy arrays in ValuesDict must be 1D or 2D."
					)
			# By haplotype tuples
			elif isinstance(vals, tuple):
				if len(vals) == 2:
					idx_letter_pairs = [('a', 0), ('b', 1)]
					for idx_letter, idx in idx_letter_pairs:
						if vals[idx].ndim == 1:
							df_dict[f'{key}*-*{idx_letter}'] = vals[idx]
						elif vals[idx].ndim == 2:
							for i in range(vals[idx].shape[0]):
								df_dict[f'{key}*-*{idx_letter}*-*{i}'] = vals[idx][i]
						else:
							raise ValueError(
								"Numpy arrays in ValuesDict must be 1D or 2D."
							)
				else:
					raise ValueError(
						"Tuples in ValuesDict must have length 2."
					)
			else:
				raise ValueError(
					"ValuesDict values must be numpy arrays or tuples."
				)
			
		return pd.DataFrame(df_dict)
	
	@staticmethod
	def dataframe_to_vals_dict(df: pd.DataFrame) -> ValuesDict:
		""" Convert a pandas DataFrame to a ValuesDict. 

		Values in Values dict are either 1D or 2D numpy arrays, or a two
		length tuple of 1D or 2D numpy arrays. Column names in the dataframe
		will must be named in one of the following formats and will become
		values in the ValuesDict with the corresponding key:

			* Single 1D array: '{key}'
			* Single 2D array: '{key}*-*{row_index}'
			* Two length tuple of 1D arrays: '{key}*-*a' and '{key}*-*b'
			* Two length tuple of 2D arrays: '{key}*-*{a/b}*-*{row_index}'

		NOTE: '*-*' is used as the delimiter and thus cannot be used in the key.

		Args:
			df: Pandas DataFrame to convert to ValuesDict.

		Returns:
			ValueDict reformed from values from the dataframe.
		"""

		vals_dict = dict()

		# Map from all unique keys from dataframe to columns in dataframe
		key_col_map = dict()

		for col in df.columns:
			key = col.split('*-*')[0]

			if key not in key_col_map:
				key_col_map[key] = list()

			key_col_map[key].append(col)

		# Create ValuesDict from dataframe
		for col_name, col_vals in df.items():

			col_name_parts = col_name.split('*-*')

			# Single value 1D array
			if len(col_name_parts) == 1:
				vals_dict[col_name_parts[0]] = col_vals.values
			elif len(col_name_parts) == 2:
				# Single value 2D array is col_vals[1] is an integer
				if col_name_parts[1].isdigit():
					# Create 2D array if it doesn't exist
					if col_name_parts[0] not in vals_dict:
						vals_dict[col_name_parts[0]] = np.zeros(
							(len(key_col_map[col_name_parts[0]]), df.shape[0])
						)
					# Add values to 2D array by row index
					vals_dict[col_name_parts[0]][int(col_name_parts[1])] = col_vals.values
				# Two length tuple of 1D arrays
				elif col_name_parts[1] == 'a' or col_name_parts[1] == 'b':
					# Create tuple if it doesn't exist
					if col_name_parts[0] not in vals_dict:
						vals_dict[col_name_parts[0]] = [None, None]
					# Add values to tuple
					vals_dict[col_name_parts[0]][
						0 if col_name_parts[1] == 'a' else 1
					] = col_vals.values
				# Error
				else:
					raise ValueError(
						'Invalid column name format: {}'.format(col_name)
					)
			elif len(col_name_parts) == 3:
				# Two length tuple of 2D arrays
				# Create tuple if it doesn't exist
				if col_name_parts[0] not in vals_dict:
					vals_dict[col_name_parts[0]] = [
						np.zeros(
							(len(key_col_map[col_name_parts[0]]) // 2, df.shape[0])
						),
						np.zeros(
							(len(key_col_map[col_name_parts[0]]) // 2, df.shape[0])
						)
					]
				
				# Add values to tuple by row index
				vals_dict[col_name_parts[0]][0 if col_name_parts[1] == 'a' else 1][
					int(col_name_parts[2])
				] = col_vals.values
			else:
				raise ValueError(
					'Invalid column name format: {}'.format(col_name)
				)
					
		# Cast lists vals in vals_dict to tuples
		for key, val in vals_dict.items():
			if isinstance(val, list):
				vals_dict[key] = tuple(val)

		return vals_dict
	
	def get_config(self) -> dict:
		""" Get the simulation configuration. """
		return {
			"input": self.input_runner.get_config(),
			"simulation_steps": self.sim_config
		}

	def save_output(
		self,
		output_vals: ValuesDict,
		include_config: bool = True,
		output_dir='.',
		output_file_name='output.csv',
		output_config_name='sim_config.json',
		sep=',',
		add_sample_ids=True,
	):
		""" Save the output to a file.

		If 'output_dir' does not exist, will create it.
		
		Args:
			output_vals: A ValuesDict containing the values from the
				simulation.
			include_config (default True): Whether to also save the
				simulation configuration in the output directory.
			output_dir (default '.'): The directory to save the output to.
			output_file_name (default 'output.csv'): The name of the output
				file.
			output_config_name (default 'sim_config.json'): The name of the
				saved simulation configuration file. Should include any
				random choices made in setting up the simulation.
			sep (default ','): The separator to use when saving the output.
			add_sample_ids (default True): Whether to add sample ids to the
				output. If True, will add a column 'sample_id' with values
				from self.sample_ids.
		"""

		# Check if output directory exists.
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)

		# Convert to pandas DataFrame.
		output_vals = output_vals.copy()

		if add_sample_ids:
			output_vals['sample_id'] = self.sample_ids

		df = self.vals_dict_to_dataframe(output_vals)

		# Save output.
		df.to_csv(
			os.path.join(output_dir, output_file_name),
			sep=sep,
			index=False
		)

		# Save simulation configuration.
		if include_config:
			with open(os.path.join(output_dir, output_config_name), 'w') as f:
				json.dump(
					self.get_config(),
					f,
					indent=4
				)


	def estimate_heritability(
		self,
		input_vals=None,
		n_replicates: int = 100,
		n_samples=1.0,
		phenotype_alias='phenotype'
	):
		"""Estimate broad-sense heritability (H^2) of the phenotype.

		Args:
			input_vals (default None): A ValuesDict containing the input
				values. If None, will run the input step of the simulation.
			n_replicates (default 100): The number of replicates of each
				genotype to simulate.
			n_samples (default 1.0): The fraction or number of samples to
				use when estimating heritability. If value is less than or
				equal to 1, will use that fraction of samples. If value is
				greater than 1, will use that number of samples. Samples
				will be randomly selected from the input samples.
			phenotype_alias (default 'phenotype'): The alias of the
				phenotype node to use when estimating heritability.
		"""

		assert n_replicates >= 2, "n_replicates must be greater than 1."

		# Get input genotype values.
		if input_vals is None:
			input_vals = self.run_input_step()

		if n_samples > 1:
			selected_idx = np.random.choice(
				len(self.sample_ids),
				n_samples,
				replace=False
			)
			
			for key, val in input_vals.items():
				if isinstance(val, tuple):
					input_vals[key] = (
						val[0][..., selected_idx], val[1][..., selected_idx]
					)
				else:
					input_vals[key] = val[..., selected_idx]
		elif n_samples < 1:
			selected_idx = np.random.choice(
				len(self.sample_ids),
				int(n_samples * len(self.sample_ids)),
				replace=False
			)
			
			for key, val in input_vals.items():
				if isinstance(val, tuple):
					input_vals[key] = (
						val[0][..., selected_idx], val[1][..., selected_idx]
					)
				else:
					input_vals[key] = val[..., selected_idx]
		
		# Estimate heritability.

		# Step 1: Run simulation n_replicates times.
		pheno_vals = []

		for i in range(n_replicates):
			pheno_vals.append(
				self.run_simulation_steps(
					copy.deepcopy(input_vals)
				)[phenotype_alias]
			)

		# Convert to matrix where rows are replicates and columns are samples.
		pheno_vals = np.vstack(pheno_vals).astype(float)

		# Step 2: Compute total variance.
		total_var = np.var(pheno_vals)

		# Step 3: Compute inter-genotype variance (the variance of the mean
		# phenotype for each genotype).
		inter_geno_var = np.var(np.mean(pheno_vals, axis=0))

		# Step 4: Compute average intra-genotype variance
		intra_geno_var = np.var(pheno_vals, axis=0).mean()

		# Step 5: Compute genetic variance component
		genetic_var = inter_geno_var - intra_geno_var

		# Step 6: Compute heritability
		heritability = genetic_var / total_var

		return heritability


