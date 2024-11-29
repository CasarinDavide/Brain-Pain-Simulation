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


class Neuron_PKC(Neuron):
    def __init__(self, firing_rate):
        super().__init__(firing_rate)


class Neuron_SOM(Neuron):
    def __init__(self, firing_rate):
        super().__init__(firing_rate)


class Neuron_Other(Neuron):
    def __init__(self, firing_rate):
        super().__init__(firing_rate)
