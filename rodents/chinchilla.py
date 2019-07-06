from rodent import Rodent
from random import choice

class Chinchilla(Rodent):
    '''Chinchillas are weak rodents with extremely high charisma. They tend to use alternative fighting methods.'''
    def __init__(self, name, health=40.0, strength=40.0, dexterity=50.0, accuracy=50.0, charisma=70.0, ai=False):
        Rodent.__init__(self, name, health, strength, dexterity, accuracy, charisma, ai)
        self.moves['lick'] = [self.lick, 10]
        self.moves['snuggle'] = [self.snuggle, 5]
        self.moves['copycat'] = [self.copycat, 1]
    
    @staticmethod
    def lick(self, tempo, enemy):
        '''Lick deals damage proportional to your charisma, and lowers your opponents accuracy and raises your accuracy each by 10%. -10 tempo. '''
        dmg = self.stats['chr'] * .9
        crit = Rodent.crit(self.stats['acc'])
        dmg *= crit
        if crit != 0:
            self.stats['acc'] *= 1.1
            enemy.stats['acc'] *= .9
            return (dmg, -10, crit, 'Eww, it licked em, changing each rodent\'s accuracy.\n' + repr(enemy) + '\n*')
        else:
            return (dmg, -10, crit, '')
    
    @staticmethod
    def snuggle(self, tempo, enemy):
        '''Snuggle is an extremely weak attack that lowers your opponents strength by 20%. Gains 10 tempo. However, on a miss (20%) nothing happens and you lose 20 tempo.'''
        dmg = self.stats['str'] *.2
        crit = Rodent.crit(self.stats['acc'], miss_chance=20)
        dmg *= crit
        if crit == 0:
            return (dmg, -20, crit, '')
        else:
            enemy.stats['str'] *= .8
            return (dmg, 10, crit, enemy.name + ' doesn\'t want to hurt ' + self.name + ' as much.\n' + repr(enemy))
    
    @staticmethod
    def copycat(self, tempo, enemy):
        '''Copy cat steals a random move from your opponent. Deals no damage. 0 tempo cost. 10% miss chance.'''
        crit = Rodent.crit(self.stats['acc'], miss_chance=10, crit_chance=0)
        if crit != 0:
            m = choice(list(enemy.moves.keys()))
            self.moves[m] = enemy.moves[m]
            del(self.moves['copycat'])
            return (0, 0, crit, 'Successfully copied ' + m + '.')
        else:
            return (0, 0, crit, '')
