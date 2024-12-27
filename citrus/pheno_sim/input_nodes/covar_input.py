"""
Input source object and nodes using the covars engine.

Same covar file format as plink
"""

class CovarInputSource(BaseInputSource):
	""" Covariates input source object.		
	"""

	def __init__(self, input_config):
		super().__init__(input_config)