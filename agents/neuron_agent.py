# TYPE PKC e SOM e OTHER
#
import random
import pandas as pd

dtype_dict = {
    "Type": str,
    "Freq": str,
    "pA": str  # Add any other columns to be read as strings
}

df = pd.read_csv('agents/data_csv/firing_data.csv', sep=';', header=0, dtype=dtype_dict)


def trunc_gauss(mu, sigma, bottom, top):

    if mu > top:
        c = 10
    a = random.gauss(mu, sigma)
    while not (bottom <= a <= top):
        a = random.gauss(mu, sigma)
    return a


def getXY(stimulation, firing_rate, type_neuron):
    # stimulation=120
    # type_neuron = type(self).__name__[-3:]

    query_str = f"Type == '{type_neuron}' and Freq == '{firing_rate}' and pA == '{stimulation}'"
    filtered_rows = df.query(query_str)

    # Check if any rows match
    if filtered_rows.empty:
        raise ValueError("No matching row found in the DataFrame for the given parameters.")

    # Extract the first matching row
    row = filtered_rows.iloc[0].tolist()
    X = trunc_gauss(int(row[3]), int(row[4]), int(row[5]), int(row[6]))  # X_mu X_std X_min X_max
    Y = trunc_gauss(int(row[7]), int(row[8]), int(row[9]), int(row[10]))  # X_mu X_std X_min X_max
    return X, Y


class Neuron:
    def __init__(self, firing_rate=''):
        self.firing_rate = firing_rate
        self.accumulate_damage = 0
        self.freq = 0

        # la sensibilità dipende dal tipo

        self.sensitivity = random.uniform(40, 80)  # t_l
        self.resistance_stimuli_duration = random.uniform(50, 150)  # t_s
        self.input_neighborhood = []
        self.output_neighborhood = []
        self.is_silence = 1

    def get_firing_rate_type(self):
        # LF;RS;SP
        return self.firing_rate

    def change_type_to_RS(self):
        self.firing_rate = 'RS'

    def add_input_to_neighborhood(self, neuron):
        self.input_neighborhood.append(neuron)

    def add_output_to_neighborhood(self, neuron):
        self.output_neighborhood.append(neuron)

    def is_in_input_neighborhood(self, neuron):
        return neuron in self.input_neighborhood

    def is_in_output_neighborhood(self, neuron):
        return neuron in self.output_neighborhood

    def input_degree(self):
        return len(self.input_neighborhood)

    def output_degree(self):
        return len(self.output_neighborhood)

    def update_damage(self, cum_s, stimulation):
        if cum_s > self.resistance_stimuli_duration and stimulation >= 120:
            self.accumulate_damage = min(self.accumulate_damage + 100 / self.sensitivity, 100)

    def update_frequency(self, stimulation):

        if self.firing_rate == 'SP':
            if type(self) == Neuron_PKC:
                return 4.8
            elif type(self) == Neuron_SOM:
                return 2.1
            else:
                return 0
        else:
            X, Y = getXY(stimulation, self.firing_rate, type(self).__name__[-3:])
            self.freq = X * (100 - self.accumulate_damage) / 100 + Y * self.accumulate_damage / 100

    def get_input_neighborhood(self):
        freq = 0
        for neuron in self.input_neighborhood:
            freq += neuron.get_frequency()
        return freq

    def silence_neuron(self, threshold=15):
        if self.get_input_neighborhood() > threshold:
            self.is_silence = 0

    def get_frequency(self):
        if not self.is_silence:
            # resetto per il passo successivo
            self.is_silence = 1
            return 0
        else:
            return self.freq

    def get_damage(self):
        return self.accumulate_damage


class Neuron_PKC(Neuron):
    def __init__(self, firing_rate):
        super().__init__(firing_rate)


class Neuron_SOM(Neuron):
    def __init__(self, firing_rate):
        super().__init__(firing_rate)


class Neuron_Other(Neuron):
    def __init__(self):
        super().__init__("X")
