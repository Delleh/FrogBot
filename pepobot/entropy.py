print("IMPORT: %s" % __name__)

from . import config
from . import functions

import random

frogPool = []

#the magic lavalamp, selects one from the pool and deletes it. "take a card from the deck and discord it"
def frogFromPool():
	global frogPool
	chosen = random.choice(frogPool)
	frogPool.remove(chosen)
	return chosen

#this resets the random frog pool to a full set at random "take the deck of cards and reshuffle"
def resetPool():
	global frogPool
	frogs = functions.getAllFrogs()

	for x in range(random.randint(1, 100)):
		random.shuffle(frogs)

	print("ENTROPY: Rebuilding the random list of {0} images, shuffling the deck {1} times...".format(len(frogs), x))

	frogPool = frogs
	return True

#figure out how much is left in the pool. "count how many cards are left in the deck before we are out"
def findPoolHealth():
	return (len(frogPool) / len(functions.getAllFrogs()))

#Resets the pool to a full pool and resets it "pit boss making sure the deck of cards is healthy for fair play"
def monitorPool():
	if findPoolHealth() <= 0.17:
		resetPool()
		print("ENTROPY: Pool health is low, rebuilding needed.")
	else:
		print("ENTROPY: (((DEBUG))) pool is {0}".format(round(findPoolHealth(),3)))