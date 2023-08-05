import math
import copy
import numpy as np
import pandas as pd
from functools import wraps
from sklearn.base import TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingClassifier


from .stats import WOE, probability
from .merge import merge
from .utils.func import to_ndarray, np_count, bin_by_splits, split_target
from .utils.decorator import frame_exclude, select_dtypes
from .utils.mixin import SaveMixin, DEFAULT_NAME

EMPTY_BIN = -1
ELSE_GROUP = 'else'


class Transformer(TransformerMixin, SaveMixin):
    """Base class for transformers
    """

    _fit_frame = False

    @property
    def _rules_counts(self):
        return len(self._rules.keys())

    @property
    def _fitted(self):
        return self._rules_counts > 0


    @frame_exclude(is_class = True)
    @select_dtypes(is_class = True)
    def fit(self, X, *args, update = False, **kwargs):
        """fit method, see details in `fit_` method
        """
        dim = getattr(X, 'ndim', 1)

        rules = {}

        if self._fit_frame:
            rules = self.fit_(X, *args, **kwargs)

        elif dim == 1:
            name = getattr(X, 'name', DEFAULT_NAME)
            rules[name] = self.fit_(X, *args, **kwargs)

        else:
            if len(args) > 0:
                X, y = split_target(X, args[0])
                args = (y, *args[1:])
            if 'y' in kwargs:
                X, kwargs['y'] = split_target(X, kwargs['y'])

            for col in X:
                name = X[col].name
                rules[name] = self.fit_(X[col], *args, **kwargs)

        if update:
            self._rules.update(rules)
        else:
            self._rules = rules

        return self


    def transform(self, X, *args, **kwargs):
        """transform method, see details in `transform_` method
        """
        if not self._fitted:
            return self._raiseUnfitted()


        if self._fit_frame:
            return self.transform_(self._rules, X, *args, **kwargs)

        if getattr(X, 'ndim', 1) == 1:
            if self._rules_counts == 1:
                rule = next(iter(self._rules.values()))
                return self.transform_(rule, X, *args, **kwargs)
            elif hasattr(X, 'name') and X.name in self._rules:
                return self.transform_(self._rules[X.name], X, *args, **kwargs)
            else:
                return X

        res = X.copy()
        for key in X:
            if key in self._rules:
                res[key] = self.transform_(self._rules[key], X[key], *args, **kwargs)

        return res


    def _raiseUnfitted(self):
        raise Exception('transformer is unfitted yet!')



class WOETransformer(Transformer):
    """WOE transformer
    """

    def fit_(self, X, y):
        """fit WOE transformer

        Args:
            X (DataFrame|array-like)
            y (str|array-like)
            select_dtypes (str|numpy.dtypes): `'object'`, `'number'` etc. only selected dtypes will be transform
        """
        X = to_ndarray(X)

        value = np.unique(X)
        l = len(value)
        woe = np.zeros(l)

        for i in range(l):
            y_prob, n_prob = probability(y, mask = (X == value[i]))

            woe[i] = WOE(y_prob, n_prob)

        return {
            'value': value,
            'woe': woe,
        }

    def transform_(self, rule, X, default = 'min'):
        """transform function for single feature

        Args:
            X (array-like)
            default (str): 'min'(default), 'max' - the strategy to be used for unknown group

        Returns:
            array-like
        """
        X = to_ndarray(X)
        res = np.zeros(len(X))

        value = rule['value']
        woe = rule['woe']

        if default == 'min':
            default = np.min(woe)
        elif default == 'max':
            default = np.max(woe)

        # replace unknown group to default value
        res[np.isin(X, value, invert = True)] = default

        for i in range(len(value)):
            res[X == value[i]] = woe[i]

        return res

    def _format_rule(self, rule):
        return dict(zip(rule['value'], rule['woe']))

    def _parse_rule(self, rule):
        return {
            'value': np.array(list(rule.keys())),
            'woe': np.array(list(rule.values())),
        }



class Combiner(Transformer):
    """Combiner for merge data
    """

    def fit_(self, X, y = None, method = 'chi', empty_separate = False, **kwargs):
        """fit combiner

        Args:
            X (DataFrame|array-like): features to be combined
            y (str|array-like): target data or name of target in `X`
            method (str): the strategy to be used to merge `X`, same as `.merge`, default is `chi`
            n_bins (int): counts of bins will be combined
            empty_separate (bool): if need to combine empty values into a separate group
        """
        X = to_ndarray(X)

        if y is not None:
            y = to_ndarray(y)


        if not np.issubdtype(X.dtype, np.number):
            # transform raw data by woe
            transer = WOETransformer()
            woe = transer.fit_transform(X, y)
            # find unique value and its woe value
            uni_val, ix_val = np.unique(X, return_index = True)
            uni_woe = woe[ix_val]
            # sort value by woe
            ix = np.argsort(uni_woe)
            # sort unique value
            uni_val = uni_val[ix]
            # replace X by sorted index
            X = self._raw_to_bin(X, uni_val)

            _, splits = merge(X, target = y, method = method, return_splits = True, **kwargs)

            return self._covert_splits(uni_val, splits)
        

        mask = pd.isna(X)
        if mask.any() and empty_separate:
            X = X[~mask]
            y = y[~mask]
        
        _, splits = merge(X, target = y, method = method, return_splits = True, **kwargs)

        if mask.any() and empty_separate:
            splits = np.append(splits, np.nan)
        
        return splits


    def transform_(self, rule, X, labels = False, **kwargs):
        """transform X by combiner

        Args:
            X (DataFrame|array-like): features to be transformed
            labels (bool): if need to use labels for resulting bins, `False` by default

        Returns:
            array-like
        """
        X = to_ndarray(X)

        # if is not continuous
        if rule.ndim > 1 or not np.issubdtype(rule.dtype, np.number):
            bins = self._raw_to_bin(X, rule)

        else:
            bins = np.zeros(len(X), dtype = int)

            if len(rule):
                # empty to a separate group
                if np.isnan(rule[-1]):
                    mask = pd.isna(X)
                    bins[~mask] = bin_by_splits(X[~mask], rule[:-1])
                    bins[mask] = len(rule)
                else:
                    bins = bin_by_splits(X, rule)

        if labels:
            formated = self._format_splits(rule, index = True)
            empty_mask = (bins == EMPTY_BIN)
            bins = formated[bins]
            bins[empty_mask] = EMPTY_BIN

        return bins


    def _covert_splits(self, value, splits):
        """covert combine rules to array
        """
        if value is False:
            return splits

        if isinstance(value, np.ndarray):
            value = value.tolist()

        start = 0
        l = list()
        for i in splits:
            i = math.ceil(i)
            l.append(value[start:i])
            start = i

        l.append(value[start:])

        return np.array(l)


    def _raw_to_bin(self, X, splits):
        """bin by splits

        Args:
            X (array-like): feature to be combined
            splits (array-like): splits of `X`

        Returns:
            array-like
        """
        # set default group to EMPTY_BIN
        bins = np.full(X.shape, EMPTY_BIN)
        for i in range(len(splits)):
            group = splits[i]
            # if group is else, set all empty group to it
            if isinstance(group, str) and group == ELSE_GROUP:
                bins[bins == EMPTY_BIN] = i
            else:
                bins[np.isin(X, group)] = i

        return bins

    def _format_splits(self, splits, index = False):
        l = list()
        if np.issubdtype(splits.dtype, np.number):
            has_empty = len(splits) > 0 and np.isnan(splits[-1])
            
            if has_empty:
                splits = splits[:-1]
            
            sp_l = [-np.inf] + splits.tolist() + [np.inf]
            for i in range(len(sp_l) - 1):
                l.append('['+str(sp_l[i])+' ~ '+str(sp_l[i+1])+')')
            
            if has_empty:
                l.append('nan')
        else:
            for keys in splits:
                if isinstance(keys, str) and keys == ELSE_GROUP:
                    l.append(keys)
                else:
                    l.append(','.join(keys))

        if index:
            indexes = [i for i in range(len(l))]
            l = ["{}.{}".format(ix, lab) for ix, lab in zip(indexes, l)]

        return np.array(l)


    def set_rules(self, map, reset = False):
        """set rules for combiner

        Args:
            map (dict|array-like): map of splits
            reset (bool): if need to reset combiner

        Returns:
            self
        """
        import warnings
        warnings.warn(
            """`combiner.set_rules` will be deprecated soon,
                use `combiner.load(rules, update = False)` instead!
            """,
            DeprecationWarning,
        )


        self.load(map, update = not reset)

        return self

    def _parse_rule(self, rule):
        return np.array(rule)

    def _format_rule(self, rule, format = False):
        if format:
            rule = self._format_splits(rule)

        return rule.tolist()




class GBDTTransformer(Transformer):
    """GBDT transformer
    """
    _fit_frame = True

    def __init__(self):
        self.gbdt = None
        self.onehot = None


    def fit_(self, X, y, **kwargs):
        """fit GBDT transformer

        Args:
            X (DataFrame|array-like)
            y (str|array-like)
            select_dtypes (str|numpy.dtypes): `'object'`, `'number'` etc. only selected dtypes will be transform,
        """

        if isinstance(y, str):
            X = X.copy()
            y = X.pop(y)

        gbdt = GradientBoostingClassifier(**kwargs)
        gbdt.fit(X, y)

        X = gbdt.apply(X)
        X = X.reshape(-1, X.shape[1])

        onehot = OneHotEncoder().fit(X)

        return {
            'gbdt': gbdt,
            'onehot': onehot,
        }


    def transform_(self, rules, X):
        """transform woe

        Args:
            X (DataFrame|array-like)

        Returns:
            array-like
        """
        X = rules['gbdt'].apply(X)
        X = X.reshape(-1, X.shape[1])
        res = rules['onehot'].transform(X).toarray()
        return res
