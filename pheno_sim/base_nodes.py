""" Abstract base classes for nodes. """

from abc import ABC, abstractmethod
from typing import List, Dict, Union, TypedDict
import numpy as np
from .data_types import HaplotypeValues, Values, ValuesDict

class AbstractBaseInputNode(ABC):
	""" Abstract base class for input nodes.
	
	Input nodes read in genotype values from some file and convert them into
	HaplotypeValues or Values. They are all ran by the run_input_step method
	of the PhenoSimulation class.
	
	input_file_map can be None when all input nodes specify their input file paths in the specification file. If you want to use filename alias in the specification file instead, then input_file_map should be a Dict[str, str] where the keys are the aliases and the values are the paths to the files.

	Attributes:
		alias: A string that is used to identify the node in the simulation.
		
	Methods:
		load_vals(input_file_map: Dict[str, str] = None)
			-> Values or HaplotypeValues
			This method should be implemented in the child classes to load the
			appropriate values from the genotype files.
	"""
	def __init__(self, alias: str, **kwargs):
		self.alias = alias

	@abstractmethod
	def load_vals(
		self,
		input_file_map: Dict[str, str] = None
	) -> Union[Values, HaplotypeValues]:
		"""
		This method should be implemented in the child classes to load the
		appropriate values from the genotype files.
		
		Args:
			input_file_map (default None, otherwise Dict[str, str]): A dict
				where the keys are the aliases of input files and the values
				are the paths to the files. Only used when input nodes do not
				specify their input file paths in the specification file and
				instead use aliases to refer to the files. In this case, the
				specification file should have a key called "input_file_map"
				whose value is this dict.
		"""
		pass

class AbstractBaseFunctionNode(ABC):
	""" Abstract base class for function nodes.
	
	Function nodes apply some function to some values from the ValueDict and
	return a Values/HaplotypeValues object of the result. These nodes are ran by
	SimluationStep objects, which pass them the proper input from the ValuesDict
	and add the output to the ValuesDict.
	
	Functions can be divided into combine functions (which combine values from
	the two haplotypes into a single np.array) and general functions which apply
	some function to one of the following:

	- A single Values object or multiple Values objects. Returns a single Values
	object.

	- A single HaplotypeValues object or multiple HaplotypeValues objects. Returns
	a single HaplotypeValues object.

	- One or more Values objects and one or more HaplotypeValues objects. Returns
	a single HaplotypeValues object.
	
	Attributes:
		alias: A string that is used to identify the node in the simulation,
			including in the specification file and the ValuesDict.
		inputs: str, List[str], or Dict[str, str or List[str]]. If str,
			then the value in the ValuesDict with the key specified by
			input_mapping is passed to the function. If List[str], then the
			values in the ValuesDict with the keys specified by input_mapping
			are passed to the function as a list in that order. If 
			Dict[str, str or List[str]], then the values in the ValuesDict
			with the keys specified by the keys of input_mapping are passed
			to the function. If the value of a key in input_mapping is a str,
			then the value in the ValuesDict with the key specified by the
			value of the key in input_mapping is passed to the function. If
			the value of a key in input_mapping is a List[str], then the values
			in the ValuesDict are returned as a list in that order.
	
	Methods:
		__call__(input) -> Values or HaplotypeValues. Input is either a single
			Values object, a single HaplotypeValues object, or a list of
			Values and/or HaplotypeValues, or a dict where the keys are the
			names of inputs to the function and the values are the Values or
			HaplotypeValues objects from the ValuesDict. This method should be
			implemented in the child classes to perform the desired operation.
	"""
	def __init__(self, alias: str, *args, **kwargs):
		self.alias = alias
		self.inputs = None

	@abstractmethod
	def __call__(
		self, 
		*args: Union[Values, HaplotypeValues],
		**kwargs: Union[Values, HaplotypeValues]
	) -> Union[Values, HaplotypeValues]:
		"""
		This method should be implemented in the child classes to perform
		the desired operation.
		"""
		pass

class AbstractBaseCombineFunctionNode(AbstractBaseFunctionNode):
	""" Abstract base class for combine function nodes.
	
	Different from AbstractBaseFunctionNode in that the __call__ method
	should takes just HaplotypeValues objects as input and returns a
	single Values object.

	see AbstractBaseFunctionNode for more details.
	"""
	@abstractmethod
	def __call__(
		self, *args: HaplotypeValues, **kwargs: HaplotypeValues
	) -> Values:
		"""
		This method should be implemented in the child classes to perform
		the desired operation.
		"""
		pass
		