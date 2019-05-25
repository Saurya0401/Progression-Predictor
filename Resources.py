try:
    import pandas as pd
    import numpy as np
    import csv
    import playsound
    import random
    from sklearn import preprocessing, model_selection, linear_model, metrics
except ModuleNotFoundError:
    pass

# TODO: Make Ridge model more accurate


class ProgPred:
    """
    This class has the dual functionality of creating a dataset for a new user and playing a user provided chord
    progression.

    chord_dict: A dictionary that contains chords and their corresponding integer values.
    cnv: An integer that corresponds to a specific chord. An abbreviation for Chord-Numeric Value.
    """

    chord_dict = {'a': 1, 'a#': 2, 'b': 3, 'c': 4, 'c#': 5, 'd': 6, 'd#': 7, 'e': 8, 'f': 9, 'f#': 10, 'g': 11,
                  'g#': 12, 'am': 13, 'a#m': 14, 'bm': 15, 'cm': 16, 'c#m': 17, 'dm': 18, 'd#m': 19, 'em': 20,
                  'fm': 21, 'f#m': 22, 'gm': 23, 'g#m': 24}

    cnv = []

    def __init__(self, datafile=None, c0_array=None, c_array=None):
        """
        :param datafile: The file to which data will be added.
        :param c0_array: A list of cnvs provided by the user.
        :param c_array: A list of cnvs provided by the user.
        """

        self.datafile = datafile
        self.c0_array = c0_array
        self.c_array = c_array
        if datafile is not None:
            self.df = pd.read_csv(self.datafile)

    def add_data(self, total_count):
        """
        Adds a specific number of non-duplicate rows of data to a csv file specified by self.datafile.
        :param total_count: number of rows of data to be added.
        :return: close the file.
        """

        print("Adding data, please wait...")
        df_file = open(self.datafile, 'a', newline='')
        fieldnames = ['C0', 'C1', 'C2', 'C3', 'L']
        chord_writer = csv.DictWriter(df_file, fieldnames=fieldnames)
        ids = []
        current_count = 0
        while current_count < total_count:
            self.make_cnv()
            # creates a unique id for each row
            cnv_id = ''.join([str(self.cnv[0]), str(self.cnv[1]), str(self.cnv[2]), str(self.cnv[3])])
            # prevents duplication by only writing rows with unique ids and storing the ids of written rows
            if cnv_id not in ids:
                chord_writer.writerow({'C0': self.cnv[0],
                                       'C1': self.cnv[1],
                                       'C2': self.cnv[2],
                                       'C3': self.cnv[3],
                                       'L': self.cnv[4]})
                ids.append(cnv_id)
                current_count += 1
            else:
                current_count += 0
            self.cnv.clear()
        print("Done.")
        return df_file.close()

    def make_cnv(self):
        """
        Function responsible for writing every row in the dataset (csv file). First a random progression is created. The
        cnvs in this progression are compared with the cnvs in the start_chord and chord arrays provided by the user.
        Based on the commonality between the random progression and the user provided chords, an arbitrary score is
        assigned to the progression.
        :return: add the final value of the score to row
        """

        self.cnv = random.sample(range(1, 25), 4)
        self.c_array = random.sample(self.c_array, len(self.c_array))
        score = float(0)
        common = [i for i in self.cnv[1:] if i in self.c_array]
        if self.cnv[0] in self.c0_array:
            score += 0.25
        elif self.cnv[0] not in self.c0_array:
            score -= 0.25
        for i in range(len(common)):
            score += 0.25
        if score > 1:
            score = 1
        elif score < 0:
            score = 0
        return self.cnv.append(score)

    def make_prog(self):
        """
        Currently unused function, creates a chord progression based on the most common chords in a dataset.
        """

        self.cnv.clear()
        cdf = self.df[self.df.L != 0]
        c0 = cdf['C0'].value_counts().idxmax()
        c1 = cdf['C1'].value_counts().idxmax()
        c2 = cdf['C2'].value_counts().idxmax()
        c3 = cdf['C3'].value_counts().idxmax()
        self.cnv.extend([c0, c1, c2, c3])

    def play_prog(self):
        """
        Plays a user provided chord progression.
        """

        serial_number = range(47845, 47869)
        chord_number = range(1, 25)
        for i in self.cnv:
            # Look for matching audio files and play them.
            try:
                filename = "audio files/{}__{}.wav".format(serial_number[i-1], chord_number[i-1])
                playsound.playsound(filename)
            except FileNotFoundError:
                print('Error: audio files not found.')

    @staticmethod
    def to_cnv(chord_list):
        """
        Converts chords provided in a string format to corresponding integers.
        :param chord_list: list of chords in string format.
        :return: a list containing a list of converted chords and errors.
        """

        cnv_list = []
        err_list = []
        for c in chord_list:
            if c in ProgPred.chord_dict.keys():
                cnv_list.append(ProgPred.chord_dict[c])
            elif c not in ProgPred.chord_dict.keys():
                err_list.append(''.join(["#" if x == "s" else x for x in c]))
        return [cnv_list, err_list]


class ProgTest:
    """
    This class contains the machine learning algorithm and methods to format and count data in the dataset.
    """

    def __init__(self, df, test_array=None):
        """
        Formats the dataset to make in compatible with the Ridge model and also does rudimentary cross-validation.
        :param df: The provided dataset.
        :param test_array: User provided chord progression.
        """

        self.df = pd.read_csv(df)
        self.df.drop_duplicates(keep='first', inplace=True)
        self.test_array = test_array
        # select X and y from the dataset
        self.X = np.asanyarray(self.df[['C0', 'C1', 'C2', 'C3']])
        self.y = np.asanyarray(self.df['L'])
        c = [i for i in range(1, 25)]
        # one hot encoding
        self.enc = preprocessing.OneHotEncoder(categories=[c, c, c, c], handle_unknown='ignore').fit(self.X)
        self.X = self.enc.transform(self.X)
        # cross-validating
        self.X_train, self.X_test, self.y_train, self.y_test = model_selection.train_test_split(self.X, self.y,
                                                                                                test_size=0.2,
                                                                                                random_state=4)

    def data_count(self):
        """
        Returns the number of rows of data in the dataset.
        :return: number of rows of data
        """

        shp = self.df.shape
        row_count = shp[0]
        return row_count

    def predict(self):
        """
        This function creates a Ridge Regression model and trains and tests it with the provided dataset. Then the model
        predicts with the user provided chords and returns the result.
        :return: a list containing the output of the model and information about the model.
        """

        # reshape test_array since it is a single row of data
        user_array = np.asanyarray(self.test_array).reshape(1, -1)
        # one hot encode user_array
        self.enc.fit(user_array)
        user_array = self.enc.transform(user_array)
        # create, train and predict the model with the dataset
        model = ("Ridge", linear_model.Ridge(alpha=0.01, random_state=4))
        model[1].fit(self.X_train, self.y_train)
        y_pred = model[1].predict(self.X_test)
        # predict with user provided chords
        y_usr = model[1].predict(user_array)
        if y_usr[0] < 0:
            y_usr[0] = 0
        acc = metrics.r2_score(self.y_test, y_pred)
        output = "I am {}% sure that you like this progression.".format('%.2f' % (100 * y_usr[0]))
        model_info = "Predicted using a {} model with {} accuracy from {} data samples.".format(model[0], '%.3f' % acc,
                                                                                                self.data_count())
        return [output, model_info]
