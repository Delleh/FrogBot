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
	return round(len(frogPool) / len(functions.getAllFrogs()), 3)

#Used to make sure the random pool has something in it, and resets when too low. Call on on_message() "pit boss making sure the deck of cards is healthy for fair play"
def monitorPool():
	if findPoolHealth() <= 0.17:
		print("ENTROPY: Pool health is low, rebuilding needed.")
		resetPool()