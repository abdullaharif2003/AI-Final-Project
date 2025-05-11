import os
from numpy import hstack, ndindex 
import numpy as np
from grid import Grid 
import random
import copy

class Solver:
    EXPECTIMAX_DEPTH = 1

    def __init__(self, size):
        self.size = size

        self.env = Grid(size, initialize_pygame_display=True) 

    def no_moves(self):
        return not self.env._can_any_move_be_made(self.env.grid)


    def next_move_predictor(self):
        """
        Determines the best move using Expectimax.
        """
        directions = ['w', 's', 'a', 'd']
        best_direction = None
        max_expected_score = -float('inf')

        current_game_grid_array = copy.deepcopy(self.env.grid)

        for direction in directions:

            sim_env_after_first_move = Grid(self.size, initialize_pygame_display=False)
            sim_env_after_first_move.grid = copy.deepcopy(current_game_grid_array)
            
            original_board_state_for_move = copy.deepcopy(sim_env_after_first_move.grid)

            moved = False
            if direction == 'w':
                moved = sim_env_after_first_move.move_up(sim_env_after_first_move.grid)
            elif direction == 's':
                moved = sim_env_after_first_move.move_down(sim_env_after_first_move.grid)
            elif direction == 'a':
                moved = sim_env_after_first_move.move_left(sim_env_after_first_move.grid)
            elif direction == 'd':
                moved = sim_env_after_first_move.move_right(sim_env_after_first_move.grid)

            current_move_eval_score = 0
            grid_changed = not np.array_equal(sim_env_after_first_move.grid, original_board_state_for_move)

            if not grid_changed: 
                current_move_eval_score = -1e9 
            else:
                current_move_eval_score = self.expectimax(
                    sim_env_after_first_move.grid, 
                    self.EXPECTIMAX_DEPTH, 
                    is_player_node=False 
                )
            
            if current_move_eval_score > max_expected_score:
                max_expected_score = current_move_eval_score
                best_direction = direction
        
        if best_direction is None: 
            simple_scores = {}
            for d_fallback in directions:
                grid_c = copy.deepcopy(current_game_grid_array)
                
                sim_env_f = Grid(self.size, initialize_pygame_display=False); sim_env_f.grid = grid_c
                
                original_fallback_grid = copy.deepcopy(sim_env_f.grid)
                moved_f = False
                if d_fallback == 'w': moved_f = sim_env_f.move_up(sim_env_f.grid)
                elif d_fallback == 's': moved_f = sim_env_f.move_down(sim_env_f.grid)
                elif d_fallback == 'a': moved_f = sim_env_f.move_left(sim_env_f.grid)
                elif d_fallback == 'd': moved_f = sim_env_f.move_right(sim_env_f.grid)
                
                grid_changed_fallback = not np.array_equal(sim_env_f.grid, original_fallback_grid)

                if grid_changed_fallback:
                    simple_scores[d_fallback] = self.get_score(np.array(sim_env_f.grid))
                else: 
                    simple_scores[d_fallback] = -float('inf') 

           
            valid_simple_scores = {k:v for k,v in simple_scores.items() if v > -float('inf')}
            if valid_simple_scores:
                best_direction = max(valid_simple_scores.items(), key=lambda x: x[1])[0]
                max_expected_score = valid_simple_scores[best_direction]
            else: 
                best_direction = random.choice(directions) 
                max_expected_score = self.get_score(np.array(current_game_grid_array))


        return best_direction, max_expected_score

    def expectimax(self, grid_state, depth, is_player_node):
        if depth == 0: 
            return self.get_score(np.array(grid_state))

        if is_player_node: 
            best_score = -float('inf')
            possible_move_made = False 
            for direction in ['w', 's', 'a', 'd']:
                
                sim_env_player = Grid(self.size, initialize_pygame_display=False)
                sim_env_player.grid = [row[:] for row in grid_state] 
                
                original_sim_grid = copy.deepcopy(sim_env_player.grid)

                moved_in_sim = False
                if direction == 'w': moved_in_sim = sim_env_player.move_up(sim_env_player.grid)
                elif direction == 's': moved_in_sim = sim_env_player.move_down(sim_env_player.grid)
                elif direction == 'a': moved_in_sim = sim_env_player.move_left(sim_env_player.grid)
                elif direction == 'd': moved_in_sim = sim_env_player.move_right(sim_env_player.grid)
                
                grid_changed_in_sim = not np.array_equal(sim_env_player.grid, original_sim_grid)

                current_path_score = 0
                if not grid_changed_in_sim: 
                    current_path_score = self.get_score(np.array(original_sim_grid)) 
                else:
                    possible_move_made = True
                    current_path_score = self.expectimax(sim_env_player.grid, depth, is_player_node=False)
                
                best_score = max(best_score, current_path_score)
            
           
            if not possible_move_made:
                 return self.get_score(np.array(grid_state))
            return best_score

        else: 
            empty_cells = self.get_empty_cells(grid_state)
            if not empty_cells:
                
                return self.expectimax(grid_state, depth - 1, is_player_node=True)

            accumulated_weighted_score = 0
           
            
            num_empty = len(empty_cells)
            if num_empty == 0: 
                 return self.get_score(np.array(grid_state)) 

            for r, c in empty_cells:
               
                grid_with_2 = [row[:] for row in grid_state]
                grid_with_2[r][c] = 2
                score_if_2_in_this_cell = self.expectimax(grid_with_2, depth - 1, is_player_node=True)
                
                
                grid_with_4 = [row[:] for row in grid_state]
                grid_with_4[r][c] = 4
                score_if_4_in_this_cell = self.expectimax(grid_with_4, depth - 1, is_player_node=True)
                
               
                expected_score_for_this_cell = (0.9 * score_if_2_in_this_cell) + \
                                               (0.1 * score_if_4_in_this_cell)
                
                accumulated_weighted_score += expected_score_for_this_cell 
            return accumulated_weighted_score / num_empty


    def get_empty_cells(self, grid): 
        cells = []
        for r_idx, row in enumerate(grid):
            for c_idx, val in enumerate(row):
                if val == 0:
                    cells.append((r_idx, c_idx))
        return cells

    def score_adjacent_tiles(self, grid): 
        return (self.score_count_neighbor(grid) + self.score_mean_neighbor(grid)) / 2

    def score_snake(self, grid, base_value=0.25): 
        size = len(grid)
        rewardArray = np.array([base_value ** i for i in range(size ** 2)])
        current_max_score = 0 
        temp_grid_np = np.array(grid) 
        
        orientations = [temp_grid_np, np.transpose(temp_grid_np)] 
        
        for current_orientation_grid in orientations:
            for i in range(2): 
                flat_snake_array_list = []
                for row_idx in range(size):
                    row_data = current_orientation_grid[row_idx]
                    if row_idx % 2 == (i % 2): 
                        flat_snake_array_list.extend(row_data)
                    else:
                        flat_snake_array_list.extend(row_data[::-1]) 
                
                gridArray_snake = np.array(flat_snake_array_list)
                
                current_max_score = max(current_max_score, np.sum(rewardArray * gridArray_snake))
                
        return current_max_score


    def score_mean_neighbor(self, newgrid): 
        horizontal_sum, count_horizontal = self.check_adjacent(newgrid)
        vertical_sum, count_vertical = self.check_adjacent(newgrid.T)
        if count_horizontal == 0 and count_vertical == 0: 
            return 0
        return (horizontal_sum + vertical_sum) / (count_horizontal + count_vertical + 1e-6)

    def check_adjacent(self, grid): 
        count = 0
        total_sum = 0
        for row_idx in range(grid.shape[0]):
            previous = -1
            for col_idx in range(grid.shape[1]):
                tile = grid[row_idx, col_idx]
                if tile != 0 and previous == tile: 
                    total_sum += tile 
                    count += 1
                previous = tile
        return total_sum, count

    def score_count_neighbor(self, grid): 
        _, horizontal_count = self.check_adjacent(grid)
        _, vertical_count = self.check_adjacent(grid.T)
        return horizontal_count + vertical_count

    def calculate_empty_tiles(self, grid): 
        empty_tiles = np.count_nonzero(np.array(grid) == 0) 
        return empty_tiles

    def get_score(self, grid): 
        current_grid_np = np.array(grid)

        adjacent_tiles_score = self.score_adjacent_tiles(current_grid_np)
        snake_score = self.score_snake(current_grid_np) 
        empty_tiles = self.calculate_empty_tiles(current_grid_np)
        max_tile_value = np.max(current_grid_np) if current_grid_np.size > 0 else 0
        
       
        w_adj = 0.1
        w_snake = 2.0
        w_empty = 2.5
        w_max_tile = 1.5 

        total_score = (w_adj * adjacent_tiles_score + 
                       w_snake * snake_score + 
                       w_empty * empty_tiles +
                       w_max_tile * np.log2(max_tile_value + 1) 
                      )
        
        if max_tile_value >= 2048: 
            total_score += 10000 

        mono_score = 0
        for i in range(self.size): 
            row_diffs = np.diff(current_grid_np[i,:])
            if np.all(row_diffs <= 0) or np.all(row_diffs >= 0): 
                mono_score += np.sum(current_grid_np[i,:]) * 0.5 
        for j in range(self.size): # Cols
            col_diffs = np.diff(current_grid_np[:,j])
            if np.all(col_diffs <= 0) or np.all(col_diffs >= 0):
                mono_score += np.sum(current_grid_np[:,j]) * 0.5
        total_score += 0.5 * mono_score

        return total_score

    def run(self):
        self.env.flag = 1 
        self.env.reset() 

        while True:
            if self.initialize_pygame_display: 
                os.system("cls" if os.name == "nt" else "clear")
            
            print("\nTOTAL SCORE:", self.env.score, "\n")
            
            if self.initialize_pygame_display:
                 self.env.render() 
            else: 
                 import time
                 time.sleep(0.05)


            if self.no_moves(): 
                if self.initialize_pygame_display: self.env.render() 
                print(np.array(self.env.grid))
                print("\n\nX---X---X  GAME OVER  X---X---X\n\n")
                input("Press Enter to exit...")
                break
            
            best_move = ''
            best_score = -float('inf')

            
            best_move, best_score = self.next_move_predictor()
            print(f"AI chose: {best_move} (Predicted Score: {best_score:.2f})")
            
            if not best_move : 
                print("CRITICAL: No best_move determined by predictor, even fallback failed. Taking random action.")
                best_move = random.choice(['w','a','s','d']) # Last resort

            moved_successfully = False
            if best_move == "w": moved_successfully = self.env.move_up()
            elif best_move == "s": moved_successfully = self.env.move_down()
            elif best_move == "a": moved_successfully = self.env.move_left()
            elif best_move == "d": moved_successfully = self.env.move_right()
            
            if moved_successfully:
                self.env.generate_new_cell()
            else:
                print(f"Warning: Chosen move '{best_move}' did not change the board state.")
                
                if self.no_moves(): 
                    if self.initialize_pygame_display: self.env.render()
                    print(np.array(self.env.grid))
                    print("\n\nX---X---X  GAME OVER (move did nothing)  X---X---X\n\n")
                    input("Press Enter to exit...")
                    break


if __name__ == "__main__":
    size = 4
    
    solver = Solver(size)
    
    solver.initialize_pygame_display = solver.env.initialize_pygame_display
    
    solver.run()