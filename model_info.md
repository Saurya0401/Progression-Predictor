### Data and data structure:
The dataset this model runs on is a `.csv` file initially containing 5 columns. These colums are `C0`, `C1`, `C2`, `C3`, and `L`. For the model, `C0`, `C1`, `C2`, `C3` are the X values and `L` is the y value. Here's a sample of the data:

|C0|C1|C2|C3|L|
|--|--|--|--|-|
| 1| 4|20| 5|0|
| 5|15| 7|13|0.25|
|12| 2| 6|18|0.75|

`C0`, `C1`, `C2`, `C3` are **cnv** (**C**hord-**N**umber **V**alue) columns and every cell under these colums contain a value from 1-24. These 
directly correspond to 24 chords (A Major to G# Minor). Every row is a four chord progression, wherein `C0` is the first chord, `C1` the second chord, `C2` the third chord and `C3` the fourth. 
`L` represents, on a scale from 0.00 - 1.00, the 'score' of the progression. The higher the score, the more likely it is for the user to like the progression.
The function `make_cnv` function from the `ProgPred` class in [Resources.py](Resources.py) is resposible for making every progression row and calculating the value of `L`.

#### Preparing the dataset for the Ridge model:
The problem with the dataset in it's initial form is that `C0`, `C1`, `C2`, `C3` are categorical integer values while `L` is a continuous value, which is not compatible with the Ridge model. As such [one-hot encoding](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html) is done to make the dataset compatible. Then, [train-test split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) is performed in a test ratio of 0.2 as a rudimentary form of cross-validation. Both these steps are sequentially done by the `__init__` function from the `ProgTest` class in [Resources.py](Resources.py).

### The Ridge model:
A [**Ridge Regression**](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html) model from the SciKit-Learn library is used in this program. Currently the only hyperparameters set are `alpha=0.01` and `random_state=4`. Everything concerning the model as well as the final results provided by the model is handled by the [`predict()`](https://github.com/Saurya0401/ProgressionPredictor/blob/92f032bf61fa3d9a9a893edac0bbb9cc9bb1ee21/Resources.py#L121-L135) function.
