import numpy as np
from typing import Optional
from py.davidlynchnumbers import DavidLynchNumbers

master_dln = DavidLynchNumbers()
starting_pick = 400


class DavidLynchPredictor:
    """A class for doing prediction experiments with the DavidLynchNumbers class"""
    def __init__(self, starting_pick: Optional[int] = 400, training_proportion: float = 0.75) -> None:
        """For initialising the object.
        Args:
            starting_pick: the draw at which we start"""
        self.starting_pick = starting_pick
        self.training_proportion = training_proportion
        self.master_dln = DavidLynchNumbers()

    def test_random_predictions(self, function_name: str):
        """for testing the success of predicting randomly."""
        predictions = []
        is_correct_prediction = []
        for i in range(self.starting_pick, len(self.master_dln.numbers) - 1):
            train = master_dln.numbers[:i]
            prediction = getattr(DavidLynchNumbers(numbers=train), function_name)()
            predictions.append(prediction)
            is_correct_prediction.append(prediction == master_dln.numbers[i + 1])
        accuracy = sum(is_correct_prediction) / len(is_correct_prediction)
        return accuracy

    def test_uniform_predictions(self):
        accuracy = self.test_random_predictions('predict_random_uniform')
        return accuracy

    def test_longest_not_picked(self):
        accuracy = self.test_random_predictions('predict_longest_not_picked')
        return accuracy


dlp = DavidLynchPredictor(starting_pick=400)
a = dlp.test_random_predictions()
