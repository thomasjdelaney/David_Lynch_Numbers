"""For analysing the distribution of David Lynch's daily number draw."""
import os
import platform
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List, Dict
from scipy.stats import chisquare
from scipy.stats.stats import Power_divergenceResult


class DavidLynchNumbers:

    def __init__(self, numbers: Optional[List[int]] = None) -> None:
        """For initialising the object
        Args:
            numbers: We can initialise the object with given numbers."""
        self.numbers: List[int] = numbers
        self.load_numbers(numbers)
        self.days_since_picked: Dict[int, int] = {i: np.NaN for i in range(1, 11)}
        self.set_days_since_picked()
        self.times_picked = {i+1: c for i, c in enumerate(np.bincount(self.numbers).tolist()[1:])}
        self.proportion_picked = {n: tp / len(self.numbers) for n, tp in self.times_picked.items()}

    def load_numbers(self, numbers: Optional[List[int]] = None) -> None:
        """For loading the numbers.
        Args:
            numbers: the numbers can be provided as a list of ints, if desired"""
        if numbers is None:
            is_linux = platform.system() != 'Windows'
            home_path = os.environ['HOME'] if is_linux else os.environ['HOMEPATH']
            proj_path = os.path.join(home_path, 'David_Lynch_Numbers')
            numbers_file_name = os.path.join(proj_path, 'txt', 'davidlynchnumbers.txt')
            with open(numbers_file_name, 'r') as file:
                numbers_str = file.read()
            with_zeros = [int(n_str) for n_str in numbers_str]
            numbers = []
            for n in with_zeros:
                if n == 0:
                    numbers.append(10)
                else:
                    numbers.append(n)
            self.numbers = numbers

    def set_days_since_picked(self) -> None:
        """For setting a dictionary of Dict[int, int] representing the number of days since each number has been
        picked."""
        for i in range(1, 11):
            if i in self.numbers:
                self.days_since_picked[i] = self.numbers[::-1].index(i)

    def plot_number_counts(self, ax: Optional[plt.Axes] = None) -> None:
        """For plotting a bar chart showing the count of each number.
        Args:
            ax: Axes object"""
        if ax is None:
            fig, ax = plt.subplots(1, 1)
        unique_numbers, counts = np.unique(self.numbers, return_counts=True)
        proportions = counts / len(self.numbers)
        ax.bar(unique_numbers, proportions)
        ax.hlines(
            y=0.1, xmin=ax.get_xlim()[0], xmax=ax.get_xlim()[1], color='red', label='Expected')
        ax.set_xlabel('Number')
        ax.set_ylabel('Proportion of picks')
        ax.set_xlim(0.1, 10.9)
        ax.set_xticks(unique_numbers)
        ax.legend()
        ax.grid(visible=True, alpha=0.2)

    def one_way_chi_squared_test(self) -> Power_divergenceResult:
        """For performing a one way chi squared test on the numbers
        Returns:
            the result of the chi-squared test."""
        observed_frequencies = np.bincount(self.numbers)[1:] / len(self.numbers)
        return chisquare(observed_frequencies)

    @staticmethod
    def predict_random_uniform() -> int:
        return np.random.randint(1, 11)

    def predict_longest_not_picked(self) -> int:
        """For predicting the number that has not been picked for the longest time"""
        return max(self.days_since_picked, key=self.days_since_picked.get)

    def predict_least_often_picked(self) -> int:
        """For predicting the number that has been picked least often"""
        return min(self.times_picked, key=self.times_picked.get)

    def predict_naive(self) -> int:
        """For predicting the number according a multinomial with naive proportions as the parameters."""
        rng = np.random.default_rng()
        multinomial_params = list(self.proportion_picked.values())
        draw_result = rng.multinomial(n=1, pvals=multinomial_params)
        return np.flatnonzero(draw_result)[0] + 1

    def predict_inverted_naive(self):
        """For predicting from a multinomial with parameters equal to the difference between the naive parameter and
        the analytical parameter. p = analytical + (analytical - naive)."""
        rng = np.random.default_rng()
        multinomial_params = 0.2 - np.array(list(self.proportion_picked.values()))
        draw_result = rng.multinomial(n=1, pvals=multinomial_params)
        return np.flatnonzero(draw_result)[0] + 1


if __name__ == '__main__':
    david_lynch_numbers = DavidLynchNumbers()
    david_lynch_numbers.plot_number_counts()
    test_result = david_lynch_numbers.one_way_chi_squared_test()
    print("{0} INFO: Probability of David Lynch's numbers being drawn from a uniform distribution "
          "of integers 1 through 10: {1}".format(dt.datetime.now(), test_result.pvalue))
