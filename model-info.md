### Summary:
This program uses a regression based machine learning algorithm ([Ridge Regression][1]) to predict the arbitrary 'score' of an integer sequence provided by the user. The model is trained and tested via [train-test split][2] from a dataset containing, at a minimum, 10,000 samples of data.

### Data and data structure:
The dataset this model runs on is a `.csv` file initially containing 5 columns. These colums are `C0`, `C1`, `C2`, `C3`, and `L`. For the model, `C0`, `C1`, `C2`, `C3` are the **X features** and `L` is the **y feature**. Here's a sample of the data:

|C0|C1|C2|C3|L|
|--|--|--|--|-|
| 1| 4|20| 5|0|
| 5|15| 7|13|0.25|
|12| 2| 6|18|0.75|

`C0`, `C1`, `C2`, `C3` are **cnv** columns and every cell under these colums contain a integer value from 1-24. These 
directly correspond to 24 chords (A Major to G# Minor). Every row is a 4-chord progression, wherein `C0` is the first chord, `C1` the second chord, `C2` the third chord and `C3` the fourth. 
`L` represents, on a scale from 0.00 - 1.00, the arbitrary 'score' of the progression. The higher the score, the more likely it is for the user to like the progression.
The function `make_cnv()` method from the `ProgCreate` class in [Resources.py][4] is resposible for making every progression row and calculating the value of `L`.

#### Preparing the dataset for the Ridge model:
The problem with the dataset in it's initial form is that `C0`, `C1`, `C2`, `C3` are categorical integer values while `L` is a continuous value, which is not compatible with the Ridge model. As such [one-hot encoding][3] is done to make the dataset compatible and upon doing so the number of X features changes to 96 (4 * 24). Then, train-test split is performed with a test ratio of 0.2 as a rudimentary form of cross-validation. Both these steps are sequentially done by the `__init__()` method from the `ProgTest` class in [Resources.py][4].

### The Ridge model:
A Ridge Regression model from the SciKit-Learn library is used in this program. Currently the only hyperparameters set are `alpha=0.01` and `random_state=4`. Everything concerning the model as well as the final results provided by the model is handled by the `predict()` method from the `ProgTest` class in [Resources.py][4].

### User Inputs:
There are 3 user inputs. Since these inputs are stored under different named variables in different scritps, the variables from [Resources.py][4] will be referred to here:
1. `c0_array` :  A list of chords provided by the user. These are the chords the user prefers progressions to start with. All chords in this list are converted to **cnvs** by the `to_cnv()` class method before they are used.
2. `c_array` : A list of chords provided by the user. These are the chords the user prefers to be in a progression. All chords in this list are converted to **cnvs** by the `to_cnv()` class method before they are used.
3. `test_array` : The 4-chord progression provided by the user, also converted to **cnvs**. The Ridge model uses this array to predict the arbitrary 'score' i.e. the probability of user liking this chord progression based on `c0_array` and `c_array`.


### Glossary:
**CNV/cnv**: An integer value that directly corresponds to a chord. It is an abbreviation for **C**hord-**N**umber **V**alue. The `chord_dict` dictionary from the `ProgCreate` class in [Resources.py][4] contains all chords and their corresponding cnvs.

[1]: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html
[2]: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
[3]: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
[4]: Resources.py
