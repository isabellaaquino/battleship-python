from tkinter import *
from tkinter import messagebox

class PlayerInterface:
    def __init__(self):
        self.main_window = Tk() 
        self.fill_main_window()

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
        self.water_tile = PhotoImage(file="implementacao/images/tile_water.png")
        self.key_tiles_image = PhotoImage(file="implementacao/images/key_tiles.png")
        self.key_ships_image = PhotoImage(file="implementacao/images/key_ships.png")
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
            coluna = [] 
            for x in range(8):
                player_tile = Label(self.player_frame, bd = 0, image=self.water_tile)
                player_tile.grid(row=x, column=y)
                player_tile.bind(
                    "<Button-1>", lambda event, a_line=x, a_column=y: self.select_tile(event, a_line, a_column)
                )
                coluna.append(player_tile)
            self.board_view.append(coluna)

        

        # Second board
        for y in range(8):
            coluna = [] 
            for x in range(8):
                enemy_tile = Label(self.enemy_frame, bd = 0, image=self.water_tile)
                enemy_tile.grid(row=x, column=y)
                enemy_tile.bind(
                    "<Button-1>", lambda event, a_line=x, a_column=y: self.select_tile(event, a_line, a_column)
                )
                coluna.append(enemy_tile)
            self.board_view.append(coluna)
        
        

        # self.board_title = Label(self.player_frame, text="A B C D E F G H I J", font="arial 20")
        # self.board_title.grid(row=0, column=0)
        
        self.message_label = Label(self.title_frame, bg="#D9D9D9", text='BATALHA NAVAL', font=("Gulim", 30))
        self.message_label.grid(row=0, column=1)

        # Menu region

        self.menubar = Menu(self.main_window)
        self.menubar.option_add("*tearOff", FALSE)
        self.main_window["menu"] = self.menubar

        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label="File")

        # Itens menu:
        self.menu_file.add_command(label="Iniciar jogo", command=self.start_match) # TODO: add command
        self.menu_file.add_command(label="Recomeçar jogo", command=self.restart_match) # TODO: add command

    def start_match(self):
        answer = messagebox.askyesno('START', 'Are you sure you want to start a match?')
        if(answer):
            print('start game')
            # self.menu_file.entryconfigure('restaurar estado inicial', state="normal")
        else:
            print('continue game')
            # self.menu_file.entryconfigure('restaurar estado inicial', state="disabled")

    def restart_match(self):
        answer = messagebox.askyesno('START', 'Are you sure you want to restart the match?')
        if(answer):
            print('restart game')
        #     self.menu_file.entryconfigure('restaurar estado inicial', state="normal")
        else:
            print('continue game')
        #     self.menu_file.entryconfigure('restaurar estado inicial', state="disabled")

    def select_tile(self, event, line, column):
        messagebox.showinfo(message=f'Clique na linha: {line} coluna: {column}')
        print(f'Clique na linha: {line} coluna: {column}')