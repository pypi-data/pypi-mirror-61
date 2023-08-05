import re
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression

from .transform import WOETransformer, Combiner, ELSE_GROUP, EMPTY_BIN
from .utils import to_ndarray, bin_by_splits, save_json, read_json


RE_NUM = r'-?\d+(.\d+)?'
RE_SEP = r'[~-]'
RE_BEGIN = r'(-inf|{num})'.format(num = RE_NUM)
RE_END = r'(inf|{num})'.format(num = RE_NUM)
RE_RANGE = r'\[{begin}\s*{sep}\s*{end}\)'.format(
    begin = RE_BEGIN,
    end = RE_END,
    sep = RE_SEP,
)


NUMBER_EMPTY = -9999999
NUMBER_INF = 1e10
FACTOR_EMPTY = 'MISSING'
FACTOR_UNKNOWN = 'UNKNOWN'



class ScoreCard(BaseEstimator):
    def __init__(self, pdo = 60, rate = 2, base_odds = 35, base_score = 750,
        card = None, combiner = {}, transer = None, **kwargs):
        """

        Args:
            card (dict|str|IOBase): dict of card or io to read json
            combiner (toad.Combiner)
            transer (toad.WOETransformer)
        """
        self.pdo = pdo
        self.rate = rate
        self.base_odds = base_odds
        self.base_score = base_score

        self.factor = pdo / np.log(rate)
        self.offset = base_score - self.factor * np.log(base_odds)

        self.combiner = combiner
        self.transer = transer
        self.model = LogisticRegression(**kwargs)

        if card is not None:
            self.generate_card(card = card)
        
    @property
    def coef_(self):
        """ coef of LR model
        """
        return self.weight


    def generate_card(self, card = None):
        """

        Args:
            card (dict|str|IOBase): dict of card or io to read json
        """
        if card is not None:
            if not isinstance(card, dict):
                card = read_json(card)

            return self.set_card(card)


        rules = self._get_rules(self.combiner, self.transer)
        self.set_combiner(rules)

        map = self.generate_map(self.transer, self.model)
        self.set_score(map)

        return self


    def fit(self, X, y):
        """
        Args:
            X (2D DataFrame)
            Y (array-like)
        """
        self.features_ = X.columns.tolist()

        for f in self.features_:
            if f not in self.transer._rules:
                raise Exception('column \'{f}\' is not in transer'.format(f = f))

        self.model.fit(X, y)

        self.generate_card()

        return self


    def _transer_to_rules(self, transer):
        c = dict()
        for k in transer._rules:
            c[k] = np.reshape(transer._rules[k]['value'], (-1, 1)).tolist()

        return c


    def _merge_combiner(self, cbs):
        res = dict()
        for item in cbs[::-1]:
            if isinstance(item, Combiner):
                item = item.export()

            res.update(item)

        return res


    def _get_rules(self, combiner, transer):
        transer_rules = self._transer_to_rules(transer)

        if isinstance(combiner, list):
            combiner = self._merge_combiner(combiner)
        elif isinstance(combiner, Combiner):
            combiner = combiner.export()

        if self._check_rules(combiner, transer_rules):
            transer_rules.update(combiner)

        return transer_rules


    def _check_rules(self, combiner, transer):
        for col in combiner:
            if col not in transer:
                continue

            l_c = len(combiner[col])
            l_t = len(transer[col])

            if l_c == 0:
                continue

            if isinstance(combiner[col][0], (int, float)):
                if l_c != l_t - 1:
                    raise Exception('column \'{col}\' is not matched, assert {l_t} bins but given {l_c}'.format(col = col, l_t = l_t, l_c = l_c + 1))
            else:
                if l_c != l_t:
                    raise Exception('column \'{col}\' is not matched, assert {l_t} bins but given {l_c}'.format(col = col, l_t = l_t, l_c = l_c))

        return True


    def _parse_range(self, bins):
        exp = re.compile(RE_RANGE)

        l = list()
        for item in bins:
            if item == 'nan':
                l.append(np.nan)
                continue
            
            m = exp.match(item)

            # if is not range
            if m is None:
                return None

            # get the end number of range
            split = m.group(3)
            if split == 'inf':
                split = np.inf
            else:
                split = float(split)

            l.append(split)

        return np.array(l)


    def _parse_card(self, card):
        bins = card.keys()
        scores = card.values()
        scores = np.array(list(scores))

        groups = self._parse_range(bins)
        # if is continuous
        if groups is not None:
            ix = np.argsort(groups)
            scores = scores[ix]
            groups = groups[ix[:-1]]
        else:
            groups = list()
            for item in bins:
                if item == ELSE_GROUP:
                    groups.append(item)
                else:
                    groups.append(item.split(','))
            groups = np.array(groups)

        return groups, scores


    def set_card(self, card):
        """set card dict
        """
        combiner = dict()
        map = dict()
        for feature in card:
            bins, scores = self._parse_card(card[feature])
            combiner[feature] = bins
            map[feature] = scores

        self.set_combiner(combiner)
        self.set_score(map)

        return self


    def set_combiner(self, combiner):
        """set combiner
        """
        if not isinstance(combiner, Combiner):
            combiner = Combiner().load(combiner)

        self.combiner = combiner


    def set_score(self, map):
        """set score map by dict
        """
        sm = dict()
        for key in map:
            s = map[key]
            if isinstance(s, np.ndarray):
                sm[key] = np.copy(s)
            else:
                sm[key] = np.array(s)

        self.score_map = sm


    def predict(self, X, **kwargs):
        """predict score
        Args:
            X (2D array-like): X to predict
            return_sub (bool): if need to return sub score, default `False`

        Returns:
            array-like: predicted score
            DataFrame: sub score for each feature
        """
        select = list(self.score_map.keys())
        bins = self.combine(X[select])
        return self.bin_to_score(bins, **kwargs)

    def proba_to_score(self, prob):
        """covert probability to score
        """
        odds = (1 - prob) / prob
        return self.factor * np.log(odds) + self.offset

    def combine(self, X):
        return self.combiner.transform(X)


    def bin_to_score(self, bins, return_sub = False):
        """predict score from bins
        """
        res = bins.copy()
        for col in self.score_map:
            s_map = self.score_map[col]
            b = bins[col].values
            # set default group to min score
            b[b == EMPTY_BIN] = np.argmin(s_map)
            # replace score
            res[col] = s_map[b]

        score = np.sum(res.values, axis = 1)

        if return_sub is False:
            return score

        return score, res

    def woe_to_score(self, woe, weight = None):
        """calculate score by woe
        """
        woe = to_ndarray(woe)

        if weight is None:
            weight = self.weight

        b = self.offset - self.factor * self.bias
        s = -self.factor * weight * woe

        # drop score whose weight is 0
        mask = 1
        if isinstance(weight, np.ndarray):
            mask = (weight != 0).astype(int)

        return (s + b / self.n_features_) * mask


    def set_model(self, model):
        """set logistic regression model
        """
        self.weight = model.coef_[0]
        self.bias = model.intercept_[0]
        self.n_features_ = (self.weight != 0).sum()


    def generate_map(self, transer, model):
        """calculate score map by woe
        """
        self.set_model(model)

        s_map = dict()
        for i, k in enumerate(self.features_):
            weight = self.weight[i]
            # skip feature whose weight is 0
            if weight == 0:
                continue

            woe = transer._rules[k]['woe']
            s_map[k] = self.woe_to_score(woe, weight = weight)

        return s_map


    def export(self, to_frame = False, to_json = None, to_csv = None, decimal = 2):
        """generate a scorecard object

        Args:
            to_frame (bool): return DataFrame of card
            to_json (str|IOBase): io to write json file
            to_csv (filepath|IOBase): file to write csv

        Returns:
            dict
        """
        card = dict()
        combiner = self.combiner.export(format = True)

        for col in self.score_map:
            bins = combiner[col]
            card[col] = dict()

            for i in range(len(bins)):
                card[col][bins[i]] = round(self.score_map[col][i], decimal)

        if to_json is not None:
            save_json(card, to_json)

        if to_frame or to_csv is not None:
            rows = list()
            for name in card:
                for value, score in card[name].items():
                    rows.append({
                        'name': name,
                        'value': value,
                        'score': score,
                    })

            card = pd.DataFrame(rows)


        if to_csv is not None:
            return card.to_csv(to_csv)

        return card



    def _generate_testing_frame(self, maps, size = 'max', mishap = True, gap = 1e-2):
        """
        Args:
            maps (dict): map of values or splits to generate frame
            size (int|str): size of frame. 'max' (default), 'lcm'
            mishap (bool): is need to add mishap patch to test frame
            gap (float): size of gap for testing border

        Returns:
            DataFrame
        """
        number_patch = np.array([NUMBER_EMPTY, NUMBER_INF])
        factor_patch = np.array([FACTOR_EMPTY, FACTOR_UNKNOWN])

        values = []
        cols = []
        for k, v in maps.items():
            v = np.array(v)
            if np.issubdtype(v.dtype, np.number):
                items = np.concatenate((v, v - gap))
                patch = number_patch
            else:
                # remove else group
                mask = np.argwhere(v == ELSE_GROUP)
                if mask.size > 0:
                    v = np.delete(v, mask)

                items = np.concatenate(v)
                patch = factor_patch

            if mishap:
                # add patch to items
                items = np.concatenate((items, patch))

            cols.append(k)
            values.append(np.unique(items))

        # calculate length of values in each columns
        lens = [len(x) for x in values]

        # get size
        if isinstance(size, str):
            if size == 'lcm':
                size = np.lcm.reduce(lens)
            else:
                size = np.max(lens)

        stacks = dict()
        for i in range(len(cols)):
            l = lens[i]
            # generate indexes of value in column
            ix = np.arange(size) % l
            stacks[cols[i]] = values[i][ix]

        return pd.DataFrame(stacks)

    def testing_frame(self, **kwargs):
        """get testing frame with score

        Returns:
            DataFrame: testing frame with score
        """
        maps = self.combiner.export()

        frame = self._generate_testing_frame(maps, **kwargs)
        frame['score'] = self.predict(frame)

        return frame
