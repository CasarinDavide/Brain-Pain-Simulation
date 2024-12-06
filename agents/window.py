import pygame
import random

import amygdala as amygdala
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style



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

        # Colors
        # Initialize agents
        self.num_particles = 50

        # Initialize the figure and line object
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], color='g', lw=2)

        # Set axis limits
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 1)

        # Data storage
        self.x_data, self.y_data = [], []

    # Animation update function
    def animate(self,frame):
        x, y = frame
        self.x_data.append(x)
        self.y_data.append(y)

        self.line.set_data(self.x_data, self.y_data)

        if x > self.ax.get_xlim()[1]:
            self.ax.set_xlim(self.ax.get_xlim()[0] + 1, x + 1)

        return self.line,

    def simulate(self):
        # Simulation loop
        running = True
        clock = pygame.time.Clock()

        # pA and duration
        stimulis = [(120, 1200), (160, 23), (180, 123), (220, 100)]
        brain = amygdala.Brain(neurons_number=1680, SOM_RS_rate=0.27, SOM_LF_rate=0.18,
                               SOM_SP_rate=0.55, PCK_RS_rate=0.48, PCK_LF_rate=0.25,
                               PCK_SP_rate=0.27, SOM_SOM_connectivity=0.55, SOM_PCK_connectivity=0.15,
                               SOM_other_connectivity=0.30, PCK_PCK_connectivity=0.20,
                               PCK_SOM_connectivity=0.10, PCK_other_connectivity=0.70, SOM_rate=0.4, PCK_rate=0.4,
                               others_rate=0.2,
                               in_min_connection=0, in_max_connection=5, out_min_connection=0, out_max_connection=5)

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

            time_elapsed = +1
            if stimulis[stimulis_pos][1] == time_elapsed:
                time_elapsed = 0
                stimulis_pos += 1 % 5

                # Update the display
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

        # Create the animation
        anim = animation.FuncAnimation(self.fig, self.animate, frames=frames, interval=100, blit=True, cache_frame_data=False)

        plt.show()


        pygame.quit()
