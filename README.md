# SpiderSolitaireProject
Code for (1) playing 4-suit Spider Solitaire without undo and (2) estimating the win rate with intelligent human play

In this project we aim to fulfill two (related) objectives:

(1) Given a Spider Solitaire starting hand with known identity of face-down cards, 
estimate the winning probability for an intelligent human player.

(2) Design an AI to achieve a reasonable win rate on random hands, assuming perfect shuffling.

It is assumed we play with four suits and UNDO IS NOT ALLOWED.

NOTE: There are plenty of research papers on Spider Solitaire, but they all assume undoing moves is 
allowed (or equivalently we are allowed to know the identity of unseen cards). In this case the winning chances
of any starting hand is always 0% or 100% with perfect play - at least in theory.


The AI uses the following concepts

(i) basic tree search (i.e. examine N random different options, choose the best one)
(ii) static evaluation function (rewards in-suit builds, turnovers, moving suits to foundations etc)
(iii) multiple-move look-ahead, stopping as soon as at least one new card is turned over.
(iv) super-moves (a term borrowed from Freecell) to traverse the search space more efficiently


It is assumed the reader already knows the basic rules and terminology of Spider Solitaire. 
This is easily found online.



## Description of *.py files:

Card.py: implements the Card class. Each card has a rank, suit, and is-visible flag. The game starts with
10 visible cards and 94 non-visible cards

Gamestate.py: implements the Gamestate class. The game state records the arrangement of cards in the tableau and stock.
Gamestate also implements useful functionality to help the AI. Example functions include evaluating the
position (e.g. +1 point for every in-suit build) and working out if a proposed move is legal (e.g. do we have
enough empty columns to shift an off-suit 65432 onto a seven?)

IMPORTANT: The Gamestate class records the rank/suit of both visible and non-visible cards but the AI can only
use information from visible cards when determining the best move(s).


Generate_random_startposition: This generates a random valid starting position (valid means every card
appears exactly twice, each column contains the correct number of cards and only 10 cards are visible etc).

NOTE: if you wanna generate a start position with known arrangement of face-down cards, simply generate a random
position to get the "correct format", then edit each card to have the correct suit and rank.

Calculate_equity: This estimates the equity (i.e. probability of winning) by repeatedly playing the same hand
and computing the ratio "number of wins" : "number of games".

The algorithm for playing one iteration of a starting hand is as follows: 

LOOP
	Let S be the current game state
	Guess 100 different legal move sequences (or "moveblocks"), but refusing to turn over any face-down cards 
	that are at the head of a pile 
	Evaluate each of the 100 resulting game states (using static evaluation function).
	Choose the move sequence with highest evaluation function
	Compute the "partial move sequence" that stops as soon as one turnover occurs 
	If the evaluation function has not improved (i.e. S' is not better than S): 
		if the stock is not empty:
			deal 10 more cards
		else:
			declare victory if 8 suits removed, else concede defeat.
END LOOP

Notes:
(i) The move sequence allows multiple columns to be headed by face-down cards. Effectively the move sequence
computes a "worst-case-scenario" where all newly turned cards are useless forcing us to deal a new row of cards.
(ii) If the move sequence does result in multiple turnovers, we execute a "partial sequence" turning over the first card
only. There is no need to commit ourselves to the whole sequence, since re-evaluation after seeing our new card may
lead to something even better.
(iii) Since we evaluate the whole sequence rather than a partial sequence, we might see strange behaviour at the
beginning, e.g. building off-suit is preferred to in-suit because both lead to the same worst-case scenario.
(iv) Each iteration might take some time to run, depending on the luck of the cards.

NOTE: The program never breaks an in-suit sequence like 8-7 of Spades, unless it is moving the 7 onto the
"other" 8 of Spades. In some deals this may be necessary to achieve victory, but my previous attempts to
allow breaking in-suit only succeed in trashing the win rate.


## USAGE:

To generate a random position and calculate its equity with 30 iterations of that hand.
(1) python generate_random_position foo.txt
(2) python calculate_equity.py foo.txt 30

To generate a specific position and calculate its equity with 30 iterations of that hand
(1) python generate_random_position foo.txt
(2) edit the text file manually
(3) python calculate_equity.py foo.txt 30

NOTE: it is not possible to calculate the equity of a hand with only the identity of the 10 face-up cards known.

FUN FACT: If you suspect a certain Spider Solitaire software XYZ is rigged (i.e. stacks the cards against a player
who wins too much) this program allows one to investigate XYZ by
comparing the equities of hands generated randomly versus hands generated by XYZ.


## TODO: Here are possibilities for further improvement of the program:

(1) The AI will only report number of wins/losses. It will not e.g. record the moves played to achieve a win or loss.
Edit the program to record moves to a log file

(2) I estimate the current version of this AI can win about 6% of games, assuming cards are shuffled perfectly.
I haven't tested many "data points" so 6% should be taken with a pinch of sodium chloride.
Edit the program to achieve an even higher win rate.

(3) Make a config file for various parameters (e.g. change numtries=100 when trying to find the best moveblock).

(4) Modify the algorithm to handle games played at the 1- or 2-suit level.

(5) Add a test suite consisting on various initial game states of various difficulty (easy, hard, impossible)
