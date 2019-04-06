#Fransiskus Derian 82691258. ICS 32 Project 5

import OthelloGameLogic
import tkinter


class OthelloInitInput:
    def __init__(self):
        self._root_window = tkinter.Tk()
        
        tkinter.Label(self._root_window, text="Specify Rows:").grid(row = 0, column = 0)
        tkinter.Label(self._root_window, text="Specify Column:").grid(row = 4, column = 0)
        tkinter.Label(self._root_window, text="Top Left Disc: ").grid(row = 0, column = 2)
        tkinter.Label(self._root_window, text="First Player :").grid(row = 4, column = 2)
        tkinter.Label(self._root_window, text="Winning Method :").grid(row = 2, column = 1)
        button = tkinter.Button(self._root_window, text="START GAME", command = self.quit_function)
        button.grid(row = 6, column = 2, padx= 30, pady= 30)
        
        self._row_var = tkinter.StringVar()
        self._row_var.set("4")
        self._col_var = tkinter.StringVar()
        self._col_var.set("4")
        self._topLeft_var = tkinter.StringVar()
        self._topLeft_var.set("Black")
        self._firstPlayer_var = tkinter.StringVar()
        self._firstPlayer_var.set("Black")
        self._winningMethod_var = tkinter.StringVar()
        self._winningMethod_var.set("Most")
        
        row_option_List = ("4", "6", "8", "10", "12", "14", "16")
        col_option_List = ("4", "6", "8", "10", "12", "14", "16")
        black_or_white = ("Black", "White")
        winning_methods = ("Most", "Least")
        row_opt = tkinter.OptionMenu(self._root_window, self._row_var, *row_option_List)
        col_opt = tkinter.OptionMenu(self._root_window, self._col_var, *col_option_List)
        top_left_opt = tkinter.OptionMenu(self._root_window, self._topLeft_var, *black_or_white)
        first_player_opt = tkinter.OptionMenu(self._root_window, self._firstPlayer_var, *black_or_white)
        winning_method_opt = tkinter.OptionMenu(self._root_window, self._winningMethod_var, *winning_methods)
        row_opt.grid(row = 1, column = 0, padx= 30,pady = 5)
        col_opt.grid(row = 5, column = 0, padx = 30,pady = 5)
        top_left_opt.grid(row = 1, column = 2, padx = 30,pady = 5)
        first_player_opt.grid(row = 5, column = 2, padx = 30,pady = 5)
        winning_method_opt.grid(row = 3, column = 1, padx = 30,pady = 5)


        
        self._root_window.mainloop()

    def quit_function(self):
        self._root_window.destroy()

    


        
class OthelloGraphic:

    def __init__(self, row, col, topLeft, firstPlayer, winningMethod):
        self._row = row
        self._col = col
        self._topLeft = topLeft
        self._firstPlayer = firstPlayer
        self._winningMethod = winningMethod
        self._width = 800
        self._height = 800
        self._window = tkinter.Tk()
    

        self._game = OthelloGameLogic.OthelloGame(self._row, self._col,
                                                  self._topLeft, self._firstPlayer,
                                                  self._winningMethod)
        self._turn = self._game._turn
        #self._game.place_disc(3,1)
        
        self._canvas = tkinter.Canvas(
            master = self._window, width = self._width,
            height = self._height, background= 'green')

        self._canvas.grid(
            row = 2, column = 0, sticky = tkinter.N + tkinter.S
            + tkinter.E + tkinter.W)


        self._white_score = tkinter.Label(master = self._window,
                                          text = 'White: ' + str(self._game.count_white())
                                          , font = ('Helvetica', 14))
        self._white_score.grid(row = 0, column = 0, padx = 30, pady = 10,
                          sticky = tkinter.W + tkinter.N)
        self._current_turn = tkinter.Label(master = self._window,
                                           text = 'Current Turn: ' + self.full_word()
                                           , font = ('Helvetica', 14))
        self._current_turn.grid(row = 0, column = 0, padx = 10, pady = 10,
                                sticky = tkinter.N)
        self._black_score = tkinter.Label(master = self._window,
                                          text = 'Black: ' + str(self._game.count_black())
                                          , font = ('Helvetica', 14))
        self._black_score.grid(row = 0, column = 0, padx = 30, pady = 10,
                          sticky = tkinter.E + tkinter.N)



        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._window.rowconfigure(0, weight = 0)
        self._window.rowconfigure(1, weight = 0)
        self._window.rowconfigure(2, weight = 1)
        self._window.columnconfigure(0, weight = 1)


    def top_display(self):        
        self._black_score.configure(text = 'Black: ' + str(self._game.count_black()))
        self._white_score.configure(text='White: ' + str(self._game.count_white()))
        self._current_turn.configure(text='Current Turn: ' + self.full_word())

    def full_word(self):
        if self._turn == 'B':
            return 'Black'
        else:
            return 'White'
     
    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        self._make_the_grid()
        self._draw_disc()
        
        

    def _create_vertical_line(self, num_of_line: int):
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        second_y_vertical = canvas_height
        first_y_vertical = 0
        first_x_vertical = canvas_width/self._col * num_of_line
        second_x_vertical = canvas_width/self._col * num_of_line

        self._canvas.create_line(first_x_vertical, first_y_vertical,
                                 second_x_vertical, second_y_vertical,
                                 fill = 'white')

    def _create_horizontal_line(self, num_of_line: int):
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        second_x_horizontal = canvas_width
        first_x_horizontal = 0
        first_y_horizontal = canvas_height/self._row * num_of_line
        second_y_horizontal = canvas_height/self._row * num_of_line

        self._canvas.create_line(first_x_horizontal,first_y_horizontal,
                                 second_x_horizontal, second_y_horizontal,
                                 fill = 'white')




    def _draw_disc(self):
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        colSpan = canvas_width/self._col
        rowSpan = canvas_height/self._row
        extra_col = colSpan/12
        extra_row = rowSpan/12
        
        for row in range(len(self._game._board)):
            for col in range(len(self._game._board[0])):
                if self._game._board[row][col] == 'B':
                    self._canvas.create_oval(col * colSpan + extra_col,row*rowSpan + extra_row,
                                             (col+1)*colSpan-extra_col,(row+1)*rowSpan-extra_row,
                                             fill = 'black')
                elif self._game._board[row][col] == 'W':
                    self._canvas.create_oval(col * colSpan + extra_col,row*rowSpan + extra_row,
                                             (col+1)*colSpan-extra_col,(row+1)*rowSpan-extra_row,
                                             fill = 'white')
        
    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        colSpan = canvas_width/self._col
        rowSpan = canvas_height/self._row
        
        for row in range(self._row):
            for col in range(self._col):
                if event.x in range(round(col*colSpan), round((col+1)*colSpan)) and event.y in range(round(row*rowSpan), round((row+1)*rowSpan)):
                    if self._game.is_legal_move(row, col):
                        self._game.place_disc(row, col)
                        self._draw_disc()
                        self._turn = self._game._turn
                        self.top_display()

        if self._game.winning_player() != None:       
            self._current_turn.configure(text = "GAME OVER !")
            tkinter.Label(master = self._window, text='Method: ' +self._winningMethod , font = ('Helvetica', 14)).grid(row = 1, column= 0, padx = 15, pady = 10,
                                                                                                                       sticky = tkinter.S + tkinter.W)
            tkinter.Label(master = self._window, text=self._game.winning_player(), font = ('Helvetica', 14)).grid(row = 1, column= 0, pady = 10,
                                                                                                                  sticky= tkinter.S)
            tkinter.Button(self._window, text="EXIT GAME", command = self.quit_function).grid(row = 1, column = 0, padx = 15, pady = 10, sticky= tkinter.S +
                                                                                                   tkinter.E)
            
        elif self._game.black_pass():
            self._current_turn.configure(text="BLACK PASS! Turn: WHITE")
            self._turn = self._game._turn
                    
        elif self._game.white_pass():
            self._current_turn.configure(text="WHITE PASS! Turn: BLACK")
            self._turn = self._game._turn
                            
                     
    def quit_function(self):
        self._window.destroy()


        
    def _make_the_grid(self):
        self._canvas.delete(tkinter.ALL)

        for num in range(self._col):
            self._create_vertical_line(num)
        for num in range(self._row):
            self._create_horizontal_line(num)

    def start(self):
        self._make_the_grid()
        self._window.mainloop()



if __name__ == '__main__':
    y = OthelloInitInput()
    inputs = y._row_var.get(), y._col_var.get(), y._topLeft_var.get(), y._firstPlayer_var.get(), y._winningMethod_var.get()    
    x = OthelloGraphic(int(inputs[0]), int(inputs[1]), inputs[2][0], inputs[3][0], inputs[4].upper())                       

    x.start()
        
