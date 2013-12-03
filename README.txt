w4701 Artificial Intelligence
Project 3: Gomoku Playing Agent

Oren Finard
obf2107


Python 2.7 was used to develop and implement the Gomoku agent.
To run the program, navigate in terminal to the folder containing all the files.
Then type:
ptyhon
>>import gomoku 
>>gomoku.gomoku()

And you will be prompted for all appropriate inputs

My Evaluation Function:
A heads up: my program does not implement simple alpha-beta pruning.  I talked with Prof. Voris before and after writing my code, and he is aware of this.  Please feel free to double check with him if you have any concerns.

So, the story my evaluation function (further abbreviated as EF()) is a fun one.  After hours and hours of searching for a good evaluate a board of gomoku, I came up empty handed.  And so, like all frustrated people, I decided to give up and go in a new direction.
In my searching for a good EF() for evaluating a board, I came across this website: http://yjyao.com/2012/06/gomoku-in-html5.html.  The coder here talked about his EF(), and I thought it sounded very promising, so I started playing around with some of his ideas.  After a lot of fooling around and testing, I came up with a EF() to evaluate the most powerful positions on a give board.  This function became the evaluation function evaluate_position(), and it is described below:

evaluate_position():
It is important to recognize that gomoku is a zero-sum game.  An implication of this fact is that for a given board/game, your best move is also your opponent's best move.  If a position is a really good move for one player, it is an equally good move for the other player to move there so as to PREVENT their opponent from taking that space.  Thus, any position on a gomoku board can be represented as the sum of how useful that space is as an attack space for you and how useful that space is as an attack space for your opponents, or in other words, the space's attack value plus its defensive value.  Thus, by isolating a function that rates the attack value of a space, we can run that function for both teams, then add up the two scores, and that is the value of the position for either player.  The only slight caveat is that an attacking player should ALWAYS go for a win above going to block a win: other than a heavier weighting on winning than stopping a win, evaluate_position() needn't care whose turn it is.
An addendum: not every free space on the board needs to be checked.  Only spaces within a winning length of another piece need be checked for value, because anything further away from an existing piece than a winning connection is of value zero: it really offers no benefit to the game whatsoever, especially in a game where a single piece offers such a HUGE advantage to one player over another.  That's why black has such an advantage in gomoku- going first offers black a one-piece advantage as compared to white.
_eval_func() is the function abstractly talked about above that rates the attack power of a space for a give player.  Essentially, it looks at every possible way that a winning connection could be made for a given player, and counts the number of pieces already in that connection possibility.  The number of connections are then raised to the 5th, and summed together, and that is the score of the attack value.
Rephrased, a position's attack score = ∑(Player's Pieces in Possible Path)^5
There is a caveat that a winning move is given a rating of 100^9 (if the _eval_func() is evaluating attack power) or 100^8 (if the _eval_func() is evaluating a position's defensive power).  This makes sure that a position that represents a win or a loss will dominate any other moves on the board.
And that's all I have to say about that.

The purpose of having an EF() to evaluate a board was to be able to tell which moves were better than others by the board states they would result in.  However, I found that by having an EF() that would accurately order the importance of a move's position on the board, I could easily and naturally prune away silly or bad moves.  While the relation between how good one move versus another was could not be defined in an exact relationship (what does it mean that one move is 438, while another is 267?), the concepts that higher-valued moves were better, and that moves close together in numerical value reflected similar importance were strongly consistent. Thus, the most interesting moves could be easily and effectively isolated.

This EF() became an effective game playing agent when coupled with a quiescent search.  Without a good way to compare to game-states, it was impossible to rate two non-consecutive boards against each other.  And since evaluate_position() only rated importance of a position relative to specific game-state, it was effectively useless as tool to compare two non-consecutive boards.  Any attempt to use the numerical values of evaluate_position() would be thwarted by the fact that the actual numerical values produced were only meaningful in relation to the other numerical values of other positions in the same game-state: taken out of context of a specific game-state, the numbers produced by evaluate_position() are meaningless.  So the quiescent search developed was simply trinary: if looked ahead a depth, predicting all the best moves along the way, and would return 1 if it perceived a win, -1 if it perceived a loss, and 0 if it reached its limit before it could reach an end-state.  After rigorous testing, it was found that the quiescent search was more effective by trading depth for completeness in terms of forward-searching: by this, I mean that EF() was so good at predicting the best moves, that it was more effective to take the top X moves, and do a deep DLS on them than to continue checking the best moves of every node along the quiescent search.  This is because EF() so accurately predicts position importance: the approximate games played out by EF() along the quiescent search are accurate enough approximations of a reasonable agent that if a winning game is detected by the quiescent search, it means that a reasonable agent could lose along that tree, and so heading down that tree is a good idea.  Since the quiescent search trades completeness for depth, it can see accurately a long way ahead, and predict good ideas far in the future, and the accurate reasoning of EF() prevents blind-sided losses of getting within one move of a win, only to realize that the other player can win on their next move.
If no end states are detected by the quiescent search, then the AI will simply take EF()'s best move suggestion (or one of EF's suggestions if there are multiple equally valued moves).

The power of EF() ultimately in a powerful and efficient gomoku playing agent.  Since there are only a limited set of reasonable moves for a given board, and EF() can easily identify them, then the AI gets to spend the rest of it's time searching for a way to win.  It became easy to tell how effective this agent was when tested against various internet players, both automated and human.  I am excited to see how it performs in the tournament.



Me versus my AI:
I lose.  Every time.  I'm much better at computer science than I am at gomoku.  That said, my Dad is much better at gomoku than at computer science, so I got him to help me out here.  While we were debugging the AI and developing it, he could regularly crush the AI.  However, once EF() was fully debugged, it became impossible for him to win while he was white.  He put up a fairly strong fight when he was black, but he would still lose 7/10 times.  However, once the quiescent search was added, the difference in skill became enormous.  The AI would make moves that seemed ridiculous, but ended up being completely winning moves that neither of us could understand their initial (although critical) value.  The AI moved to a level where it became difficult to understand just how much better of a player it was.  It's anyone's guess how good it "actually" is- all I know is that it beats me and my dad every time.

Random versus my AI:
My AI wins every time.  But it takes longer to decide which move to make during the game than it does with a human.  This is because the AI is slower at the beginning of the game: when most moves are relatively trivial, and equally trivial, then the AI checks to it's maximum depth before coming up empty-handed, and just taking any move.  Since the random agent places tiles sporadically, and most often separated by large spaces, then to the AI it is like starting the game over and over repeatedly.  That said, it has never taken the AI more than 7 moves to beat Random (one time, Random made a chain, and AI decided to block it: that accounts for the extra 2 moves in that game)

AI versus AI:
This is the most interesting situation I have seen so far.  Ceteris paribus, black always beats white.  5/5, every time.  In fact, same parameters usually result in same games.  But I did a lot of exploring to find out how to get white to beat black.  What I have found is that white needs to be looking at least 5 moves ahead of black on average to have a fighting chance.  This doesn't always win, but the farther the gap in prediction depth, the greater chance white has of beating black.  This actually doesn't mean that white needs to take much longer than black; just that it needs the ability to look deeper than black.  If white can look 30 nodes deep, it can actually take LESS time to reach a decision than a shallower depth: if a win exists at depth 29 of EF()'s first suggested move, but no game state exists less than 20 nodes away from the current game state, black won't see an end coming, but white will be able to have 9 moves toward an endgame before black realize's it's being set-up for a loss.  This provides a strong argument for quiescent searching with a weighting of depth based on the value of EF(), but I have yet to experimentally establish a strong correlation between EF() value and a more likely win at a much deeper value: while I strongly suspect that to be true, until I establish that correlation, I can't make a decision to weight the depth of the moves checked in the quiescent search other than based off the fact that EF() returns moves in order of it's importance values (random ordering given for moves of equal position value).  I may do further testing to determine this correlation before the tournament. 







