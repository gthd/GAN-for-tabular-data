from __future__ import annotations

import gc
from typing import Tuple
import logging

from abc import ABC, abstractmethod
import pandas as pd

__author__ = "Insaf Ashrapov"
__copyright__ = "Insaf Ashrapov"
__license__ = "Apache 2.0"


class SampleData(ABC):
    """
        Factory method for different sampler strategies. The goal is to generate more train data
        which should be more close to test, in other word we trying to fix uneven distribution.
    """

    @abstractmethod
    def get_object_generator(self):
        """
        Getter for object sampler aka generator, which is not a generator
        """
        raise NotImplementedError

    def generate_data_pipe(self, train_df, target, test_df) -> pd.DataFrame:
        """
        Defines logic for sampling
        """
        generator = self.get_object_generator()
        train_df, target, test_df = generator.preprocess_data(train_df, target, test_df)
        new_train, new_target = generator.generate_data(train_df, target, test_df)
        new_train, new_target = generator.postprocess_data(new_train, new_target, test_df)
        new_train, new_target = generator.adversarial_filtering(new_train, new_target, test_df)
        gc.collect()
        return new_train, new_target


class Sampler(ABC):
    """
        Interface for each sampling strategy
    """

    def get_generated_shape(self, input_df):
        """
        Calcs final output shape
        """
        if self.gen_x_times <= 0:
            raise ValueError("Passed gen_x_times = {} should be bigger than 0".format(self.gen_x_times))
        return int(self.gen_x_times * input_df.shape[0] / input_df.shape[0])

    @abstractmethod
    def preprocess_data(self, train_df, target, test_df, ):
        """Before we can start data generation we might need some preprosing, numpy to pandas
        and etc"""
        raise NotImplementedError

    @abstractmethod
    def generate_data(self, train_df, target, test_df):
        raise NotImplementedError

    @abstractmethod
    def postprocess_data(self, train_df, target, test_df, ):
        """Filtering data which far beyond from test_df data distribution"""
        raise NotImplementedError

    def adversarial_filtering(self, train_df, target, test_df, ):
        raise NotImplementedError
