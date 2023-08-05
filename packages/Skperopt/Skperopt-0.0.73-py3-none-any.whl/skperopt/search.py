import copy
import datetime
from random import shuffle
import random as rnd
import numpy
import pandas
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score
from sklearn.metrics import mean_squared_error
from hyperopt.base import STATUS_SUSPENDED
from hyperopt.base import STATUS_OK
from hyperopt.base import Trials
from hyperopt.fmin import fmin
from hyperopt import tpe
from hyperopt import hp
from sklearn.model_selection import StratifiedKFold, KFold, train_test_split


def get_splitter(score_type):
    if score_type in ["f1", "auc", "accuracy"]:
        return stratifiedkfold
    else:
        return kfold


def return_score_type(scorer):
    if scorer in ["f1", "auc", "accuracy"]:
        return "classification"
    else:
        return "regression"


def stratifiedkfold(X, y, splits):
    skf = StratifiedKFold(n_splits=splits)

    for train_index, test_index in skf.split(X, y):
        X_train = X.loc[train_index]
        X_test = X.loc[test_index]  #
        y_train = y.loc[train_index]
        y_test = y.loc[test_index]  #

        yield X_train, X_test, y_train, y_test


def kfold(X, y, splits):
    kf = KFold(n_splits=splits)

    for train_index, test_index in kf.split(X, y):
        X_train = X.loc[train_index]
        X_test = X.loc[test_index]  #
        y_train = y.loc[train_index]
        y_test = y.loc[test_index]  #

        yield X_train, X_test, y_train, y_test


def check_scorer(est, scorer):
    est_score = return_score_type(est.scorer)
    scorerclas = return_score_type(scorer)

    if est_score == scorerclas:
        return scorer
    elif est_score != scorerclas:
        return est.scorer


def get_default_split_type(est_type):
    if est_type.lower() == "classification".lower():
        return "stratified"
    elif est_type.lower() == "regression".lower():
        return "kfold"


def change_to_df(df):
    """Makes sure that the input data is dataframe format if not it is converted
    also makes sure that the column names are in string format"""
    if not hasattr(df, "iloc") or hasattr(df, "unique"):
        df = pandas.DataFrame(df)
    df.columns = [str(x) for x in df.columns.tolist()]
    return df


def cross_validation(est, X, y, cv=10, cv_times=1, scorer=None, fold_type=None, random=False, randomState=1, holdout=0):
    X = change_to_df(X)
    y = change_to_df(y)
    ans = []

    if scorer == None:
        scorer = est.scorer

    if fold_type == None:
        fold_type = get_default_split_type(return_score_type(scorer))

    if holdout > 0:
        X, holdX, y, holdy = train_test_split(X, y, test_size=holdout, random_state=10)

    for cv_time in range(cv_times):

        if random or cv_times > 0:
            randomState += 10
            X = X.sample(len(X), random_state=randomState)
            y = y.loc[X.index]  #

        for X_train, X_test, y_train, y_test in get_splitter(fold_type)(X, y, cv):
            est.fit(X_train, y_train)
            pred = est.predict(X_test, y_test)
            score = get_score(y_test, pred, scorer)
            ans.append(score)

    score = numpy.mean(ans)

    if holdout > 0:
        est.fit(X, y)
        pred = est.predict(holdX)
        holdscore = get_score(holdy, pred, scorer)
        return numpy.mean([score, holdscore])
    else:
        return score


def scorer_is_better(test_type, new_score, old_score):
    if type(test_type) == list:
        test_type = test_type[0]

    if test_type in ["f1", "auc", "accuracy"]:
        if old_score <= new_score:
            return True
        else:
            return False
    else:
        if old_score >= new_score:
            return True
        else:
            return False


def get_score(y_true, y_pred, scorer):
    """
    Get score from predicitons and true Y data
    :param y_true:
    :param y_pred:
    :param scorer:
    :return:
    """
    score_list = []

    if type(scorer) == str:
        scorer = [scorer]

    for score_type in scorer:
        if score_type == "f1":
            score_list.append(f1_score(y_true, y_pred, average='macro'))
        elif score_type == "rmse":
            score_list.append(mean_squared_error(y_true, y_pred, squared=False))
        elif score_type == "mse":
            score_list.append(mean_squared_error(y_true, y_pred, squared=True))
        elif score_type == "auc":
            try:
                score_list.append(roc_auc_score(y_true, y_pred, average="macro"))
            except:
                score_list.append(roc_auc_score(y_true, y_pred, average="ovo"))
        elif score_type == "accuracy":
            score_list.append(accuracy_score(y_true, y_pred))
        else:
            return None
    return numpy.mean(score_list)


def create_hyper(paramgrid):
    new_grid = {}
    for k, v in paramgrid.items():
        new_grid[k] = hp.choice(k, v)
    return new_grid


class HyperSearch:
    """
    A parameter searing algorithm wrapper that uses TPE to search for the best parameters,
    implements early stopping. Accepts sklearn style estimators as the input EST

    :param est:            class: sklearn style estimator
    :param X:              X data
    :param y:              y data
    :param iters:          number of iterations of searches to try - default 500 = no time contraint
    :param time_to_search: max time in seconds to try searching  - default None = no time contraint
    :param cv:             the number of folds to base the score on
    :param cv_times:       The number of times to randomly select data and perform cross validation (higher = reduced variance)
    :param scorer:         the scoring method used
    :param verbose:        show information? 0 = no, > 0 increases verboseness
    :param params:         parameter grid - if a mltooler.SelfImprovingEstimator passed then none needed

    Run with:
        HyperSearch.search()

    Once complete gather the best parameter grid with:
        HyperSearch.best_params

    View run stats with:
        HyperSearch.stats

    """

    def __init__(self, est, X, y, params=None, iters=500, time_to_search=None, cv=5, cv_times=1, scorer="f1", verbose=1,
                 random=False, foldtype="Kfold"):

        # check and get skiperopt style parameters
        if params == None and not hasattr(est, "param_grid"):
            raise ValueError("No parameters supplied")
        else:
            params = est.param_grid

        self.params = params
        self.best_params = None
        self.__space = create_hyper(params)
        self.__initparams = est.get_params()
        # set hyper settings
        self.__algo = tpe.suggest
        self.__trial = Trials()

        # set run settings
        self.verbose = verbose
        self.iters = iters
        self.cv = cv
        self.cv_times = cv_times
        self.scorer = scorer
        self.__run = 0

        self.est = est

        self.stats = {}
        self.__init_score = cross_validation(self.est, X, y, cv=self.cv, scorer=self.scorer)
        self.best_score = self.__init_score

        self.__X = X
        self.__y = y

        self.__start_now = None

        self.__runok = True
        self.time_to_search = time_to_search

        self.random = random
        self.foldtype = foldtype

    def __objective(self, params):
        """Objective function for Gradient Boosting Machine Hyperparameter Tuning"""

        if self.__runok:
            est = copy.deepcopy(self.est)
            try:

                est.set_params(**params)
                best_score = cross_validation(est, self.__X, self.__y,
                                              cv=self.cv, scorer=self.scorer,
                                              random=self.random)
                if self.verbose > 1:
                    print(f"Current score = {best_score} and best score = {self.best_score}")

                # Loss must be minimized
                if self.scorer in ["f1", "auc", "accuracy"]:
                    loss = 1 - best_score
                else:
                    loss = best_score

                # check if the latest score is best?
                if scorer_is_better(self.scorer, best_score, self.best_score):
                    if self.verbose > 0 and best_score != self.best_score:
                        print(f"New Best Found - {best_score}")
                    self.best_score = copy.copy(best_score)
                    self.best_params = params
                # log in the stats dict
                self.stats[self.__run] = copy.copy(self.best_score)
                self.__run += 1

                # get finish time
                now_fin = datetime.datetime.now()
                if self.time_to_search is not None and (now_fin - self.__start_now).seconds > self.time_to_search:
                    if self.verbose > 0:
                        print("Random parameter search stopped early due to time overlapse")
                    self.__runok = False

                # return score or if early stopping has been initiated then return POOR score
                return {'loss': loss, 'params': params, 'status': STATUS_OK}
            except:
                return {'loss': 9999, 'params': params, 'status': STATUS_SUSPENDED}
        else:
            return {'loss': 9999, 'params': params, 'status': STATUS_SUSPENDED}

    def __reset(self):
        # When a new search is initiated then reset all the scores
        self.stats = {}
        self.__run = 0
        self.__init_score = cross_validation(self.est, self.__X, self.__y, cv=self.cv, cv_times=self.cv_times, scorer=self.scorer)
        self.best_score = self.__init_score
        if self.verbose > 0:
            print(f"Initial Score is {self.best_score}")

    def search(self):
        """
        Search the parameter grid
        """
        self.__start_now = datetime.datetime.now()
        self.__reset()

        if self.verbose > 0:
            print("Starting HyperOpt Parameter Search")

        best = fmin(fn=self.__objective, space=self.__space, algo=self.__algo,
                    max_evals=self.iters, trials=self.__trial, verbose=self.verbose,
                    timeout=self.time_to_search)

        if self.verbose > 0:
            print("Finished HyperOpt Parameter Search")

        if self.best_score > self.__init_score:
            self.best_params = self.__trial.best_trial["result"]["params"]
        else:
            self.best_params = self.__initparams
