import os
import datetime
from Roulette_Wheel import RouletteWheel
import uuid
import matplotlib.pyplot as plt
from collections import Counter

# Get the current date and time
current_datetime = datetime.datetime.now()


basePath = r"".join(os.getcwd())  # get the current directory
savePath = os.path.join(basePath, 'data')
# Create a folder using the formatted string as the folder name



def main():

    data = False
    games = 100000
    rounds_per_game = 500
    start_balance = 300
    profit_goal = 100
    game_history = []



    for i in range(games):
        game_history.append(game(rounds=rounds_per_game, start_balance=start_balance, data=data, goal=profit_goal))

    # Count occurrences
    counts = {0: game_history.count(0), 1: game_history.count(1), 2: game_history.count(2), 3: game_history.count(3)}

    # Calculate percentages
    total = len(game_history)
    percentages = {key: (count / total) * 100 for key, count in counts.items()}

    # Output the report with percentages
    print("\n\n\nReport with Percentages:")
    print(f"Lost all of your money (0): {counts[0]} occurrences, {percentages[0]:.2f}%")
    print(f"Lost some money (1): {counts[1]} occurrences, {percentages[1]:.2f}%")
    print(f"Gained some profit (2): {counts[2]} occurrences, {percentages[2]:.2f}%")
    print(f"Met or exceeded your profit goal (3): {counts[3]} occurrences, {percentages[3]:.2f}%")

#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Receive the file id to stream from the user and then close the connection
#############################################################################################################
def game(rounds=50, start_balance=300, data=False, goal=300):
    if not os.path.exists(savePath):
        os.makedirs(savePath)
        # print("data folder not found. Making one.")

    # # Check if the folder already exists, and create it if it doesn't
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)

    roulette_wheel = RouletteWheel()
    balance = start_balance

    # ! Change this if you want to do different bets
    bet_numbers = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    fibonacci_numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229]
    fibonacci_multiplier = 5

    fibonacci_tracker = 0

    balance_history = [balance]
    highest_balance = {0: balance}
    bet_history = []

    for i in range(rounds):
        if (balance - start_balance) >= goal:
            print("Goal met. Stopping game")
            break

        number = roulette_wheel.spin()
        # !!: If you are changing up the strategy revisit the math to make sure it is correct.
        current_bet = fibonacci_numbers[fibonacci_tracker] * fibonacci_multiplier

        # see if the player has enough to lose
        lost = current_bet
        if balance - lost < 0:
            print("Uhh Ohh. You lost. Stopping game")
            break

        bet_history.append(current_bet)
        if number in bet_numbers:
            #               chip on the number * 35                -    number of other chips on the board * the amount on the chip
            # balance += (current_bet * 35) - ((len(bet_numbers) - 1) * current_bet)            my 10 number strategy
            balance += current_bet * 2
            fibonacci_tracker = 0
        else:
            # balance -= current_bet * len(bet_numbers)                                         my 10 number strategy
            balance -= current_bet
            fibonacci_tracker += 1

        if balance > highest_balance[0]:
            highest_balance.update({i + 1: balance})
        balance_history.append(balance)

    if data:
        # print(roulette_wheel.get_history())
        generate_graphs(roulette_wheel.get_history(), balance_history)

    if balance < 0:
        return 0

    if 0 < balance < start_balance:
        return 1

    if start_balance < balance < goal:
        return 2

    elif (balance - start_balance) >= goal:
        return 3


#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Receive the file id to stream from the user and then close the connection
#############################################################################################################
def generate_graphs(history, balance_history):
    folder_path = os.path.join(savePath, generate_random_folder_names())
    number_history = list()
    color_history = list()

    # Check if the folder already exists, and create it if it doesn't
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # get the balance history
    for rounds in history:
        number_history.append(rounds[0])
        color_history.append(rounds[1])

    plot_balance(balance_history, os.path.join(folder_path, "balance_history.jpg"))
    plot_num_hist(number_history, os.path.join(folder_path, "number_freq.jpg"))
    graph_color(color_history, os.path.join(folder_path, "color_freq.jpg"))

    with open(os.path.join(folder_path, "Report.txt"), "w") as file:
        file.write("Balance History: " + str(balance_history))
        file.write("\n")
        file.write("Color History: " + str(color_history))
        file.write("\n")
        file.write("Number History: " + str(number_history))




#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Receive the file id to stream from the user and then close the connection
#############################################################################################################
def plot_balance(balance_history, save_path):
    # Find the index of the highest point
    highest_point_index = balance_history.index(max(balance_history))
    highest_point_value = balance_history[highest_point_index]

    # Set up the figure with a larger width
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot the line graph
    plt.plot(balance_history, label='Balance History')

    # Annotate the highest point with its value
    plt.annotate(f'Highest: {highest_point_value}',
                 xy=(highest_point_index, highest_point_value),
                 xytext=(highest_point_index + 1, highest_point_value + 1),
                 arrowprops=dict(facecolor='red', arrowstyle='->'),
                 fontsize=8,
                 color='red')

    # Set tick marks at each data point on the x-axis
    plt.xticks(range(len(balance_history)))

    # Set tick marks at each data point on the y-axis
    plt.yticks(balance_history)

    # Rotate x-axis tick labels to avoid overlapping
    plt.xticks(rotation=45, ha='right')

    # Show the plot
    plt.title('Balance History')
    plt.xlabel('Rounds')
    plt.ylabel('Balance')
    plt.legend()

    # Adjust layout to avoid overlapping of tick labels on the x-axis
    plt.tight_layout()

    plt.savefig(save_path)

    plt.clf()
    plt.close()

#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Receive the file id to stream from the user and then close the connection
#############################################################################################################
def plot_num_hist(number_history, save_path):
    # Count the occurrences of each number
    number_counts = {i: number_history.count(i) for i in range(37)}

    # Remove numbers with 0 occurrences
    number_counts = {number: count for number, count in number_counts.items() if count > 0}

    # Plot the bar graph
    plt.bar(number_counts.keys(), number_counts.values(), color='blue')

    # Add labels and title
    plt.title('Roulette Wheel Number Frequency')
    plt.xlabel('Number')
    plt.ylabel('Frequency')

    # Add text annotations on top of the bars
    for number, count in number_counts.items():
        plt.text(number, count + 0.1, str(count), ha='center', va='bottom')

    plt.savefig(save_path)

    plt.clf()
    plt.close()

#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Receive the file id to stream from the user and then close the connection
#############################################################################################################
def graph_color(color_history, save_path):
    # Count the occurrences of each color
    color_counts = {color: color_history.count(color) for color in set(color_history)}

    # Plot the bar graph
    bars = plt.bar(color_counts.keys(), color_counts.values(), color=color_counts.keys())

    # Add labels and title
    plt.title('Color Frequency from Given Data')
    plt.xlabel('Color')
    plt.ylabel('Frequency')

    # Add text annotations on top of the bars
    for bar, (color, count) in zip(bars, color_counts.items()):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, str(count), ha='center', va='bottom')

    plt.savefig(save_path)

    plt.clf()
    plt.close()


def generate_random_folder_names():
    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    return str(str(formatted_datetime) + "___" + str(uuid.uuid4()))




if __name__ == "__main__":
    main()
