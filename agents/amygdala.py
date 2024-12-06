import random

import queue
import neuron_agent as neuronAgent


class Neurons_Container:
    def __init__(self, max_out_degree, max_in_degree):
        self.list = []
        self.available_size = 0
        self.max_out_degree = max_out_degree
        self.max_in_degree = max_in_degree
        self.LF_population = 0
        self.RS_population = 0
        self.SP_population = 0

    def hide(self, pos):
        tmp = self.list[pos]
        self.list[pos] = self.list[self.available_size - 1]
        self.list[self.available_size - 1] = tmp
        self.available_size -= 1

    def at(self, pos):
        return self.list[pos]

    def insert(self, neuron):
        self.list.append(Neuron_element(neuron, len(self.list), self))

        if neuron.get_firing_rate_type == 'LF':
            self.LF_population += 1
        elif neuron.get_firing_rate_type == 'RS':
            self.RS_population += 1
        elif neuron.get_firing_rate_type == 'SP':
            self.SP_population += 1

        self.available_size += 1

    def get_max_out_degree(self):
        return self.max_out_degree

    def get_max_in_degree(self):
        return self.max_in_degree

    def calculate_freq(self, neuron):
        return;

    def get_total_freq(self):
        accumulative_freq = 0
        for neuron_element in self.list:
            neuron = neuron_element.neuron
            if neuron.get_firing_rate_type() == 'SP':
                continue
            accumulative_freq += self.calculate_freq(neuron)
        return accumulative_freq

    def __iter__(self):

        # TODO capire come cambiarlo

        # Initialize a queue with all elements
        self.visiting_queue = queue.Queue()
        for neuron_element in self.list[:len(self.list)]:
            self.visiting_queue.put(neuron_element)
        return self

    def __next__(self):
        if not self.visiting_queue.empty():
            return self.visiting_queue.get()
        else:
            raise StopIteration

    def __getitem__(self, item):
        return self.list[item]

    def react_to_stimuli(self, stimuli, cumulative_time_stimuli):
        for el in self.list:
            neuron = el.neuron
            neuron.update_damage(cum_s=cumulative_time_stimuli, stimulation=stimuli)

            if neuron.get_firing_rate_type() == 'SP' and neuron.get_damage() == 100 and self.SP_population / len(
                    self.list) > 0.48:
                neuron.change_type_to_RS()
                self.RS_population += 1
                self.SP_population -= 1

            neuron.update_frequency(stimulation=stimuli)

    def silence_all_neurons(self):
        for neuron in self.list:
            neuron.silence_neuron()


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


class Neuron_Container_PCK(Neurons_Container):
    def __init__(self, max_out_degree, max_in_degree):
        super().__init__(max_out_degree, max_in_degree)

    def insert(self, neuron: neuronAgent.Neuron_PCK):
        super().insert(neuron)

    def calculate_freq(self, neuron):
        return neuron.get_damage() * neuron.get_frequency()


class Neuron_Container_SOM(Neurons_Container):
    def __init__(self, max_out_degree, max_in_degree):
        super().__init__(max_out_degree, max_in_degree)

    def insert(self, neuron: neuronAgent.Neuron_SOM):
        super().insert(neuron)

    def calculate_freq(self, neuron):
        return neuron.get_frequency()


class Neuron_Container_other(Neurons_Container):
    def __init__(self, max_out_degree, max_in_degree):
        super().__init__(max_out_degree, max_in_degree)

    def insert(self, neuron: neuronAgent.Neuron_Other):
        super().insert(neuron)


class Amygdala:
    def __init__(self, neurons_number, SOM_RS_rate, SOM_LF_rate, SOM_SP_rate, PCK_RS_rate, PCK_LF_rate,
                 PCK_SP_rate, SOM_SOM_connectivity, SOM_PCK_connectivity, SOM_other_connectivity, PCK_PCK_connectivity,
                 PCK_SOM_connectivity, PCK_other_connectivity, SOM_rate=0.5, PCK_rate=0.4, others_rate=0.1,
                 in_min_connection=0, in_max_connection=5, out_min_connection=0, out_max_connection=5):
        self.neurons_number = neurons_number

        self.SOM_RS_rate = SOM_RS_rate
        self.SOM_LF_rate = SOM_LF_rate
        self.SOM_SP_rate = SOM_SP_rate
        self.PCK_RS_rate = PCK_RS_rate
        self.PCK_LF_rate = PCK_LF_rate
        self.PCK_SP_rate = PCK_SP_rate

        self.SOM_SOM_connectivity = SOM_SOM_connectivity
        self.SOM_PCK_connectivity = SOM_PCK_connectivity
        self.SOM_other_connectivity = SOM_other_connectivity
        self.PCK_PCK_connectivity = PCK_PCK_connectivity
        self.PCK_SOM_connectivity = PCK_SOM_connectivity
        self.PCK_other_connectivity = PCK_other_connectivity

        self.SOM_rate = SOM_rate
        self.PCK_rate = PCK_rate
        self.others_rate = others_rate
        self.in_min_connection = in_min_connection
        self.in_max_connection = in_max_connection
        self.out_min_connection = out_min_connection
        self.out_max_connection = out_max_connection

        self.population_SOM = Neuron_Container_SOM(self.out_max_connection, self.in_max_connection)
        self.population_PCK = Neuron_Container_PCK(self.out_max_connection, self.in_max_connection)
        self.population_Other = Neuron_Container_other(self.out_max_connection, self.in_max_connection)
        self.firing_type = ["LF", "RS", "SP"]

        self.prob_PCK_firing_type = [self.PCK_LF_rate, self.PCK_RS_rate, self.PCK_SP_rate]
        self.prob_SOM_firing_type = [self.SOM_LF_rate, self.SOM_RS_rate, self.SOM_SP_rate]

        self.prob_edges_SOM = [SOM_SOM_connectivity, SOM_PCK_connectivity, SOM_other_connectivity]
        self.prob_edges_PCK = [PCK_PCK_connectivity, PCK_SOM_connectivity, PCK_other_connectivity]

        self.create_network()

    def create_network(self):
        PCK_number = int(self.neurons_number * self.PCK_rate)
        SOM_number = int(self.neurons_number * self.SOM_rate)
        other_number = int(self.neurons_number * self.others_rate)

        PCK_types = random.choices(self.firing_type, weights=self.prob_PCK_firing_type, k=PCK_number)
        SOM_types = random.choices(self.firing_type, weights=self.prob_SOM_firing_type, k=SOM_number)

        for types in PCK_types:
            self.population_PCK.insert(neuronAgent.Neuron_PCK(types))

        for types in SOM_types:
            self.population_SOM.insert(neuronAgent.Neuron_SOM(types))

        for _ in range(0, other_number):
            self.population_Other.insert(neuronAgent.Neuron_Other())

        self.create_edges()

    def create_edges(self):

        for input_SOM_neuron in self.population_SOM:
            self.create_edge(input_SOM_neuron)

        for input_PCK_neuron in self.population_PCK:
            self.create_edge(input_PCK_neuron)

    def create_edge(self, input_neuron):
        rnd = int(random.uniform(self.in_min_connection, self.in_max_connection))
        types = random.choices(["SOM", "PCK", "OTHER"], weights=self.prob_edges_SOM, k=rnd)
        for type in types:
            if type == "SOM":
                self.select_output(input_neuron, self.population_SOM)
            elif type == "PCK":
                self.select_output(input_neuron, self.population_PCK)
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

    def get_global_population(self):
        return self.population_PCK.list + self.population_SOM.list + self.population_Other.list

    def update_states(self, stimuli, cumulative_time_stimuli):
        self.population_SOM.react_to_stimuli(stimuli,cumulative_time_stimuli)
        self.population_PCK.react_to_stimuli(stimuli,cumulative_time_stimuli)
        # magari un giorno ...
        # self.population_Other.react_to_stimuli(cumulative_time_stimuli,stimuli)


class Amygdala_R(Amygdala):
    def __init__(self, neurons_number, SOM_RS_rate, SOM_LF_rate, SOM_SP_rate, PCK_RS_rate, PCK_LF_rate,
                 PCK_SP_rate, SOM_SOM_connectivity, SOM_PCK_connectivity, SOM_other_connectivity, PCK_PCK_connectivity,
                 PCK_SOM_connectivity, PCK_other_connectivity, SOM_rate=0.5, PCK_rate=0.4, others_rate=0.1,
                 in_min_connection=0, in_max_connection=5, out_min_connection=0, out_max_connection=5):
        super().__init__(neurons_number, SOM_RS_rate, SOM_LF_rate, SOM_SP_rate, PCK_RS_rate,
                         PCK_LF_rate, PCK_SP_rate, SOM_SOM_connectivity, SOM_PCK_connectivity, SOM_other_connectivity,
                         PCK_PCK_connectivity, PCK_SOM_connectivity, PCK_other_connectivity, SOM_rate, PCK_rate,
                         others_rate,
                         in_min_connection, in_max_connection, out_min_connection, out_max_connection)


class Amygdala_L(Amygdala):
    def __init__(self, neurons_number, SOM_RS_rate, SOM_LF_rate, SOM_SP_rate, PCK_RS_rate, PCK_LF_rate,
                 PCK_SP_rate, SOM_SOM_connectivity, SOM_PCK_connectivity, SOM_other_connectivity, PCK_PCK_connectivity,
                 PCK_SOM_connectivity, PCK_other_connectivity, SOM_rate=0.5, PCK_rate=0.4, others_rate=0.1,
                 in_min_connection=0, in_max_connection=5, out_min_connection=0, out_max_connection=5):
        super().__init__(neurons_number, SOM_RS_rate, SOM_LF_rate, SOM_SP_rate, PCK_RS_rate,
                         PCK_LF_rate, PCK_SP_rate, SOM_SOM_connectivity, SOM_PCK_connectivity, SOM_other_connectivity,
                         PCK_PCK_connectivity, PCK_SOM_connectivity, PCK_other_connectivity, SOM_rate, PCK_rate,
                         others_rate,
                         in_min_connection, in_max_connection, out_min_connection, out_max_connection)


class Brain:
    def __init__(self, neurons_number, SOM_RS_rate, SOM_LF_rate, SOM_SP_rate, PCK_RS_rate, PCK_LF_rate,
                 PCK_SP_rate, SOM_SOM_connectivity, SOM_PCK_connectivity, SOM_other_connectivity, PCK_PCK_connectivity,
                 PCK_SOM_connectivity, PCK_other_connectivity, SOM_rate=0.5, PCK_rate=0.4, others_rate=0.1,
                 in_min_connection=0, in_max_connection=5, out_min_connection=0, out_max_connection=5):
        # TODO aggiungere alla parametrizzazione tutti i parametri separandoli dalla regione sx da quella destra
        # quindi ci saranno sempre gli stessi parametri ma _l o _r
        # es neurons_number_l e neurons_number_r ....
        self.amygdala_r = Amygdala_R(neurons_number, SOM_RS_rate, SOM_LF_rate, SOM_SP_rate, PCK_RS_rate,
                                     PCK_LF_rate,
                                     PCK_SP_rate, SOM_SOM_connectivity, SOM_PCK_connectivity, SOM_other_connectivity,
                                     PCK_PCK_connectivity,
                                     PCK_SOM_connectivity, PCK_other_connectivity, SOM_rate, PCK_rate, others_rate,
                                     in_min_connection, in_max_connection, out_min_connection, out_max_connection)
        self.amygdala_l = Amygdala_L(neurons_number, SOM_RS_rate, SOM_LF_rate, SOM_SP_rate, PCK_RS_rate,
                                     PCK_LF_rate,
                                     PCK_SP_rate, SOM_SOM_connectivity, SOM_PCK_connectivity, SOM_other_connectivity,
                                     PCK_PCK_connectivity,
                                     PCK_SOM_connectivity, PCK_other_connectivity, SOM_rate, PCK_rate, others_rate,
                                     in_min_connection, in_max_connection, out_min_connection, out_max_connection)

    def get_damage_r(self):
        return self.amygdala_r.population_PCK.get_total_freq() - self.amygdala_r.population_SOM.get_total_freq()

    def get_damage_l(self):
        return self.amygdala_l.population_PCK.get_total_freq() - self.amygdala_l.population_SOM.get_total_freq()

    def iterations(self, stimuli, max_duration):
        damage_list = []
        for cumulative_time_stimuli in range(1, max_duration):
            self.amygdala_l.update_states(stimuli, cumulative_time_stimuli)
            self.amygdala_r.update_states(stimuli, cumulative_time_stimuli)

            damage_list.append((self.get_damage_l(), self.get_damage_r()))
