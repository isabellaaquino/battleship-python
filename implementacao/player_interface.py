from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from game_view import GameView


class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        # Tk and graphic interface
        self.main_window = Tk() 
        self.fill_main_window()

        # Problem domain attributes
        self.gameview = GameView()
        self.selected_tiles = []

        player_name = simpledialog.askstring(title="Player identification", prompt="What is your name?")
        #self.dog_server_interface = DogActor()
        #message = self.dog_server_interface.initialize(player_name, self)
        #messagebox.showinfo(message=message)

        #match_status = self.gameview.get_match_status()
        #self.update_gui(match_status)

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

        
        # Images region
        self.water_tile = PhotoImage(file="images/tile_water.png")
        self.water_miss = PhotoImage(file="images/tile_water_miss.png")
        self.hit_ship_tile = PhotoImage(file="images/tile_ship_hit.png")



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
        
        # First board
        for y in range(8):
            remote_board = [] 
            for x in range(8):
                player_tile = Label(self.player_frame, bd = 0, image=self.water_tile)
                player_tile.grid(row=x, column=y)
                player_tile.bind(
                    "<Button-1>", lambda event, a_line=x, a_column=y: self.select_tile(event, 0, a_line, a_column)
                )
                remote_board.append(player_tile)
            self.board_view.append(remote_board)

        

        # Second board
        for y in range(8):
            local_board = [] 
            for x in range(8):
                enemy_tile = Label(self.enemy_frame, bd = 0, image=self.water_tile)
                enemy_tile.grid(row=x, column=y)
                enemy_tile.bind(
                    "<Button-1>", lambda event, a_line=x, a_column=y: self.select_tile(event, 1, a_line, a_column)
                )
                local_board.append(enemy_tile)
            self.board_view.append(local_board)
        
        

        # self.board_title = Label(self.player_frame, text="A B C D E F G H I J", font="arial 20")
        # self.board_title.grid(row=0, column=0)
        
        self.title_label = Label(self.title_frame, bg="#D9D9D9", text='BATALHA NAVAL', font=("Gulim", 30))
        self.title_label.grid(row=0, column=1)

        # Menu region

        self.menubar = Menu(self.main_window)
        self.menubar.option_add("*tearOff", FALSE)
        self.main_window["menu"] = self.menubar

        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label="File")

        # Itens menu:
        self.menu_file.add_command(label="Iniciar jogo", command=self.start_match) # TODO: add command
        self.menu_file.add_command(label="Recomeçar jogo", command=self.restart_match) # TODO: add command


    def get_label(self, board_id, x, y) -> Label:
        row = x
        if board_id == 1:
            row = x + 8
        column = y
        return self.board_view[row][column]

    def start_match(self):
        answer = messagebox.askyesno('START', 'Are you sure you want to start a match?')
        if(answer):
            start_status = self.dog_server_interface.start_match(2)
            message = start_status.get_message()
            messagebox.showinfo(message=message)

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)

    def restart_match(self):
        answer = messagebox.askyesno('START', 'Are you sure you want to restart the match?')
        if(answer):
            print('restart game')
        #     self.menu_file.entryconfigure('restaurar estado inicial', state="normal")
        else:
            print('continue game')
        #     self.menu_file.entryconfigure('restaurar estado inicial', state="disabled")

    def reset_selected_tiles(self):
        self.selected_tiles = []

    def set_selected_tile(self, x, y):
        if (x,y) not in self.selected_tiles:
            self.selected_tiles.append((x,y))
        else:
            self.selected_tiles.pop((x,y))

    def select_tile(self, event, board_id, line, column):
        """
        USE CASE SELECT TILE
        """
    
        messagebox.showinfo(message=f'Clique na linha: {line} coluna: {column} no board: {board_id}')
        print(f'Clique na linha: {line} coluna: {column}')
        tile = self.get_label(board_id, line, column)
        print(tile)
        tile.config(image=self.water_miss)
        return
        
        if not self.gameview.is_local_player_turn():
            messagebox.showinfo(message=f'Não é a sua vez.')
            return


        #TESTING
        

        match_status = self.gameview.get_match_status()

        if match_status == 3:
            if not self.gameview.is_local_board_id(board_id):
                messagebox.showinfo(message=f'Você clicou no tabuleiro errado. Para colocar navios, selecione-os no tabuleiro abaixo.')
            self.set_selected_tile(line, column)
            

        elif match_status == 5:
            if not self.gameview.is_remote_board_id(board_id):
                messagebox.showinfo(message=f'Você clicou no tabuleiro errado. Para realizar um tiro, selecione o tabuleiro do seu oponente (superior).')
            remote_board = self.gameview.get_local_board()
            tile = remote_board.get_tile(line, column)
            if tile.is_selectable():
                tile.update_state()

            is_winner = self.gameview.evaluate_end_of_match()
            if not is_winner:
                self.gameview.local_player.toggle_turn()
                self.gameview.remote_board.toggle_turn()


            self.dog_server_interface.send_move({'coord_x': line, 'coord_y': column, 'is_winner': is_winner})

            match_status = self.gameview.get_match_status()
            self.update_gui(match_status)

    def set_ships(self):
        """
        USE CASE SET SHIPS
        """
        game_view = self.gameview

        if not game_view.is_tiles_sum_valid(self.selected_tiles):
            messagebox.showinfo('O número de tiles selecionados é inválido. Por favor tente novamente.')
            self.reset_selected_tiles()

        if game_view.are_there_ships_close(self.selected_tiles):
            messagebox.showinfo('Existem navios adjacentes. Por favor tente novamente.')
            self.reset_selected_tiles()

        all_ships_placed, instantiated_ships = game_view.are_all_ships_placed(self.selected_tiles)

        if all_ships_placed:
            game_view.get_local_board().create_ships(instantiated_ships)
            match_status = game_view.get_match_status()
            self.update_gui(match_status)

            self.dog_server_interface.send_move({'ships': instantiated_ships})

        else:
            messagebox.showinfo('Você não seleciou todos os tipos de navios necessários.'
            'Por favor tente novamente. Dica: Siga a legenda de navios requeridos.')
            self.reset_selected_tiles()

    def receive_move(self, move_to_send: dict):
        game_view = self.gameview
        match_status = game_view.get_match_status()

        if match_status == 5:
            remote_board = game_view.get_remote_board()
            remote_board.create_ships(move_to_send['ships'])

        elif match_status == 6:
            x, y = move_to_send['coord_x'], move_to_send['coord_y']
            local_board = game_view.get_local_board()
            tile = local_board.get_tile(x, y)
            tile.update_state()


        if move_to_send['is_winner']:
            remote_player = game_view.get_remote_player()
            remote_player.set_as_winner()

        match_status = game_view.get_match_status()
        self.update_gui(match_status)

    def update_gui(self, match_status: int):
        remote_board = self.gameview.get_remote_board()
        

