""" Conditional functions. """

import numpy as np

from pheno_sim.base_nodes import AbstractBaseFunctionNode


class IfElse(AbstractBaseFunctionNode):
	""" Implements an If-Else conditional statement.
	
	A node that takes as input a numpy array of values, parameters for
	a conditional statement, one array of values to be returned if the
	condition is true, and one array of values to be returned if the
	condition is false. The condition is evaluated element-wise. All
	arrays must have the same shape.
	
	Comparison function may be greater that (gt), greater than or equal (ge),
	less than (lt), less than or equal (le), equal (eq), or not equal (ne).
		
	Args:
		alias: The alias of the node.
		input_cond_vals: The alias of the input node for values used to
			evaluate the condition.
		input_if_vals: The alias of the input node for values to be
			returned if the condition is true.
		input_else_vals: The alias of the input node for values to be
			returned if the condition is false.
		threshold: The threshold to use for the condition. Default is 1.
		comparison: The comparison operator to use. One of 'ge' (default),
			'le', 'gt', 'lt', 'eq', or 'ne'.
	
	Examples:
		>>> cond_vals = np.array([0, 1, 0])
		>>> if_vals = np.array([1, 1, 1])
		>>> else_vals = np.array([-1, -1, -1])
		>>> IfElse("if_else", "cond_vals", "if_vals", "else_vals")(cond_vals)
		array([-1, 1, -1])

		>>> cond_vals = np.array([[0, .9, 0], [.8, .1, .5]])
		>>> if_vals = np.array([[1, 1, 1], [1, 1, 1]])
		>>> else_vals = np.array([[-1, -1, -1], [-1, -1, -1]])
		>>> IfElse("if_else", "cond_vals", "if_vals", "else_vals",
		...		threshold=.5, comparison="lt")(cond_vals)
		array([[1, -1,  1],
			   [-1, 1, -1]])
	"""

	def __init__(
		self,
		alias: str,
		input_cond_vals: str,
		input_if_vals: str,
		input_else_vals: str,
		threshold: float = 1,
		comparison: str = "ge"
	):
		super().__init__(alias)
		self.inputs = {
			"cond_vals": input_cond_vals,
			"if_vals": input_if_vals,
			"else_vals": input_else_vals
		}
		self.threshold = threshold
		self.comparison = comparison

	def run(self, cond_vals, if_vals, else_vals):
		if self.comparison == "ge":
			return np.where(cond_vals >= self.threshold, if_vals, else_vals)
		elif self.comparison == "le":
			return np.where(cond_vals <= self.threshold, if_vals, else_vals)
		elif self.comparison == "gt":
			return np.where(cond_vals > self.threshold, if_vals, else_vals)
		elif self.comparison == "lt":
			return np.where(cond_vals < self.threshold, if_vals, else_vals)
		elif self.comparison == "eq":
			return np.where(cond_vals == self.threshold, if_vals, else_vals)
		elif self.comparison == "ne":
			return np.where(cond_vals != self.threshold, if_vals, else_vals)
		else:
			raise ValueError(
				"comparison must be one of 'ge', 'le', 'gt', 'lt', 'eq', or 'ne'"
			)
		

if __name__ == "__main__":
	
	# Test IfElse
	cond_vals = np.array([0, 1, 0])
	if_vals = np.array([1, 1, 1])
	else_vals = np.array([-1, -1, -1])
	input_kwargs = {
		'cond_vals': cond_vals, 'if_vals': if_vals, 'else_vals': else_vals
	}
	print(IfElse("if_else", "cond_vals", "if_vals", "else_vals")(**input_kwargs))

	cond_vals = np.array([[0, .9, 0], [.8, .1, .5]])
	if_vals = np.array([[1, 1, 1], [1, 1, 1]])
	else_vals = np.array([[-1, -1, -1], [-1, -1, -1]])
	input_kwargs = {
		'cond_vals': cond_vals, 'if_vals': if_vals, 'else_vals': else_vals
	}
	print(IfElse(
			"if_else", "cond_vals", "if_vals", "else_vals",
			threshold=.5, comparison="lt"
		)(**input_kwargs)
	)