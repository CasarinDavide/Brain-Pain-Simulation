# TYPE PKC e SOM e OTHER
#
import random


class Neuron:
    def __init__(self, firing_rate =''):
        self.firing_rate = firing_rate
        self.accumulate_damage = 0
        self.freq = 0

        # la sensibilità dipende dal tipo

        self.sensitivity = random.uniform(1, 50)
        self.resistance_stimuli_duration = random.uniform(50, 150)
        self.input_neighborhood = []
        self.output_neighborhood = []
        self.is_enabled = 1

    def add_input_to_neighborhood(self,neuron):
        self.input_neighborhood.append(neuron)

    def add_output_to_neighborhood(self,neuron):
        self.output_neighborhood.append(neuron)

    def is_in_input_neighborhood(self,neuron):
        return neuron in self.input_neighborhood

    def is_in_output_neighborhood(self,neuron):
        return neuron in self.output_neighborhood

    def input_degree(self):
        return len(self.input_neighborhood)

    def output_degree(self):
        return len(self.output_neighborhood)



class Neuron_PKC(Neuron):
    def __init__(self, firing_rate):
        super().__init__(firing_rate)


class Neuron_SOM(Neuron):
    def __init__(self, firing_rate):
        super().__init__(firing_rate)


class Neuron_Other(Neuron):
    def __init__(self):
        super().__init__()
