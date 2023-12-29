import random

class RouletteWheel:
    def __init__(self):
        # Define the numbers on the wheel and their corresponding colors
        self.wheel_numbers = list(range(0, 37))
        self.wheel_colors = {
            0: 'green',
            32: 'red', 15: 'black', 19: 'red', 4: 'black', 21: 'red', 2: 'black',
            25: 'red', 17: 'black', 34: 'red', 6: 'black', 27: 'red', 13: 'black',
            36: 'red', 11: 'black', 30: 'red', 8: 'black', 23: 'red', 10: 'black',
            5: 'red', 24: 'black', 16: 'red', 33: 'black', 1: 'red', 20: 'black',
            14: 'red', 31: 'black', 9: 'red', 22: 'black', 18: 'red', 29: 'black',
            7: 'red', 28: 'black', 12: 'red', 35: 'black', 3: 'red', 26: 'black'
        }
        self.history = []

    def spin(self):
        # Spin the wheel and return the result
        result = random.choice(self.wheel_numbers)
        self.history.append((result, self.wheel_colors.get(result)))
        return result

    def get_history(self) -> list:
        # Return the history of numbers and their colors
        return self.history