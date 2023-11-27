from random import randint

import poker_functions


# Note: I feel like classes would work better for this program, but that wasn't
# covered in the course so I'll use lists and player indeces instead


# Utility functions
def pause():
	'''
	Pauses until the user presses the enter key
	'''
	input("(Press enter to continue)")
	print()


def pinput() -> str:
	'''
	Same as builtin input(), but prints '>>> ' before-hand

	Returns:
		str: whatever the user input
	'''
	return input('>>> ')


def print_action(action: str):
	'''
	Prints the given action
	'''
	print('>', action, '<')


def dealer_says(quote: str):
	'''
	Prints a quote from the dealer
	'''
	print(f'\n\nDEALER: "{quote}"\n')


# Constants
WELCOME_TEXT = """
==---------------------------- $$$ 10 J Q K A $$$ ----------------------------==
||====================================POKER===================================||
==----------------------------- $$$$$ ----- $$$$$ ----------------------------==

Welcome to Poker, {}!
"""

MENU_TEXT = """
You currently have ${} to bet with

Please choose one of the following:
	1) Start a round
	2) Check rules
	3) Quit
"""

RULES_TEXT = """
--- Rules ---

Flow of Play:
1) At the start of a round, you and 4 CPUs ante up (place a minimum required
	bet of $10)
2) All the players are dealt 5 cards each at the start of a round
3) Each player may choose to be redealt up to 4 cards
4) Each player then takes a turn to either:
	a) call (match the current bet size),
	b) raise (raise the current bet size by a given amount), or
	c) fold (give up their already submitted bet)
5) This is repeated until all betting players call or there is only one player
	left
6) After all bets have been made, every player reveals their hand, and the
	winner takes all bets this round
"""

CLOSING_TEXT = """
Thanks for playing! See you soon!
"""

PLAYER_INDEX = 2
MINIMUM_BET = 10
STARTING_MONEY = 1000
PLAYER_NUM = 5
NAMES = []
for this_player in range(PLAYER_NUM):
	if this_player == PLAYER_INDEX:
		print("What's your name?")
		NAMES.append(pinput())
		continue
	cpu_number = this_player
	if this_player > PLAYER_INDEX:
		cpu_number -= 1
	NAMES.append('CPU' + str(cpu_number + 1))



def ante_up(money):
	'''
	Each player makes a minimum bet

	Parameters:
		money (list[int]): the amount of betting money each player has
		bet (int): the current bet
>>>
	'''
	dealer_says('Ante up!')
	print("Minimum bet:", MINIMUM_BET)
	print()
	# For each player...
	for this_player in range(PLAYER_NUM): 

		# Bet the minimum bet
		money[this_player] -= MINIMUM_BET

		# Print the bet
		print_action(NAMES[this_player] + ' met the minimum bet')

		# Print the balance
		poker_functions.print_balance(money[this_player], NAMES[this_player])
		pause()


def player_redraw_cards(hand, deck):
	'''
	A menu to let the player choose which cards to redraw
	'''
	# Does the player wish to discard cards?
	print('Do you wish to discard any cards? (y/n)')
	discard_answer = pinput()
	# Validate input
	while discard_answer != 'y' and discard_answer != 'n':
		print("Answer must be 'y' or 'n'. Try again")
		discard_answer = pinput()
	if discard_answer == 'n':
		return
	
	# How many cards does the player wish to replace?
	print('How many?')
	card_num = pinput()
	# Validate input
	while (int(card_num) < 1 or int(card_num) > 4) \
			if card_num.isnumeric() else True:
		print('Answer must be an integer between 1 and 4 (inclusive).',
			  'Try again')
		card_num = pinput()
	card_num = int(card_num)
	
	# What options are there?
	card_options = []
	for suit in hand.values():
		card_options += suit.copy()
	
	# Which cards?
	for _ in range(card_num):
		# Print cards
		print()
		for index, card in enumerate(card_options):
			print(f"{index + 1}) ", end='')
			poker_functions.print_card(card)
	
		# Which card?
		print(f"Which card? (1-{len(card_options)})")
		card = pinput()
		# Validate input
		while (int(card) < 1 or int(card) > len(card_options)) \
				if card.isnumeric() else True:
			print("Answer must be an integer between 1 and",
				  f"{len(card_options)} (inclusive). Try again")
			card = pinput()
		card = card_options[int(card) - 1]
	
		# Replace the card in the hand
		poker_functions.replace_card(card, hand, deck)
		# Remove the card from the list of options
		card_options.remove(card)
	print_action(NAMES[PLAYER_INDEX] + " replaced " + str(card_num) + " card(s)")
	print("\nHere are your final cards now:")
	poker_functions.print_hand(hand)
	pause()


def cpu_redraw_cards(name, hand, deck):
	'''
	The AI for a CPU player to redraw cards
	'''
	bad_cards = poker_functions.choose_bad_cards(hand)
	for card in bad_cards:
		# Replace the card in the hand
		poker_functions.replace_card(card, hand, deck)
	print_action(name + " replaced " + str(len(bad_cards)) + " card(s)")


def redraw_cards(hands, deck):
	'''
	Cycle through each player and let them discard
	'''
	dealer_says("You may redraw any cards, if necessary.")
	for this_player in range(len(hands)):
		if this_player == PLAYER_INDEX:
			player_redraw_cards(hands[PLAYER_INDEX], deck)
		else:
			cpu_redraw_cards(NAMES[this_player], hands[this_player], deck)
			pause()


def cpu_decisions(money, hands, bet) -> list:
	'''
	Creates a list of parameters for the decisions each AI could make

	Parameters:
		money (list[int]): a list containing the betting money for each player
		hands (list[hand]): a list containing the hand of each player
		bet (int): the current bet
	
	Returns:
		list[tuple(int, int, int)]: the decision parameters for each AI
			0: the maximum the bet can be before the AI folds
			1: the base number for the raise amount the AI can make
			2: the minimum the bet can be for the AI to call
			The main player's spot is filled, but can be ignored
	'''
	bet_decisions = []
	for this_player, hand in enumerate(hands):
		# This is the best hand in the game, so the value of a hand out of 1 is
		# based from this
		royal_flush_value = poker_functions.hand_value({
			0: [(10, 0), (11, 0), (12, 0), (13, 0), (1, 0)],
			1: [], 2: [], 3: []
			})[1]
		this_hand_value = poker_functions.hand_value(hand)[1]

		max_bet = int((this_hand_value / royal_flush_value) * \
				(money[this_player] + bet))

		raise_base = max_bet // 10

		min_bet = max_bet // 2

		bet_decisions.append((max_bet, raise_base, min_bet))
	return bet_decisions


def cpu_main_loop(name, money, to_call, bet_decisions, bet) -> tuple:
	'''
	The turn of a CPU player

	Parameters:
		money (int): the betting money available to this CPU
		hand (hand): the hand of this CPU
		to_call (int): the amount this CPU has to call to
		bet_decisions (tuple(int, int, int)): the parameters for the CPU to
			make a decision
		bet (int): the current bet
	
	Returns:
		tuple(int, int, bool): the remaining betting money for this CPU, and if
			the CPU is still playing
	'''
	max_bet = bet_decisions[0]
	raise_amount = bet_decisions[1] + randint(0, 3)
	min_bet = bet_decisions[2]

	# If the CPU can't or won't make the call, then fold
	if to_call > money or bet > max_bet:
		print_action(name + ' folded')
		return (money, bet, False)

	# Meet the current bet
	money -= to_call

	# If the CPU won't raise, then call
	if bet > min_bet:
		print_action(name + ' called the bet')
		return (money, bet, True)

	# The CPU will raise the bet
	money, bet = poker_functions.raise_bet(
			money, raise_amount, bet
		)

	print(f"> {name} raised the bet to ${bet} <")
	return (money, bet, True)


def player_main_loop(money, hand, to_call, bet) -> tuple:
	'''
	The turn of the main player

	Parameters:
		money (int): the betting money available to the player
		hand (hand): the hand of the player
		to_call (int): the amount the player has to call to
		bet (int): the current bet
	
	Returns:
		tuple(int, int, bool): the remaining betting money for the player, and
			if the player is still playing
	'''
	print("Current bet:", bet)
	print("Your available betting money:", money)
	print("The amount to call to:", to_call)
	print("Your hand:")
	poker_functions.print_hand(hand)
	print()

	if to_call > money:
		print("You do not have enough money to meet the bet, you are forced", \
				"to fold.")
		print_action(NAMES[PLAYER_INDEX] + ' folded')
		return (money, bet, False)

	print("What do you want to do? (fold/call/raise)")
	choice = pinput()
	while choice != 'fold' and choice != 'call' and choice != 'raise':
		print("Answer must be 'fold', 'call', or 'raise'. Please try again")
		choice = pinput()
	
	print()
	
	if choice == 'fold':
		print_action(NAMES[PLAYER_INDEX] + ' folded')
		return (money, bet, False)

	if choice == 'call':
		money -= to_call
		print_action(NAMES[PLAYER_INDEX] + ' called the bet')
		return (money, bet, True)

	# Choice was 'raise'
	print("How much do you want to raise by?")
	raise_amount = pinput()
	while (int(raise_amount) < 0 or int(raise_amount) > money) \
			if raise_amount.isnumeric() else True:
		print("Answer must be a number between 0 and your betting money.", \
				"Please try again")
		raise_amount = pinput()
	raise_amount = int(raise_amount)

	money -= raise_amount
	bet += raise_amount
	print_action(f"{NAMES[PLAYER_INDEX]} raised the bet to {bet}")
	return (money, bet, True)


def round_main_loop(money, start_money, fold_losses, hands, bet_decisions, \
		player_is_playing) -> int:
	'''
	The main loop of a round, where each player can call, raise, or fold
	'''
	dealer_says("Place your bets!")

	bet = MINIMUM_BET

	# The amount a given player still has to call to
	to_call = [0] * PLAYER_NUM
	call_amount = 0
	this_player = -1

	# Loop until everyone calls
	while call_amount < player_is_playing.count(True) - 1:

		this_player += 1
		# If all players played, loop again
		if this_player >= PLAYER_NUM:
			this_player = 0

		if not player_is_playing[this_player]:
			continue

		call_add = 0

		old_bet = bet
		# Find player action for main player or CPU
		money[this_player], bet, player_is_playing[this_player] = player_main_loop(
				money[this_player], hands[this_player], to_call[this_player], bet
			) if this_player == PLAYER_INDEX else cpu_main_loop(
				NAMES[this_player], money[this_player], to_call[this_player],
				bet_decisions[this_player], bet
			)
		if not player_is_playing[this_player]:
			fold_losses[this_player] = start_money[this_player] - \
					money[this_player]
			pause()
			continue
		call_add = bet - old_bet
		if call_add != 0:
			call_amount = 0
		else:
			call_amount += 1
		# Update the amount each player needs to call to
		for player_to_call in range(PLAYER_NUM):
			if player_to_call != this_player:
				to_call[player_to_call] += call_add

		#print(call_amount)
		pause()
	
	return bet


def play_round(money):
	'''
	Plays a round of poker, given the bet money of the 5 players

	Parameters:
		money (list[int]): the betting money available to all players
	'''
	print("\n\n---NEW ROUND---\n")
	start_money = money.copy()

	# Create and shuffle a new deck
	deck = poker_functions.create_deck()
	deck = poker_functions.shuffle(deck)

	# Ante up
	# A minimum bet is made, and all players must meet it
	# The check for if a player CAN make the bet has already been made
	ante_up(money)
	bet = MINIMUM_BET
	
	# Deal hands
	dealer_says("Dealing...")
	hands = poker_functions.deal_hands(PLAYER_NUM, deck)

	# Print the player's hand
	print("Your hand:")
	poker_functions.print_hand(hands[PLAYER_INDEX])
	pause()

	# Redraw cards
	redraw_cards(hands, deck)

	# A list of tuples containing:
	#	the max bet for a player
	#	the amount they're willing to raise per turn
	#	the minimum they're willing to bet
	# (actual game player's isn't counted)
	bet_decisions = cpu_decisions(money, hands, bet)

	# Main loop
	# The status of each player
	player_is_playing = [True] * PLAYER_NUM
	fold_losses = [0] * PLAYER_NUM
	bet = round_main_loop(money, start_money, fold_losses, hands, \
			bet_decisions, player_is_playing)

	# Find the winner
	dealer_says("The results are...")
	pause()
	playing_hands = []
	playing_names = []
	for player, hand in enumerate(hands):
		if player_is_playing[player]:
			playing_hands.append(hand)
			playing_names.append(NAMES[player])
	winner = poker_functions.compare_hands(playing_hands, playing_names)
	winner_money = player_is_playing.count(True) * bet + sum(fold_losses)
	pause()
	print("\nThe winning hand:")
	poker_functions.print_hand(hands[winner])
	print("The winner's earnings:", winner_money)
	money[winner] += winner_money
	pause()
	print("\nYour loss:", bet if player_is_playing[PLAYER_INDEX] \
			else fold_losses[PLAYER_INDEX])
	pause()


def main():

	money = [STARTING_MONEY] * PLAYER_NUM
	# Welcome
	print(WELCOME_TEXT.format(NAMES[PLAYER_INDEX]))
	pause()

	# Game loop
	while(True):
		if money[PLAYER_INDEX] < MINIMUM_BET:
			print("Get outta here, you don't have enough cash!")
			quit()
		for this_player in range(PLAYER_NUM):
			if money[this_player] < MINIMUM_BET:
				money[this_player] = STARTING_MONEY
		# Print the menu
		print(MENU_TEXT.format(money[PLAYER_INDEX]))

		# Get the player's choice
		choice = pinput()
		# Check if the choice is valid
		while (int(choice) < 1 or int(choice) > 3) \
				if choice.isnumeric() else True:
			print('Choice is invalid. Please try inputting something else')
			choice = pinput()

		choice = int(choice)

		# Play round
		if choice == 1:
			play_round(money)

		# Check rules
		if choice == 2:
			print(RULES_TEXT)
			pause()
		
		# Quit
		if choice == 3:
			break

	# Quit text
	print(CLOSING_TEXT)
	pause()


# Main program entry
if __name__ == '__main__':
	main()
