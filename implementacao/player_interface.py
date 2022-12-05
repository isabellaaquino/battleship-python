from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from game_view import GameView
from tile import TileState


class PlayerInterface(DogPlayerInterface):
    def __init__(self):

        # Problem domain attributes
        self.gameview = GameView()
        self.selected_tiles = []
        self.started_selecting = False

        # Tk and graphic interface
        self.main_window = Tk() 
        self.fill_main_window()

        player_name = simpledialog.askstring(title="Player identification", prompt="What is your name?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

        self.main_window.mainloop()

    def fill_main_window(self):

        self.main_window.title("Batalha Naval")
        #self.main_window.iconbitmap("images/ship.ico")
        self.main_window.geometry("720x700")
        self.main_window.resizable(False, False)
        self.main_window["bg"]="#D9D9D9"

        self.keys_frame = Frame(self.main_window, padx=0, pady=0, bg="#D9D9D9")
        self.keys_frame.grid(row=1, column=0)

        self.player_frame = Frame(self.main_window, padx=0, pady=0, bg="#D9D9D9")
        self.player_frame.grid(row=1, column=0)

        self.enemy_frame = Frame(self.main_window, padx=240, pady=50, bg="#D9D9D9")
        self.enemy_frame.grid(row=2, column=0)

        self.title_frame = Frame(self.main_window, padx=0, pady=10, bg="#D9D9D9")
        self.title_frame.grid(row=0, column=0)

        self.confirm_frame = Frame(self.main_window, padx=100, pady=700, bg="#D9D9D9")
        self.confirm_frame.grid(row=3, column=0)

        
        # Images region

        # Tiles icons
        self.water_tile = PhotoImage(file="images/tile_water.png")
        self.water_miss_tile = PhotoImage(file="images/tile_water_miss.png")
        self.hit_ship_tile = PhotoImage(file="images/tile_ship_hit.png")
        self.ship_tile = PhotoImage(file="images/tile_ship.png")

        self.key_tiles_image = PhotoImage(file="images/key_tiles.png")
        self.key_ships_image = PhotoImage(file="images/key_shipsv2.png")

        #self.logo = PhotoImage(file="implementacao/images/logo.png") 

        self.key_tiles = Label(self.keys_frame, bd=0, image=self.key_tiles_image)
        self.key_tiles.grid(row=0, column=2)

        self.empty_label = Label(self.keys_frame, bd=0, padx=125)
        self.empty_label.grid(row=0, column=1)

        self.key_ships = Label(self.keys_frame, bd=0, image=self.key_ships_image)
        self.key_ships.grid(row=0, column=0)

        self.board_view=[]
        
        self.title_label = Label(self.title_frame, bg="#D9D9D9", text='BATALHA NAVAL', font=("Gulim", 30))
        self.title_label.grid(row=0, column=1)

        # Confirm button 

        #self.confirm_button = Button(self.confirm_frame, text='Confirmar', command=self.set_ships)

        # Menu region

        self.menubar = Menu(self.main_window)
        self.menubar.option_add("*tearOff", FALSE)
        self.main_window["menu"] = self.menubar

        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label="File")

        # Itens menu:
        self.menu_file.add_command(label="Iniciar jogo", command=self.start_match) 
        self.menu_file.add_command(label="Recomeçar jogo", command=self.restart_match)

        

        self.confirm_button = Label(self.confirm_frame, text='Confirmar navios', bg="#A9A9A9", font=("Gulim", 30))
        self.confirm_button.grid(row=0, column=0)
        self.confirm_button.bind(
                    "<Button-1>", lambda event: self.set_ships()
                )

        self.update_gui()


    def get_tile_image(self, state, remote: bool):
        if state == TileState.WATER:
            return self.water_tile
        elif state == TileState.WATER_MISS:
            return self.water_miss_tile
        elif state == TileState.SHIP:
            if remote: # The remote parameter is used to hide opponent ships from the player
                return self.water_tile
            return self.ship_tile
        elif state == TileState.HIT:
            return self.hit_ship_tile

    def start_match(self):
        match_status = self.gameview.get_match_status()
        if match_status == 1:
            answer = messagebox.askyesno("START", "Deseja iniciar uma nova partida?")
            if answer:
                start_status = self.dog_server_interface.start_match(2)
                code = start_status.get_code()
                message = start_status.get_message()
                if code == "0" or code == "1":
                    messagebox.showinfo(message=message)
                else:  #    (code=='2')
                    players = start_status.get_players()
                    local_player_id = start_status.get_local_id()
                    self.gameview.start_match(players, local_player_id)
                    messagebox.showinfo(message=start_status.get_message())
                    self.update_gui()

    def restart_match(self):
        match_status = self.gameview.get_match_status()
        if match_status == 2 or match_status == 6:
            self.gameview.reset_game()
            self.update_gui()

    def receive_start(self, start_status):
        self.restart_match()  #    use case reset game
        players = start_status.get_players()
        local_player_id = start_status.get_local_id()
        self.gameview.start_match(players, local_player_id)
        self.update_gui()

    def receive_withdrawal_notification(self):
        self.gameview.receive_withdrawal_notification()
        self.update_gui()

    def reset_selected_tiles(self):
        self.selected_tiles = []
        self.update_gui()

    def set_selected_tile(self, x, y):
        coords = [x,y]
        if coords not in self.selected_tiles:
            self.selected_tiles.append(coords)
        else:
            self.selected_tiles.remove(coords)

    def select_tile(self, event, board_id, line, column):
        """
        USE CASE SELECT TILE
        """
        
        if not self.gameview.is_local_player_turn():
            messagebox.showinfo(message=f'Não é a sua vez.')
            return
        
        match_status = self.gameview.get_match_status()

        """	
        Gameview matchStatus

        1 - no match (initial state)
        2 - finished match (game with winner)
        3 - your turn, match in progress AND is setting ships
        4 - your turn, match in progress AND is select tile
        5 - NOT your turn, match in progress - waiting ships to be set
        6 - NOT your turn, match in progress - waiting select tile move
        7 - match abandoned by opponent
        """

        if match_status == 3:
            if not self.gameview.is_local_board_id(board_id):
                messagebox.showinfo(message=f'Você clicou no tabuleiro errado. Para colocar navios, selecione-os no tabuleiro abaixo.')
                return
            self.set_selected_tile(line, column)
            self.started_selecting = True
            
        elif match_status == 4:
            if not self.gameview.is_remote_board_id(board_id):
                messagebox.showinfo(message=f'Você clicou no tabuleiro errado. Para realizar um tiro, selecione o tabuleiro do seu oponente (superior).')
                return
            remote_board = self.gameview.get_remote_board()
            tile = remote_board.get_tile(line, column)
            if tile.is_selectable():
                tile.update_state()

                is_winner = self.gameview.evaluate_end_of_match()

                if not is_winner:
                    self.gameview.remote_player.toggle_turn()
                    self.gameview.set_match_status(6) # Waiting for remote select tile move
                    status = 'next'
                else:
                    self.gameview.set_match_status(2)
                    self.gameview.local_player.toggle_turn() # removes turn from current player
                    status = 'finished'
            else:
                self.gameview.set_match_status(2) # There is a winner
                return

            self.dog_server_interface.send_move({'coord_x': line, 'coord_y': column, 'is_winner': is_winner, 'match_status': status})

        self.update_gui()

    def set_ships(self):
        """
        USE CASE SET SHIPS
        """
        game_view = self.gameview

        if not game_view.is_tiles_sum_valid(self.selected_tiles):
            messagebox.showinfo('Jogada Inválida', message='O número de tiles selecionados é inválido. Por favor tente novamente.')
            self.reset_selected_tiles()
            return
            

        if game_view.are_there_ships_close(self.selected_tiles):
            messagebox.showinfo('Jogada Inválida', message='Existem navios adjacentes ou ladrilhos solitários. Por favor tente novamente.')
            self.reset_selected_tiles()
            return

        all_ships_placed, ship_tiles = game_view.are_all_ships_placed(self.selected_tiles)

        if all_ships_placed:
            game_view.get_local_board().create_ships(ship_tiles)
            self.started_selecting = False

            if game_view.get_remote_player().get_ships() == []: # remote player haven't set their ships yet
                self.gameview.set_match_status(5) # Wait for remote select tile move
                self.update_gui()

            else:
                self.gameview.set_match_status(6) # Wait for remote select tile move

            self.gameview.local_player.toggle_turn()
            self.gameview.remote_player.toggle_turn()

            self.reset_selected_tiles()

            self.dog_server_interface.send_move({'ships': ship_tiles, 'match_status': 'next'})
            return

        else:
            messagebox.showinfo('Jogada Inválida', message='Você não seleciou todos os tipos de navios necessários.'
            'Por favor tente novamente. Dica: Siga a legenda de navios requeridos.')
            self.reset_selected_tiles()
            self.update_gui()
            return
        

    def receive_move(self, move_to_send: dict):
        """	
        Gameview matchStatus

        1 - no match (initial state)
        2 - finished match (game with winner)
        3 - your turn, match in progress AND is setting ships
        4 - your turn, match in progress AND is select tile
        5 - NOT your turn, match in progress - waiting ships to be set
        6 - NOT your turn, match in progress - waiting select tile move
        7 - match abandoned by opponent
        """
        game_view = self.gameview
        match_status = game_view.get_match_status()

        if match_status == 5:
            remote_board = game_view.get_remote_board()
            remote_board.create_ships(move_to_send['ships'])
            if game_view.get_local_player().get_ships() == []:
                game_view.set_match_status(3) # Local player turn to set ships
            else:
                game_view.set_match_status(4)

        elif match_status == 6:
            x, y = move_to_send['coord_x'], move_to_send['coord_y']
            local_board = game_view.get_local_board()
            tile = local_board.get_tile(x, y)
            tile.update_state()

            if move_to_send['is_winner']:
                remote_player = game_view.get_remote_player()
                remote_player.set_as_winner()
                game_view.set_match_status(2)
            else:
                game_view.set_match_status(4) # Local player turn to select tiles

        game_view.get_local_player().toggle_turn()
        game_view.get_remote_player().toggle_turn()

        self.update_gui()

    def update_gui(self):
        self.update_menu_status()
        # Resets both boards
        self.board_view = []

        # Update tiles
        remote_board_matrix = self.gameview.get_remote_board().get_matrix()
        for y in range(8):
            remote_board = [] 
            for x in range(8):
                remote_tile = remote_board_matrix[x][y]
                player_tile = Label(self.player_frame, bd = 0, image=self.get_tile_image(remote_tile.get_state(), remote=True))
                player_tile.grid(row=x, column=y)
                player_tile.bind(
                    "<Button-1>", lambda event, a_line=x, a_column=y: self.select_tile(event, 0, a_line, a_column)
                )
                remote_board.append(player_tile)
            self.board_view.append(remote_board)

        local_board_matrix = self.gameview.get_local_board().get_matrix()
        # Second board
        for y in range(8):
            local_board = [] 
            for x in range(8):
                tile = [x,y]
                if tile in self.selected_tiles:
                    enemy_tile = Label(self.enemy_frame, bd = 0, image=self.ship_tile) # Tile being selected on ship selection
                else:
                    local_tile = local_board_matrix[x][y]
                    enemy_tile = Label(self.enemy_frame, bd = 0, image=self.get_tile_image(local_tile.get_state(), remote=False))
                enemy_tile.grid(row=x, column=y)
                enemy_tile.bind(
                    "<Button-1>", lambda event, a_line=x, a_column=y: self.select_tile(event, 1, a_line, a_column)
                )
                local_board.append(enemy_tile)
            self.board_view.append(local_board)

        message = self.gameview.get_status()
        if message and not self.started_selecting:
            messagebox.showinfo(message=message)

    def update_menu_status(self):
        match_status = self.gameview.get_match_status()
        if match_status == 2 or match_status == 6:
            self.menu_file.entryconfigure("Recomeçar jogo", state="normal")
        else:
            self.menu_file.entryconfigure("Recomeçar jogo", state="disabled")
        if match_status == 1:
            self.menu_file.entryconfigure("Iniciar jogo", state="normal")
        else:
            self.menu_file.entryconfigure("Iniciar jogo", state="disabled")
        

