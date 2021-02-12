import random

# frame_count = 10
# pin_count = 10
# max_ball_attempts = 2
# current_ball_attempts = 0
# current_pin_down_count = 0
# current_frame = 0
# is_strike = (current_ball_attempts == 1 and current_pin_down_count == 10)
# is_spare = (current_ball_attempts == 2 and current_pin_down_count == 10)
# is_tenth_frame_bonus = (current_frame == 10 and is_strike)

# Pending:
'''If you bowl a strike in the tenth frame, you get two more balls. If you
throw a spare, you get one more ball. A maximum of three balls can be
rolled in the final frame.'''
# is_open = (not is_strike and not is_spare)
# Pending:
'''Scoring is based on the number of pins you knock down. However, if
you bowl a spare, you get to add the pins in your next ball to that frame.
For strikes, you get the next two balls.'''
'''In a single lane, all players must bowl a frame before moving onto the
next frame. Say, p1 starts bowling frame1, followed by p2, p3... that
also bowl frame1 after which p1 steps in to bowl frame2.'''


def get_random_score():
    return random.randint(0, 10)


class Score:
    def __init__(self, frame):
        self.score = 0
        self.frame = frame
score1 = Score(1)

class Frame:
    def __init__(self, id):
        self.is_spare = False
        self.is_strike = False
        self.frame_score = 0
        self.id = id
        self.ball_count = 2
        self.pin_count = 10

class Player:
    def __init__(self, ident, name):
        self.ident = ident
        self.name = name

        self.score_list = []
        self.frame_list = []
        self.total_score = 0
        self.current_frame_id = 0
        self.current_frame = None
        self.current_score = None

    def play_match(self):
        self.play_frame()
        for i in range(len(self.score_list)):
            is_strike = self.score_list[i].frame.is_strike
            is_spare = self.score_list[i].frame.is_spare
            if(is_strike):
                self.total_score += self.score_list[i].score
                if(i + 2 < len(self.score_list)):
                    self.total_score += self.score_list[i+1].score + self.score_list[i+2].score
                continue
            elif(is_spare):
                self.total_score += self.score_list[i].score
                if(i + 2 < len(self.score_list)):
                    self.total_score += self.score_list[i+1].score + self.score_list[i+2].score
                i += 1
            else:
                self.total_score += self.score_list[i].score

    def play_frame(self):
        if(self.current_frame_id <= 10):
            self.current_frame_id += 1
            self.current_frame = Frame(self.current_frame_id)
            self.frame_list.append(self.current_frame)
            self.play_ball()
            self.play_frame()
        else:
            return

    def play_ball(self):
        if(self.current_frame.ball_count > 0 and self.current_frame.pin_count > 0):
            self.current_score = Score(self.current_frame)
            self.score_list.append(self.current_score)
            self.current_score.score = self.get_score()
            self.current_score.frame.ball_count -= 1
            self.current_frame.pin_count -= self.current_score.score
            if(self.current_frame.pin_count == 0):
                if(self.current_score.frame.ball_count == 1):
                    self.current_score.frame.is_strike = True
                else:
                    self.current_score.frame.is_spare = True
            self.play_ball()
        else:
            return

    def get_score(self):
        return get_random_score()

    def __str__(self):
        return "Name: " + str(self.name) + ", Score: " + str(self.total_score)

class Game:
    def __init__(self, player_list):
        self.player_list = player_list
        self.winner = None

    def set_winner(self):
        max_score = 0
        # for player in self.player_list:
        #     print(player)
        for player in self.player_list:
            player.play_match()
            print("The player with id: {}, name: {} has scored: {}".format(player.ident, player.name, player.total_score))
            if(player.total_score > max_score):
                max_score = player.total_score
                self.winner = player
            else:
                continue
        return

    def get_winner(self):
        return self.winner

def main():
    player1 = Player(1, "A")
    player2 = Player(2, "A")
    player3 = Player(3, "A")
    player4 = Player(4, "A")
    player5 = Player(5, "A")
    player6 = Player(6, "A")
    players = []
    players.append(player1)
    players.append(player2)
    players.append(player3)
    players.append(player4)
    players.append(player5)
    players.append(player6)
    # for player in players:
    #     print(player)
    game = Game(players)
    game.set_winner()
    print("The winner is: \n{}".format(game.get_winner()))

if __name__ == "__main__":
    main()

