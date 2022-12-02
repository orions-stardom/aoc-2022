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
        opponent =  "ABC".index(plays[0])
        you = "XYZ".index(plays[1])
       
        # we have plays is 0-2 but need to inc score by 1-3
        score += you + 1
        if you == opponent:
            # draw
            score += 3

        needed = (opponent + 1) % 3
        if you == needed:
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
        opponent =  "ABC".index(plays[0])
        result = plays[1]
        
        if result == "X":
            score += (opponent - 1) % 3 + 1
        elif result == "Y":
            score += (opponent + 1) + 3
        elif result == "Z":
            you = (opponent + 1) % 3
            score += (you + 1) + 6
    
    return score
