# ProgressionPredictor
A python program that predicts how much a user will like a particular chord progression.
The program uses a machine learning algorithm called [Ridge Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html) to predict based on inputs provided by the user. The inputs include a list of 'start chords' and a list of 'chords' provided by the user. For more details on the ML model, see [model_info](model_info.md).

To use the program, download `ProgressionPredictor.py`, `Resources.py`, `GUI.py`, and the 'audio files' folder to the same directory, then run `ProgressionPredictor.py`.


### Dependancies:
- The program requires the following Python modules to work:
  1. tkinter
  2. pandas
  3. numpy
  4. sklearn
  5. playsound

- Python 3 is required.


### TODO:
- Insert comments and docstrings in all scripts.
- Complete error handling for user inputs passed via GUI.get_inputs().
- Make error handling for importing modules more pythonic.
- Further optimise Ridge model.
- Make GUI more aesthetic.
