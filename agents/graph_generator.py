import random
import networkx as nx
import plotly.graph_objects as go


# Assuming the provided Neurons_Container, Neuron_element, and related classes are defined above

# Function to build the graph from the Neurons_Container
def build_graph_from_container(container):
    G = nx.DiGraph()  # Directed graph for input/output relationships

    # Add nodes
    for neuron_element in container:
        neuron = neuron_element.neuron
        G.add_node(neuron_element,
                   neuron_type=type(neuron).__name__,
                   firing_rate=neuron.get_firing_rate_type(),
                   damage=neuron.get_damage(),
                   frequency=neuron.get_frequency())

    # Add edges based on input/output neighborhoods
    for neuron_element in container:
        neuron = neuron_element.neuron
        for input_neuron in neuron.input_neighborhood:
            G.add_edge(input_neuron, neuron_element)  # Input connection
        for output_neuron in neuron.output_neighborhood:
            G.add_edge(neuron_element, output_neuron)  # Output connection

    return G

# Function to visualize the graph in 3D
def plot_neurons_container(container):
    # Build the graph
    G = build_graph_from_container(container)

    # Use spring layout for positioning in 3D
    pos = nx.spring_layout(G, dim=10, seed=42)

    # Extract node positions
    x_nodes = [pos[i][0] for i in G.nodes()]
    y_nodes = [pos[i][1] for i in G.nodes()]
    z_nodes = [pos[i][2] for i in G.nodes()]

    # Extract edge positions
    x_edges = []
    y_edges = []
    z_edges = []
    for edge in G.edges():
        x_coords = [pos[edge[0]][0], pos[edge[1]][0], None]
        y_coords = [pos[edge[0]][1], pos[edge[1]][1], None]
        z_coords = [pos[edge[0]][2], pos[edge[1]][2], None]
        x_edges += x_coords
        y_edges += y_coords
        z_edges += z_coords

    # Create traces for edges
    trace_edges = go.Scatter3d(
        x=x_edges, y=y_edges, z=z_edges,
        mode='lines',
        line=dict(color='black', width=2),
        hoverinfo='none'
    )

    colors = {'Neuron_PCK': 'blue', 'Neuron_SOM': 'red', 'Neuron_Other': 'green'}

    # Create traces for nodes
    node_colors = []

    for i in G.nodes():
        try:
            type = G.nodes[i]['neuron_type']
            node_colors.append(colors[type])
        except:
            a = G.nodes[i]
    node_text = [
        f"Type: {G.nodes[i]['neuron_type']}<br>"
        f"Firing Rate: {G.nodes[i]['firing_rate']}<br>"
        f"Damage: {G.nodes[i]['damage']:.2f}<br>"
        f"Frequency: {G.nodes[i]['frequency']:.2f}"
        for i in G.nodes()
    ]
    trace_nodes = go.Scatter3d(
        x=x_nodes, y=y_nodes, z=z_nodes,
        mode='markers',
        marker=dict(
            size=10,
            color=node_colors,
            line=dict(color='black', width=0.5)
        ),
        text=node_text,
        hoverinfo='text'
    )

    # Layout for the 3D graph
    layout = go.Layout(
        title="Neuron Network Visualization",
        scene=dict(
            xaxis=dict(showbackground=False),
            yaxis=dict(showbackground=False),
            zaxis=dict(showbackground=False)
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    # Combine traces and plot
    fig = go.Figure(data=[trace_edges, trace_nodes], layout=layout)
    fig.show()


