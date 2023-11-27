'''
	SUITS => {0:"Hearts", 1:"Diamonds",  2:"Clubs",  3:"Spades"}  dict to map card suit to hand suit
	RANKS => (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)          tuple of card ranks
	CARD  => (rank,suit)                                          card is a tuple of rank and suit
	DECK  => [(rank,suit), (rank,suit), (rank,suit) . . . etc]    list of cards
	HAND  => {0:[], 1:[], 2:[], 3:[]}                             hands are organized by suit

	HAND RANKS
	1. Straight Flush:  All five cards are the same suit and in order
	2. Four of a Kind:  Four Cards of the same rank
	3. Full House:      Three Cards of one rank and two of another
	4. Flush:           Five cards of the same suit but not in order
	5. Straight:        Five Cards in sequence but not the same suit
	6. Three of a Kind: Three Cards of the same rank
	7. Two Pair:        A pair is two cards of the same rank. Two pair is two collections of pairs
	8. One Pair:        Two cards of the same rank
	9. No combination:  Ranked by highest card
'''

import random

def empty_hand() -> dict:
	'''
		generates an empty poker hand with the suits {0 - 3}
		as the keys and an empty list as teh value

		Parameter:
			None
		
		Returns:
			a dictionary
	'''
	return {0:[], 1:[], 2:[], 3:[]}

def generate_two_pair() -> dict:
	'''
		generates a 5 card poker hand containing 2 pair of matching ranks

		Parameter:
			None
		
		Returns:
			a dictionary of the format {0:[], 1:[], 2:[], 3:[]}
	'''
	# setup
	h       = empty_hand()				# start with an empty hand
	rank    = random.randint(1, 13)		# get a random rank	
	used    = []						# remember used cards
	ranks   = [rank]					# remember used ranks

	# generate first pair
	while len(used) < 2:
		suit = random.randint(0, 3)		# get a random suit
		if (rank, suit) not in used:	# has this card been seen yet?
			h[suit].append((rank, suit))	# no, add it to the hand
			used.append((rank, suit))		# remember it to not duplicate

	# pick a new rank, make sure it's new
	rank = random.randint(1, 13)		# get a random rank
	while rank in ranks:				# have we used this rank before"
		rank = random.randint(1, 13)		# yes, get a new one
	ranks.append(rank)					# got a new one, remember it and move on

	# generate second pair
	while len(used) < 4:				# this will take us up to 4 cards
		suit = random.randint(0, 3)		# get a random suit
		if (rank, suit) not in used:	# have we seen this card yet?
			h[suit].append((rank, suit))	# no, add it to the hand
			used.append((rank, suit))		# remember it to not duplicate

	# pick last card, must not have been used
	while len(used) < 5:				# need one more card to make a hand of 5
		suit = random.randint(0, 3)		# get a random suit
		rank = random.randint(1, 13)	# get a random rank
		if (rank, suit) not in used and rank not in ranks:	# have we seen this card yet?
			h[suit].append((rank, suit))						# no, add it to the hand
			used.append((rank, suit))							# remember it
	return h							# return the hand

def generate_N_of_a_kind(n: int) -> dict:
	'''
		generates a 5 card poker hand containing N cards of matching rank

		Parameter:
			n (int): the number of matching ranks to generate
		
		Returns:
			a dictionary of the format {0:[], 1:[], 2:[], 3:[]}
	'''
	# setup
	h           = empty_hand()			# start with an empty hand
	rank        = random.randint(1, 13)	# generate tyhe first rank
	used_card   = []					# keep track od used cards
	used_rank   = [rank]				# keep track of used ranks

	# generate N cards of same rank
	while len(used_card) < n:				# need N cards of matching rank
		suit = random.randint(0, 3)			# random suit
		if (rank, suit) not in used_card:	# have we used this card before?
			h[suit].append((rank, suit))		# no, add it to the hand
			used_card.append((rank, suit))		# remember this card to avoid duplicating

	# generate remaining (5 - N) cards, must not have been used
	while len(used_card) < 5:				# finish out the hand, up to 5 cards
		rank = random.randint(1, 13)		# random rank
		suit = random.randint(0, 3)			# random suit
		if (rank, suit) not in used_card and rank not in used_rank:	# has card been seen before?
			h[suit].append((rank, suit))								# no, add it to the hand 
			used_card.append((rank, suit))								# remember the card to avoid duplicating
			used_rank.append(rank)
	return h

def generate_straight() -> dict:
	'''
		generates a 5 card poker hand containing with the ranks in a sequence

		Parameter:
			None
		
		Returns:
			a dictionary of the format {0:[], 1:[], 2:[], 3:[]}
	'''
	# setup
	h		= empty_hand()			# start with an empty hand
	rank	= random.randint(1, 8)	# choose a random rank

	# generate a sequence of cards of same rank
	for i in range(5):				# need five cards
		suit = random.randint(0, 3)	# random suit
		h[suit].append((rank, suit))# add the card to the hand
		rank += 1					# increment the rank to ensure a sequence
	return h						# return the hand

def generate_flush() -> dict:
	'''
		generates a 5 card poker hand with all cards having the same suit

		Parameter:
			None
		
		Returns:
			a dictionary of the format {0:[], 1:[], 2:[], 3:[]}
	'''
	# setup
	h       = empty_hand()			# start with an empty hand
	suit    = random.randint(0, 3)	# get a random suit
	used    = []					# remember all used cards to not duplicate

	# generate five cards of same suit, must be unique
	while len(used) < 5:				# need 5 cards
		rank = random.randint(1, 13)	# get a random rank
		if rank not in used:			# have we used this rank before?
			h[suit].append((rank, suit))	# no, add the card to the hand
			used.append(rank)				# remember the card to not duplicate
	return h							# return the hand

def generate_full_house() -> dict:
	'''
		generates a 5 card poker hand with 3 cards of one rank
		and 2 cards of another rank

		Parameter:
			None
		
		Returns:
			a dictionary of the format {0:[], 1:[], 2:[], 3:[]}
	'''
	# setup
	h       = empty_hand()			# start with an empty hand
	rank    = random.randint(1, 13)	# get a random rank
	suit    = random.randint(0, 3)	# get a random suit
	ranks   = [rank]				# remember the ranks

	# generate 3 cards of same rank
	for i in range(3):
		h[suit].append((rank, suit))# add card to the hand
		suit = (suit + 1) % 4		# calculate a new suit

	# pick a new rank, must be new
	rank = random.randint(1, 13)
	while rank in ranks:
		rank = random.randint(1, 13)

	# generate remaining 2 cards of new rank
	suit = random.randint(0, 3)
	for i in range(2):
		h[suit].append((rank, suit))
		suit = (suit + 1) % 4
	return h

def generate_straight_flush() -> dict:
	'''
		generates a 5 card poker hand with a cards in the same rank and in order

		Parameter:
			None
		
		Returns:
			a dictionary of the format {0:[], 1:[], 2:[], 3:[]}
	'''
	# setup
	h       = empty_hand()			# start with an empty hand
	suit    = random.randint(0, 3)	# get a random suit
	rank    = random.randint(1, 8)	# get a random rank

	# generate sequence of five cards in same suit
	for i in range(5):
		h[suit].append((rank, suit))
		rank += 1					# increment rank to ensure order
	random.shuffle(h[suit])			# cards don't HAVE to be generated in order to be "in order"
	return h						# return hand