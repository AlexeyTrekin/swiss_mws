from typing import List
from TM.tournament import Round


def calc_rating_selections(rounds: List[Round]):
    # self.rating_score_1, self.rating_score_2 = rating_fn(self.rounds)
    # Критерии определения лучших: количество побед, количество ничьих, разница нанесенных и пропущенных
    # Поэтому за победу даем 10000, за ничью 1000, разницу учитываем как есть
    # Порядок критериев строго соблюдается если ничьих меньше 10, а баллов меньше 1000, что всегда верно
    # Selections (1-round fight)
    assert len(rounds) == 1

    score_diff = rounds[0].score_1 - rounds[0].score_2

    # Both lose on doubles, saving the point diff
    if rounds[0].doubles >= 4:
        return score_diff, -score_diff

    if score_diff == 0:
        # Draw rating
        return 1000, 1000
    elif score_diff > 0:
    # Win rating + score diff rating
        rating_1 = 10000 + score_diff
        rating_2 = 0 - score_diff
    else: #score_diff < 0
        rating_1 = 0 + score_diff
        rating_2 = 10000 - score_diff

    return rating_1, rating_2


def calc_rating_playoff(rounds: List[Round]):
    '''
    wins_1 = wins_2 = 0
    for round in rounds:
        if round.score_1 - round.score_2 > 0:
            wins_1 += 1
        elif round.score_1 - round.score_2 < 0:
            wins_2 += 1
    # We do not change the winner's rating and make the loser's rating negative so that we could remove him
    # Initial max rating equals number of finalists, so -100 will be enough
    if wins_1 > wins_2:
        return 0, -100
    elif wins_2 < wins_1:
        return -100, 0
    else:
        raise ValueError('Draw is not allowed in the finals')
    '''
    assert len(rounds) == 1

    # Both lose on doubles
    # However it would spoil the pairings (will fix it later) so we will assign a win, but without  a
    # if rounds[0].doubles >= 4:
    #    return -100, -100
    #

    if rounds[0].score_2 > rounds[0].score_1:
        return -100, 0
    elif rounds[0].score_1 > rounds[0].score_2:
        return 0, -100
    else:
        raise ValueError('Draw is not allowed in the playoff fights')
