import sys
from random import randint
import math
import time
 
class Engine(object):
 
        def __init__(self, scene_map):
                self.scene_map = scene_map
 
        def play(self):
                current_scene = self.scene_map.opening_scene()
 
                while True:
                        print "\n----------"
                        next_scene_name = current_scene.enter()
                        current_scene = self.scene_map.next_scene(next_scene_name)
                        self.setter = current_scene
 
class BattleSystem(object):
 
        def __init__(self, room):
                self.room = room
                print "\nYou entered a room and there are %i monsters!" % len(self.room)
                time.sleep(2)
                print "\nThey spotted you!"
                time.sleep(2)
                print "\nHere they come!"
                time.sleep(1)
                       
        def kill_monster(self):
                self.room.pop(0)
       
        def first_attack_hint(self):
                if self.mark in range(1, 16):
                        self.first_aim = "running really low to the ground!"
                elif self.mark in range(86, 101):
                        self.first_aim = "suddenly jumped!"
                elif self.mark in range(16, 33):
                        self.first_aim = "running hunched a bit!"
                elif self.mark in range(33, 66):
                        self.first_aim = "running right at you!"
                elif self.mark in range(66, 85):
                        self.first_aim = "running very upright!"
 
        def combat(self):
                # Keeps track of turns - user attacks on odd numbers, Monster on even
                turn = 1
                # Not done/might scrap aim function
                aim = 0
                # Shows if guess was high or low relative to position of Monster
                self.space = ""
                # Gives clue on Monster's new position for the next turn
                self.closeness = ""
                # When shooting new monster, tells if Monster position is in lower, middle, or upper third
                self.first_aim = ""
                # Stores Max HP of each monster in order to print current HP v. starting HP
                max_hp = self.room[0][0]
                # This is the position of Monster, randomly given
                self.mark = randint(1, 101)
                # Shows how many steps Monster is away before they can begin attacking
                self.steps = self.room[0][4]
 
                # Makes indication of first monster attacking since there's only 3 monsters per room
                if len(self.room) == 3:
                        self.first_attack_hint()
                        print "\nThe first one is charging! It has a health of %i and %s" % (self.room[0][0], self.first_aim)
                else:
                        self.first_attack_hint()
                        print "\nHere comes another! It has health of %i and %s" % (self.room[0][0], self.first_aim)
               
                #While the room has any Monster in it or if player has not been killed
                while self.room and Player.health > 0:
                        # If you're not aiming, either aim or attack without aiming
                        if turn % 2 == 1 and aim == 0:
                                self.guess = int(raw_input("\nEnter value 1 - 100 or value 0 to take aim: "))
                                if self.guess == 0:
                                        print "\nYou've steadied your shot and the enemy is in your sights!"                           
                                        aim = 1
                                else:
                                        #attack with no aim
                                        self.no_aim()
                        # If you're aiming
                        elif turn % 2 == 1 and aim == 1:
                                mark = randint(1, 20)
                                self.guess = int(raw_input("\nEnter value 1 - 20: "))
                                #Placeholder no_aim function, but might get rid of aim altogether
                                self.no_aim(self.guess, self.room[0][0], self.mark)
                                aim = 0
                                print """
                   | Your HP: %s/100 |                      | Monster HP: %s/%s |
                                        """ % (Player.health, self.room[0][0], max_hp)
                        #If monster is killed
                        if self.room[0][0] <= 0:
                                self.room[0][0] = 0
                                print """
                   | Your HP: %s/100 |                      | Monster HP: %s/%s |
                                        """ % (Player.health, self.room[0][0], max_hp)
                                print "\nYou killed the monster!"
                                self.kill_monster()
                                if self.room:
                                        self.combat()
                                else:
                                        return
                        # Monster attacks on all even turns
                        if turn % 2 == 0:
                                # Monster inflicts damage or kills player - see below
                                self.steps_away()
                                # Monster attacks
                                self.defense()
                                print """
                   | Your HP: %s/100 |                      | Monster HP: %s/%s |
                                        """ % (Player.health, self.room[0][0], max_hp)
                        #print self.mark
                        turn += 1
       
        # If a valid number is entered, proceed to attack
        def no_aim(self):
                if math.isnan(self.guess) or self.guess < 1 or self.guess > 100:
                        print "\nYou're a Master Hunter, not a dumbass."
                else:
                        self.attack_wo_aim()
       
        # Assigns damage based on how close your guess is
        def attack_wo_aim(self):
                self.fatal_hit = randint(200, 250)
                self.critical_hit = randint(75, 80)
                self.hit = randint(30, 35)
                self.damage = 0
                self.distance()
 
                if self.guess == self.mark:
                        self.damage = self.fatal_hit
                        print """
                                |-----------------|
                                |                 |
                                |                 |
                                |  BOOM HEADSHOT! |
                                |                 |
                                |                 |
                                |-----------------|
                               
                                """
                        print "\nYou dealt a fatal blow of %s and killed the monster!" % self.fatal_hit
 
                elif self.guess in range(self.mark - 5, self.mark + 5):
                        self.damage = self.critical_hit
                        print """
                                |-----------------------|
                                |                       |
                                |                       |
                                |  CRITICAL HIT OF %s!  |
                                |                       |
                                |                       |
                                |-----------------------|
                               
                                """ % self.damage
                        print "\nYou dealt a critical blow of %s!" % self.critical_hit
 
                elif self.guess in range(self.mark - 10, self.mark + 10):
                        self.damage = self.hit
                        print """
                                |-----------------------|
                                |                       |
                                |                       |
                                |      HIT OF %s!       |
                                |                       |
                                |                       |
                                |-----------------------|
                               
                                """ % self.damage
                        print "\nYou dealt a blow of %s!" % self.hit
 
                else:
                        print """
                                |-----------------|
                                |                 |
                                |                 |
                                |   You missed!   |
                                |                 |
                                |                 |
                                |-----------------|
                               
                                """
                        print "\nYou missed! Your guess of %i was %s!" % (self.guess, self.space)
               
                self.room[0][0] -= self.damage
       
        #Tells how close guess is relative to Monster's previous location
        def distance(self):
                if self.guess > self.mark + 20:
                        self.space = "too high!"
                elif self.guess > self.mark:
                        self.space = "a bit high!"
                elif self.guess < self.mark - 20:
                        self.space = "too low!"
                elif self.guess < self.mark:
                        self.space = "a bit low!"
                else:
                        return
 
        #Tells where you should aim next
        def relative(self):
                if self.guess > self.mark + 15:
                        self.einstein = "Aim lower!"
                elif self.guess > self.mark:
                        self.einstein = "Aim a bit lower!"
                elif self.guess < self.mark - 15:
                        self.einstein = "Aim higher!"
                elif self.guess < self.mark:
                        self.einstein = "Aim a bit higher!"
                else:
                        return
 
        # Generates Monster'sn ext position
        def defense(self):
               
                chance = randint(1, 10)
 
                if self.mark in range(1, 15):
                        chance = randint(6, 10)
                elif self.mark in range(86, 100):
                        chance = randint(1, 5)
 
                if chance == 2 or chance == 3 and self.mark > 11:
                        self.mark -= randint(3, 10)
                        self.relative()
                        if self.mark in range(1, 15):
                                self.closeness = "\nThe monster is running really low to the ground!"
                        else:
                                self.closeness = "\nThe monster ducked a little! %s" % self.einstein
                elif chance == 4 or chance == 5 and self.mark > 25:
                        self.mark -= randint(11, 25)
                        self.relative()
                        if self.mark in range(1,15):
                                self.closeness = "\nThe monster is running really low to the ground!"
                        else:
                                self.closeness = "\nThe monster ducked! %s" % self.einstein
                elif chance == 6 or chance == 7 and self.mark < 89:
                        self.mark += randint(3, 10)
                        self.relative()
                        if self.mark in range(86, 101):
                                self.closeness = "\nThe monster jumped!"
                        else:
                                self.closeness = "\nThe monster raised its head a little! %s" % self.einstein
                elif chance == 8 or chance == 9 and self.mark < 75:
                        self.mark += randint(11, 25)
                        self.relative()
                        if self.mark in range(86, 101):
                                self.closeness = "\nThe monster jumped!"
                        else:
                                self.closeness = "\nThe monster raised its head! %s" % self.einstein
                elif chance == 1:
                        self.mark = randint(1, 15)
                        self.relative()
                        self.closeness = "\nThe monster is running really low to the ground!"
                elif chance == 10:
                        self.mark = randint(86, 101)
                        self.relative()
                        self.closeness = "\nThe monster jumped!"
               
                if self.mark > 100 or self.mark < 0:
                        self.mark = 50
                        print "\nThe monster is dead center!"
                        return
               
                print self.closeness
                if self.steps > 0:
                        print "\nThe monster is %i steps away" % self.steps
                        self.steps -= 1
                else:
                        return
 
                #print chance
 
        def steps_away(self):
 
                if self.steps == 0:
                        self.monster_inflict = randint(self.room[0][2], self.room[0][3])
                        Player.health -= self.monster_inflict
                        print "\nThe monster attacked you and did %i damage!" % self.monster_inflict
                        if Player.health <= 0:
                                Player.health = 0
                                print "\nYou lose the game!\n"
                                return
 
 
#Player's health stored here
class Player(object):
 
        health = 100
 
#All monsters stored here [HEALTH, (not relevant anymore), MINIMUM DAMAGE, MAXIMUM DAMAGE, STEPS AWAY,]
class Monsters(object):
       
        room1 = [[100, 100, 7, 10, 4], [140, 100, 12, 15, 4], [200, 100, 15, 20, 4]]
        room2 = [[100, 100, 7, 10, 3], [140, 100, 12, 15, 3], [200, 100, 15, 20, 3]]
        room3 = [[100, 100, 7, 10, 3], [140, 100, 12, 15, 3], [200, 100, 25, 30, 2]]
 
#"credits"
class Prologue(object):
 
        def enter(self):
                time.sleep(0.5)
                print "You are the greatest assassin never known."
                time.sleep(2.5)
                print "You arm yourself with just one weapon: an innocuous looking single-shot rifle"
                time.sleep(3.0)
                print "\n\nYou are Haven, the Master Hunter, and it's time to shoot some monsters down."
 
                time.sleep(2.5)
                print """
                                |--------------------------------------|
                                |                                      |
                                |                                      |
                                |        MASTER HUNTER                 |
                                |          a game by drivelous         |
                                |                                      |
                                |--------------------------------------|
                               
                                """
               
                time.sleep(2)
                game_decision = raw_input("Press ANY KEY to continue.")
 
                try:
                        input = raw_input
                except NameError:
                        pass
               
                return 'opening_scene'
 
class OpeningScene(object):
 
        def enter(self):
                print "You're standing outside of a large castle."
                time.sleep(1.5)
                print "You know the horror that exists within the walls"
                time.sleep(1.5)
                print "...and the likelihood that you won't come out alive..."
                time.sleep(2)
                print "...and the possibility for riches if you do."
                time.sleep(2)
                print "\n\nHAVEN: It has come."
                time.sleep(2.5)
 
                return 'first_scene'
 
class FirstScene(object):
 
        def enter(self):
                print "THE FIRST ROOM"
                time.sleep(2)
                print "Haven spots a group of other-worldly creatures."
                time.sleep(1.5)
                print "\n\nHAVEN: It's back to where you came from, demons!"
                time.sleep(2.0)
                first = BattleSystem(Monsters.room1)
                first.combat()
               
                if Player.health <= 0:
                        return 'death'
                else:
                        return 'second_scene'
       
       
class SecondScene(object):
       
        def enter(self):
                print "THE SECOND ROOM"
                time.sleep(2)
                second = BattleSystem(Monsters.room2)
                second.combat()
 
                if Player.health <= 0:
                        return 'death'
                else:
                        return 'third_scene'
 
class ThirdScene(object):
 
        def enter(self):
                print "THE THIRD ROOM"
                time.sleep(2)
                third = BattleSystem(Monsters.room3)
                third.combat()
               
                if Player.health <= 0:
                        return 'death'
                else:
                        print "Quitting!"
                        exit()
 
class DeathScene(object):
 
        def enter(self):
                print "Haven was devoured alive by the monsters."
                self.death = raw_input("Type T to try again or Q to quit: ")
 
                if self.death == 'T' or self.death == 't':
                        Player.health += 100
                        return 'first_scene'
                elif self.death == 'Q' or self.death == 'q':
                        exit()
                else:
                        print "\nI'm not sure what that means"
                        self.enter()
 
 
class Map(object):
 
        scenes = {
                'prologue': Prologue(),
                'opening_scene': OpeningScene(),
                'first_scene': FirstScene(),
                'second_scene': SecondScene(),
                'third_scene': ThirdScene(),
                'death': DeathScene()
        }
 
        def __init__(self, start_scene):
                self.start_scene = start_scene
 
        def next_scene(self, scene_name):
                return Map.scenes.get(scene_name)
 
        def opening_scene(self):
                return self.next_scene(self.start_scene)
 
#if you open with 2nd arg skip, skips long opening sequence
if len(sys.argv) == 2 and sys.argv[1] == "skip":
        a_map2 = Map('first_scene')
        a_game2 = Engine(a_map2)
        a_game2.play()
else:
        a_map = Map('prologue')
        a_game = Engine(a_map)
        a_game.play()