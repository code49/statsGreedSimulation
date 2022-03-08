# ----- import libraries -----

import random

import json
import os

# ----- helper functions -----


def sumList(sum_list: list) -> int:
    """

    sums the values of a list.

    Parameters:
    -----------

    sum_list: list
        list of integers to find the sum of.

    Returns:
    --------

    sum: int
        sum of the values in the list.

    """

    sum = 0
    for value in sum_list:
        sum += value

    return sum


def rollDie() -> int:
    """

    'rolls' a die and returns the result.

    Parameters:
    -----------

    None

    Returns:
    --------

    result: int
        integer representing the value of the roll of the die.

    """

    return random.randint(1, 6)


def createJSON(data: dict, filepath: str, filename: str) -> None:
    """

    creates a JSON file with the given data

    Parameters:
    -----------

    data: dict
        the data to be saved in the .json file.

    filepath: str
        path to store the .json file in.

    filename: str
        name of the .json file to create. must include the .json filetype ending.

    Returns:
    --------

    None

    """

    with open(os.path.join(filepath, filename), 'w') as outfile:
        json.dump(data, outfile)


def readJSON(filepath: str, filename: str) -> dict:
    """

    reads a JSON file and returns the dictionary contained within

    Parameters:
    -----------

    filepath: str
        path to read the .json file from.

    filename: str
        name of the .json file to read JSON data from. must include the .json filetype ending.

    Returns:
    --------

    results: dict
        dictionary read from the JSON file

    """

    with open(os.path.join(filepath, filename), 'r') as infile:
        data = json.load(infile)

    return data

# ----- create strategy class -----


class decisionFunction():

    def __init__(self, decision_function, constant_parameters: list):

        self.decision_function = decision_function
        self.constant_parameters = constant_parameters

    def getDecision(self, winning_score, current_score, opponent_score, current_rolls):

        return self.decision_function(winning_score, current_score, opponent_score,  current_rolls, self.constant_parameters)


class strategy():

    def __init__(self, name: str, decision_function: decisionFunction) -> None:

        # ----- initialise the strategy class instance for a specific strategy -----

        # strategy name
        self.name = name

        # winning and current scores
        self.winning_score = 0
        self.current_score = 0

        # decision function (parameters included)
        self.decision_function = decision_function

    def getDecision(self, opponent_score: int, current_rolls: list) -> bool:
        """
        given parameters a player can take into account, make a decision as to whether the strategy should accept the current score or roll again.

        Parameters:
        -----------

        opponent_score: int
            integer representing the oppoenent strategy's score.

        current_rolls: list
            list of integers representing the current roll-set.

        Returns:
        --------

        decision: bool
            boolean representing the strategy's decision. True if accept, False if roll again.

        """

        return self.decision_function.getDecision(self.winning_score, self.current_score, opponent_score, current_rolls)

# ----- create functions to test strategies against one another -----


def runSimulation(strategy_1: strategy, strategy_2: strategy, winning_score: int) -> list:
    """
    runs a single simulation of a game between two strategies.

    Parameters:
    -----------

    strategy_1: strategy object
        strategy object for the first strategy in the simulation.

    strategy_2: strategy object
        strategy object for the second strategy in the simulation.

    winning_score: int
        integer representing the score needed to win a game.

    Returns:
    --------

    results: list
        tuple containing the results of the simulation. formatted as follows:
        [winner:string, margin:int]

    """

    # ensure both strategies have their scores reset, and the winning score updated

    strategy_1.winning_score = winning_score
    strategy_1.current_score = 0

    strategy_2.winning_score = winning_score
    strategy_2.current_score = 0

    # loop the turns until one strategy gets enough points to win
    while True:

        # strategy_1 turn
        current_moves = []
        while (strategy_1.current_score + sumList(current_moves) < winning_score):

            roll = rollDie()

            if roll == 1:
                current_moves = []  # reset the moves so that the strategy has no points added
                break

            else:
                # add the result of the roll to the moves list
                current_moves.append(roll)
                if not strategy_1.getDecision(strategy_2.current_score, current_moves):
                    break

        strategy_1.current_score = strategy_1.current_score + \
            sumList(current_moves)  # update the score of strategy_1

        # check that strategy_1 has not won yet; if so, game is over
        if strategy_1.current_score >= winning_score:
            break

        # strategy_2 turn
        current_moves = []
        while (strategy_2.current_score + sumList(current_moves) < winning_score):

            roll = rollDie()

            if roll == 1:
                current_moves = []  # reset the moves so that the strategy has no points added
                break

            else:
                # add the result of the roll to the moves list
                current_moves.append(roll)
                if not strategy_2.getDecision(strategy_1.current_score, current_moves):
                    break

        strategy_2.current_score = strategy_2.current_score + \
            sumList(current_moves)  # update the score of strategy_2

        # check that strategy_2 has not won yet; if so, game is over
        if strategy_2.current_score >= winning_score:
            break

    # someone has now won, return results accordingly
    winner = ""
    margin = 0

    if strategy_1.current_score >= winning_score:

        winner = strategy_1.name
        margin = 100 - strategy_2.current_score

    else:

        winner = strategy_2.name
        margin = 100 - strategy_1.current_score

    return [winner, margin]


def runSimulationBlock(strategy_1: strategy, strategy_2: strategy, winning_score: int, games: int) -> dict:
    """

    runs a set of simulations between two strategies.

    Parameters:
    -----------

    strategy_1: strategy object
        strategy object for the first strategy in the simulation.

    strategy_2: strategy object
        strategy object for the second strategy in the simulation.

    winning_score: int
        integer representing the score needed to win a game.

    games: int
        integer representing the number of games to simulate.

    Returns:
    --------

    results: dict
        dictionary of results. formatted as follows:
        {
            "game_settings": {
                "game_count": number of games played,
                "winning_score": winning score,
                "strategy_1": strategy_1.name,
                "strategy_2": strategy_2.name
            },
            "win_count" : [strategy_1_wins, strategy_2_wins],
            "win_margins" : [strategy_1_win_margin_list, strategy_2_win_margin_list]
            "average_margins" : [strategy_1_average_margin, strategy_2_average_margin]
        }

    """

    print(
        f"running {str(games)} simulations for {strategy_1.name} vs. {strategy_2.name}: \n")

    # ----- run the games -----

    results_list = []

    for i in range(0, games):

        results = runSimulation(strategy_1, strategy_2, winning_score)
        results_list.append(results)

        print(f"     game {i} of {games}: {results}")

    # ----- create the results dictionary -----

    results = {
        "game_settings": {
            "game_count": games,
            "winning_score": winning_score,
            "strategy_1": strategy_1.name,
            "strategy_2": strategy_2.name
        }
    }

    # assemble win count, margins

    strategy_1_wins = 0
    strategy_2_wins = 0
    strategy_1_margins = []
    strategy_2_margins = []

    for result in results_list:

        if result[0] == strategy_1.name:

            strategy_1_wins += 1
            strategy_1_margins.append(result[1])
            strategy_2_margins.append(-result[1])

        else:

            strategy_2_wins += 1
            strategy_2_margins.append(result[1])
            strategy_1_margins.append(-result[1])

    results["win_count"] = [strategy_1_wins, strategy_2_wins]
    results["win_margins"] = [strategy_1_margins, strategy_2_margins]

    # assemble average win margins

    strategy_1_average = (
        sumList(results["win_margins"][0]))/(len(results["win_margins"][0]))
    strategy_2_average = (
        sumList(results["win_margins"][1]))/(len(results["win_margins"][1]))

    results["average_margins"] = [strategy_1_average, strategy_2_average]

    # ----- return final results dict -----

    return results


strategies = []

# ----- test all strategies against one another -----


def testStrategies(strategies: list, winning_score: int, vs_count: int) -> dict:
    """

    tests a set of strategies against each other

    Parameters:
    -----------

    strategies: list
        list containing strategy objects to be tested.

    winning_score: int
        integer representing the minimum number of points required to win a game.

    vs_count: int
        integer representing the number of games strategies should play against each other.

    Returns:
    --------

    aggregated_results: dict
        dictionary containing aggregated results. formatted as follows:
        {
            strategy_name: {
                "games_played": games played,
                "average_margin": {
                    "average": average game margin,
                    "match_count": match count
                }
                "win_loss_rate": {
                    "overall": {
                        "wins": win count,
                        "losses": loss count,
                        "rate": winrate
                    },
                    "first": { #when strategy is first player
                        "wins": win count,
                        "losses": loss count,
                        "rate": winrate
                    },
                    "second": { #when strategy is second player
                        "wins": win count,
                        "losses": loss count,
                        "rate": winrate
                    }

                }
            },

            <continues for all the strategies in strategies>
        }

    """

    # test all strategies against each other

    # for strategy_1 in strategies:  # this gets the first strategy

    #     for strategy_2 in strategies:  # this gets the second strategy

    #         createJSON(runSimulationBlock(strategy_1, strategy_2, winning_score,
    #                    vs_count), "./match_data/", f"{strategy_1.name}-{strategy_2.name}.json")

    # aggregate the results
    aggregate_results = {}

    current_results = {}  # results currently being processed

    for filename in os.listdir("./match_data"):

        current_results = readJSON("./match_data", filename)

        # update data for first strategy in the match
        try:
            current_strategy = aggregate_results[current_results["game_settings"]["strategy_1"]]

            aggregate_results[current_results["game_settings"]["strategy_1"]] = {

                # games played
                "games_played": current_strategy["games_played"] + current_results["game_settings"]["game_count"],

                # marginal averages
                "average_margin": {
                    "average": (current_strategy["average_margin"]["average"] * current_strategy["average_margin"]["match_count"] + current_results["average_margins"][0]/(10000 * current_strategy["average_margin"]["match_count"]+1)),
                    "match_count": current_strategy["average_margin"]["match_count"] + 1
                },

                #wins and losses
                "win_loss_rate": {

                    # overall
                    "overall": {
                        "wins": current_strategy["win_loss_rate"]["overall"]["wins"] + current_results["win_count"][0],
                        "losses": current_strategy["win_loss_rate"]["overall"]["losses"] + (current_results["game_settings"]["game_count"] - current_results["win_count"][0]),
                    },

                    # because this was the first strategy, update the first win-loss-rate column
                    "first": {
                        "wins": current_strategy["win_loss_rate"]["first"]["wins"] + current_results["win_count"][0],
                        "losses": current_strategy["win_loss_rate"]["first"]["losses"] + (current_results["game_settings"]["game_count"] - current_results["win_count"][0])
                    },

                    # copy the 'when this strategy is the second strategy' statistics; no new computation required
                    "second": {
                        "wins": current_strategy["win_loss_rate"]["second"]["wins"],
                        "losses": current_strategy["win_loss_rate"]["second"]["losses"]
                    }

                }
            }

        except KeyError as error:  # should only occur when strategy hasn't been recorded yet

            aggregate_results[current_results["game_settings"]["strategy_1"]] = {

                # games played
                "games_played": current_results["game_settings"]["game_count"],

                # marginal averages
                "average_margin": {
                    "average": (current_results["average_margins"][0]/10000),
                    "match_count": 1
                },

                #wins and losses
                "win_loss_rate": {

                    # overall
                    "overall": {
                        "wins": current_results["win_count"][0],
                        "losses": (current_results["game_settings"]["game_count"] - current_results["win_count"][0])
                    },

                    # because this was the first strategy, update the first win-loss-rate column
                    "first": {
                        "wins": current_results["win_count"][0],
                        "losses": (current_results["game_settings"]["game_count"] - current_results["win_count"][0])
                    },

                    # this strategy has not been the 'second strategy' yet, so add some blanks
                    "second": {
                        "wins": 0,
                        "losses": 0,
                    }

                }
            }

        # update data for second strategy in the match
        try:
            current_strategy = aggregate_results[current_results["game_settings"]["strategy_2"]]

            aggregate_results[current_results["game_settings"]["strategy_2"]] = {

                # games played
                "games_played": current_strategy["games_played"] + current_results["game_settings"]["game_count"],

                # marginal averages
                "average_margin": {
                    "average": (current_strategy["average_margin"]["average"] * current_strategy["average_margin"]["match_count"] + current_results["average_margins"][0]/(10000 * current_strategy["average_margin"]["match_count"]+1)),
                    "match_count": current_strategy["average_margin"]["match_count"] + 1
                },

                #wins and losses
                "win_loss_rate": {

                    # overall
                    "overall": {
                        "wins": current_strategy["win_loss_rate"]["overall"]["wins"] + current_results["win_count"][0],
                        "losses": current_strategy["win_loss_rate"]["overall"]["losses"] + (current_results["game_settings"]["game_count"] - current_results["win_count"][0])
                    },

                    # copy the 'when this strategy is the first strategy' statistics; no new computation required
                    "first": {
                        "wins": current_strategy["win_loss_rate"]["first"]["wins"],
                        "losses": current_strategy["win_loss_rate"]["first"]["losses"]
                    },

                    # because this was the first strategy, update the first win-loss-rate column
                    "second": {
                        "wins": current_strategy["win_loss_rate"]["second"]["wins"] + current_results["win_count"][0],
                        "losses": current_strategy["win_loss_rate"]["second"]["losses"] + (current_results["game_settings"]["game_count"] - current_results["win_count"][0])
                    }

                }
            }

        except KeyError as error:  # should only occur when strategy hasn't been recorded yet

            aggregate_results[current_results["game_settings"]["strategy_2"]] = {

                # games played
                "games_played": current_results["game_settings"]["game_count"],

                # marginal averages
                "average_margin": {
                    "average": (current_results["average_margins"][0]/10000),
                    "match_count": 1
                },

                # wins and losses
                "win_loss_rate": {

                    # overall
                    "overall": {
                        "wins": current_results["win_count"][0],
                        "losses": (current_results["game_settings"]["game_count"] - current_results["win_count"][0])
                    },

                    # this strategy has not been the 'first strategy' yet, so add some blanks
                    "first": {
                        "wins": 0,
                        "losses": 0,
                    },

                    # update the second win-loss-rate column
                    "second": {
                        "wins": current_results["win_count"][0],
                        "losses": (current_results["game_settings"]["game_count"] - current_results["win_count"][0])
                    }

                }
            }

    # add winrates to each strategy

    for strategy_name in aggregate_results:

        # overall winrate

        aggregate_results[strategy_name]["win_loss_rate"]["overall"]["rate"] = aggregate_results[strategy_name]["win_loss_rate"]["overall"]["wins"]/(
            aggregate_results[strategy_name]["win_loss_rate"]["overall"]["wins"] + aggregate_results[strategy_name]["win_loss_rate"]["overall"]["losses"])

        # first strategy winrate

        aggregate_results[strategy_name]["win_loss_rate"]["first"]["rate"] = aggregate_results[strategy_name]["win_loss_rate"]["first"]["wins"]/(
            aggregate_results[strategy_name]["win_loss_rate"]["first"]["wins"] + aggregate_results[strategy_name]["win_loss_rate"]["first"]["losses"])

        # second strategy winrate

        aggregate_results[strategy_name]["win_loss_rate"]["second"]["rate"] = aggregate_results[strategy_name]["win_loss_rate"]["second"]["wins"]/(
            aggregate_results[strategy_name]["win_loss_rate"]["second"]["wins"] + aggregate_results[strategy_name]["win_loss_rate"]["second"]["losses"])

    # save the results in a file
    createJSON(aggregate_results, "./", "aggregate_results.json")

    # return the results as well
    return aggregate_results

# ----- base strategy functions -----


"""

all of these should be defined as follows to prevent errors:

def functionName(winning_score, current_score, opponent_score, current_rolls, constant_parameters) -> bool:

    function-y stuff, blah blah blah ....

"""


def untilValue(winning_score, current_score, opponent_score, current_rolls, constant_parameters) -> bool:
    """

    continues rolling until a certain total value is reached.

    Constant Parameters:
    --------------------

    value: int
        total value (sum of rolls) after which to stop rolling

    """

    value = constant_parameters[0]

    if sumList(current_rolls) >= value:
        return True
    else:
        return False


def untilRoll(winning_score, current_score, opponent_score, current_rolls, constant_parameters) -> bool:
    """

    continues rolling unless a value in a set is rolled.

    Constant Parameters:
    --------------------

    values: list
        list containing integers representing dice rolls for which the function should stop rolling.

    """

    # because this would be called every time, only need to check the most recent roll
    if current_rolls[-1] in constant_parameters[0]:
        return False
    else:
        return True


def randomDecision(winning_score, current_score, opponent_score, current_rolls, constant_parameters) -> bool:
    """

    returns a random decision, True or False.

    """

    return [True, False][random.randint(0, 1)]


def alwaysTrue(winning_score, current_score, opponent_score, current_rolls, constant_parameters) -> bool:
    """

    always continues to roll.

    Constant Parameters:
    --------------------

    None

    """

    return True


def alwaysFalse(winning_score, current_score, opponent_score, current_rolls, constant_parameters) -> bool:
    """

    always stops rolling.

    Constant Parameters:
    --------------------

    None

    """

    return False


def agroAfter(winning_score, current_score, oppponent_score, current_rolls, constant_parameters) -> bool:
    """

    after the strategy reaches a certain distance away from the winning score, play ultra aggressive. otherwise, chooses randomly.

    Constant Parameters:
    --------------------

    delta: int
        integer representing the distance from the winning_score before the decision goes ultra aggressive

    """

    if (winning_score - current_score) <= constant_parameters[0]:
        return True
    else:
        return randomDecision(winning_score, current_score, oppponent_score, current_rolls, constant_parameters)


def agroAfterOpponent(winning_score, current_score, opponent_score, current_rolls, constant_parameters) -> bool:
    """

    after the opponent reaches a certain distance from the winning score, plays ultra aggressively. otherwise chooses randomly.

    Constant Parameters:
    --------------------

    delta: int
        distance from winning score after which the algorithm plays ultra aggressively.

    """

    if (winning_score - opponent_score) <= constant_parameters[0]:
        return True
    else:
        return randomDecision(winning_score, current_score, opponent_score, current_rolls, constant_parameters)


def beatOpponent(winning_score, current_score, opponent_score, current_rolls, constant_parameters) -> bool:
    """

    plays aggressively until its score is higher than the opponent's. otherwise, chooses randomly.

    Constant Parameters:
    --------------------

    None

    """

    if current_score < opponent_score:
        return True
    else:
        return randomDecision(winning_score, current_score, opponent_score, current_rolls, constant_parameters)


# ----- decision function, strategy definitions -----


randomControl = strategy("randomControl", decisionFunction(randomDecision, []))

untilReach5 = strategy("untilReach5", decisionFunction(untilValue, [5]))
untilReach8 = strategy("untilReach8", decisionFunction(untilValue, [8]))
untilReach10 = strategy("untilReach10", decisionFunction(untilValue, [10]))
untilReach15 = strategy("untilReach15", decisionFunction(untilValue, [15]))
untilReach20 = strategy("untilReach20", decisionFunction(untilValue, [20]))
untilReach25 = strategy("untilReach25", decisionFunction(untilValue, [25]))

untilRoll3456 = strategy(
    "untilRoll3456", decisionFunction(untilRoll, [[3, 4, 5, 6]]))
untilRoll456 = strategy(
    "untilRoll456", decisionFunction(untilRoll, [[4, 5, 6]]))
untilRoll56 = strategy("untilRoll56", decisionFunction(untilRoll, [[5, 6]]))
untilRoll6 = strategy("untilRoll6", decisionFunction(untilRoll, [[6]]))

agroAfter6 = strategy("agroAfter6", decisionFunction(agroAfter, [6]))
agroAfter10 = strategy("agroAfter10", decisionFunction(agroAfter, [10]))
agroAfter15 = strategy("agroAfter15", decisionFunction(agroAfter, [15]))
agroAfter20 = strategy("agroAfter20", decisionFunction(agroAfter, [20]))
agroAfter25 = strategy("agroAfter25", decisionFunction(agroAfter, [25]))

alwaysTrueStrategy = strategy("alwaysTrue", decisionFunction(alwaysTrue, []))
alwaysFalseStrategy = strategy(
    "alwaysFalse", decisionFunction(alwaysFalse, []))

beatOpponentStrategy = strategy(
    "beatOpponent", decisionFunction(beatOpponent, []))

strategies = [
    randomControl,
    untilReach5,
    untilReach8,
    untilReach10,
    untilReach15,
    untilReach20,
    untilReach25,
    untilRoll3456,
    untilRoll456,
    untilRoll56,
    untilRoll6,
    agroAfter6,
    agroAfter10,
    agroAfter15,
    agroAfter20,
    agroAfter25,
    alwaysTrueStrategy,
    alwaysFalseStrategy,
    beatOpponentStrategy
]

print(len(strategies))

results = testStrategies(strategies, 100, 10000)
