##                                                    Assignment 2: Games and Bayes 

##### Part 1: IJK:

■  The problem is solved using :
	
    For determinstic Board
    ○ Minimax algorithm
    ○ Alpha Beta pruning
    For Non - Determinstic Board
    ○ Minimax algorithm
    ○ Alpha Bata Pruning 
    ○ Chance Nodes in Between Max and Min Nodes.
    
■  We have referred to the following :

    ○ https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
	
	
■ The program is implemented in a Minimax Algorithm to find the optimal solution.

■ To increase the computational efficiency we have used the alpha beta pruning technique.

■ Initial State :

    ○ With “A” present on the table in the position of (0,0). 

 A | -- | -- | -- | -- | -- 

 -- | -- | -- | -- | -- | -- 

 -- | -- | -- | -- | -- | -- 

 -- | -- | -- | -- | -- | -- 

 -- | -- | -- | -- | -- | -- 

 -- | -- | -- | -- | -- | -- 

■ Goal State :
	
	○ It depends on the player ::
		■ If the first player is “+” then the result is K.
		■ If the first  player is “-” then the result is k.

■ State Space & Successor Function:

	○ While we are iterating to reach our goal state , the successor function returns the successors of the 
	current board (i.e ‘L’,’R’,’U’,’D’) .

■ Mini-Max and Expectiminimax :

    ○ We have implemented the minimax algorithm and expecti-minimAax using alpha-beta pruning . For a deterministic games ,
    we are using minimax algorithm and for a non-deterministic game we are using the expectiminimax algorithm . 
    ○ For determinitic approach , while expanding the game tree , if we are reaching the pre-defined limit,
    we are computing the scores using the heuristic and returning the values , in non-deterministic we are doing the same but,
    if at the final depth, if it is a chance node, we are computing the avergae or expected values over that chance node using
    the heuritic and taking the avergae for that particular chance code.In non-deterministic game,
    for chance nodes, we are generating multiple instances for each move since after each move ,
    the placement of the next player can be on any of the empty tiles, so we are generating instances for the same move
    (Total number of instances = Number of empty tiles of that board and recursively running the minimax and avergaing 
    over all the succesors for that move .So, we simulated the placement of all possible placements by the generating
    intances of that move - (number of empty tile times) and computed expected/average values .  

■ Cost Function:

	No Cost Function.

■ We have calculated the following heuristics :

	○ A heuristic is a static Evaluation function which claluclates the winning and losing chance of position and gives
	the optimal move to win for the max player

■ We Implemented the following Heuristic for our MinMax Algorithm:
	
	First Part
	○ For max player we have considered the weighted values of all capital letters in the Board
	○ For min player we have considered the weighted values of all small letters in the Board 
	Second Part
	○ There is more advantage for the max player if he has same value adjacent to it in any other direction so we have
	considered the weighted averages of all capital letters who has letter(capital or small) adjacent to it and given
	more weightage to them
	○ There is more advantage for the min player if he has same value adjacent to it in any other direction so we have
	considered the weighted averages of all small letters who has letter(capital or small) adjacent to it and given more
	weightage to them
	
	

■ We also tried a number of heuristics such as : 

	○ Giving weightage to the whole matrix according to the various positions on the board.
	○ Calculating the score by iterating over the board.
	○ Max Tile on the Board : 
		■ Returning the highest valued letter on the board.
	○ Smoothness across the board:
		■ Measuring the difference between the neighbouring tiles.To check the similarity between the neighbouring tiles.
	○ Empty Tiles:
		■ Calculate the empty tiles present on the board.
	○ Corner Tiles present on the board:
		■ Calculating the presence of max tile on the corners of the board.


■ Observations :

	Effects due to increase in depth :
	○ As the depth kept increasing the computational time was increasing at a high rate but the steps to the goal state
		were optimal .
	Effects due to different heuristics :
	○ We have used a number of heuristics which are good for 2048 puzzle such as mentioned above. But our heuristic outperformed
	 them.though they are working fine with the randomly generated moves.
		■ We have included both the codes in the part 1 file with names
			ai_IJK.py (ORIGINAL)
			ai_IJK_2048.py (With researched Heuristes)
	 

<b> We implemented Expectiminimax using chance nodes for Non Determinstic case by creating another game instance and creating successor moves using the makeMove method in the empty tiles place, but we  got below error:
	
    File "C:\Users\Admin\Desktop\IUB-pvajja\Elements Of AI - David Crandel\Assingments\2\part1\logic_IJK.py", line 118, in 	__cover_up
    if mat[i][j] != ' ':
      IndexError: list index out of range
      
By the time we resolved the error , the time was up , knidly excuse us for the same.But unfortunately, non deterministic approach is taking lot of time.


##### Part 2: Horizon ﬁnding :

■ Emission Probability :

    ○ Case 1 and 2 : Simple and Viterbi 
    For these cases I have caluclated each pixels emission probability by its (edge strength)/(sum of edge strength of the column)
    ○ Case 3:
    Here , Given a human input (i,j) I am updating the emission probabilities for that particular column and row as well as adjacent
    column on each side and their corresponding rows. I am assigning a value of -log(math.inf) for all the other pixels and the jth
    row is assigned a value of log(1) .That is , I'm ensuring the that probability is 1 for the human observed point and same for
    the adjacent points.

■ Transitional Probability :

    ○ Assigned high priority of 0.1 for nearest 6 pixels transition and then next 3 pixel a value of 0.074999925
    and the remaining 3e-7 / remaining number of pixels.
    So, the main idea here is to ensure that there is high probability of the ridge line transitioning to near
    by pixels, since a ridge cannot have huge variations among adjacent pixels.
	
■ Observations :

    ○ We have noticed that for images which have good edge strength along the ridge line , the simple, viterbi and 
    human did fairly better in identifying the ridge line.But, in cases where the ridge line does not have enough edge
    strength, simple faired poorly, viterbi could in some cases develop a  smooth ridge line if edge strength is strong along 
    the line for example  in sample 1 and mountain7 images but the results weren't satifcatory. But, given the human feed back,
    the algorithm is able to develop a ridge line around that point and could stay on course if the edge strength is decent
    enough to allow transition and suprisngly performed better for example in  sample1,mounatin7,mountain images and ,
    but could not provide any better results when the edge strength is too strong ,hence deviated from the point 
    human has provided which can be seen from sample2 results,mountain3 and mountain 2 images images in results folder.
