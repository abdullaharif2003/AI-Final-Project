import random
import copy
import pygame as pg
import numpy as np 
class Grid:
    def __init__(self, size, initialize_pygame_display=True): 
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.score = 0
        
        
        self.initialize_pygame_display = initialize_pygame_display

        if self.initialize_pygame_display:
            pg.init()
            pg.font.init() 
            try:
                self.myfont = pg.font.SysFont('Arial', 30)
            except Exception as e:
                print(f"Warning: Font 'Arial' not found, using default. Error: {e}")
                self.myfont = pg.font.Font(None, 30) 

            self.screen_width = 400
            self.screen_height = 400
            self.cell_size = self.screen_width // self.size
            self.padding = 10
            self.colors = {
                0: (205, 193, 180), 2: (238, 228, 218), 4: (237, 224, 200),
                8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
                64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97),
                512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46)
            }
            try:
                self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
                pg.display.set_caption("2048")
            except pg.error as e:
                print(f"Pygame display initialization error: {e}. Game will run without GUI.")
                self.initialize_pygame_display = False
                self.screen = None
        else:
            self.myfont = None
            self.screen = None
            self.colors = {} 

        if self.initialize_pygame_display and not any(any(row) for row in self.grid): # if grid is empty
            self.grid[random.randint(0, size - 1)][random.randint(0, size - 1)] = 2


    def render(self):
        if not self.initialize_pygame_display or not self.screen or not pg.display.get_init():
            return 

        self.screen.fill((187, 173, 160))
        for i in range(self.size):
            for j in range(self.size):
                value = self.grid[i][j]
                color = self.colors.get(value, (100, 105, 100))
                pg.draw.rect(self.screen, color, (j * self.cell_size + self.padding,
                                                 i * self.cell_size + self.padding,
                                                 self.cell_size - 2 * self.padding,
                                                 self.cell_size - 2 * self.padding))
                if value != 0 and self.myfont:
                    text_surface = self.myfont.render(str(value), True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(
                        j * self.cell_size + self.cell_size / 2,
                        i * self.cell_size + self.cell_size / 2
                    ))
                    self.screen.blit(text_surface, text_rect)
        pg.display.flip()
        self.handle_events()

    def handle_events(self):
        if not self.initialize_pygame_display or not pg.display.get_init():
            return
        try:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
        except pg.error: # Catch error if display was closed abruptly elsewhere
            pass


    def is_safe(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] == 0
    
    def _can_any_move_be_made(self, grid_state_to_check):
        """ Helper to check if any move changes the provided grid_state. Uses non-visual Grid."""
        for direction_code in range(4): # 0:up, 1:down, 2:left, 3:right
            temp_sim_grid = Grid(self.size, initialize_pygame_display=False)
            temp_sim_grid.grid = copy.deepcopy(grid_state_to_check) # Operate on a copy
            
            original_for_comparison = copy.deepcopy(temp_sim_grid.grid) # Save state before move
            
            moved_flag = False
            if direction_code == 0: moved_flag = temp_sim_grid.move_up(temp_sim_grid.grid)
            elif direction_code == 1: moved_flag = temp_sim_grid.move_down(temp_sim_grid.grid)
            elif direction_code == 2: moved_flag = temp_sim_grid.move_left(temp_sim_grid.grid)
            elif direction_code == 3: moved_flag = temp_sim_grid.move_right(temp_sim_grid.grid)

            if not np.array_equal(temp_sim_grid.grid, original_for_comparison):
                return True 
        return False 

    def is_full(self):
        return not self._can_any_move_be_made(self.grid)

    def reset(self):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.score = 0
        self.generate_new_cell()
        self.generate_new_cell()
        return copy.deepcopy(self.grid)

    def generate_new_cell(self):
        empty_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    empty_cells.append((r,c))
        if not empty_cells:
            return False 
        
        r, c = random.choice(empty_cells)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4
        return True
    

    def move_up(self, grid_param=None): 
        is_simulation = grid_param is not None
        current_grid = grid_param if is_simulation else self.grid
        original_score = self.score 
                                    

        moved = False
        for j in range(self.size):
            col = [current_grid[i][j] for i in range(self.size)]
            new_col_values = [0]*self.size
            write_idx = 0
            merged_score_this_col = 0

            temp_col_no_zeros = [val for val in col if val != 0]
            
            i = 0
            while i < len(temp_col_no_zeros):
                val = temp_col_no_zeros[i]
                if i + 1 < len(temp_col_no_zeros) and temp_col_no_zeros[i] == temp_col_no_zeros[i+1]:
                    new_val = val * 2
                    new_col_values[write_idx] = new_val
                    merged_score_this_col += new_val
                    i += 2 
                else:
                    new_col_values[write_idx] = val
                    i += 1
                write_idx += 1
            
            for r in range(self.size):
                if current_grid[r][j] != new_col_values[r]:
                    current_grid[r][j] = new_col_values[r]
                    moved = True
            
            if not is_simulation and merged_score_this_col > 0:
                 self.score += merged_score_this_col

        return moved
            
    def move_down(self, grid_param=None):
        is_simulation = grid_param is not None
        current_grid = grid_param if is_simulation else self.grid
        moved = False
        for j in range(self.size):
            col = [current_grid[i][j] for i in range(self.size -1, -1, -1)] 
            new_col_values = [0]*self.size
            write_idx = 0
            merged_score_this_col = 0
            temp_col_no_zeros = [val for val in col if val != 0]
            i = 0
            while i < len(temp_col_no_zeros):
                val = temp_col_no_zeros[i]
                if i + 1 < len(temp_col_no_zeros) and temp_col_no_zeros[i] == temp_col_no_zeros[i+1]:
                    new_val = val * 2
                    new_col_values[write_idx] = new_val
                    merged_score_this_col += new_val
                    i += 2
                else:
                    new_col_values[write_idx] = val
                    i += 1
                write_idx += 1
            for r in range(self.size):
                if current_grid[self.size - 1 - r][j] != new_col_values[r]:
                    current_grid[self.size - 1 - r][j] = new_col_values[r]
                    moved = True
            if not is_simulation and merged_score_this_col > 0:
                 self.score += merged_score_this_col
        return moved

    def move_left(self, grid_param=None):
        is_simulation = grid_param is not None
        current_grid = grid_param if is_simulation else self.grid
        moved = False
        for i in range(self.size):
            row = [current_grid[i][j] for j in range(self.size)]
            new_row_values = [0]*self.size
            write_idx = 0
            merged_score_this_row = 0
            temp_row_no_zeros = [val for val in row if val != 0]
            k = 0
            while k < len(temp_row_no_zeros):
                val = temp_row_no_zeros[k]
                if k + 1 < len(temp_row_no_zeros) and temp_row_no_zeros[k] == temp_row_no_zeros[k+1]:
                    new_val = val * 2
                    new_row_values[write_idx] = new_val
                    merged_score_this_row += new_val
                    k += 2
                else:
                    new_row_values[write_idx] = val
                    k += 1
                write_idx += 1
            for j in range(self.size):
                if current_grid[i][j] != new_row_values[j]:
                    current_grid[i][j] = new_row_values[j]
                    moved = True
            if not is_simulation and merged_score_this_row > 0:
                 self.score += merged_score_this_row
        return moved

    def move_right(self, grid_param=None):
        is_simulation = grid_param is not None
        current_grid = grid_param if is_simulation else self.grid
        moved = False
        for i in range(self.size):
            row = [current_grid[i][j] for j in range(self.size -1, -1, -1)] # Iterate from right
            new_row_values = [0]*self.size
            write_idx = 0
            merged_score_this_row = 0
            temp_row_no_zeros = [val for val in row if val != 0]
            k = 0
            while k < len(temp_row_no_zeros):
                val = temp_row_no_zeros[k]
                if k + 1 < len(temp_row_no_zeros) and temp_row_no_zeros[k] == temp_row_no_zeros[k+1]:
                    new_val = val * 2
                    new_row_values[write_idx] = new_val
                    merged_score_this_row += new_val
                    k += 2
                else:
                    new_row_values[write_idx] = val
                    k += 1
                write_idx += 1
            for j in range(self.size):
                if current_grid[i][self.size -1 - j] != new_row_values[j]:
                    current_grid[i][self.size -1 - j] = new_row_values[j]
                    moved = True
            if not is_simulation and merged_score_this_row > 0:
                 self.score += merged_score_this_row
        return moved

    def step(self, action):
        current_score = self.score
        moved = False
        if action == 'w': moved = self.move_up()
        elif action == 's': moved = self.move_down()
        elif action == 'a': moved = self.move_left()
        elif action == 'd': moved = self.move_right()
        else: raise ValueError("Invalid action")

        reward = self.score - current_score 
        
        if not moved: 
            if reward == 0 : 
                 reward = -0.1 
        else: 
            self.generate_new_cell()

        done = self.is_full() 
        next_state = copy.deepcopy(self.grid)
        return next_state, reward, done