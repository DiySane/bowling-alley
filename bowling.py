import random

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


def get_random_score(remaining):
    return random.randint(0, remaining)

def get_random_score_ten():
    return random.randint(0, 10)


class Chance:
    def __init__(self, frame):
        self.score = 0
        self.frame = frame
score1 = Chance(1)

class Frame:
    def __init__(self, id):
        self.is_spare = False
        self.is_strike = False
        self.frame_score = 0
        self.id = id
        self.ball_count = 2
        self.pin_count = 10

    def get_status(self):
        status = "!(spare||strike)"
        if self.is_strike:
            status = "strike"
        elif self.is_spare:
            status = "spare"
        return status

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

    def play_match(self, frame_id):
        self.play_frame(frame_id)

    def play_frame(self, frame_id):
        self.score_list = []
        self.current_frame_id = frame_id
        self.current_frame = Frame(self.current_frame_id)
        self.frame_list.append(self.current_frame)
        self.play_ball(frame_id)
        for i in range(len(self.score_list)):
            is_strike = self.score_list[i].frame.is_strike
            is_spare = self.score_list[i].frame.is_spare
            if(is_strike):
                self.score_list[i].frame.frame_score += self.score_list[i].score
                continue
            elif(is_spare):
                self.score_list[i].frame.frame_score += self.score_list[i].score
                i += 1
            else:
                self.score_list[i].frame.frame_score += self.score_list[i].score
        if(frame_id > 0 and self.frame_list[frame_id - 1].is_spare):
            self.frame_list[frame_id - 1].frame_score += self.score_list[0].score
        elif(frame_id > 0 and self.frame_list[frame_id - 1].is_strike):
            if(self.frame_list[frame_id].is_strike):
                self.frame_list[frame_id - 1].frame_score += self.score_list[0].score
            elif(frame_id - 1 > 0 and self.frame_list[frame_id - 2].is_strike):
                self.frame_list[frame_id - 2].frame_score += self.score_list[0].score
            else:
                self.frame_list[frame_id - 1].frame_score += self.score_list[0].score + self.score_list[1].score

    def play_ball(self, frame_id):
        if(self.current_frame.ball_count > 0 and self.current_frame.pin_count > 0):
            self.current_score = Chance(self.current_frame)
            self.score_list.append(self.current_score)
            self.current_score.score = self.get_score(self.current_frame.pin_count)
            self.current_score.frame.ball_count -= 1
            self.current_frame.pin_count -= self.current_score.score
            if(self.current_frame.pin_count == 0):
                if(self.current_score.frame.ball_count == 1):
                    current_score_amt = 0
                    for i in self.score_list:
                        current_score_amt += i.score
                    if(frame_id == 9 and current_score_amt < 30):
                        self.current_score.frame.ball_count += 1
                    self.current_score.frame.is_strike = True
                else:
                    self.current_score.frame.is_spare = True
            self.play_ball(frame_id)
        else:
            return

    def get_score(self, pin_count):
        return get_random_score(pin_count)

    def update_total_score(self):
        self.total_score = 0
        for frame in self.frame_list:
            self.total_score += frame.frame_score
        return self.total_score

    def __str__(self):
        return "Name: " + str(self.name) + ", Score: " + str(self.total_score)

class Game:
    def __init__(self, player_list):
        self.player_list = player_list
        self.winner = None
        self.runners_up = None

    def set_winner(self):
        max_score = 0
        next_max_score = 0
        count = 0
        is_winner_decided = False
        while (count < 10):
            for player in self.player_list:
                player.play_match(count)
                player.update_total_score()
                # print("The player with id: {}, name: {} for frame: {} has scored: {} with status: {}".format(player.ident, player.name, str(count), player.frame_list[count].frame_score, player.frame_list[count].get_status()))
                # print("The player with id: {}, name: {} for frame: {} has scored in total: {}".format(player.ident, player.name, str(count), player.total_score))
                if(player.total_score > max_score):
                    max_score = player.total_score
                    if(not is_winner_decided):
                        self.winner = player
                elif(player.total_score > next_max_score):
                    next_max_score = player.total_score
                    self.runners_up = player
                if(max_score > (next_max_score + (9 - count)*30)):
                    is_winner_decided = True
                if(count == 9):
                    print("The player with id: {}, name: {} has scored in total: {}".format(player.ident, player.name, player.total_score))
            count += 1
        return

    def get_winner(self):
        return self.winner

def main():
    player1 = Player(1, "A")
    player2 = Player(2, "B")
    player3 = Player(3, "C")
    player4 = Player(4, "D")
    player5 = Player(5, "E")
    player6 = Player(6, "F")
    players = []
    players.append(player1)
    players.append(player2)
    players.append(player3)
    players.append(player4)
    players.append(player5)
    players.append(player6)
    game = Game(players)
    game.set_winner()
    print("The winner is: \n{}".format(game.get_winner()))

    print("\n-----------------------------------\n")

if __name__ == "__main__":
    main()

