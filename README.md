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

Start with the command:
> python driver.py

Next initialise with a random file or an existing file (e.g. example.txt)

Click on single moveblock to "step through" the hand, or all moveblocks to play the entire hand.

NOTE: it is not possible to calculate the equity of a hand with only the identity of the 10 face-up cards known.


FUN FACT: This program allows you to investigate a particular Spider Solitaire program if you suspect it's rigged i.e.
it stacks the cards against a player who wins too much. 

Without loss of generality, assume the program in question is by Shay Dee Games. You can then generate 100 random hands
vs 100 hands by Shay Dee Games and compare win rates. If you find, e.g. this AI can beat random hands 15% of the time 
but 0% on Shay Dee Games hands then there is probably something fishy going on. 
Note that this does not constitute statistical proof that the game is indeed rigged, but at least the user has the tools to
investigate Shay Dee Games for himself if desired. 

In the shaydeegames directory, only 20 example hands are given. This AI should lose every hand in that directory.

NOTE: If you wish to investigate if Shay Dee Games is rigged,
I recommend you should practice playing Spider until you are able to beat virtually every hand with undo. This will
require perseverence on difficult hands - especially if Shay Dee Games *is* biased :-)