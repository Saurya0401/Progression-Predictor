try:
    from tkinter import *
    import threading
except ModuleNotFoundError:
    pass

# TODO: Make GUI more aesthetic


class GUI:

    def __init__(self, main_func, init_func, test_func, play_func, title='Progression Predictor', width=400, height=300):
        """
        Defines all functions, variables, GUI widgets and GUI variables.
        :param main_func: main() from ProgressionPredictor.py
        :param init_func: init_user() from ProgressionPredictor.py
        :param test_func: test() from ProgressionPredictor.py
        :param play_func: play_prog() from ProgressionPredictor.py
        :param title: the title of the GUI window
        :param width: default and minimum width of the GUI window
        :param height: default and minimum height of the GUI window 
        """
        
        self.title = title
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title(self.title)
        self.root.minsize(self.width, self.height)
        self.root.resizable(width=True, height=False)
        self.root.grid_rowconfigure((0, 3), weight=1)
        self.root.grid_columnconfigure((0, 2), weight=1)

        # defining functions, variables and threads
        self.info_displayed = False
        self.next_func = None
        self.main_func = main_func
        self.init_func = init_func
        self.init_thread = threading.Thread(target=self.init_func, name='init_thread')
        self.test_func = test_func
        self.play_func = play_func

        # defining widgets
        self.input_frame = Frame(master=self.root)
        self.output_frame = Frame(master=self.root)
        self.welcome_text = Label(master=self.output_frame, font='Arial 15',
                                  text="Welcome to the Progression Predictor!")
        self.usertype = IntVar()
        self.choice_nu = Radiobutton(master=self.input_frame, font='Arial 12',
                                     text="New User", variable=self.usertype, value=1)
        self.choice_eu = Radiobutton(master=self.input_frame, font='Arial 12',
                                     text="Existing User", variable=self.usertype, value=2)
        self.username_label = Label(master=self.input_frame, font='Arial 12', text="Enter your name: ")
        self.username = StringVar()
        self.username_input = Entry(master=self.input_frame, font='Arial 12', textvariable=self.username)
        self.error = Label(master=self.output_frame, text='Unknown error.', fg='red')
        self.start_chord_label = Label(master=self.input_frame, font='Arial 12',
                                       text="Please enter chords you like progressions to start with: ")
        self.start_chords = StringVar()
        self.start_chord_input = Entry(master=self.input_frame, font='Arial 12', textvariable=self.start_chords)
        self.chord_label = Label(master=self.input_frame, font='Arial 12',
                                 text="Please enter chords that you like in a progression:")
        self.chords = StringVar()
        self.chord_input = Entry(master=self.input_frame, font='Arial 12', textvariable=self.chords)
        self.accuracy_label = Label(master=self.input_frame, font='Arial 12',
                                    text="On a scale of 1-10, how accurate do you want the program to be:")
        self.accuracy = StringVar()
        self.accuracy_input = Entry(self.input_frame, font='Arial 12', textvariable=self.accuracy)
        self.accuracy_warning = Label(self.input_frame, font='Arial 10',
                                      text="Warning: Higher accuracy means a longer initialisation time.", fg='red')
        self.loading_text = Label(master=self.output_frame, font='Arial 12', text="Adding data, please wait...")
        self.finished = Label(master=self.output_frame, font='Arial 12', text='Done.')
        self.prog_input_label = Label(master=self.input_frame, font='Arial 12', text="Now enter a random progression: ")
        self.prog = StringVar()
        self.prog_input = Entry(master=self.input_frame, font='Arial 12', textvariable=self.prog)
        self.test_button = Button(master=self.input_frame, text="Test!", font='Arial 12', command=self.test_prog)
        self.play_button = Button(master=self.input_frame, text="Play!", font='Arial 12', command=self.play_prog)
        self.info_button = Button(master=self.input_frame, text="Info", font='Arial 12', command=self.show_info)
        self.output_textbox = Label(master=self.output_frame)
        self.info_textbox = Label(master=self.output_frame)
        self.next_button = Button(master=self.input_frame, text="Next", font='Arial 12', command=self.next_button_click)

    def start_window(self):
        """
        Displays the first GUI window. Also sets column weights for both input_frame and output_frame so that all
        widgets inside them are centered.
        """

        self.rearrange_widgets({self.input_frame: {'row': 2, 'column': 1, 'sticky': 'nsew'},
                                self.output_frame: {'row': 1, 'column': 1, 'sticky': 'nsew'}})
        self.input_frame.grid_columnconfigure((0, 4), weight=1)
        self.output_frame.grid_columnconfigure((0, 2), weight=1)
        self.rearrange_widgets({self.next_button: {'row': 1, 'column': 1, 'pady': 5},
                                self.welcome_text: {'row': 1, 'column': 1}})
        self.next_func = self.get_usertype

    def get_usertype(self):
        self.remove_widget([self.output_frame])
        self.rearrange_widgets({self.input_frame: {'row': 1}})
        self.rearrange_widgets({self.choice_nu: {'row': 1, 'column': 1},
                                self.choice_eu: {'row': 1, 'column': 2},
                                self.next_button: {'row': 3, 'column': 1, 'columnspan': 2, 'pady': 5}})
        self.next_func = self.get_filename

    def get_filename(self):
        self.rearrange_widgets({self.username_label: {'row': 1, 'column': 1}, self.username_input: {'row': 1, 'column': 2},
                                self.next_button: {'row': 3, 'column': 1, 'columnspan': 2, 'pady': 5}})
        self.next_func = self.main_func

    def get_inputs(self):
        self.rearrange_widgets({self.start_chord_label: {'row': 1, 'column': 1, 'padx': 5},
                                self.start_chord_input: {'row': 1, 'column': 2, 'padx': 8},
                                self.chord_label: {'row': 2, 'column': 1, 'padx': 5},
                                self.chord_input: {'row': 2, 'column': 2, 'padx': 8},
                                self.accuracy_label: {'row': 3, 'column': 1, 'padx': 5},
                                self.accuracy_input: {'row': 3, 'column': 2, 'padx': 8},
                                self.accuracy_warning: {'row': 4, 'column': 1, 'columnspan': 2, 'padx': 5},
                                self.next_button: {'row': 6, 'column': 1, 'columnspan': 2, 'pady': 5}})
        self.next_func = self.loading_screen

    def loading_screen(self):
        self.init_thread.start()
        self.reset_frames()
        self.next_button.config(state='disabled', command=self.test_window)
        self.rearrange_widgets({self.output_frame: {'row': 1, 'column': 1}, self.input_frame: {'row': 2, 'column': 1}})
        self.rearrange_widgets({self.loading_text: {'row': 1, 'column': 1},
                                self.next_button: {'row': 1, 'column': 1, 'pady': 5}})

    def test_window(self):
        if self.init_thread.is_alive():
            self.init_thread.join()
        self.reset_frames()
        self.rearrange_widgets({self.input_frame: {'row': 1, 'column': 1}, self.output_frame: {'row': 2, 'column': 1}})
        self.rearrange_widgets({self.prog_input_label: {'row': 1, 'column': 1, 'padx': 5},
                                self.prog_input: {'row': 1, 'column': 2, 'padx': 8, 'columnspan': 2},
                                self.info_button: {'row': 2, 'column': 1, 'pady': 5},
                                self.test_button: {'row': 2, 'column': 2, 'pady': 5},
                                self.play_button: {'row': 2, 'column': 3, 'pady': 5}})

    def play_prog(self):
        """
        Creates a thread whose target is self.play_func and joins the thread if it is already running.
        :return: Starts the thread.
        """
        self.play_button.config(state='disabled')
        play_thread = threading.Thread(target=self.play_func)
        if play_thread.is_alive():
            play_thread.join(0.1)
        return play_thread.start()

    def test_prog(self):
        """
        Creates a thread whose target is self.test_func and joins the thread if it is already running.
        :return: Starts the thread.
        """

        self.test_button.config(state='disabled')
        test_thread = threading.Thread(target=self.test_func)
        if test_thread.is_alive():
            test_thread.join(0.1)
        return test_thread.start()

    def next_button_click(self):
        """
        Removes all widgets from both input_frame and output_frame and calls a specified function.
        :return:
        """

        self.reset_frames()
        self.next_func()

    def show_output(self):
        self.remove_widget(
            [i for i in self.output_frame.winfo_children() if len(self.output_frame.winfo_children()) > 0])
        self.rearrange_widgets({self.output_textbox: {'row': 1, 'column': 1, 'columnspan': 2}})

    def show_info(self):
        if self.info_displayed:
            self.info_textbox.grid_remove()
            self.info_displayed = False
        elif not self.info_displayed:
            self.info_textbox.grid(row=2, column=1)
            self.info_displayed = True

    def show_error_window(self):
        self.remove_widget([i for i in self.output_frame.winfo_children() if len(self.output_frame.winfo_children()) > 0])
        self.rearrange_widgets({self.output_frame: {'row': 2, 'column': 1}, self.error: {'row': 1, 'column': 1}})

    def reset_frames(self):
        """
        Removes all widgets from both input_frame and output_frame.
        """

        self.remove_widget([
            i for i in self.output_frame.winfo_children() if len(self.output_frame.winfo_children()) > 0])
        self.remove_widget([
            i for i in self.input_frame.winfo_children() if len(self.input_frame.winfo_children()) > 0])

    @staticmethod
    def remove_widget(widgets, p_g='g'):
        """
        Removes widgets using either grid_remove() or pack_forget().
        :param widgets: a list of widgets to be removed
        :param p_g: geometry manager used to place the widgets, p = pack, g = grid (default).
        """

        for i in widgets:
            if p_g == 'p':
                i.pack_forget()
            elif p_g == 'g':
                i.grid_remove()

    @staticmethod
    def rearrange_widgets(widgets_properties, p_g='g'):
        """
        Modifies the shape and placement of widgets.
        :param widgets_properties: A dictionary containing the widgets and their properties.
        :param p_g: geometry manager used to place the widgets, p = pack, g = grid (default).
        """

        for widget, properties in widgets_properties.items():
            if p_g == 'p':
                widget.pack(cnf=properties)
            elif p_g == 'g':
                widget.grid(cnf=properties)
