class Character:
    

    def __init__(self, x, y, radius, speed):
        self.position_x = x
        self.position_y = y
        self.speed = speed
        self.health = 100
        self.size = radius
        self.round_lost = False
        self.wins = 0

    def move_player_x(self, direction, dt):
        self.position_x += self.speed*direction*dt

    def move_player_y(self, dt):
        self.position_y += self.speed*dt
    
    def decrease_health(self, number):
        self.health -= number

    def new_round(self, opponent):
        self.round_lost = False
        self.health = 100
        opponent.health = 100

    def death(self, opponent):
        self.round_lost = True
        opponent.wins += 1


