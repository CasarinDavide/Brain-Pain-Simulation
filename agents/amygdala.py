class Amygdala:
    def __init__(self, neurons_number, in_stimulation, SOM_RS_rate, SOM_LF_rate, SOM_SP_rate, PKC_RS_rate, PKC_LF_rate,
                 PKC_SP_rate, SOM_SOM_connectivity, SOM_PKC_connectivity, SOM_other_connectivity, PKC_PKC_connectivity,
                 PKC_SOM_connectivity, PKC_other_connectivity, SOM_rate=0.5, PKC_rate=0.5, others_rate=0,
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

        self.population = []


class Amygdala_R:
    def __init__(self):
        return


class Amygdala_L:
    def __init__(self):
        return
