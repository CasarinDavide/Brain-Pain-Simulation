import pygame
import random

#classe per gestire la finestra di dialogo, mostra in real time la simulazione
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
        self.BLUE = (0, 0, 255)
        # Colors
        # Initialize agents
        self.num_particles = 50
        self.particles = [{'x': random.randint(0, self.width),
                           'y': random.randint(0, self.height),
                           'vx': random.choice([-1, 1]),
                           'vy': random.choice([-1, 1])} for _ in range(self.num_particles)]

    def simulate(self):
        # Simulation loop
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen
            self.screen.fill(self.BLACK)

            # Update and draw particles
            for particle in self.particles:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']

                # Bounce off walls
                if particle['x'] <= 0 or particle['x'] >= self.width:
                    particle['vx'] *= -1
                if particle['y'] <= 0 or particle['y'] >= self.height:
                    particle['vy'] *= -1

                # Draw particle
                pygame.draw.circle(self.screen, self.BLUE, (particle['x'], particle['y']), 5)

            # Update the display
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

        pygame.quit()
