# Input Sources

Each input source represents a file or multiple files and defines the input nodes who's values are derived from that data.

# Defining Input Sources

Each input source is represented by a dictionary with the following keys:

* file (optional, otherwise provided by command line argument): Path to the data file, list of file paths (if not using CLI), or hadoop glob pattern matching file(s).
* engine (optional str, default "hail"): The engine to use to read the data file. Currently only hail is supported.
* file_format (optional str, default "vcf"): The format of the data file. Currently only VCF is supported.
* input_nodes (optional list of dicts): A list of dictionaries that define the input nodes that use this data source.

### Engine Specific Keys

Based on the engine being used to load the data, there are additional optional keys that may be provided:

#### Hail

* reference_genome (optional str, default "GRCh38"): The reference genome to use when reading the data file. Must be one of: GRCh37, GRCh38, GRCm38, or CanFam3.

When using file_format "vcf", the force_bgz key may also be used:

* force_bgz (optional bool, default false): If true, force hail to read the file as bgzipped, even if the file extension is not .bgz. See [Hail import_vcf](https://hail.is/docs/0.2/methods/impex.html#hail.methods.import_vcf) for more information.
