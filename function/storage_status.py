class Storage():
    def __init__(self):
        self.result_monster = []
        self.result_player = []
        self.result_ground = []
        self.result_ladder = []
    def main(self, obj):
        #
        result_monster = obj['Monster']
        result_player = obj['Player']
        result_ground = obj['Ground']
        result_ladder = obj['Ladder']
        #
        self.result_monster = self.result_monster if len(result_monster)<1 else result_monster
        self.result_player = self.result_player if len(result_player)<1 else result_player
        self.result_ground = self.result_ground if len(result_ground)<1 else result_ground
        self.result_ladder = self.result_ladder if len(result_ladder)<1 else result_ladder
        #
        return {'Monster':self.result_monster, 
                'Player':self.result_player,
                'Ground':self.result_ground,
                'Ladder':self.result_ladder,}
