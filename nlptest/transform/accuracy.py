from abc import ABC, abstractmethod
import asyncio
from typing import List

import pandas as pd
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score

from nlptest.utils.custom_types import Sample, MinScoreOutput
from nlptest.modelhandler import ModelFactory


class BaseAccuracy(ABC):
    """
    Abstract base class for implementing accuracy measures.

    Attributes:
        alias_name (str): A name or list of names that identify the accuracy measure.

    Methods:
        transform(data: List[Sample]) -> Any: Transforms the input data into an output based on the implemented accuracy measure.
    """
    alias_name = None

    @staticmethod
    @abstractmethod
    def transform(y_true):
        """
        Abstract method that implements the accuracy measure.

        Args:
            y_true: True values
            y_pred: Predicted values
            model (ModelFactory): Model to be evaluted.

        Returns:
            Any: The transformed data based on the implemented accuracy measure.
        """

        return NotImplementedError

    @staticmethod
    @abstractmethod
    async def run(sample_list: List[Sample], y_true, y_pred) -> List[Sample]:
        return NotImplementedError()

    @classmethod
    async def async_run(cls, sample_list: List[Sample],  y_true, y_pred):
        created_task = asyncio.create_task(cls.run(sample_list, y_true, y_pred))
        return created_task


class MinPrecisionScore(BaseAccuracy):
    """
    Subclass of BaseAccuracy that implements the minimum precision score.

    Attributes:
        alias_name (str): The name "min_precision_score" for config.

    Methods:
        transform(y_true, y_pred) -> Any: Creates accuracy test results.
    """

    alias_name = "min_precision_score"

    @staticmethod
    def transform(y_true, params):
        """
        Computes the minimum F1 score for the given data.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            List[Sample]: Precision test results.
        """
        labels = set(y_true) #.union(set(y_pred))

        if isinstance(params["min_score"], dict):
            min_scores = params["min_score"]
        elif isinstance(params["min_score"], float):
            min_scores = {
                label: params["min_score"] for label in labels
            }

        precision_samples = []
        for k in labels:
            if k not in min_scores.keys():
                continue
            sample = Sample(
                original="-",
                category="accuracy",
                test_type="min_precision_score",
                test_case=k,
                expected_results=MinScoreOutput(min_score=min_scores[k])
            )
            precision_samples.append(sample)
        return precision_samples
    
    async def run(sample_list: List[Sample], y_true, y_pred):
        df_metrics = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        df_metrics.pop("accuracy")
        df_metrics.pop("macro avg")
        df_metrics.pop("weighted avg")
        
        for sample in sample_list:
            if sample.test_case not in df_metrics:
                continue
            precision = df_metrics.get(sample.test_case)
            sample.actual_results=MinScoreOutput(min_score=precision['precision'])
            sample.state = "done"
        
        return sample_list



class MinRecallScore(BaseAccuracy):
    """
    Subclass of BaseAccuracy that implements the minimum precision score.

    Attributes:
        alias_name (str): The name "min_precision_score" for config.

    Methods:
        transform(y_true, y_pred) -> Any: Creates accuracy test results.
    """

    alias_name = "min_recall_score"

    @staticmethod
    def transform(y_true, params):
        """
        Computes the minimum recall score for the given data.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            List[Sample]: Precision recall results.
        """

        labels = set(y_true) #.union(set(y_pred))

        if isinstance(params["min_score"], dict):
            min_scores = params["min_score"]
        elif isinstance(params["min_score"], float):
            min_scores = {
                label: params["min_score"] for label in labels
            }

        rec_samples = []
        for k in labels:
            if k not in min_scores.keys():
                continue
            sample = Sample(
                original="-",
                category="accuracy",
                test_type="min_recall_score",
                test_case=k,
                expected_results=MinScoreOutput(min_score=min_scores[k])
            )
            rec_samples.append(sample)
        return rec_samples

    async def run(sample_list: List[Sample], y_true, y_pred):
        df_metrics = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        df_metrics.pop("accuracy")
        df_metrics.pop("macro avg")
        df_metrics.pop("weighted avg")
        
        for sample in sample_list:
            if sample.test_case not in df_metrics:
                continue
            precision = df_metrics.get(sample.test_case)
            sample.actual_results=MinScoreOutput(min_score=precision['recall'])
            sample.state = "done"
        
        return sample_list

class MinF1Score(BaseAccuracy):
    """
    Subclass of BaseAccuracy that implements the minimum precision score.

    Attributes:
        alias_name (str): The name "min_precision_score" for config.

    Methods:
        transform(y_true, y_pred) -> Any: Creates accuracy test results.
    """

    alias_name = "min_f1_score"

    @staticmethod
    def transform(y_true, params):
        """
        Computes the minimum F1 score for the given data.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            List[Sample]: F1 score test results.
        """

        labels = set(y_true) #.union(set(y_pred))

        if isinstance(params["min_score"], dict):
            min_scores = params["min_score"]
        elif isinstance(params["min_score"], float):
            min_scores = {
                label: params["min_score"] for label in labels
            }

        f1_samples = []
        for k in labels:
            if k not in min_scores.keys():
                continue
            sample = Sample(
                original="-",
                category="accuracy",
                test_type="min_f1_score",
                test_case=k,
                expected_results=MinScoreOutput(min_score=min_scores[k])
            )
            f1_samples.append(sample)
        return f1_samples
    
    async def run(sample_list: List[Sample], y_true, y_pred):
        df_metrics = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        df_metrics.pop("accuracy")
        df_metrics.pop("macro avg")
        df_metrics.pop("weighted avg")
        
        for sample in sample_list:
            if sample.test_case not in df_metrics:
                continue
            f1_scores = df_metrics.get(sample.test_case)
            sample.actual_results=MinScoreOutput(min_score=f1_scores['f1-score'])
            sample.state = "done"
        
        return sample_list


class MinMicroF1Score(BaseAccuracy):
    """
    Subclass of BaseAccuracy that implements the minimum precision score.

    Attributes:
        alias_name (str): The name for config.

    Methods:
        transform(y_true, y_pred) -> Any: Creates accuracy test results.
    """

    alias_name = "min_micro_f1_score"

    @staticmethod
    def transform(y_true, params):
        """
        Computes the minimum F1 score for the given data.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            Any: The transformed data based on the minimum F1 score.
        """

        min_score = params["min_score"]

        # f1 = f1_score(y_true, y_pred, average="micro", zero_division=0)

        sample = Sample(
            original="-",
            category="accuracy",
            test_type="min_micro_f1_score",
            test_case="micro",
            expected_results=MinScoreOutput(min_score=min_score),
            # actual_results=MinScoreOutput(min_score=f1),

            # state="done"
        )

        return [sample]
    
    async def run(sample_list: List[Sample], y_true, y_pred):
        f1 = f1_score(y_true, y_pred, average="micro", zero_division=0)
        for sample in sample_list:
            sample.actual_results=MinScoreOutput(min_score=f1)
            sample.state = "done"
        return sample_list


class MinMacroF1Score(BaseAccuracy):
    """
    Subclass of BaseAccuracy that implements the minimum precision score.

    Attributes:
        alias_name (str): The name "min_precision_score" for config.

    Methods:
        transform(y_true, y_pred) -> Any: Creates accuracy test results.
    """

    alias_name = "min_macro_f1_score"

    @staticmethod
    def transform(y_true, params):
        """
        Computes the minimum F1 score for the given data.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            Any: The transformed data based on the minimum F1 score.
        """

        min_score = params["min_score"]

        sample = Sample(
            original="-",
            category="accuracy",
            test_type="min__macro_f1_score",
            test_case="macro",
            expected_results=MinScoreOutput(min_score=min_score)
        )

        return [sample]
    
    async def run(sample_list: List[Sample], y_true, y_pred):
        f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
        for sample in sample_list:
            sample.actual_results=MinScoreOutput(min_score=f1)
            sample.state = "done"
        return sample_list


class MinWeightedF1Score(BaseAccuracy):
    """
    Subclass of BaseAccuracy that implements the minimum weighted f1 score.

    Attributes:
        alias_name (str): The name for config.

    Methods:
        transform(y_true, y_pred) -> Any: Creates accuracy test results.
    """

    alias_name = "min_weighted_f1_score"

    @staticmethod
    def transform(y_true, params):
        """
        Computes the minimum weighted F1 score for the given data.

        Args:
            y_true: True values
            y_pred: Predicted values   

        Returns:
            Any: The transformed data based on the minimum F1 score.
        """

        min_score = params["min_score"]

        sample = Sample(
            original="-",
            category="accuracy",
            test_type="min_weighted_f1_score",
            test_case="weighted",
            expected_results=MinScoreOutput(min_score=min_score)
        )

        return [sample]
    
    async def run(sample_list: List[Sample], y_true, y_pred):
        f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
        for sample in sample_list:
            sample.actual_results=MinScoreOutput(min_score=f1)
            sample.state = "done"
        return sample_list
