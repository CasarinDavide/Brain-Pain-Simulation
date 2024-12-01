import window as window
import firing_rate_data as data
import os as os
import amygdala

# window il modulo per gestire la finestra di simulazione

agent = window.AgentBased()
# agent.simulate()

agent_amygdala = amygdala.Amygdala(neurons_number=10000, in_stimulation=120, SOM_RS_rate=0.27, SOM_LF_rate=0.18,
                                   SOM_SP_rate=0.55, PKC_RS_rate=0.48, PKC_LF_rate=0.25,
                                   PKC_SP_rate=0.27, SOM_SOM_connectivity=0.55, SOM_PKC_connectivity=0.15,
                                   SOM_other_connectivity=0.30, PKC_PKC_connectivity=0.20,
                                   PKC_SOM_connectivity=0.10, PKC_other_connectivity=0.70, SOM_rate=0.5, PKC_rate=0.4,
                                   others_rate=0.1,
                                   in_min_connection=0, in_max_connection=5, out_min_connection=0, out_max_connection=5)

agent_amygdala.create_network()
a = 10
# print(os.getcwd())
# file_path = os.getcwd() + "\\data_csv"
# data.load_firing_data(file_path)
