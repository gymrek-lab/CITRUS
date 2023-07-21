import pydot

def visualize(input_spec: dict, filename: str, format: str):

        # Create the graph
        graph = pydot.Dot(graph_type='digraph')

        # Define clusters
        cluster_0 = pydot.Cluster('cluster_0', label='Cis effects')
        graph.add_subgraph(cluster_0)

        cluster_1 = pydot.Cluster('cluster_1', label='Inheritance effects')
        graph.add_subgraph(cluster_1)

        cluster_2 = pydot.Cluster('cluster_2', label='Trans effects')
        graph.add_subgraph(cluster_2)
        
        # Iterate over input nodes
        for input_node in input_spec['input'][0]['input_nodes']:

            alias = input_node['alias']
            input_label= f'{alias}\n<input_node>'
            # cluster_0.add_node(pydot.Node(alias, label=input_label, style='filled', fillcolor="blue"))
            graph.add_node(pydot.Node(alias, label=input_label, style='filled', fillcolor='bisque'))

        # cluster_0.add_subgraph(input_nodes)
        # Iterate over simulation steps
        for step in input_spec['simulation_steps']:
            step_type = step['type']
            alias = step['alias']
            input_label = f'{alias}\n<{step_type}>'

            if 'Combine' in step_type:  
                graph.add_node(pydot.Node(alias, label=input_label, style='filled', fillcolor='lightskyblue'))
            else:
                graph.add_node(pydot.Node(alias, label=input_label, style='filled', fillcolor='aquamarine'))
            
            if 'input_alias' in step:
                input_alias = step['input_alias']
                graph.add_edge(pydot.Edge(input_alias, alias))
            elif 'input_aliases' in step:
                input_aliases = step['input_aliases']		
                for input_alias in input_aliases:	
                    graph.add_edge(pydot.Edge(input_alias, alias))
                    
        # Save the graph to a file
        graph.write(filename, format=format)
