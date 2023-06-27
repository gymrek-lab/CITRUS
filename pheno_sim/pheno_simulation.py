""" Object that runs the simulation. It is constructed from a JSON
specification file. The specification file contains definitions of the
inputs, the function nodes, and the output.

Attributes:
	input_step (InputStep): The input step of the simulation. Loads input
		genotype values as a ValuesDict.
	simulation_steps (List[SimulationStep]): List of the steps that when
		ran sequentially will run the simulation.
	output_step (OutputStep): The output step of the simulation. TODO.
	input_file_map (Dict[str, str]): A mapping from input file aliases to
		their paths. This is only used if 'input_file_map' is a key in the
		simulation specification dict.
		
Methods:
	__init__(self, spec_dict: Dict) -> None
		Initializes the PhenoSimulation object. This object will create the
			input step, the simulation steps, and the output step from the
			simulation specification dict.
			
	from_JSON_file(cls, file_path: str) -> PhenoSimulation
		Alternative constructor. Creates a PhenoSimulation object from a
			simulation specification JSON file. Class method.
			
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

import json
from typing import Dict, List

from pheno_sim.data_types import ValuesDict
from pheno_sim.base_nodes import AbstractBaseFunctionNode
from pheno_sim.func_nodes import FunctionNodeBuilder
from pheno_sim.input_nodes import InputRunner


class PhenoSimulation:
	""" Object that runs the simulation. Also handles creating function nodes.
	
	Designed to be constructed from a JSON/dict simulation specification.
	"""
	
	def __init__(self, spec_dict: Dict, custom_func_node_classes=[]) -> None:
		""" Initializes the PhenoSimulation object. This object will create the
		input step, the simulation steps, and the output step from the
		simulation specification dict.
		
		Args:
			spec_dict: A dict containing the simulation specification.
				See the documentation for the simulation specification
				format.
			custom_func_node_classes (default []): A list of custom function
				node classes that can be used in the simulation.
		"""
		self._setup_input(spec_dict)
		self._setup_simulation_steps(spec_dict, custom_func_node_classes)
		self._setup_output(spec_dict)

	@classmethod
	def from_JSON_file(cls, file_path: str, custom_func_node_classes=[]):
		""" Alternative constructor. Creates a PhenoSimulation object from a
		simulation specification JSON file. Class method.
		
		Args:
			file_path: Path to the simulation specification JSON file.
			custom_func_node_classes (default []): A list of custom function
				node classes to be used in the simulation.
			
		Returns:
			A PhenoSimulation object.
		"""
		
		# Load JSON file as dict.
		with open(file_path, 'r') as f:
			spec_dict = json.load(f)
		
		# Create PhenoSimulation object from dict.
		return cls(spec_dict, custom_func_node_classes)
	
	@classmethod
	def from_sim_steps_list(
		cls,
		sim_steps: List[AbstractBaseFunctionNode],
		input_spec: Dict = None,
		output_spec: Dict = None
	):
		""" Alternative constructor. Creates a PhenoSimulation object from a
		list of simulation steps. Class method.
		
		Args:
			sim_steps: A list of simulation steps.
			input_spec (default {}): A dict containing the input specification.
			output_spec (default {}): A dict containing the output
				specification.
			
		Returns:
			A PhenoSimulation object.
		"""
		
		# Create PhenoSimulation object from dict.
		sim_obj = cls({
			'input': input_spec,
			'output': output_spec
		})

		# Set the simulation steps.
		sim_obj.simulation_steps = sim_steps

		return sim_obj
	
	def _setup_input(self, spec_dict: Dict) -> None:
		""" Sets up the input step from the simulation specification dict.
		
		Args:
			spec_dict: A dict containing the simulation specification.
				See the documentation for the simulation specification
				format.
		"""
		
		self.input_spec = spec_dict['input']

		self.input_runner = InputRunner(self.input_spec)

	def _setup_simulation_steps(
		self,
		spec_dict: Dict,
		custom_func_node_classes=[]
	) -> None:
		""" Sets up the simulation steps from the simulation specification
		dict.
		
		Args:
			spec_dict: A dict containing the simulation specification.
				See the documentation for the simulation specification
				format.
			custom_func_node_classes (default []): A list of custom function
				node classes that can be used in the simulation.
		"""

		self.simulation_steps = []

		if 'simulation_steps' in spec_dict:
			self.func_node_builder = FunctionNodeBuilder(custom_func_node_classes)

			for step_spec in spec_dict['simulation_steps']:
				node_type = step_spec.pop('type')
				self.simulation_steps.append(
					self.func_node_builder.create_node(node_type, **step_spec)
				)

	def _setup_output(self, spec_dict: Dict) -> None:
		""" Sets up the output step from the simulation specification dict.
		
		Args:
			spec_dict: A dict containing the simulation specification.
				See the documentation for the simulation specification
				format.

		TODO Implement output step
		"""
		
		self.output_spec = None

		if 'output' in spec_dict:
			self.output_spec = spec_dict['output']

	def run_input_step(self) -> ValuesDict:
		""" Run the input step and return the ValuesDict to be passed to the
		simulation steps.

		Sets the sample_ids attribute to the sample IDs from the input step.

		Returns:
			A ValuesDict containing the input values.
		"""	
		if self.input_spec is None:
			self.sample_ids = None
			return dict()
		else:
			self.sample_ids, input_node_vals = self.input_runner()
			return input_node_vals
		
	def run_output_step(self, val_dict: ValuesDict) -> ValuesDict:
		""" Save and/or return the output values ('pheno' and any any
		additional 'vals').

		TODO Implement output step.
		"""
		if self.output_spec is None:
			return val_dict
		else:
			raise NotImplementedError("Output step not implemented yet.")
		
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
			self, val_dict: ValuesDict, run_output_step=True
	):
		""" Run the simulation steps and optionally the output step. Returns
		whatever is returned by the last step run.
		
		Args:
			val_dict: A ValuesDict containing the input values.
			run_output_step: Whether to run the output step. Default is True.
			
		Returns:
			Whatever is returned by the last step run.
		"""
		
		# Run simulation steps.
		for step in self.simulation_steps:
			val_dict = self.run_function_node(step, val_dict)
		
		# Run output step if specified.
		if run_output_step:
			val_dict = self.run_output_step(val_dict)
		
		return val_dict
	
	def run_simulation(self):
		""" Run phenotype simulation. """

		# Run input step.
		val_dict = self.run_input_step()

		# Run simulation steps.
		return self.run_simulation_steps(val_dict)
