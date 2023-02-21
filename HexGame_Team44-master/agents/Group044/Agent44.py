import socket
import random
from time import sleep
import copy
import math


class NaiveAgent():
    """This class describes the default Hex agent. It will randomly send a
    valid move at each turn, and it will choose to swap with a 50% chance.
    """

    HOST = "127.0.0.1"
    PORT = 1234

    def __init__(self, board_size=11):
        self.s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        self.s.connect((self.HOST, self.PORT))

        self.board_size = board_size
        self.board = []
        self.colour = ""
        self.count_of_turn = 0
        self.moves_depth = 2
        self.visited = []
        self.count_of_eval = 0
        self.currWinner = False
        self.bestMove = tuple
        self.evaluted_states = dict()
        self.displace_x = [-1, -1, 0, 1, 1, 0]
        self.displace_y = [0, 1, 1, 0, -1, -1]
        self.emergency_move_found = False
        self.win_found = False


    def run(self):
        """Reads data until it receives an END message or the socket closes."""

        while True:
            data = self.s.recv(1024)
            if not data:
                break
            # print(f"{self.colour} {data.decode('utf-8')}", end="")
            if (self.interpret_data(data)):
                break

        # print(f"Naive agent {self.colour} terminated")

    def interpret_data(self, data):
        """Checks the type of message and responds accordingly. Returns True
        if the game ended, False otherwise.
        """

        messages = data.decode("utf-8").strip().split("\n")
        messages = [x.split(";") for x in messages]
        # print(messages)
        for s in messages:
            if s[0] == "START":
                self.board_size = int(s[1])
                self.colour = s[2]
                self.board = [
                    [0]*self.board_size for i in range(self.board_size)]

                if self.colour == "R":
                    self.make_move()

            elif s[0] == "END":
                return True

            elif s[0] == "CHANGE":
                if s[3] == "END":
                    return True

                elif s[1] == "SWAP":
                    self.colour = self.opp_colour()
                    if s[3] == self.colour:
                        self.make_move()

                elif s[3] == self.colour:
                    action = [int(x) for x in s[1].split(",")]
                    self.board[action[0]][action[1]] = self.opp_colour()

                    self.make_move()

        return False


    def get_choices(self, currBoard):
        choices = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if currBoard[i][j] == 0:
                    choices.append((i, j))

        return choices

    def get_colored(self, currBoard, color):
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if currBoard[i][j] == self.opp_colour():
                    S= (i, j)

        return S
    # Clears the list so we can check connectivity for the next hex.
    def clear_visited(self):
        self.visited = []

    

    def check_Swap(self, board):
        move = self.get_colored(board, self.colour)

        swap_border = math.sqrt(self.board_size)
        if ( (move[0]+1) > swap_border and (move[1]+1) < swap_border ):
            return True

        elif ( (move[1]+1) > swap_border and (move[0]+1) < swap_border ):
            return True
        else:
            return False


    def is_empty(self, coordinates, board):

        # print("is empty?: ", self.board[coordinates[0]][coordinates[1]] == 0)

        return board[coordinates[0]][coordinates[1]] == "0"

    def is_color(self, coordinates, color, board):

        # print("is color?: ", self.board[coordinates[0]][coordinates[1]] == color)

        return board[coordinates[0]][coordinates[1]] == color



    def update_board(self, updateboard, x,y, colour):
        updateboard[x][y] = colour
        return updateboard   


    def get_neighbors(self, coordinates):

        (x,y) = coordinates
        neighbors = []
        if x-1 >= 0: neighbors.append((x-1,y))
        if x+1 < self.board_size: neighbors.append((x+1,y))
        if x-1 >= 0 and y+1 <= self.board_size-1: neighbors.append((x-1,y+1))
        if x+1 < self.board_size and y-1 >= 0: neighbors.append((x+1,y-1))
        if y+1 < self.board_size: neighbors.append((x,y+1))
        if y-1 >= 0: neighbors.append((x,y-1))

        return neighbors

    def make_move(self):
        """Makes a random move from the available pool of choices. If it can
        swap, chooses to do so 50% of the time.
        """
        self.Played= False
        if self.count_of_turn > (self.board_size-2):
            print("!!!!!!")
            self.look_for_confirmed_win(self.board)

        if self.colour == "B" and self.count_of_turn == 0 and self.check_Swap(self.board):
                    self.s.sendall(bytes("SWAP\n", "utf-8"))

  

        else:
            if not self.Played:
                print("HI")
                choices = self.get_choices(self.board)
                boardCopy = copy.deepcopy(self.board)
                self.Minimax(boardCopy, self.moves_depth, float('-inf'), float('inf'), True )
                pos = self.bestMove
                print(pos)
                if pos not in choices:
                    pos = random.choice(choices)
                self.s.sendall(bytes(f"{pos[0]},{pos[1]}\n", "utf-8"))
                self.board[pos[0]][pos[1]] = self.colour
        self.count_of_turn += 1

    def dijkstra_eval(self, color, board):

        self.count_of_eval += 1

        heuristic = self.score_of_dijkstra(self.get_opposite_color(color), board) - self.score_of_dijkstra(color, board)
        return heuristic

    def update_dijkstra(self, color, distances, vistied, board):
 
        is_updating = True
        while is_updating: 
            is_updating = False
            for i, row in enumerate(distances): 
                for j, location in enumerate(row):       
                    if not vistied[i][j]: 
                        neighbors = self.get_neighbors((i,j))  
                        for neighbor in neighbors:
                            neighbor = tuple(neighbor)
                            cost_of_path = 100  
                            if board[neighbor[0]][neighbor[1]] == 0:
                                cost_of_path = 1
                            elif board[neighbor[0]][neighbor[1]] == color:
                                cost_of_path = 0
                            


                            if distances[neighbor[0]][neighbor[1]] > distances[i][j] + cost_of_path:

                                distances[neighbor[0]][neighbor[1]] = distances[i][j] + cost_of_path 
                                vistied[neighbor[0]][neighbor[1]] = False 
                                is_updating = True 
        return distances

    def score_of_dijkstra(self, color, board):

        distances = [ [100]*self.board_size for i in range(self.board_size)]
        vistied = [ [True]*self.board_size for i in range(self.board_size)]

        liner = (1, 0) if color == "B" else (0, 1)


        for i in range(self.board_size):
            coords = tuple([i * j for j in liner])


            vistied[coords[0]][coords[1]] = False
            if self.is_color(coords, color, board):
                distances[coords[0]][coords[1]] = 0
            elif self.is_empty(coords, board):
                distances[coords[0]][coords[1]] = 1
                distances[coords[0]][coords[1]] = 100
 
        distances = self.update_dijkstra(color, distances, vistied, board)

        results = [distances[liner[0] * i - 1 + liner[0]][liner[1]*i - 1 + liner[1]]
                   for i in range(self.board_size)]
 
        best_result = min(results)
 
        return best_result 

    def Minimax(self, board, moves_depth, alpha, beta, maximising: bool):

        alpha = alpha
        beta = beta
        bestPos = []

        self.winner(board)

        if moves_depth == 0 or self.currWinner: 
            curr_colour = self.opp_colour()
            if maximising:
                curr_colour = self.colour

            #state = sum(board, [])

            stringState = ''.join(str(item) for innerlist in board for item in innerlist)
            #m print(stringState)
            if stringState in self.evaluted_states:
                return self.evaluted_states[stringState]

            x = self.dijkstra_eval(curr_colour, board)

            self.evaluted_states[stringState] = x    
            
            return x

        if maximising:

           
            maxEval = float('-inf')
            positions = self.get_choices(board)


            for position in positions :
                vistiedBoard = copy.deepcopy(board) 
                vistiedBoard[position[0]][position[1]] = self.colour
                _eval = self.Minimax(vistiedBoard, moves_depth-1 , alpha , beta, False)
                if _eval > maxEval:
                    bestPos = position
                maxEval = max(maxEval, _eval)
                alpha = max(alpha, _eval)
                if maxEval >= beta:
                    break
            
            self.bestMove = bestPos
            return maxEval

        else:

            minEval = float('inf')
            positions = self.get_choices(board)
            for position in positions : 
                vistiedBoard = copy.deepcopy(board) 
                vistiedBoard[position[0]][position[1]] = self.opp_colour()
                _eval = self.Minimax(vistiedBoard, moves_depth-1 , alpha , beta, True)
                if _eval < minEval:
                    bestPos = position
                minEval = min(minEval, _eval)
                beta = min(beta, _eval)
                if minEval <= alpha:
                        break
            self.bestMove = bestPos
            return minEval


    def look_for_confirmed_win(self, board):
        print(self.colour)

        self.clear_visited()
        self.zero_visited= False
        if self.colour== 'R' :
            for i in range(self.board_size):

                self.zero_visited= False
                self.clear_visited()
                if self.emergency_move_found:
                    break
                elif board[0][i] == 'R':
                    self.check_connectivity2(board, 0, i)


            if  not self.emergency_move_found:
                for i in range(self.board_size):
                    self.clear_visited()
                    if board[0][i] == 0:
                        board[0][i] = 'R'
                        self.winner(board)
                        board[0][i] = 0
                        if self.currWinner:
                            print("2EMERGENY MOVE!!!!!!   Playing : " , (0,i)  )
                            if not self.Played:
                            
                                self.s.sendall(bytes(f"{0},{i}\n", "utf-8"))
                                self.board[0][i] = self.colour
                                self.Played= True
                                break

  

        else:

            for i in range(self.board_size):
                self.zero_visited= False
                self.clear_visited()
                if self.emergency_move_found:
                    break
                elif board[i][0] == 'B':
                    self.check_connectivity2(board, i, 0)



            if  not self.emergency_move_found:
                for i in range(self.board_size):
                    self.clear_visited()
                    if board[i][0] == 0:
                        board[i][0] = 'B'
                        self.winner(board)
                        board[i][0] = 0
                        if self.currWinner:
                            print("2EMERGENY MOVE!!!!!!   Playing : " , (i,0)  )
                            if not self.Played:
                            
                                self.s.sendall(bytes(f"{i},{0}\n", "utf-8"))
                                self.board[i][0] = self.colour
                                self.Played= True
                                break


    def winner(self, board):
    
        self.clear_visited()
        self.win_found = False
        for i in range(self.board_size):
            if self.win_found == False:
                self.clear_visited()
                if board[0][i] == 'R':
                    self.check_connectivity(board, 0, i)
            else:
                return


        for i in range(self.board_size):
            if self.win_found == False:
                self.clear_visited()
                if board[i][0] == 'B':
                    self.check_connectivity(board, i, 0)

            else:
                return



    #def mostConnected(self, board, color):
        # If your'e red and it's the first turn in the game.
       # if len(self.get_choices(board))== self.board_size**2 :
          #  return random.randint(1,10)

       # else:
           # currPositions = self.get_colored(board, color)
           # for position in currPositions:



    def check_connectivity(self, board, x, y):
        self.visited.append((x,y))




        if (x == self.board_size-1) and board[x][y]== 'R':


            self.currWinner = True

        if (y == self.board_size-1) and board[x][y]== 'B':

            self.currWinner = True

        for i in range(5):
            xd = x + self.displace_x[i]
            yd = y + self.displace_y[i]
            if xd >= 0 and yd >= 0 and xd < self.board_size and yd < self.board_size :
                if (board[x][y] == board[xd][yd]) and (xd,yd) not in self.visited:
                    self.check_connectivity(board, xd, yd)

                

    def check_connectivity2(self, board, x, y):
        path_exist = False
        self.visited.append((x,y))
        neighbors = []
        for i in range(5):
            xd = x + self.displace_x[i]
            yd = y + self.displace_y[i]
            if xd >= 0 and yd >= 0 and xd < self.board_size and yd < self.board_size :
                neighbors.append((xd, yd))


        for n in neighbors:
            if board[n[0]][n[1]] == self.colour:
                if(n[0],n[1]) not in self.visited:

                    path_exist= True
           # if board[n[0]][n[1]] == 0 and (self.colour=='R') and (n[0] == self.board_size-1)  :


        print((x,y) , path_exist)

        if (x == self.board_size-1) and board[x][y]== 0 and self.colour=='R':

            print("ending1")

            self.win_found = True
        if (x == self.board_size-1) and board[x][y]== 'R':

            print("ending2")
            self.win_found = True
        

        elif (y == self.board_size-1) and board[x][y]== 0 and self.colour=='B':

            print("ending3")
            self.win_found = True

        elif (y == self.board_size-1) and board[x][y]== 'B':

            print("ending4")
            self.win_found = True
            

        elif board[x][y] == 0 :
            for i in range(5):
                xd = x + self.displace_x[i]
                yd = y + self.displace_y[i]
                if xd >= 0 and yd >= 0 and xd < self.board_size and yd < self.board_size :
                    if (self.colour == board[xd][yd]) and (xd,yd) not in self.visited:
                        self.check_connectivity2(board, xd, yd)

        elif path_exist:
                    
            for i in range(5):
                xd = x + self.displace_x[i]
                yd = y + self.displace_y[i]
                if xd >= 0 and yd >= 0 and xd < self.board_size and yd < self.board_size :
                    if (board[x][y] == board[xd][yd]) and (xd,yd) not in self.visited:
                        self.check_connectivity2(board, xd, yd)


        else:
            if not self.zero_visited:
                self.zero_visited = True
                for i in range(5):
                    xd = x + self.displace_x[i]
                    yd = y + self.displace_y[i]
                    if xd >= 0 and yd >= 0 and xd < self.board_size and yd < self.board_size :
                        if (0 == board[xd][yd]) and ( (xd,yd) not in self.visited ) and (board[x][y]== self.colour) :
                            self.check_connectivity2(board, xd, yd)
                            if self.win_found == True :
                                self.emergency_move_found= True
                                print("EMERGENY MOVE!!!!!!   Playing : " , (xd,yd)  )
                                if not self.Played:
                                
                                    self.s.sendall(bytes(f"{xd},{yd}\n", "utf-8"))
                                    print("SENT!")
                                    self.board[xd][yd] = self.colour
                                    self.Played= True
                                break
                                
            else:
                pass                    




    def opp_colour(self):
        """Returns the char representation of the colour opposite to the
        current one.
        """
        if self.colour == "R":
            return "B"
        elif self.colour == "B":
            return "R"
        else:
            return "None"


    def get_opposite_color(self, colour):
        """Returns opp color.
        """
        if colour == "R":
            return "B"
        elif colour == "B":
            return "R"
        else:
            return "None"


if (__name__ == "__main__"):
    agent = NaiveAgent()
    agent.run()