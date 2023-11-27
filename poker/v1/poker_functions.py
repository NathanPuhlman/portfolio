from random import randint

suits = { 0: "Hearts", 1: "Diamonds", 2: "Clubs", 3: "Spades" }
ranks = ( 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 )
rank_names = { 1: "Ace", 11: "Jack", 12: "Queen", 13: "King" }


def create_deck() -> list:
	'''
	Creates a new deck of cards

	Returns:
		list[tuple(int,int)]: The newly created deck as a list. Each tuple in
			the list represents a card (rank, suit)

	Doctest:
		>>> create_deck()
		[(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), \
(9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (1, 1), (2, 1), (3, 1), (4, 1), \
(5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), \
(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), \
(10, 2), (11, 2), (12, 2), (13, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), \
(6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3)]
	'''
	deck = []
	# Loop through every possible card, adding each possibility to the new
	# deck
	for suit in suits.keys():
		for rank in ranks:
			deck.append((rank, suit))
	return deck


def print_card(card: tuple):
	'''
	Prints the given card

	Parameters:
		card (tuple(int, int)): The card to print in the format: (rank, suit)
	
	Doctests:
		>>> print_card((1, 0))
		Ace of Hearts

		>>> print_card((2, 1))
		2 of Diamonds

		>>> print_card((10, 2))
		10 of Clubs

		>>> print_card((11, 3))
		Jack of Spades

		>>> print_card((12, 0))
		Queen of Hearts

		>>> print_card((13, 1))
		King of Diamonds
	'''
	# More readable variable names
	rank = card[0]
	suit = card[1]

	# Get the rank name from the rank_names dictionary
	rank_text = rank_names.get(rank)

	# Ranks without names are not in the dictionary, so they should be the
	# number
	if rank_text == None:
		rank_text = rank
	
	# Get the suit name from the suits dictionary
	suit_text = suits[suit]

	# Print card
	print(rank_text, 'of', suit_text)


def shuffle(deck: list) -> list:
	'''
	Changes the order of the cards in the deck randomly

	Parameters:
		deck (list[tuple(int, int)]): a list of cards in the format: (rank, suit)
	
	Returns:
		(list[tuple(int, int)]): the same list as the given list, with the
			order of its elements randomly organized
	'''
	# There may be times when I want to keep the original deck, so its best to
	# make a copy and shuffle that
	working_deck = deck.copy()

	# Do 1000 shuffles
	for _ in range(1000):

		# Get the positions of the cards to be swapped
		position1 = randint(0, len(working_deck) - 1)
		position2 = randint(0, len(working_deck) - 1)

		# Get the cards
		card1 = working_deck[position1]
		card2 = working_deck[position2]

		# Swap the cards
		working_deck[position2] = card1
		working_deck[position1] = card2

	# Shuffled!
	return working_deck


def deal(deck: list) -> tuple:
	'''
	Removes the top card from the deck, and returns said card

	Parameters:
		deck (list[tuple(int, int)]): a list of cards in the format
			(rank, suit); the last card will be removed
	
	Returns:
		(tuple(int, int)): the last card in the deck
	
	Doctests:
		>>> deck = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 0)]
		>>> deal(deck)
		(5, 0)
		>>> deck
		[(1, 0), (2, 1), (3, 2), (4, 3)]

		>>> deck = [(2, 1), (3, 2), (4, 3), (5, 0), (1, 0)]
		>>> deal(deck)
		(1, 0)
		>>> deck
		[(2, 1), (3, 2), (4, 3), (5, 0)]

		>>> deck = [(3, 2), (4, 3), (5, 0), (1, 0), (2, 1)]
		>>> deal(deck)
		(2, 1)
		>>> deck
		[(3, 2), (4, 3), (5, 0), (1, 0)]
	'''
	# The list.pop() method does exactly what I need
	return deck.pop()


def replace_card(card: tuple, hand: dict, deck: list) -> bool:
	'''
	Returns the given card to the given deck and replaces it with the top card

	Parameters:
		card (tuple(int, int)): the card to discard in the format: (rank, suit)
		hand (dict{list[tuple(int, int)]}): cards in the format: (rank, suit)
			organized by their suit
		deck (list[tuple(int, int)]): a list of cards in the format (rank, suit)
	
	Returns:
		(bool): True if the card was found, False otherwise
	
	Doctests:
>>> deck = [(1, 0), (2, 1), (3, 2), (4, 3)]
>>> hand = {0: [(5, 0)], 1: [(5, 1)], 2: [(5, 2)], 3: [(5, 3), (1, 3)]}
>>> replace_card((1, 3), hand, deck)
True
>>> deck
[(1, 3), (1, 0), (2, 1), (3, 2)]
>>> hand
{0: [(5, 0)], 1: [(5, 1)], 2: [(5, 2)], 3: [(5, 3), (4, 3)]}

>>> deck = [(1, 0), (2, 1), (3, 2), (4, 3)]
>>> hand = {0: [(5, 0)], 1: [(5, 1)], 2: [(5, 2)], 3: [(5, 3), (1, 3)]}
>>> replace_card((2, 3), hand, deck)
False
>>> deck
[(1, 0), (2, 1), (3, 2), (4, 3)]
>>> hand
{0: [(5, 0)], 1: [(5, 1)], 2: [(5, 2)], 3: [(5, 3), (1, 3)]}
	'''
	# Check if the hand has the card
	if card not in hand[card[1]]:
		return False
	# Remove the card from the hand
	hand[card[1]].remove(card)
	# Put the card in the deck
	deck.insert(0, card)
	# Deal a card from the deck...
	new_card = deal(deck)
	# and give it to the hand
	hand[new_card[1]].append(new_card)
	return True


def deal_hands(hand_num: int, deck: list) -> list:
	'''
	Creates a dictionary of hands with 5 cards each from the given deck

	Parameters:
		hand_num (int): the number of hands to deal
		deck (list[tuple(int, int)]): a list of cards in the format:
			(rank, suit); this list will be modified
	Returns:
		(list[dict{int: list[tuple(int, int)]}]): the dealt hands, each
			with 5 cards, organized by suit
	
	Doctests:
		>>> deck = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 0), (6, 1), (7, 2), \
(8, 3), (9, 0), (10, 1), (11, 2), (12, 3), (13, 0)]
		>>> deal_hands(2, deck)
		[{0: [(13, 0), (9, 0), (5, 0)], 1: [], 2: [(11, 2), (7, 2)], 3: []}, \
{0: [], 1: [(10, 1), (6, 1)], 2: [], 3: [(12, 3), (8, 3), (4, 3)]}]
		>>> deck
		[(1, 0), (2, 1), (3, 2)]

		>>> deck = [(3, 2), (4, 3), (5, 0), (6, 1), (7, 2), (8, 3), (9, 0), \
(10, 1), (11, 2), (12, 3), (13, 0), (1, 0), (2, 1)]
		>>> deal_hands(1, deck)
		[{0: [(1, 0), (13, 0)], 1: [(2, 1)], 2: [(11, 2)], 3: [(12, 3)]}]
		>>> deck
		[(3, 2), (4, 3), (5, 0), (6, 1), (7, 2), (8, 3), (9, 0), (10, 1)]
	'''
	# Dictionary of hands to return
	hands = []

	# Deal 5 cards
	for _ in range(5):
		# Deal to all hands
		for hand in range(hand_num):
			# If an entry for the current hand in the hands dictionary hasn't
			# been made yet, make one
			if len(hands) <= hand:
				hands.append({ 0: [], 1: [], 2: [], 3: [] })

			# Deal a card
			card = deal(deck)
			# Find the suit of the card
			card_suit = card[1]
			# Give the card to the current hand
			hands[hand][card_suit].append(card)

	return hands


def find_card(card_index: int, hand: dict) -> tuple:
	'''
	Finds the card at the given index

	Parameters:
		card_index (int): the index of the card to find
		hand (dict{list[tuple(int, int)]}): a dictionary of cards in the format
			(rank, suit) sorted by their suit

	Returns:
		(tuple(int, int)): the found card
	
	Doctests:
>>> find_card(3, {0: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)], 1: [], 2: [], 3: []})
(3, 0)

>>> find_card(5, {0: [(1, 0), (5, 0)], 1: [(2, 1)], 2: [(3, 2)], 3: [(4, 3)]})
(4, 3)
	'''
	card_count = 0
	for suit in hand.values():
		for card in suit:
			card_count += 1
			if card_count == card_index:
				return card
	return (0, 0)


def print_hand(hand: dict):
	'''
	Prints the cards in the given hand

	Parameters:
		hand (dict{int: list[tuple(int, int)]}): a dictionary of cards in the
			format: (rank, suit) sorted by suit
	
	Doctests:
		>>> print_hand({0: [(1, 0), (2, 0)], 1: [(3, 1)], 2: [(4, 2), (5, 2)], 3: []})
		1) Ace of Hearts
		2) 2 of Hearts
		3) 3 of Diamonds
		4) 4 of Clubs
		5) 5 of Clubs

		>>> print_hand({0: [], 1: [], 2: [], 3: [(6, 3), (9, 3), (8, 3), (1, 3), (7, 3)]})
		1) 6 of Spades
		2) 9 of Spades
		3) 8 of Spades
		4) Ace of Spades
		5) 7 of Spades
	'''
	# The number of the card in the hand
	card_number = 1

	# Get each card in their respective suit
	for suit in hand.keys():
		for card in hand[suit]:

			# Print the card
			print(f"{card_number}) ", end='')
			print_card(card)

			# Increment the card number
			card_number += 1


def check_raise(money: int, bet: int, bet_raise: int) -> bool:
	'''
	Checks if the player has enough money to raise the bet

	Parameters:
		money (int): the money a player has to bet with
		bet (int): the amount the player wishes to raise by
		bet_raise (int): the amount the bet has been raised to
	
	Returns:
		(bool): True if the bet is valid, False otherwise
	
	Doctests:
>>> check_raise(50, 10, 30)
True

>>> check_raise(50, 20, 30)
True

>>> check_raise(50, 30, 30)
False
	'''
	return money >= bet + bet_raise


def raise_bet(money: int, bet: int, current_bet: int) -> tuple:
	'''
	Places a bet

	Parameters:
		money (int): the money a player has to bet with
		bet (int): the amount to raise the current bet
		current_bet (int): the current bet
	
	Returns:
		tuple(int, int): the amount of money the player now has, and the new
			current bet
	
	Doctests:
>>> raise_bet(100, 10, 50)
(90, 60)

>>> raise_bet(10, 10, 0)
(0, 10)
	'''
	money -= bet
	current_bet += bet
	return (money, current_bet)


def print_raise(raised_bet: int, bet: int, name: str):
	'''
	Prints the given bet

	Parameters:
		raised_bet: the amount the bet is currently
		bet (int): the amount the player bet
		name (string): the name of the player betting
	
	Doctests:
>>> print_raise(25, 5, 'Nathan')
> Nathan bet $5, putting the bet to $25 <

>>> print_raise(200, 100, 'CPU 1')
> CPU 1 bet $100, putting the bet to $200 <

>>> print_raise(50, 0, 'CPU 3')
> CPU 3 met the bet of $50 <
	'''
	if bet == 0:
		print(f"> {name} met the bet of ${raised_bet} <")
		return
	print(f"> {name} bet ${bet}, putting the bet to ${raised_bet} <")


def print_balance(money: int, name: str):
	'''
	Prints the balance of the player

	Parameters:
		money (int): the available betting money of this player
		name (int): the name of this player
	
	Doctests:
>>> print_balance(50, 'Nathan')
Nathan has $50 to bet with

>>> print_balance(0, 'CPU 1')
CPU 1 has $0 to bet with
	'''
	print(f"{name} has ${money} to bet with")


def print_current_bet(bet: int):
	'''
	Prints the current bet amount

	Parameters:
		bet (int): the bet amount
	
	Doctests:
>>> print_current_bet(100)
The bet is at $100

>>> print_current_bet(50)
The bet is at $50
	'''
	print(f"The bet is at ${bet}")


def flush(hand: dict) -> int:
	'''
	Is the given hand a flush?

	Parameters:
		hand (dict{int: list[tuple(int, int)]}): a dictionary containing cards
			in the format: (rank, suit) sorted by their suit
	
	Returns:
		(int): 5 if a flush, 0 otherwise

	Doctests:
>>> flush({0: [(1, 0), (3, 0), (5, 0), (7, 0), (9, 0)], 1: [], 2: [], 3: []})
5

>>> flush({0: [], 1: [(1, 1), (2, 1), (3, 1), (4, 1)], 2: [(5, 2)], 3: []})
0
	'''
	# Check every suit in hand
	for suit in hand.values():

		# If suit doesn't have 5 cards, it isn't a flush
		if len(suit) != 5:

			# If suit also has more than 0 cards, no other suit is a flush and
			# so the hand isn't a flush
			if len(suit) > 0:
				return 0

			# Other suits may be a flush
			continue

		# This hand is a flush
		return 5

	# Getting here shouldn't be possible, unless the hand doesn't have 5 cards
	return 0


def hand_ranks(hand: dict) -> list:
	'''
	Creates a histogram of the hand, finding the number of cards in each rank

	Parameters:
		hand (dict{int: list[tuple(int, int)]}): a dictionary containing cards
			in the format (rank, suit) sorted by their suit
	
	Returns:
		(list[int]): a list of length 13, where each index represents a rank
	
	Doctests:
>>> hand_ranks({0: [(1, 0), (7, 0), (5, 0), (10, 0), (9, 0)], 1: [], 2: [], 3: []})
[1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0]

>>> hand_ranks({0: [(5, 0)], 1: [(5, 1), (9, 1)], 2: [(9, 3)], 3: [(9, 3)]})
[0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0]
	'''
	# The histogram, with an entry for every rank
	hist = [0] * 13

	# Loop through every suit
	for suit in hand.values():

		# Loop through every card in the suit
		for card in suit:

			# Add the value at the index of the card rank
			hist[card[0] - 1] += 1
	
	# Histogram is complete
	return hist


def straight(ranks: list) -> int:
	'''
	Is this hand a straight?

	Parameters:
		ranks (list[int]): a histogram of the cards ranks in a hand
	
	Returns:
		(int): 4 if a straight, 0 otherwise
	
	Doctests:
>>> straight([0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
4

>>> straight([0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0])
0

>>> straight([0, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0])
0

>>> straight([1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
4

>>> straight([1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
4

>>> straight([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1])
0
	'''
	# Check all the ranks up until the last 4
	# (to prevent overflow errors, also is unnecessary)
	for rank, count in enumerate(ranks[:-4]):

		# If the hand has an ace, and isn't A 2 3 4 5, check for the scenario
		# of 10 J Q K A
		if rank == 0 and ranks[1] == 0 and ranks[-4:] == [1] * 4:
			return 4

		# If the hand has the current rank...
		if count == 1:

			# If the next four ranks had a card, this hand is a straight
			if ranks[rank:rank+5] == [1] * 5:
				return 4

			# Otherwise, this hand is not a straight
			return 0

		# Otherwise, check the next rank
	
	# Getting here should be impossible, unless the hand didn't have 5 cards
	return 0


def straight_flush(hand: dict) -> int:
	'''
	Is the given hand a straight flush?

	Parameters:
		hand (dict{int: list[tuple(int, int)]}): a dictionary containing cards
			in the format (rank, suit) sorted by their suit

	Returns:
		(int): 8 if a straight flush, 0 otherwise

	Doctests:
>>> straight_flush({0: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)], 1: [], \
2: {}, 3: []})
8

>>> straight_flush({0: [], 1: [(8, 1), (7, 1), (5, 1), (9, 1), (6, 1)], \
2: [], 3: []})
8

>>> straight_flush({0: [], 1: [], 2: [(9, 2), (10, 2), (11, 2), (12, 2)], \
3: [(13, 3)]})
0

>>> straight_flush({0: [(1, 0), (2, 0), (3, 0), (4, 0), (6, 0)], 1: [], \
2: [], 3: []})
0
	'''
	# Is the hand a flush?
	if flush(hand) != 5:
		return 0

	# Is the hand a straight?
	if straight(hand_ranks(hand)) != 4:
		return 0

	# This hand is a straight flush
	return 8


def four_of_a_kind(ranks: list) -> int:
	'''
	Is this hand a four of a kind?

	Parameters:
		ranks (list[int]): a histogram of the cards ranks in a hand

	Returns:
		(int): 7 if hand is four of a kind, 0 otherwise
	
	Doctests:
>>> four_of_a_kind([0, 0, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0])
7

>>> four_of_a_kind([0, 0, 0, 1, 1, 0, 0, 0, 0, 3, 0, 0, 0])
0
	'''
	# Check every rank
	for rank in ranks:

		# If this rank has four cards, the hand is a four of a kind
		if rank == 4:
			return 7

		# If a rank has 2 cards, the hand can't be a four of a kind
		if rank >= 2:
			return 0
	
	# No ranks have 4 cards, this hand can't be a four of a kind
	return 0


def full_house(ranks: list) -> int:
	'''
	Is this hand a full house?

	Parameters:
		ranks (list[int]): a histogram of the cards ranks in a hand

	Returns:
		(int): 6 if hand is a full house, 0 otherwise
	
	Doctests:
>>> full_house([0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0])
6

>>> full_house([0, 0, 0, 0, 1, 1, 0, 0, 3, 0, 0, 0, 0])
0

>>> full_house([0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0])
0
	'''
	# Variables that will be true if there is a pair and a triple, respectively
	has_two = False
	has_three = False

	# Check every rank
	for rank in ranks:
		if rank == 3:
			has_three = True
		if rank == 2:
			has_two = True
	
	# Only if one rank has 3 cards and another rank has 2 can this hand be a
	# full house
	if has_three and has_two:
		return 6

	# This hand isn't a full house
	return 0


def three_of_a_kind(ranks: list) -> int:
	'''
	Is this hand a three of a kind?

	Parameters:
		ranks (list[int]): a histogram of the cards ranks in a hand
	
	Returns:
		(int): 3 if hand is three of a kind, 0 otherwise
	
	Doctests:
>>> three_of_a_kind([0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 1, 0, 0])
3

>>> three_of_a_kind([0, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0])
0

>>> three_of_a_kind([0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 2])
0
	'''
	# Make sure the hand isn't a full house
	if full_house(ranks) == 6:
		return 0

	# Check every rank
	for rank in ranks:

		# If the rank has 3 cards, it's a three of a kind
		if rank == 3:
			return 3

	# This hand isn't a three of a kind
	return 0


def two_pair(ranks: list) -> int:
	'''
	Is this hand a two pair?

	Parameters:
		ranks (list[int]): a histogram of the cards ranks in a hand

	Returns:
		(int): 2 if hand is two pair, 0 otherwise
	
	Doctests:
>>> two_pair([0, 0, 2, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0])
2

>>> two_pair([0, 0, 1, 1, 0, 0, 2, 0, 0, 1, 0, 0, 0])
0

>>> two_pair([2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
0
	'''
	# The number of pairs in the hand
	pair_num = 0

	# Check every rank
	for rank in ranks:

		# If this rank is a pair, add it to the count
		if rank == 2:
			pair_num += 1
	
	# If there were two pairs, then this hand is a two pair
	if pair_num == 2:
		return 2

	# This hand isn't a two pair
	return 0


def one_pair(ranks: list) -> int:
	'''
	Is this hand a one pair?

	Parameters:
		ranks (list[int]): a histogram of the cards ranks in a hand
	
	Returns:
		(int): 1 if the hand is a one pair, 0 otherwise
	
	Doctests:
>>> one_pair([0, 1, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0])
1

>>> one_pair([0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0])
0

>>> one_pair([0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0])
0
	'''
	# Make sure this hand isn't a two pair
	if two_pair(ranks) == 2:
		return 0

	# Check every rank
	for rank in ranks:
		
		# If this rank is a pair, the hand is a one pair
		if rank == 2:
			return 1
	
	# This hand isn't a one pair
	return 0


def hand_value(hand: dict) -> tuple:
	'''
	Finds the value of the hand based on its cards

	Parameters:
		hand (dict{int, list[tuple(int, int)]}): a hand of cards of the format
			(rank, suit) sorted by their suit
	
	Returns:
		(int, float): the first number is the highest card; the second number is
			a number to represent the value of the hand based on the values of
			the cards, like this:
			({2} * 5^0 + {3} * 5^1 + {4} * 5^2 + ... + {K} * 5^11 + {A} * 5^12)
			/ {1 * 5^11 + 4 * 5^12} + {hand rank}
	
	Doctests:
>>> hand_value({0: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)], 1: [], 2: [], 3: []})
(1, 8.238095390232381)

>>> hand_value({0: [(10, 0), (11, 0), (12, 0), (13, 0), (1, 0)], 1: [], 2: [], 3: []})
(1, 8.29752380952381)

>>> hand_value({0: [(10, 0), (11, 0), (12, 0), (13, 0)], 1: [(1, 1)], 2: [], 3: []})
(1, 4.29752380952381)
	'''
	# Card ranks in the hand
	ranks = hand_ranks(hand)
	# Move Ace to top rank (Ace has the highest value)
	ranks.append(ranks.pop(0))
	# Each rank in the ranks list has 5 possible values in a deck with only 4 suits
	# 0, 1, 2, 3, 4
	rank_amounts_num = 5
	# The max value a hand can have on ranks alone
	max_value = rank_amounts_num**11 + 4 * rank_amounts_num**12

	# Find the hand value on ranks alone
	hand_ranks_value = 0
	for rank, value in enumerate(ranks):
		# Like binary, this method allows any amount of any rank to not overlap
		# in value with other ranks
		hand_ranks_value += value * rank_amounts_num**(rank)
	
	# The hand's value: whole digit is the hand rank, decimal is the value of
	# the ranks in the hand
	hand_value = hand_ranks_value / max_value + find_hand_rank(hand)
	
	# If there is an ace, it is the highest
	if ranks[-1] != 0:
		return (1, hand_value)

	# Record the highest card
	highest = 0

	# Check every rank
	for rank, count in enumerate(ranks[:-1]):
		
		# If there is a card of this rank, then because we're iterating
		# upwards, it is the highest so far
		if count != 0:
			highest = rank + 2 # Fix zero index problem
	
	# Found the highest card
	return (highest, hand_value)


def find_hand_rank(hand: dict) -> int:
	'''
	Finds the ranking of this hand

	Parameters:
		hand (dict{int, list[tuple(int, int)]}): a dictionary containing cards
			in the format (rank, suit), sorted by their suit
	
	Returns:
		(int): the rank of the hand
	
	Doctests:
>>> find_hand_rank( \
{0: [], 1: [(1, 1), (2, 1), (8, 1), (9, 1), (5, 1)], 2: [], 3: []})
5

>>> find_hand_rank( \
{0: [], 1: [], 2: [(10, 2), (11, 2), (12, 2), (13, 2), (1, 2)], 3: []})
8

>>> find_hand_rank( \
{0: [(1, 0), (5, 0)], 1: [(1, 1)], 2: [(1, 2)], 3: [(1, 3)]})
7
	'''
	# A histogram of this hand's card ranks
	ranks = hand_ranks(hand)

	# Get the rank of this hand
	return max(straight_flush(hand),
		max(four_of_a_kind(ranks),
		max(full_house(ranks),
		max(flush(hand),
		max(straight(ranks),
		max(three_of_a_kind(ranks),
		max(two_pair(ranks), one_pair(ranks)
	)))))))


def compare_hands(hands: list, names: list) -> int:
	'''
	Find the best hand

	Parameters:
		hands (list[dict[int: list[tuple(int, int)]]]): a list of hands with
			cards in the format: (rank, suit) sorted by suit
		names (list[string]): a list of names for the players holding the hands
	
	Returns:
		int: the index of the winner
	
	Doctest:
>>> compare_hands([ \
{0: [], 1: [(1, 1), (2, 1), (8, 1), (9, 1), (5, 1)], 2: [], 3: []}, \
{0: [], 1: [], 2: [(10, 2), (11, 2), (12, 2), (13, 2), (1, 2)], 3: []}], \
["Nathan", "CPU"])
CPU's hand is the best!
Nathan's hand looses...
1

>>> compare_hands([ \
{0: [(2, 0), (8, 0)], 1: [(3, 1)], 2: [(5, 2)], 3: [(7, 3)]}, \
{0: [(5, 0), (13, 0)], 1: [(7, 1)], 2: [(9, 2)], 3: [(11, 3)]}], \
["Nathan", "CPU"])
CPU's hand is the best!
Nathan's hand looses...
1

>>> compare_hands([ \
{0: [(1, 0), (9, 0)], 1: [(3, 1)], 2: [(5, 2)], 3: [(7, 3)]}, \
{0: [(1, 0), (5, 0)], 1: [(1, 1)], 2: [(1, 2)], 3: [(1, 3)]}, \
{0: [], 1: [(10, 1), (11, 1), (12, 1), (13, 1), (1, 1)], 2: [], 3: []}], \
["Nathan", "CPU 1", "CPU 2"])
CPU 2's hand is the best!
Nathan's hand looses...
CPU 1's hand looses...
2
	'''
	# A list of the hand rank per hand
	ranking = []

	# Find the rank of each hand
	for hand in hands:
		ranking.append(find_hand_rank(hand))
		continue
	
	# Get the highest ranked hand
	highest_hand = 0

	# Check each hand
	for hand_index, this_hand in enumerate(hands):
		if hand_value(this_hand)[1] > hand_value(hands[highest_hand])[1]:
			highest_hand = hand_index

	# Found the highest hand

	# Message for winning hand
	print(f"{names[highest_hand]}'s hand is the best!")

	# Messages for loosing hands
	for this_hand in range(len(hands)):
		# Skip the winning hand
		if this_hand == highest_hand:
			continue
		print(f"{names[this_hand]}'s hand looses...")
	
	return highest_hand


def choose_bad_cards(hand: dict) -> list:
	'''
	Finds the cards to replace based on the rank of the hand

	Parameters:
		hand (dict{int, list[tuple(int, int)]}): a hand containing cards in the
			format (rank, suit) sorted by suit
	
	Returns:
		(list): a list of cards to be replaced in the hand
	
	Doctests:
>>> choose_bad_cards({0: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)], 1: [], 2: [], 3: []})
[]

>>> choose_bad_cards({0: [(1, 0), (2, 0)], 1: [(1, 1)], 2: [(1, 2)], 3: [(1, 3)]})
[(2, 0)]

>>> choose_bad_cards({0: [(1, 0), (2, 0)], 1: [(1, 1), (2, 1)], 2: [(1, 2)], 3: []})
[]

>>> choose_bad_cards({0: [(1, 0), (5, 0)], 1: [(2, 1)], 2: [(3, 2)], 3: [(4, 3)]})
[]

>>> choose_bad_cards({0: [(1, 0), (3, 0), (5, 0), (7, 0), (9, 0)], 1: [], 2: [], 3: []})
[]

>>> choose_bad_cards({0: [(1, 0)], 1: [(1, 1)], 2: [(1, 2)], 3: [(2, 3), (3, 3)]})
[(2, 3), (3, 3)]

>>> choose_bad_cards({0: [(1, 0), (2, 0)], 1: [(1, 1), (2, 1)], 2: [(3, 2)], 3: []})
[(3, 2)]

>>> choose_bad_cards({0: [(1, 0), (2, 0)], 1: [(1, 1), (3, 1)], 2: [(4, 2)], 3: []})
[(2, 0), (3, 1), (4, 2)]

>>> choose_bad_cards({0: [(1, 0), (9, 0)], 1: [(3, 1)], 2: [(5, 2)], 3: [(7, 3)]})
[(9, 0), (3, 1), (5, 2), (7, 3)]
	'''
	# find hand rank
	hand_rank = find_hand_rank(hand)
	ranks = hand_ranks(hand)

	# If the hand is a straight flush, don't discard at all
	if hand_rank == 8:
		return []

	# Four of a kind (1H, 1D, 1S, 1C, 2H)
	if hand_rank == 7:
		# Find rank that doesn't have 4 cards
		bad_rank = 0
		for rank, card_num in enumerate(ranks):
			if card_num != 4 and card_num != 0:
				bad_rank = rank + 1
				break
		# If the rank is good enough, keep it
		if bad_rank > 7:
			return []
		# Find the card with the found rank
		for suit in hand.values():
			for this_card in suit:
				if this_card[0] == bad_rank:
					return [this_card]
		# Shouldn't be possible to get here, unless hand is invalid
		return []

	# If the hand is a full house, don't discard at all
	if hand_rank == 6:
		return []

	# If the hand is a flush, don't discard at all
	if hand_rank == 5:
		return []

	# If the hand is a straight, don't discard at all
	if hand_rank == 4:
		return []

	# Three of a Kind (1H, 1D, 1S, 2C, 3C)
	if hand_rank == 3:
		# Find the ranks that don't have 3 cards
		bad_ranks = []
		for rank, card_num in enumerate(ranks):
			if card_num != 3 and card_num != 0:
				bad_ranks.append(rank + 1)
		# Find the cards for the found ranks
		bad_cards = []
		for suit in hand.values():
			for this_card in suit:
				if this_card[0] in bad_ranks:
					bad_cards.append(this_card)
		return bad_cards

	# Two Pair (1H, 1D, 2S, 2C, 3C)
	if hand_rank == 2:
		# Find the rank that doesn't have 2 cards
		bad_rank = 0
		for rank, card_num in enumerate(ranks):
			if card_num != 2 and card_num != 0:
				bad_rank = rank + 1
				break
		# Find the cards for the found ranks
		for suit in hand.values():
			for this_card in suit:
				if this_card[0] == bad_rank:
					return [this_card]
		# Shouldn't be possible to get here, unless hand is invalid
		return []

	# One Pair (1H, 1D, 2S, 3C, 4C)
	if hand_rank == 1:
		# Find the ranks that don't have 2 cards
		bad_ranks = []
		for rank, card_num in enumerate(ranks):
			if card_num != 2 and card_num != 0:
				bad_ranks.append(rank + 1)
		# Find the cards for the found ranks
		bad_cards = []
		for suit in hand.values():
			for this_card in suit:
				if this_card[0] in bad_ranks:
					bad_cards.append(this_card)
		return bad_cards

	highest_rank = hand_value(hand)[0]
	bad_cards = []
	for suit in hand.values():
		for this_card in suit:
			if this_card[0] != highest_rank:
				bad_cards.append(this_card)

	return bad_cards
