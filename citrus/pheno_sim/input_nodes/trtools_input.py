"""
Input source object and nodes using the TRTools engine.
"""

import trtools.utils.utils as utils

class TRToolsInputSource(BaseInputSource):
	""" TRTools input source object.		
	"""

	def __init__(self, input_config):
		super().__init__(input_config)

		# Initialize reader
		self.trreader = utils.LoadSingleReader(args.vcf, checkgz=True)
		self.input_sample_ids = np.array(invcf.samples).astype(str)