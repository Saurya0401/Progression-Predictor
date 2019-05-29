from Resources import ProgCreate, ProgTest
from GUI import GUI
from os import path, mkdir

# TODO: Remove lists from return statements.


def format_inputs(inputs):
    """
    Formats inputs provided by init_user() then returns them to init_user().
    :param inputs: raw inputs
    :return: formatted inputs or errors
    """

    usertype = int(inputs[0])
    fname = str(inputs[1] + '.csv')
    start_chord_array = ProgCreate.to_cnv([x.lower() for x in inputs[2].split(', ')])
    start_chord_array[0] = sorted(start_chord_array[0])
    chord_array = ProgCreate.to_cnv([x.lower() for x in inputs[3].split(', ')])
    chord_array[0] = sorted(chord_array[0])
    acc = float(inputs[4]) * 10000
    inputs = [usertype, fname, start_chord_array[0], chord_array[0], acc]
    errors = ["Invalid start chords: {}".format(", ".join(start_chord_array[1])) if start_chord_array[1] else None,
              "Invalid chords: {}".format(", ".join(chord_array[1])) if chord_array[1] else None,
              "Invalid accuracy: %.2f" % (acc/10000) if (acc < 10000 or acc > 100000) else None]
    return inputs, errors


def init_user():
    """
    Passes raw inputs from gui variables to format_inputs(), then uses the returned inputs to call functions that create
    csv file.
    """

    try:
        all_inputs = format_inputs([gui.usertype.get(), gui.username.get(), gui.start_chords.get(), gui.chords.get(),
                                    gui.accuracy.get()])
        print(all_inputs)
        inputs = all_inputs[0]
        errors = all_inputs[1]
        if all(err == errors[0] for err in errors):
            gui.loading_screen()
            create_datafile('users/{}'.format(inputs[1]))
            ini_prog = ProgCreate(datafile='users/{}'.format(inputs[1]), c0_array=inputs[2], c_array=inputs[3])
            ini_prog.add_data(inputs[4])
            gui.loading_text.config(text="Done.")
            return gui.next_button.config(state='normal')
        else:
            raise ValueError("INVALID INPUTS\n{}".format("\n".join(str(e) for e in errors if e is not None)))
    except ValueError as input_error:
        gui.error.config(text=input_error.args[0])
        gui.show_error_window()
        gui.get_inputs()


def create_datafile(filename):
    """
    Creates the 'users' folder if it doesn't exist, then creates a (csv) file with a predetermined header in
    that folder.
    """
    if not path.exists('users/'):
        mkdir('users/')
    file = open(filename, 'w', newline='')
    file.writelines("C0,C1,C2,C3,L\n")
    return file.close()


def test():
    """
    Tests a user provided chord progression.
    :return: change state of gui.test_button to normal provided an instance of ProgTest is successfully created.
    """

    filename = str(gui.username.get() + '.csv')
    test_list = ProgCreate.to_cnv([x.lower() for x in gui.prog_input.get().split(', ')])
    print(test_list)
    try:
        if len(test_list[0]) == 4:
            # create an instance of the ProgTest class provided no exceptions are raised.
            pred = ProgTest(df='users/{}'.format(filename), test_array=test_list[0])
            gui.output_textbox.config(text=pred.predict()[0])
            gui.info_textbox.config(text=pred.predict()[1])
            gui.info_displayed = False
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
    """
    Plays a user provided chord progression.
    :return: change state of gui.test_button to normal provided an instance of ProgPred is successfully created.
    """

    chords = ProgCreate.to_cnv([x.lower() for x in gui.prog.get().split(', ')])
    print(chords)
    try:
        if len(chords[0]) == 4:
            # create an instance of the ProgPred class provided no exceptions are raised.
            prog = ProgCreate()
            prog.cnv = chords[0]
            print(prog.cnv)
            prog.play_prog()
            return gui.play_button.config(state='normal')
        elif len(chords[1]):
            if chords[1][0] == '':
                raise ValueError("Bad Input: No chords.")
            else:
                raise ValueError("Bad Input: Invalid chords: '{}'".format(", ".join(chords[1])))
        else:
            raise ValueError("Bad Input: Incorrect number of chords.")
    except ValueError as input_error:
        gui.error.config(text=input_error.args[0])
        gui.show_error_window()
        gui.play_button.config(state='normal')


def main():
    """
    Creates a new user profile or calls the test() function on an existing user profile based on the user type.
    """

    u_type = int(gui.usertype.get())
    f_name = str(gui.username.get() + '.csv')
    if u_type == 1:
        try:
            if path.exists('users/{}'.format(f_name)):
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
            if not path.exists('users/{}'.format(f_name)):
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
