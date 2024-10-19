""" Class that initializes and returns function nodes. Used by
PhenoSimulation to initialize steps. 

By default registers all function nodes (subclasses of AbstractBaseFunctionNode)
in the func_nodes package. User can also provide a list of custom function nodes
to register.
"""

import inspect

from ..base_nodes import AbstractBaseFunctionNode
from .. import func_nodes


class FunctionNodeBuilder:
	
	def __init__(self, custom_classes=[]):
		""" Initialize node builder.
		
		By default registers all function nodes (subclasses of
		AbstractBaseFunctionNode) in func_nodes dir. 

		Any classes specified in custom_classes list will also be registered.
		"""
		self.node_class_registry = {}

		# Register all function nodes in func_nodes dir.
		self._register_all_func_nodes()

		# Register any custom classes.
		self._register_custom_classes(custom_classes)

	def _register_all_func_nodes(self):
		""" Registers all function nodes in func_nodes. """
		for name, obj in inspect.getmembers(func_nodes):
			if inspect.isclass(obj) and issubclass(obj, AbstractBaseFunctionNode):
				self.node_class_registry[obj.__name__] = obj

	def _register_custom_classes(self, custom_classes):
		""" Registers any custom classes. """
		for node_class in custom_classes:
			if (
				inspect.isclass(node_class) 
       			and issubclass(node_class, AbstractBaseFunctionNode)
			):
				self.node_class_registry[node_class.__name__] = node_class
			else:
				raise ValueError(f"Invalid class {node_class}. "
					"Must be a subclass of AbstractBaseFunctionNode."
				)
			
	def create_node(self, class_name, **kwargs):
		""" Creates a function node of the specified class. """
		node_class = self.node_class_registry.get(class_name, None)
		if node_class is None:
			raise ValueError(f"No node class found with name {class_name}")
		return node_class(**kwargs)
