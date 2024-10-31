"""Plot simulation as directed graph."""

import pydot
from PIL import Image, ImageDraw

from pheno_sim.pheno_simulation import PhenoSimulation
from pheno_sim.base_nodes import AbstractBaseCombineFunctionNode
from .utils import MSG

def visualize(input_spec: dict, filename: str, 
    img_format: str, verbose: bool=False) -> int:
    """
    Visualize a phenotype model

    Parameters
    ----------
    input_spec : dict
       Model configuration
    filename : str
       Prefix of output filename
    img_format : str
       Format of output file (jpg, png, or svg})
    verbose : bool
       If true, print extra output to terminal

    Returns
    -------
    retcode : int
       Return code (0 for success)
    """

    # Generate sim object
    sim = PhenoSimulation(input_spec)

    # Add input nodes
    sim_nodes = dict()

    for input_source in sim.input_runner.input_sources:
        for input_node in input_source.input_nodes:
            sim_nodes[input_node.alias] = CITRUSNode(
                alias=input_node.alias,
                node_type='input',
                class_name=type(input_node).__name__
            )

    # Add operator nodes
    for sim_step in sim.simulation_steps:
        step_alias = sim_step.alias
        step_inputs = sim_step.inputs

        if isinstance(step_inputs, str):
            step_inputs = [step_inputs]
        elif isinstance(step_inputs, dict):
            step_inputs = list(step_inputs.values())

        if isinstance(sim_step, AbstractBaseCombineFunctionNode):
            step_type = 'combine'
        else:
            step_type = 'trans'
        
        sim_nodes[step_alias] = CITRUSNode(
            alias=step_alias,
            inputs=step_inputs,
            node_type=step_type,
            class_name=type(sim_step).__name__
        )

    # Identify nodes that are of type 'combine'.
    combine_nodes = [node for node in sim_nodes.values() if node.node_type == 'combine']

    # For each combine node, identify its ancestors.
    all_ancestor_nodes = set()
    for combine_node in combine_nodes:
        all_ancestor_nodes.update(get_ancestor_nodes(combine_node, sim_nodes))

    # Change the node_type of ancestor nodes which are of type 'trans' to 'cis'.
    for ancestor_node_alias in all_ancestor_nodes:
        if sim_nodes[ancestor_node_alias].node_type == 'trans':
            sim_nodes[ancestor_node_alias].node_type = 'cis'

    # Print nodes
    if verbose:
        for k,v in sim_nodes.items():
            MSG(f"{k}:\n\t{str(v)}")

    # Plot the graph
    plot_graph_with_legend(sim_nodes, filename, img_format)
    MSG(f"Plot output to {filename}.{img_format}")

    # Return
    return 0


class CITRUSNode:
    """
    Helper class for plotting.
    Represents a single CITRUS model node

    Attributes
    ----------
    alias : str
        Node alias
    inputs : list
        Simulation steps input to this node
    node_type : str
        One of: input, cis, trans, combine
    class_name : str
        Name of the class of the node
    """
    def __init__(
        self,
        alias,
        inputs=[],
        node_type=None,
        class_name=None
    ):
        self.alias = alias
        self.inputs = inputs
        self.node_type = node_type
        self.class_name = class_name

    def __str__(self):
        return f"alias: {self.alias}\tnode_type: {self.node_type}\tclass_name: {self.class_name}\tinputs: {self.inputs}"


def get_ancestor_nodes(node: CITRUSNode, 
    sim_nodes: dict[str, CITRUSNode]) -> list[CITRUSNode]:
    """
    Iteratively get ancestor nodes of a given node.

    Parameters
    ----------
    node : CITRUSNode
        node to get ancestors of
    sim_nodes : dict[str]->CITRUSNode
        Dictionary of all nodes

    Returns
    -------
    ancestors : list of CITRUSNode
        List of nodes that are ancestors of node
    """
    ancestors = set()
    to_visit = [node]

    while to_visit:
        current_node = to_visit.pop()
        
        # Add the direct parents to the ancestors set
        for input_node_alias in current_node.inputs:
            # Check if the ancestor is already in the set to avoid cycles
            if input_node_alias not in ancestors:
                ancestors.add(input_node_alias)
                to_visit.append(sim_nodes[input_node_alias])

    return list(ancestors)



def plot_graph_with_legend(sim_nodes: dict[str, CITRUSNode], 
    filename: str, img_format: str):
    """
    Make the plot from a list of nodes

    Parameters
    ----------
    sim_nodes : dict[str]->CITRUSNode
        Dictionary of all nodes
    filename : str
       Prefix of output filename
    img_format : str
       Format of output file (jpg, png, or svg})
    """
    
    # Define a dictionary for colors based on node_type
    node_colors = {
        'input': '#FF8C00',    # dark orange
        'cis': '#90EE90',      # light green 
        'trans': '#DEB887',    # burly wood (light brown)
        'combine': '#FFF44F'   # lemon yellow
    }

    # Create a new graph
    graph = pydot.Dot(graph_type='digraph', rankdir='UD', ranksep='0.5')

    # Add nodes with their respective colors
    for node in sim_nodes.values():
        label = f"{node.alias}\n<{node.class_name}>"
        graph.add_node(pydot.Node(node.alias, label=label, style="filled", fillcolor=node_colors[node.node_type]))

    # Add edges based on the inputs of each node
    for node in sim_nodes.values():
        for input_node in node.inputs:
            graph.add_edge(pydot.Edge(input_node, node.alias))

    # Save graph to file
    graph.write(filename + '.' + img_format, format=img_format)

    # Adding a legend using PIL
    img = Image.open(filename + '.' + img_format)
    legend = Image.new('RGB', (250, 100), (255, 255, 255))
    
    # Draw the legend
    for index, (label, color) in enumerate(node_colors.items()):
        d = ImageDraw.Draw(legend)
        d.rectangle([10, 10 + index * 25, 30, 30 + index * 25], fill=color)
        d.text((40, 10 + index * 25), label, fill=(0, 0, 0))

    # Scale up the legend by any desired factor
    scale_factor = 2.0
    scaled_width = int(legend.width * scale_factor)
    scaled_height = int(legend.height * scale_factor)
    legend = legend.resize(
        (scaled_width, scaled_height),
        resample=Image.BICUBIC
    )

    # Trim whitespace: Here we'll crop out 40% from the right, adjust as needed
    crop_percentage = 0.5
    cropped_width = int(scaled_width * (1 - crop_percentage))
    legend = legend.crop((0, 0, cropped_width, scaled_height))

    # Combine original image and legend
    total_width = img.width + legend.width
    max_height = max(img.height, legend.height)

    combined = Image.new('RGB', (total_width, max_height), 'white')
    combined.paste(img, (0, 0))

    # Center the legend vertically
    y_offset = (img.height - legend.height) // 2
    combined.paste(legend, (img.width, y_offset))

    combined.save(filename + '.' + img_format)