try:
    from Resources import ProgPred, ProgTest
    from GUI import GUI
    from pathlib import Path
except ModuleNotFoundError:
    pass

# TODO: Handle input errors


def format_inputs(inputs):
    usertype = int(inputs[0])
    fname = str(inputs[1] + '.csv')
    start_chord_array = ProgPred.to_cnv([x.lower() for x in inputs[2].split(', ')])
    start_chord_array[0] = sorted(start_chord_array[0])
    chord_array = ProgPred.to_cnv([x.lower() for x in inputs[3].split(', ')])
    chord_array[0] = sorted(chord_array[0])
    acc = int(inputs[4]) * 10000
    return [usertype, fname, start_chord_array, chord_array, acc]


def create_datafile(filename):
    file = open(filename, 'w', newline='')
    file.writelines("C0,C1,C2,C3,L\n")
    file.close()


def init_user():
    inputs = format_inputs([gui.usertype.get(), gui.username.get(), gui.start_chords.get(), gui.chords.get(),
                            gui.accuracy.get()])
    print(inputs)
    create_datafile('users/{}'.format(inputs[1]))
    ini_prog = ProgPred(datafile='users/{}'.format(inputs[1]), c0_array=inputs[2][0], c_array=inputs[3][0])
    ini_prog.add_data(inputs[4])
    gui.loading_text.config(text="Done.")
    return gui.next_button.config(state='normal')


def test():
    filename = str(gui.username.get() + '.csv')
    test_list = ProgPred.to_cnv([x.lower() for x in gui.prog_input.get().split(', ')])
    print(test_list)
    try:
        if len(test_list[0]) == 4:
            pred = ProgTest(df='users/{}'.format(filename), test_array=test_list[0])
            gui.output_textbox.config(text=pred.predict()[0])
            gui.info_textbox.config(text=pred.predict()[1])
            gui.show_output()
            return gui.test_button.config(state='normal')
        elif len(test_list[1]):
            if test_list[1][0] == '':
                raise ValueError("Bad Input: No chords.")
            else:
                raise ValueError("Bad Input: Invalid chords: '{}'".format(", ".join(test_list[1])))
        else:
            raise ValueError("Bad Input: Incorrect number of chords.")
    except ValueError as input_error:
        gui.error.config(text=input_error.args[0])
        gui.show_error_window()
        gui.test_button.config(state='normal')


def play_prog():
    chords = ProgPred.to_cnv([x.lower() for x in gui.prog.get().split(', ')])
    print(chords)
    prog = ProgPred()
    prog.cnv = chords[0]
    print(prog.cnv)
    prog.play_prog()
    return gui.play_button.config(state='normal')


def main():
    u_type = int(gui.usertype.get())
    f_name = str(gui.username.get() + '.csv')
    if u_type == 1:
        try:
            if Path('users/{}'.format(f_name)).exists():
                raise FileExistsError("User already exists.")
            if not gui.username.get():
                raise ValueError("Name cannot be blank.")
        except (FileExistsError, ValueError) as filename_error:
            gui.error.config(text=filename_error.args[0])
            gui.show_error_window()
            gui.get_filename()
        else:
            gui.remove_widget([gui.error, gui.output_frame])
            gui.get_inputs()
    elif u_type == 2:
        try:
            if not Path('users/{}'.format(f_name)).exists():
                raise FileNotFoundError("User not found.")
        except FileNotFoundError as filename_error:
            gui.error.config(text=filename_error.args[0])
            gui.show_error_window()
            gui.get_filename()
        else:
            gui.test_window()


if __name__ == '__main__':
    gui = GUI(main_func=main, init_func=init_user, test_func=test, play_func=play_prog)
    gui.start_window()
    gui.root.mainloop()
