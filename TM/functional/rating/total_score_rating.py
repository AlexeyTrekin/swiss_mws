from .rating import Rating, RatingCalc
from ...model import Fight


class TotalScoreRating(RatingCalc):
    def __call__(self, fight: Fight):
        total_score_1 = fight.total_score_1
        total_score_2 = fight.total_score_2
        if total_score_1 == total_score_2:
            return Rating([self.draw_rating]), Rating([self.draw_rating])


class RoundsWonRating(RatingCalc):
    pass

class ScoreDiffRating(RatingCalc):
    pass
