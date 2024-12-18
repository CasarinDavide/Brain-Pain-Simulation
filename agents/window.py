import pygame
import random

import amygdala as amygdala
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import graph_generator as graph


# classe per gestire la finestra di dialogo, mostra in real time la simulazione
class AgentBased:
    def __init__(self):

        pygame.init()
        # Screen dimensions
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Real-Time Simulation")

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.BLUE = [0, 0, 255]
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Create subplots
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(12, 10))

        # Configure first graph
        self.line1, = self.ax1.plot([], [], color='g', lw=2, label='Damage Left')
        self.ax1.set_xlim(0, 100)
        self.ax1.set_ylim(-4000, 4000)
        self.ax1.set_title('Damage Left')
        #self.ax1.set_xlabel('Time (seconds)')
        self.ax1.set_ylabel('Damage')
        self.ax1.legend()

        # Configure second graph
        self.line2, = self.ax2.plot([], [], color='b', lw=2, label='Damage Right')
        self.ax2.set_xlim(0, 10)
        self.ax2.set_ylim(-4000, 4000)
        self.ax2.set_title('Damage Right')
        #self.ax2.set_xlabel('Time (seconds)')
        self.ax2.set_ylabel('Damage')
        self.ax2.legend()

        # Configure third graph
        self.line3, = self.ax3.plot([], [], color='r', lw=2, label='Stimuli')
        self.ax3.set_xlim(0, 100)
        self.ax3.set_ylim(0, 300)
        self.ax3.set_title('Stimuli')
        #self.ax3.set_xlabel('Time (seconds)')
        self.ax3.set_ylabel('Stimuli')
        self.ax3.legend()

        # Data storage
        self.x_data, self.y_data1, self.y_data2, self.y_data3 = [], [], [], []

        plt.ion()  # Enable interactive mode

    def update_graph(self, time_elapsed, damage_left, damage_right, stimuli):
        # Append data for both graphs
        self.x_data.append(time_elapsed)
        self.y_data1.append(damage_left)
        self.y_data2.append(damage_right)
        self.y_data3.append(stimuli)

        # Update first graph
        self.line1.set_data(self.x_data, self.y_data1)
        self.ax1.set_xlim(max(0, time_elapsed - 100), time_elapsed + 10)

        # Update second graph
        self.line2.set_data(self.x_data, self.y_data2)
        self.ax2.set_xlim(max(0, time_elapsed - 100), time_elapsed + 10)

        self.line3.set_data(self.x_data, self.y_data3)
        self.ax3.set_xlim(max(0, time_elapsed - 100), time_elapsed + 10)


        # Redraw canvas
        self.fig.canvas.draw()
        plt.pause(0.5)

    # Animation update function

    def simulate(self):
        # Simulation loop
        running = True
        clock = pygame.time.Clock()

        # pA and duration
        stimulis = [(120, 20), (140, 20), (160, 20), (180, 20), (200, 20), (220, 20)]
        brain = amygdala.Brain(neurons_number=1680, SOM_RS_rate=0.27, SOM_LF_rate=0.18,
                               SOM_SP_rate=0.55, PCK_RS_rate=0.48, PCK_LF_rate=0.25,
                               PCK_SP_rate=0.27, SOM_SOM_connectivity=0.55, SOM_PCK_connectivity=0.15,
                               SOM_other_connectivity=0.30, PCK_PCK_connectivity=0.20,
                               PCK_SOM_connectivity=0.10, PCK_other_connectivity=0.70, SOM_rate=0.4, PCK_rate=0.5,
                               others_rate=0.1,
                               in_min_connection=0, in_max_connection=5, out_min_connection=0, out_max_connection=5)

        # lista contenente [ numero nodi totali, popolazione SOM, popolazione PCK, popolazione OTHER]
        network = brain.get_network_r()
        graph.plot_neurons_container(network[1].list + network[2].list + network[3].list)

        time_elapsed = 0
        stimulis_pos = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            damage_list = []
            stimuli = stimulis[stimulis_pos][0]

            # Clear the screen
            self.screen.fill(self.BLACK)

            brain.amygdala_l.update_states(stimuli, time_elapsed)
            brain.amygdala_r.update_states(stimuli, time_elapsed)

            damage_list.append((brain.get_damage_l(), brain.get_damage_r()))

            neurons_list = brain.amygdala_r.get_global_population()

            x = 0
            y = 0
            for neuron_element in neurons_list:
                # Get the neuron's frequency
                neuron = neuron_element.neuron
                frequency = neuron.get_frequency()

                # Initialize the color based on neuron type
                if type(neuron).__name__[-3:] == 'PCK':
                    color = self.RED
                elif type(neuron).__name__[-3:] == 'SOM':
                    color = self.BLUE
                else:
                    color = self.GREEN

                if type(neuron).__name__[-3:] == 'PCK' or type(neuron).__name__[-3:] == 'SOM':
                    # Calculate the brightness factor
                    frequency = frequency  # Get the neuron's frequency
                    max_frequency = 15  # Define a maximum frequency for scaling
                    brightness = min(1, frequency / max_frequency)  # Normalize to [0, 1]

                    # Scale the base color based on brightness
                    color = tuple(int(c * brightness) for c in color)

                pygame.draw.circle(self.screen, color, (x + 5, y + 5), 5)

                # Increment x and y
                x += 20
                if x > 800:
                    y += 10
                    x = 0

            time_elapsed += 1
            if stimulis[stimulis_pos][1] == time_elapsed:
                stimulis_pos += 1 % 5

            self.update_graph(time_elapsed, brain.get_damage_l(), brain.get_damage_r(), stimuli)

            # Update the display
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

        pygame.quit()
        plt.ioff()  # Disable interactive mode
        plt.show()
