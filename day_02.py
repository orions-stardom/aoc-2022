def _parse(rawdata):
    return rawdata.splitlines() 


def part_1(*lines):
    r"""
    >>> part_1(*_parse('''\
    ... A Y
    ... B X
    ... C Z    
    ... '''))
    15
    """
    score = 0
    for line in lines:
        plays = line.split()
        op_play =  "ABC".index(plays[0])
        you_play = "XYZ".index(plays[1])
        
        score += you_play + 1
        you="rock paper scissors".split()[you_play]
        op="rock paper scissors".split()[op_play]
        if you_play == op_play:
            # draw
            score += 3

        elif you == "paper" and op == "rock" or \
             you == "scissors" and op == "paper" or \
             you == "rock" and op == "scissors":
            # win
            score += 6


    return score

def part_2(*lines):
    r"""
    >>> part_2(*_parse('''\
    ... A Y
    ... B X
    ... C Z    
    ... '''))
    12
    """

    score = 0
    for line in lines:
        plays = line.split()
        op_play =  "ABC".index(plays[0])
        result = plays[1]
        
        op="rock paper scissors".split()[op_play]
        if result == "X":
            # need to lose
            if op == "rock": # we play scissors
                score += 3
            if op == "paper":
                score += 1 # we play rock
            if op == "scissors":
                score += 2 # we play paper

        elif result == "Y":
            # draw
            score += op_play +1 + 3

        elif result == "Z":
            score += 6
            if op == "rock": # we play paper
                score += 2
            if op == "paper": # we play scissors
                score += 3
            if op == "scissors": # we play rock
                score += 1
    return score
