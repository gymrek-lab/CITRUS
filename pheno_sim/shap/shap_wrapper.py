""" Wrapper class for using simulation class with SHAP library. """

import pandas as pd

class SHAPWrapper:
	""" Wrapper class for using simulation class with SHAP library. """

	def __init__(self, simulation, phenotype: str, column_names):
		""" Initialize SHAPWrapper class.

		Args:
			simulation (PhenoSimulation): PhenoSimulation object.
			phenotype (str): Phenotype key to use for SHAP values.
			column_names (list-like): List of column names for input data
				numpy array X.
		"""
		self.simulation = simulation
		self.phenotype = phenotype
		self.column_names = column_names

	def __call__(self, X):
		""" Call method for SHAPWrapper class.

		Args:
			X: Input data as numpy array.

		Returns:
			PhenoSimulation output.
		"""
		X = pd.DataFrame(X, columns=self.column_names)
		vals_dict = self.simulation.dataframe_to_vals_dict(X)
		return self.simulation.run_simulation_steps(vals_dict)[
			self.phenotype
		].astype(float)
	
