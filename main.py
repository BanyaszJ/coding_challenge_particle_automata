import sys
import pygame
from pprint import pp

GAME_FPS = 60  # [fps]
CELL_SIZE = 10  # [px]
WIDTH, HEIGHT = 800, 600  # [px]
X_CELLS_NO, Y_CELLS_NO = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE  # [cells]


class Grid:
    """Class representing a grid for the simulation.
    The grid is initialized with a specified number of cells in the x and y directions.
    The grid is represented as a 2D list of zeros.

    Attributes:
        x_cells_no (int): Number of cells in the x direction.
        y_cells_no (int): Number of cells in the y direction.
        grid_format (tuple): Tuple representing the grid dimensions.
        grid (list): 2D list representing the grid, initialized with zeros.
    """
    def __init__(self, x_cells_no=X_CELLS_NO, y_cells_no=Y_CELLS_NO):
        self.grid = list()
        self.x_cells_no = x_cells_no
        self.y_cells_no = y_cells_no
        self.grid_format = (x_cells_no, y_cells_no)

    def init(self):
        self.grid = [[0 for _ in range(self.x_cells_no)] for _ in range(self.y_cells_no)]
        print(f"Grid initialized with {self.x_cells_no} x {self.y_cells_no} cells.")

    def print_raw_grid(self):
        """Print the grid to the console"""
        for row in self.grid:
            print("".join(str(cell) for cell in row))


    def get_cell_data(self, x, y):
        """Get the data of a specific cell in the grid

        Args:
            x (int): X coordinate in the grid
            y (int): Y coordinate in the grid

        Returns:
            dict: Dictionary containing cell attributes, or None if position is invalid
        """
        if not (0 <= x < self.x_cells_no and 0 <= y < self.y_cells_no):
            return None

        cell = self.grid[y][x]
        cell_data = cell.get_particle_data()
        # print(cell_data)
        return cell_data

    def push_particle(self, particle):
        """Push a particle to the grid at its current position"""
        if 0 <= particle.grid_x_pos < self.x_cells_no and 0 <= particle.grid_y_pos < self.y_cells_no:
            self.grid[particle.grid_y_pos][particle.grid_x_pos] = particle
        else:
            print("Particle position out of bounds!")


class Particle:
    def __init__(self, grid_x_pos, grid_y_pos, cell_size, color, type="sand"):
        """
        Initialize a particle at a specific grid position

        Args:
            grid_x_pos (int): X position in the grid
            grid_y_pos (int): Y position in the grid
            cell_size (int): Size of each grid cell in pixels
            color (tuple): RGB color of the particle
            speed (int): Speed of the particle
            type (str): Type of the particle
        """
        self.grid_x_pos = grid_x_pos
        self.grid_y_pos = grid_y_pos
        self.cell_size = cell_size
        self.color = color
        self.speed = 0
        self.type = "sand"  # will be inherited later

    def get_particle_data(self):
        """Get the data of the particle"""
        return {
            "grid_x_pos": (self.grid_x_pos),
            "grid_y_pos": (self.grid_y_pos),
            "type": self.type,
            "cell_size": self.cell_size,
            "color": self.color,
            "speed": self.speed
        }

class Visualizer:
    def __init__(self):
        pass

    def push(self, what=None, where=None):
        """Push the grid to the screen"""
        # iterate through the grid
        for row_idx, row in enumerate(what.grid):
            for cell_idx, cell in enumerate(row):
                if cell != 0:
                    particle_data = cell.get_particle_data()
                    print(particle_data)
                    pygame.draw.rect(
                        where,
                        particle_data["color"],
                        (particle_data["grid_x_pos"] * particle_data["cell_size"],
                         particle_data["grid_y_pos"] * particle_data["cell_size"],
                         particle_data["cell_size"],
                         particle_data["cell_size"])
                    )

class Controls:
    def __init__(self):
        self.lmb_down_state = False
        self.rmb_down_state = False
        self.mmb_down_state = False
        self.mouse_x = 0
        self.mouse_y = 0

    def get_control_state(self):
        """Get the current state of the controls"""
        return {
            "lmb_down_state": self.lmb_down_state,
            "rmb_down_state": self.rmb_down_state,
            "mmb_down_state": self.mmb_down_state,
            "mouse_x_pos": self.mouse_x,
            "mouse_y_pos": self.mouse_y,
        }

class MainGame:
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        pygame.display.set_caption("Material Simulation")

        self.fps = GAME_FPS
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.grid = Grid()
        self.grid.init()

        self.visualizer = Visualizer()

        # controller
        self.lmb_down_state = False
        self.mouse_lmb = 1

    def run(self):
        """Main loop of the game.
        :return: None
        """

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == self.mouse_lmb:
                        self.lmb_down_state = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == self.mouse_lmb:
                        self.lmb_down_state = False

                if self.lmb_down_state:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                    particle = Particle(grid_x, grid_y, CELL_SIZE, color=(255, 255, 0), type="sand")
                    self.grid.push_particle(particle)

            self.grid.print_raw_grid()
            self.visualizer.push(what=self.grid, where=self.screen)
            pygame.display.flip()

            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = MainGame()
    game.run()
