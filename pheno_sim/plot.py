import pydot

def visualize(input_spec: dict, filename: str, format: str):

        # Create the graph
        graph = pydot.Dot(graph_type='digraph', rankdir='BT')
        
        # Define clusters
        # cluster_0 = pydot.Cluster('cluster_0', label='Cis effects')
        # graph.add_subgraph(cluster_0)

        # cluster_1 = pydot.Cluster('cluster_1', label='Inheritance effects')
        # graph.add_subgraph(cluster_1)

        # cluster_2 = pydot.Cluster('cluster_2', label='Trans effects')
        # graph.add_subgraph(cluster_2)

        legend = pydot.Cluster('legend', label='Legend')
        graph.add_subgraph(legend)
        
        
        # Iterate over input nodes
        for input_node in input_spec['input'][0]['input_nodes']:

            alias = input_node['alias']
            input_label= f'{alias}\n<input_node>'
            input_node = pydot.Node(alias, label=input_label, style='filled', fillcolor='lightgrey')
            
            graph.add_node(input_node)

        # nodes before combine node are cis nodes
        # nodes after combine node are trans nodes 
        seen_combine_node = False

        # Iterate over simulation steps
        for step in input_spec['simulation_steps']:
            step_type = step['type']
            alias = step['alias']
            input_label = f'{alias}\n<{step_type}>'

            if 'Combine' in step_type:
                inheritance_node = pydot.Node(alias, label=input_label, style='filled', fillcolor='lightskyblue')  
                graph.add_node(inheritance_node)

                attrs = inheritance_node.get_attributes()
                dest_node = pydot.Node('inheritance', label='inheritance\nnode', style=attrs['style'], fillcolor=attrs['fillcolor'])
                legend.add_node(dest_node)

                seen_combine_node = True # following nodes will be trans-nodes
            
            else:
                if seen_combine_node:
                    trans_node = pydot.Node(alias, label=input_label, style='filled', fillcolor='aquamarine')
                    graph.add_node(trans_node)
                    attrs = trans_node.get_attributes()
                    legend.add_node(pydot.Node('trans', label='trans-\nnode', style=attrs['style'], fillcolor=attrs['fillcolor'], fontname='times italic'))
                
                else:
                    cis_node = pydot.Node(alias, label=input_label, style='filled', fillcolor='lightgrey')
                    graph.add_node(cis_node)
                    attrs = cis_node.get_attributes()
                    legend.add_node(pydot.Node('cis', label='cis-\nnode', style=attrs['style'], fillcolor=attrs['fillcolor'], fontname='times italic'))

            if 'input_alias' in step:
                input_alias = step['input_alias']
                graph.add_edge(pydot.Edge(input_alias, alias))
            elif 'input_aliases' in step:
                input_aliases = step['input_aliases']		
                for input_alias in input_aliases:	
                    graph.add_edge(pydot.Edge(input_alias, alias))

        # add invisible edge from phenotype output node to legend cluster for control over layout
        if seen_combine_node:
            graph.add_edge(pydot.Edge(trans_node, dest_node, style='invis', minlen=2))

        # nodes = graph.get_node_list()
        # edges = graph.get_edge_list()
        # print(graph.number_of_edges())
        # print(nodes[0].to_string())
        # print(edges[0].get_destination())
        # print(edges[0].parse_node_ref())

        # Save the graph to a file
        graph.write(filename, format=format)
