import random
import re

#start with a deck of cards as a hash table
deck = {"AS": 11, "KS": 10, "QS": 10, "JS": 10, "10S": 10, "9S": 9, "8S": 8, "7S": 7, "6S": 6, "5S": 5, "4S": 4, "3S": 3, "2S": 2, "AC": 11, "KC": 10, "QC": 10, "JC": 10, "10C": 10, "9C": 9, "8C": 8, "7C": 7, "6C": 6, "5C": 5, "4C": 4, "3C": 3, "2C": 2, "AD": 11, "KD": 10, "QD": 10, "JD": 10, "10D": 10, "9D": 9, "8D": 8, "7D": 7, "6D": 6, "5D": 5, "4D": 4, "3D": 3, "2D": 2, "AH": 11, "KH": 10, "QH": 10, "JH": 10, "10H": 10, "9H": 9, "8H": 8, "7H": 7, "6H": 6, "5H": 5, "4H": 4, "3H": 3, "2H": 2}

#Start with a blank player hand and a blank dealer hand
playerHand = {}
dealerHand = {}

#player and dealer running total
playerHandTotal = 0
dealerHandTotal = 0

#card to show for dealer
dealerCardUp = ""

#most recent card added to hand
newCardName = ""
newCardValue = 0

#check to see if the user wants to play again after a win or loss
def playAgain():
	playAgain = raw_input("Play again? 1 for yes, 2 for no ")
	#check to see if player actually input 1 or 2
	if playAgain != "1" and playAgain != "2":
		print("Those aren't options, try again.")
		playAgain()
	#if play again, start the game back again
	elif playAgain == "1":
		startGame()
	#if no to play again, exit the program
	else:
		exit()

def aceCheck(hand):
	#regex for a key containing ace
	isAce = re.compile(r'A\w')


	#check to see if there are aces in the hand
	for key in hand.keys():
		 #check to see if the key is an ace
		 if isAce.match(key):
		 	#check to see if the ace has already been changed from 11 to 1
		 	if hand[key] != 1:
				#change the value for the ace to 1 rather than 11
				hand[key] = 1
				break

#Deal a card to a hand
def dealCard(hand):
	#import current state of the deck
	global deck
	global newCardName
	global newCardValue

	#get random card (cardName, cardValue) from deck
	cardName = random.choice(deck.keys())
	cardValue = deck[cardName]
		
	#add the cardName and cardValue to the hand
	hand[cardName] = cardValue

	#make the new card name and value updated
	newCardName = cardName
	newCardValue = cardValue

	#delete the card from the deck so it won't appear again this round
	del deck[cardName]

#start the game by giving two cards to the player
def playerHandStart(hand):
	#import current state of the players total
	global playerHandTotal

	#fill the players hand with two cards for the initial deal
	for i in range(2):
		dealCard(hand)

	#Add the values of each card in the hand to the players value
	for value in hand.values():
		playerHandTotal += value

	#check for a blackjack
	if playerHandTotal == 21:
		print("You won, blackjack!")
		playAgain()
	elif playerHandTotal == 22:
		aceCheck(playerHand)
		playerHandTotal = sum(playerHand.values())
		#print the total for the player to the console
		print("You have " + str(playerHand.keys()) + " for a total of " + str(playerHandTotal))
	else:
		#print the total for the player to the console
		print("You have " + str(playerHand.keys()) + " for a total of " + str(playerHandTotal))

#start the game by giving the dealer two cards and showing the player one
def dealerHandStart(hand):
	#import current state of dealers total
	global dealerHandTotal
	#import dealer shown card so it remains the whole hand
	global dealerCardUp

	#fill the dealers hand with two cards for the inital deal
	for i in range(2):
		dealCard(hand)

	#add the values of each card in the hand to the dealers value
	for value in hand.values():
		dealerHandTotal += value

	#check for two aces to start the hand
	if dealerHandTotal == 22:
		aceCheck(dealerHand)
		dealerHandTotal = sum(dealerHand.values())

	#get a single value for the card shown by the dealer
	for key in hand.keys():
		dealerCardUp = key

	#print one of the cards to the player
	print("The dealer is showing " + dealerCardUp)

#ask the player to hit or stay
def playerHitorStay(hand):
	#import player hand total and new card value information
	global playerHandTotal
	global newCardValue

	#get input from user, 1 to hit 2 to stay
	hitOrStay = raw_input("Hit or stay: 1 to hit, 2 to stay ")

	#check user to make sure 1 or 2 is given
	if hitOrStay != "1" and hitOrStay != "2":
		#if not 1 and not 2 ask again
		print("That's not a number, try again.")
		playerHitorStay(hand)
	#hit function	
	elif hitOrStay == "1":
		#add card to hand
		dealCard(hand)
		#add card value to value
		playerHandTotal += newCardValue

		#check to see if user busts or has 21
		if playerHandTotal == 21:
			print ("You have 21, Blackjack!")
			playAgain()
		elif playerHandTotal < 21:
			#print out to the user the players hand
			print("You have " + str(playerHand.keys()) + " totalling " + str(playerHandTotal))
			#ask for hit or stay again
			playerHitorStay(hand)
		else:
			#check to see if changing the ace
			aceCheck(hand)
			playerHandTotal = sum(hand.values()) 

			#if they are under or at 21, show the player their hand and see if they want to hit or stay
			if playerHandTotal <= 21:
				print("You have " + str(playerHand.keys()) + " totalling " + str(playerHandTotal))
				playerHitorStay(hand)
			else:
				#start the game over if they bust
				#print out to the user the players hand
				print("You have " + str(playerHand.keys()) + " totalling " + str(playerHandTotal))
				print("You busted, and lost.")
				playAgain()
	#stay function
	else:
		compareHands()

#check to see who won
def compareHands():
	#bring in hand values
	global dealerHandTotal
	global playerHandTotal
	#bring in new card value to add to dealers total
	global newCardValue

	#hit on the dealer until they go over 17
	if dealerHandTotal < 17:
		while dealerHandTotal < 17:
			dealCard(dealerHand)

			#add the new value to the dealerHandTotal
			dealerHandTotal += newCardValue

			#check to see if the hand is over 21
			if dealerHandTotal > 21:
				aceCheck(dealerHand)
				newDealerHandTotal = sum(dealerHand.values())
				if dealerHandTotal != newDealerHandTotal:
					dealerHandTotal = newDealerHandTotal
					compareHands()
				else:
					print("Dealer busts, you win")
					print("Dealer had " + str(dealerHandTotal) + str(dealerHand.keys()) + " and you had " + str(playerHandTotal) + str(playerHand.keys()))
					playAgain()
	#check if player lost
	if dealerHandTotal > playerHandTotal:
		print("You lost, dealer had " + str(dealerHandTotal) + str(dealerHand.keys()) + " and you had " + str(playerHandTotal) + str(playerHand.keys()))
		playAgain()
	#check if player won
	elif playerHandTotal > dealerHandTotal:
		print("You won, you had " + str(playerHandTotal) + str(playerHand.keys()) + " and the dealer had " + str(dealerHandTotal) + str(dealerHand.keys()))
		playAgain()
	#check for a push
	else:
		print("You tied for a push. Dealer had " + str(dealerHandTotal) + str(dealerHand.keys()) + " and you had " + str(playerHandTotal) + str(playerHand.keys()))
		playAgain()

#start the game up with default settings
def startGame():
	#set all global variables back to original settings
	global deck
	global playerHand
	global dealerHand
	global playerHandTotal
	global dealerHandTotal
	global dealerCardUp
	global newCardName
	global newCardValue
	#start with a deck of cards as a hash table
	deck = {"AS": 11, "KS": 10, "QS": 10, "JS": 10, "10S": 10, "9S": 9, "8S": 8, "7S": 7, "6S": 6, "5S": 5, "4S": 4, "3S": 3, "2S": 2, "AC": 11, "KC": 10, "QC": 10, "JC": 10, "10C": 10, "9C": 9, "8C": 8, "7C": 7, "6C": 6, "5C": 5, "4C": 4, "3C": 3, "2C": 2, "AD": 11, "KD": 10, "QD": 10, "JD": 10, "10D": 10, "9D": 9, "8D": 8, "7D": 7, "6D": 6, "5D": 5, "4D": 4, "3D": 3, "2D": 2, "AH": 11, "KH": 10, "QH": 10, "JH": 10, "10H": 10, "9H": 9, "8H": 8, "7H": 7, "6H": 6, "5H": 5, "4H": 4, "3H": 3, "2H": 2}

	#Start with a blank player hand and a blank dealer hand
	playerHand = {}
	dealerHand = {}

	#player and dealer running total
	playerHandTotal = 0
	dealerHandTotal = 0

	#card to show for dealer
	dealerCardUp = ""

	#most recent card added to hand
	newCardName = ""
	newCardValue = 0

	playerHandStart(playerHand)
	dealerHandStart(dealerHand)
	playerHitorStay(playerHand)

startGame()