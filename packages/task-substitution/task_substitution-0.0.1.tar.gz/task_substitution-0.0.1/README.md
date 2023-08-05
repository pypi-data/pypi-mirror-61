# task_substitution
> Solve an auxiliary task using ML.


### This library was created by using [nbdev](https://github.com/fastai/nbdev), please check it out.

**Task Substitution** is a method of solving an auxiliary problem ( with different features and different target ) in order to better understand the initial problem and solving it efficiently. 

Let's take a look at standard machine learning task, in the figure below you see a regression task with features `f1`, `f2`, `f3` and target variable `y`.

<img src="images/training_set.png">

We want to build on a model on the above dataset to predict for unknown `y` values in the test dataset shown below.

<img src="images/test.png">

**Exploratory Data Analysis**

First step we take to solve the problem is to look at the data, there can be many features with *missing values* or *outliers* which needs to be understood. It is possible that there is a relationship between a missing value and values of other features.

## Recover Missing Values

It is possible for a feature to have a missing value, it could be a data recording issue or bug etc. Often times for numerical features we replace missing value with `mean` or `median` value as a approximation. Sometimes we replace missing value with values like `-9999` so that model treats them differently or sometimes we leave them as is as libraries like `xgboost` and `lightgbm` can handle `nulls`. Let's look at following dataset

<img src="images/missing_full.png">

Here we have a feature `f3` with missing values, this is a numerical feature, what we can do is that we can consider `f3` as target feature and reframe this as regresion problem where we try to predict for missing values.

<img src="images/missing_train.png">

<img src="images/missing_test.png">

The above setup is identical to the original regression task, here we would build a model to use `f1` and `f2` to predict for `f3`. So instead of using `mean`, `median` etc. we can build a model to restore missing values which can help us solve the original problem efficiently.

We have to be careful to not overfit when building such models.

## Check Train Test Distributions

Whenever we train a model we want to use it on a new sample, but what if the new sample comes from a different distribution compared to the data on which the model was trained on. When we deploy our solutions on production we want to be very careful of this change as our models would fail if there is a mismatch in train and test sets. We can pose this problem as an auxiliary task and create a new binary target `y`, where `1` represents whether row comes from `test` set and `0` represents whether it comes from `train` set and then we train our model to predict whether a row comes from `train` or `test` set if the performance ( e.g. `AUC` score ) is high we can conclude that the train and test set come from different distributions. Ofcourse, we need to remove the `original target` from the analysis.

<img src="images/ttm_train.png">

<img src="images/ttm_test.png">

**In the above images you can see two different datasets, we want to verify whether these two come from same distributions or not.** 

Consider the first example set as training set and second one as test set for this example.

<img src="images/ttm_train_with_target.png">

<img src="images/ttm_test_with_target.png">

We create a new target called `is_test` which denotes whether a row belongs to test set or not.

<img src="images/ttm_train_test_combined.png">

**Then we combine training and test set and train a model to predict whether a row comes from train or test set, if our model performs well then we know that these two datasets are from different distributions.**

We would still have to dig deep into looking at whether that's the case but the above method can help identifying which features are have drifted apart in train and test datasets. If you look at feature importance of the model that was used to separated train and test apart you can identify such features.

## Install

For an editable install, use the following:

```
git clone https://github.com/numb3r33/task_substitution.git
pip install -e task_substitution
```

## How to use

**Recover Missing Values**

>Currently we only support missing value recovery for numerical features, we plan to extend support for other feature types as well. Also the model currently uses LightGBM model to recover missing values.

```
from task_substitution.recover_missing import *
from sklearn.metrics import mean_squared_error

train = train.drop('original_target', axis=1)

model_args = {
          'objective': 'regression',
          'learning_rate': 0.1,
          'num_leaves': 31,
          'min_data_in_leaf': 100,
          'num_boost_round': 100,
          'verbosity': -1,
          'seed': 41
             }
             
split_args = {
    'test_size': .2,
    'random_state': 41
}

# target_fld: feature with missing values.
# cat_flds: categorical features in the original dataset.
# ignore_flds: features you want to ignore. ( these won't be used by LightGBM model to recover missing values)

rec = RecoverMissing(target_fld='f3',
                     cat_flds=[],
                     ignore_flds=['f2'],
                     perf_fn=lambda tr,pe: np.sqrt(mean_squared_error(tr, pe)),
                     split_args=split_args,
                     model_args=model_args
                    )

train_recovered = rec.run(train)
```

**Check train test distributions**

>We use LightGBM model to predict whether a row comes from test or train distribution.

```
import lightgbm as lgb
from task_substitution.train_test_similarity import *
from sklearn.metrics import roc_auc_score

train = train.drop('original_target', axis=1)

split_args = {'test_size': 0.2, 'random_state': 41}

model_args = {
    'num_boost_round': 100,
    'objective': 'binary',
    'learning_rate': 0.1,
    'num_leaves': 31,
    'nthread': -1,
    'verbosity': -1,
    'seed': 41
}

# cat_flds: categorical features in the original dataset.
# ignore_flds: features you want to ignore. ( these won't be used by LightGBM model )

tts = TrainTestSimilarity(cat_flds=[], 
                          ignore_flds=None,
                          perf_fn=roc_auc_score,
                          split_args=split_args, 
                          model_args=model_args)
tts.run(train, test)

# to get feature importance
fig, ax = plt.subplots(1, figsize=(16, 10)
lgb.plot_importance(tts.trained_model, ax=ax, max_num_features=5, importance_type='gain')
```

## Contributing

If you want to contribute to `task_substitution` please refer to [contributions guidelines](./CONTRIBUTING.md)
