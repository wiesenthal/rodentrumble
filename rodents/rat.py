from rodent import Rodent

class Rat(Rodent):
    '''Rats are powerful, high variance rodents. They play it cool in fights, then hit hard, with high miss, high crit attacks. Their diseased bodies allow them to debuff their opponents.'''
    def __init__(self, name, health=60.0, strength=70.0, dexterity=40.0, accuracy=40.0, charisma=40.0, ai=False):
        Rodent.__init__(self, name, health, strength, dexterity, accuracy, charisma, ai)
        self.moves['tail whip'] = [self.tail_whip, 9]
        self.moves['rabid slash'] = [self.rabid_slash, 4]
        self.moves['claw'] = [self.claw, 7]
    
    @staticmethod
    def tail_whip(self, tempo, enemy):
        '''Tail whip is a low damage move which regains 5 tempo, and on crit ensares the enemy, halving their dexterity. 10% miss chance, 20% crit chance.'''
        dmg = self.stats['str'] * .5
        crit = Rodent.crit(self.stats['acc'], crit_chance=20, miss_chance=10)
        dmg*=crit
        if crit > 1:
            enemy.stats['dex'] *= .5
            return (dmg, 5, crit, 'The tail catches its target and wraps around!\n'+repr(enemy))
        else:
            return(dmg, 5, crit, '')
    
    @staticmethod
    def rabid_slash(self, tempo, enemy):
        '''Rabid slash is an unwieldy (-30 tempo), but powerful move with high miss and crit chance, reducing the opponents strength by 5. 15% miss chance, 20% crit chance. 2.5x crit damage.'''
        dmg = self.stats['str']*2
        crit = Rodent.crit(self.stats['acc'], miss_chance=15, crit_chance=20, crit_dmg=2.5)
        dmg *= crit
        if dmg > 0:
            enemy.stats['str'] -= 5
            return (dmg, -30, crit, 'The wound is infected and ' + enemy.name + ' is weakened!\n'+repr(enemy))
        else:
            return (dmg, -30, crit, '')
    
    @staticmethod
    def claw(self, tempo, enemy):
        '''Claw is a basic slashing attack which costs 5 tempo. Deals 90% damage, with 10% miss chance, 45% crit chance, with 1.5x damage.'''
        dmg = self.stats['str'] * .9
        crit = Rodent.crit(self.stats['acc'], miss_chance=10, crit_chance=45, crit_dmg=1.5)
        dmg *= crit
        return (dmg, -5, crit, '')
    