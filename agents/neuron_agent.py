

# TYPE PKC e SOM e OTHER
#
class Neuron:
    def __init__(self,neuron_type,firing_rate,accumulate_damage,sensitivity,resistance_stimuli_duration):
        self.neuron_type = neuron_type
        self.firing_rate = firing_rate
        self.accumulate_damage = accumulate_damage
        self.sensitivity = sensitivity
        self.resistance_stimuli_duration = resistance_stimuli_duration
        self.input_neighborhood = []
        self.output_neighborhood = []

