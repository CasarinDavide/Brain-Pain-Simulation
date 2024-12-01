import random

import queue
import neuron_agent as neuronAgent
import numpy as np


class Neurons_Container:
    def __init__(self, max_out_degree, max_in_degree):
        self.list = []
        self.available_size = 0
        self.max_out_degree = max_out_degree
        self.max_in_degree = max_in_degree

    def hide(self, pos):
        tmp = self.list[pos]
        self.list[pos] = self.list[self.available_size - 1]
        self.list[self.available_size - 1] = tmp
        self.available_size -= 1

    def at(self, pos):
        return self.list[pos]

    def insert(self, neuron):
        self.list.append(Neuron_element(neuron, len(self.list), self))
        self.available_size += 1

    def get_max_out_degree(self):
        return self.max_out_degree

    def get_max_in_degree(self):
        return self.max_in_degree

    def __iter__(self):
        # Initialize a queue with all elements
        self.visiting_queue = queue.Queue()
        for neuron_element in self.list[:len(self.list)]:  # Only consider active elements
            self.visiting_queue.put(neuron_element)
        return self

    def __next__(self):
        if not self.visiting_queue.empty():
            return self.visiting_queue.get()
        else:
            raise StopIteration

    def __getitem__(self, item):
        return self.list[item]


class Neuron_element:
    def __init__(self, neuron, pos, container: Neurons_Container):
        self.neuron = neuron
        self.pos = pos
        self.container = container

    def add_edge_input(self, neuron):
        self.neuron.add_input_to_neighborhood(neuron)

    def add_edge_output(self, neuron):
        self.neuron.add_output_to_neighborhood(neuron)
        if self.neuron.output_degree() == self.container.get_max_out_degree():
            self.container.hide(self.pos)

    def is_in_input_neighborhood(self, neuron):
        return self.neuron.is_in_input_neighborhood(neuron)


class Neuron_Container_PKC(Neurons_Container):
    def __init__(self, max_out_degree, max_in_degree):
        super().__init__(max_out_degree, max_in_degree)

    def insert(self, neuron: neuronAgent.Neuron_PKC):
        super().insert(neuron)


class Neuron_Container_SOM(Neurons_Container):
    def __init__(self, max_out_degree, max_in_degree):
        super().__init__(max_out_degree, max_in_degree)

    def insert(self, neuron: neuronAgent.Neuron_SOM):
        super().insert(neuron)


class Neuron_Container_other(Neurons_Container):
    def __init__(self, max_out_degree, max_in_degree):
        super().__init__(max_out_degree, max_in_degree)

    def insert(self, neuron: neuronAgent.Neuron_Other):
        super().insert(neuron)


class Amygdala:
    def __init__(self, neurons_number, in_stimulation, SOM_RS_rate, SOM_LF_rate, SOM_SP_rate, PKC_RS_rate, PKC_LF_rate,
                 PKC_SP_rate, SOM_SOM_connectivity, SOM_PKC_connectivity, SOM_other_connectivity, PKC_PKC_connectivity,
                 PKC_SOM_connectivity, PKC_other_connectivity, SOM_rate=0.5, PKC_rate=0.4, others_rate=0.1,
                 in_min_connection=0, in_max_connection=5, out_min_connection=0, out_max_connection=5):
        self.neurons_number = neurons_number

        self.in_stimulation = in_stimulation

        self.SOM_RS_rate = SOM_RS_rate
        self.SOM_LF_rate = SOM_LF_rate
        self.SOM_SP_rate = SOM_SP_rate
        self.PKC_RS_rate = PKC_RS_rate
        self.PKC_LF_rate = PKC_LF_rate
        self.PKC_SP_rate = PKC_SP_rate

        self.SOM_SOM_connectivity = SOM_SOM_connectivity
        self.SOM_PKC_connectivity = SOM_PKC_connectivity
        self.SOM_other_connectivity = SOM_other_connectivity
        self.PKC_PKC_connectivity = PKC_PKC_connectivity
        self.PKC_SOM_connectivity = PKC_SOM_connectivity
        self.PKC_other_connectivity = PKC_other_connectivity

        self.SOM_rate = SOM_rate
        self.PKC_rate = PKC_rate
        self.others_rate = others_rate
        self.in_min_connection = in_min_connection
        self.in_max_connection = in_max_connection
        self.out_min_connection = out_min_connection
        self.out_max_connection = out_max_connection

        self.population_SOM = Neuron_Container_SOM(self.out_max_connection, self.in_max_connection)
        self.population_PKC = Neuron_Container_PKC(self.out_max_connection, self.in_max_connection)
        self.population_Other = Neuron_Container_other(self.out_max_connection, self.in_max_connection)
        self.firing_type = ["LF", "RS", "SP"]

        self.prob_PKC_firing_type = [self.PKC_LF_rate, self.PKC_RS_rate, self.PKC_SP_rate]
        self.prob_SOM_firing_type = [self.SOM_LF_rate, self.SOM_RS_rate, self.SOM_SP_rate]

        self.prob_edges_SOM = [SOM_SOM_connectivity, SOM_PKC_connectivity, SOM_other_connectivity]
        self.prob_edges_PCK = [PKC_PKC_connectivity, PKC_SOM_connectivity, PKC_other_connectivity]

    def create_network(self):
        PKC_number = int(self.neurons_number * self.PKC_rate)
        SOM_number = int(self.neurons_number * self.SOM_rate)
        other_number = int(self.neurons_number * self.others_rate)

        PKC_types = random.choices(self.firing_type, weights=self.prob_PKC_firing_type, k=PKC_number)
        SOM_types = random.choices(self.firing_type, weights=self.prob_SOM_firing_type, k=SOM_number)

        for types in PKC_types:
            self.population_PKC.insert(neuronAgent.Neuron_PKC(types))

        for types in SOM_types:
            self.population_SOM.insert(neuronAgent.Neuron_SOM(types))

        for _ in range(0, other_number):
            self.population_Other.insert(neuronAgent.Neuron_Other())

        self.create_edges()

    def create_edges(self):

        for input_SOM_neuron in self.population_SOM:
            self.create_edge(input_SOM_neuron)

        for input_PKC_neuron in self.population_PKC:
            self.create_edge(input_PKC_neuron)

    def create_edge(self, input_neuron):
        rnd = int(random.uniform(self.in_min_connection, self.in_max_connection))
        types = random.choices(["SOM", "PKC", "OTHER"], weights=self.prob_edges_SOM, k=rnd)
        for type in types:
            if type == "SOM":
                self.select_output(input_neuron, self.population_SOM)
            elif type == "PKC":
                self.select_output(input_neuron, self.population_PKC)
            else:
                self.select_output(input_neuron, self.population_Other)

    def select_output(self, input_neuron, population):
        selected = False
        while not selected:
            rnd1 = int(random.uniform(0, population.available_size))
            output_neuron = population[rnd1]

            if output_neuron != input_neuron and not input_neuron.is_in_input_neighborhood(output_neuron):
                selected = True
                input_neuron.add_edge_input(output_neuron)
                output_neuron.add_edge_output(input_neuron)


class Amygdala_R(Amygdala):
    def __init__(self):
        return


class Amygdala_L(Amygdala):
    def __init__(self):
        super().__init__()
