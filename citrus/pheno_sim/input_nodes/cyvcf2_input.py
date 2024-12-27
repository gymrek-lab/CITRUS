"""
Input source object and nodes using the cyvcf2 engine.
"""

class Cyvcf2InputSource(BaseInputSource):
	""" Cyvcf2 input source object.		
	"""

	def __init__(self, input_config):
		super().__init__(input_config)