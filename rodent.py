from myprompt import select
from random import random, choice, randint
from copy import deepcopy

class Rodent:
    
    @staticmethod
    def crit(accuracy, crit_chance = 5, miss_chance = 5, crit_dmg = 2):
        hit_roll = random()*100
        acc_m = (accuracy**1.25)/(50.0**1.25)
        if hit_roll < (miss_chance - acc_m)/acc_m:
            return 0
        elif hit_roll > 100 - (crit_chance + acc_m)*acc_m:
            return crit_dmg
        else: 
            return 1
        
    
    def __init__(self, name, health, strength, dexterity, accuracy, charisma, ai=False):
        self.ai = ai
        self.name = name
        self.stats = {'hp': health, 'str' : strength, 'dex': dexterity, 'acc' : accuracy, 'chr': charisma}        
        self.friends = []
        self.money = 0 if not ai else randint(1, 10)
        self.level = 1
        self.moves = {'bite': [self.bite, -1]}   
        self.id = randint(0, 1000000)
    
    def __str__(self):
        return '"' + self.name + '", level ' + str(self.level) + ' ' + type(self).__name__
    
    def __repr__(self):
        def read(s):
            return s + ': ' +  str(round(self.stats[s], 2))
        out = str(self) + ' current stats: \n'
        for i in ['hp', 'str', 'dex', 'acc', 'chr']:
            out += read(i) + '\t'
        return out
            
    def clone(self):
        st = ['hp', 'str', 'dex', 'acc', 'chr']
        l = [None, None, None, None, None]
        for k, v in self.stats.items():
            l[st.index(k)] = v
        new = type(self)(self.name, *l, ai=self.ai)
        new.id = self.id
        new.money = self.money
        new.level = self.level
        new.moves = deepcopy(self.moves)
        new.friends = deepcopy(self.friends)
        return new
    
    def __eq__(self, right):
        return self.id == right.id
    
    def befriend(self, opponent):
        chr_roll = random()*self.stats['chr']*2
        if chr_roll > opponent.stats['chr']:
            self.friends.append(opponent)
            return True
        else:
            return False
    def get_friends(self):
        for i in self.friends:
            yield i.name
    
    def attack(self, tempo, enemy):
        h_dict = {}
        for name, (f, num) in self.moves.items():
            h_dict[name] = (f.__doc__, num)
            
        if not self.ai:
            move = select('Select a move to use for your turn', *self.moves.keys(), info_full=h_dict)
            while self.moves[move][1] == 0:
                print('You are out of uses of ' +  move + ' try again.')
                move = select('Select a move to use for your turn', *self.moves.keys(), info_full=h_dict)
            self.moves[move][1] -= 1
        else:
            move = choice([m for (m, (_, uses)) in self.moves.items() if uses != 0])
            print(self.name + ' attempts to use ' + move + '.')
        
        return self.moves[move][0](self, tempo, enemy)
    
    @staticmethod
    def bite(self, tempo, enemy):
        '''Bite is a basic move, with unlimited uses. It deals damage equal to your strength, has 10 tempo loss, and has 5% to both miss and crit.'''
        dmg = self.stats['str']
        crit = Rodent.crit(self.stats['acc'])
        dmg *= crit
        return (dmg, -10, crit, '')