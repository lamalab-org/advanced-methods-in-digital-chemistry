"""A deliberately flawed error calculation for the course practical.

Inputs in this exercise are non-empty, equal-length sequences of numbers.
"""


def mean_squared_error(predictions, observations):
    residuals = [prediction - observation
                 for prediction, observation in zip(predictions, observations)]
    return (sum(residuals) / len(residuals)) ** 2


if __name__ == "__main__":
    print(mean_squared_error([2, 0], [1, 1]))
