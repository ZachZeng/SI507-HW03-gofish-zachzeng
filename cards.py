import random
import unittest

# SI 507 Fall 2018
# Homework 2 - Code

##COMMENT YOUR CODE WITH:
# Section Day/Time: Section 01 with 02
# People you worked with: None

######### DO NOT CHANGE PROVIDED CODE #########
### Scroll down for assignment instructions.
#########

class Card(object):
	suit_names =  ["Diamonds","Clubs","Hearts","Spades"]
	rank_levels = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}

	def __init__(self, suit=0,rank=2):
		self.suit = self.suit_names[suit]
		if rank in self.faces: # self.rank handles printed representation
			self.rank = self.faces[rank]
		else:
			self.rank = rank
		self.rank_num = rank # To handle winning comparison

	def __str__(self):
		return "{} of {}".format(self.rank,self.suit)

class Deck(object):
	def __init__(self): # Don't need any input to create a deck of cards
		# This working depends on Card class existing above
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card) # appends in a sorted order

	def __str__(self):
		total = []
		for card in self.cards:
			total.append(card.__str__())
		# shows up in whatever order the cards are in
		return "\n".join(total) # returns a multi-line string listing each card

	def pop_card(self, i=-1):
		# removes and returns a card from the Deck
		# default is the last card in the Deck
		return self.cards.pop(i) # this card is no longer in the deck -- taken off

	def shuffle(self):
		random.shuffle(self.cards)

	def replace_card(self, card):
		card_strs = [] # forming an empty list
		for c in self.cards: # each card in self.cards (the initial list)
			card_strs.append(c.__str__()) # appends the string that represents that card to the empty list
		if card.__str__() not in card_strs: # if the string representing this card is not in the list already
			self.cards.append(card) # append it to the list

	def sort_cards(self):
		# Basically, remake the deck in a sorted way
		# This is assuming you cannot have more than the normal 52 cars in a deck
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card)

	def deal(self, hand_num, hand_size):
		hand_list = []

		if(hand_size == -1):
			hand_size = int(len(self.cards)/hand_num)
			for i in range(hand_num):
				hand = Hand()
				for j in range(hand_size):
					hand.draw(self)
				hand_list.append(hand)

			rest_card_num = len(self.cards) % hand_num
			for i in range(rest_card_num):
				hand_list[i].draw(self)

		else:
			for i in range(hand_num):
				hand = Hand()
				for i in range(hand_size):
					hand.draw(self)
				hand_list.append(hand)
		
		return hand_list


class Hand(object):
	def __init__(self, init_cards=[]):
		self.cards = init_cards[:]

	def add_card(self, card):
		card_strs = [] 
		for c in self.cards: 
			card_strs.append(c.__str__()) 
		if card.__str__() not in card_strs: 
			self.cards.append(card)

	def remove_card(self, card):
		i = 0
		for c in self.cards:
			if(c.__str__() == card.__str__()):
				return self.cards.pop(i)
			i += 1
		return None

	def draw(self,deck):
		draw_card = deck.pop_card()
		self.cards.append(draw_card)

	def remove_pairs(self):
		
		dic = dict() #For recording the occurrences of each rank_number 
		numToIndex = dict() #For recording the index of each appearing rank_number
		del_index = [] #For storing all the index of item which need to be deleted
		
		i = 0

		for c in self.cards:
			if c.rank_num in dic:
				dic[c.rank_num] += 1
				numToIndex[c.rank_num].append(i)

			else:
				dic[c.rank_num] = 1
				numToIndex[c.rank_num] = []
				numToIndex[c.rank_num].append(i)
			
			i += 1

			if dic[c.rank_num] == 2:
				del_index.append(numToIndex[c.rank_num][0])
				del_index.append(numToIndex[c.rank_num][1])
				del dic[c.rank_num]
				del numToIndex[c.rank_num]

		for index in sorted(del_index, reverse = True):
			del self.cards[index]



def play_war_game(testing=False):
	# Call this with testing = True and it won't print out all the game stuff -- makes it hard to see test results
	player1 = Deck()
	player2 = Deck()

	p1_score = 0
	p2_score = 0

	player1.shuffle()
	player2.shuffle()
	if not testing:
		print("\n*** BEGIN THE GAME ***\n")
	for i in range(52):
		p1_card = player1.pop_card()
		p2_card = player2.pop_card()
		print('p1 rank_num=', p1_card.rank_num, 'p1 rank_num=', p2_card.rank_num)
		if not testing:
			print("Player 1 plays", p1_card,"& Player 2 plays", p2_card)

		if p1_card.rank_num > p2_card.rank_num:

			if not testing:
				print("Player 1 wins a point!")
			p1_score += 1
		elif p1_card.rank_num < p2_card.rank_num:
			if not testing:
				print("Player 2 wins a point!")
			p2_score += 1
		else:
			if not testing:
				print("Tie. Next turn.")

	if p1_score > p2_score:
		return "Player1", p1_score, p2_score
	elif p2_score > p1_score:
		return "Player2", p1_score, p2_score
	else:
		return "Tie", p1_score, p2_score

if __name__ == "__main__":
	deck = Deck()
	deck.shuffle()
	players = deck.deal(2, 7)
	current_player = 0
	# for hand in players:
	# 	for card in hand.cards:
	# 		print(card.__str__()) 
	while True:
		if len(deck.cards) == 0 | len(players[current_player].cards) == 0 | len(players[current_player % 1].cards == 0):
			print("game over")
			break
		for card in players[current_player].cards:
			print(card.__str__()) 

		input_card_A = int(input("Player " + str(current_player) + " Please choose a card rank\n"))
		flag = False
		valid = False
		for card in players[current_player].cards:
			if card.rank_num == input_card_A:
				valid = True

		if valid:
			for card in players[current_player ^ 1].cards:
				if card.rank_num == input_card_A:
					players[current_player ^ 1].remove_card(card)
					flag = True
			if flag:
				print("Player "+ str(current_player ^ 1) +"Go Fish!\n")
				players[current_player].draw(deck)
			current_player = current_player ^ 1
		else:
			print("Please choose a card rank in your hand\n")
		
		

# ######### DO NOT CHANGE CODE ABOVE THIS LINE #########

# ## You can write any additional debugging/trying stuff out code here...
# ## OK to add debugging print statements, but do NOT change functionality of existing code.
# ## Also OK to add comments!

# #########







# ##**##**##**##@##**##**##**## # DO NOT CHANGE OR DELETE THIS COMMENT LINE -- we use it for grading your file
# ###############################################

# ### Write unit tests below this line for the cards code above.

# class TestDeck(unittest.TestCase):
# 	def test_deal(self):
		
# 		#normal deal
# 		deck = Deck()
# 		deal_hands = deck.deal(5,6)
# 		self.assertEqual(len(deck.cards),52-30)
# 		self.assertEqual(len(deal_hands),5)
# 		self.assertEqual(len(deal_hands[0].cards),6)

# 		#all deal divisiable
# 		deck1 = Deck()
# 		deal_hands1 = deck1.deal(2,-1)
# 		self.assertEqual(len(deck1.cards),0)
# 		self.assertEqual(len(deal_hands1[0].cards),26)

# 		#all deal not divisiable
# 		deck2 = Deck()
# 		deal_hands2 = deck2.deal(3,-1)
# 		self.assertEqual(len(deck2.cards),0)
# 		self.assertEqual(len(deal_hands2[0].cards),18)
# 		self.assertEqual(len(deal_hands2[1].cards),17)


# class TestHand(unittest.TestCase):

# 	def test_remove_pair(self):
# 		#initialize, including edging case like 4 cards with same rank, 3 cards with same rank, 2 cards with same rank
# 		add_card = []
# 		add_card.append(Card(0,2))
# 		add_card.append(Card(1,1))
# 		add_card.append(Card(3,10))
# 		add_card.append(Card(1,2))
# 		add_card.append(Card(2,9))
# 		add_card.append(Card(2,4))
# 		add_card.append(Card(1,9))
# 		add_card.append(Card(0,9))
# 		add_card.append(Card(3,9))
# 		add_card.append(Card(1,8))
# 		add_card.append(Card(0,8))
# 		add_card.append(Card(3,8))
# 		hand = Hand(add_card)

# 		hand.remove_pairs()

# 		self.assertEqual(len(hand.cards),4)
# 		self.assertEqual(hand.cards[0].__str__(),"Ace of Clubs")



# #############
# ## The following is a line to run all of the tests you include:
# if __name__ == "__main__":
# 	unittest.main(verbosity=2)
# ## verbosity 2 to see detail about the tests the code fails/passes/etc.
