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

    game_history = []

    for i in range(100):
        game_history.append(game(rounds=50, start_balance=500))

    # Calculate the percentage of True values
    true_percentage = (game_history.count(True) / len(game_history)) * 100

    # Print the result
    print(f"\nThe percentage of True values in the list is: {true_percentage}%")

#############################################################################################################
# Function:            establishConnection
# Author:              Peter Pham (pxp180041)
# Date Started:        08/10/2022
#
# Description:
# Receive the file id to stream from the user and then close the connection
#############################################################################################################
def game(rounds=50, start_balance=300):
    if not os.path.exists(savePath):
        os.makedirs(savePath)
        # print("data folder not found. Making one.")

    # # Check if the folder already exists, and create it if it doesn't
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)

    roulette_wheel = RouletteWheel()
    balance = start_balance

    # ! Change this if you want to do different bets
    bet_numbers = [13, 14, 15, 16, 17, 19, 20, 22, 23, 24]
    fibonacci_numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229]

    fibonacci_tracker = 0

    balance_history = [balance]
    highest_balance = {0: balance}
    bet_history = []

    for i in range(rounds):
        # if balance < 0 or (balance - start_balance) >= 300:
        #     print("Condition met. Breaking")
        #     break

        number = roulette_wheel.spin()
        # !!: If you are changing up the strategy revisit the math to make sure it is correct.
        current_bet = fibonacci_numbers[fibonacci_tracker]
        bet_history.append(current_bet)
        if number in bet_numbers:
            #               chip on the number * 35                -    number of other chips on the board * the amount on the chip
            balance += (current_bet * 35) - ((len(bet_numbers) - 1) * current_bet)
            fibonacci_tracker = 0
        else:
            balance -= current_bet * len(bet_numbers)
            fibonacci_tracker += 1

        if balance > highest_balance[0]:
            highest_balance.update({i + 1: balance})
        balance_history.append(balance)

    # print(roulette_wheel.get_history())
    generate_graphs(roulette_wheel.get_history(), balance_history)

    if balance < 0:
        return False

    if balance >= start_balance:
        return True


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
