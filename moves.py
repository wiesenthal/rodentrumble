from rodent import Rodent
MOVES = {}

def concentrate(self, tempo, enemy):
    '''Concentrate costs 8 tempo and increases your strength, accuracy, and dexterity each by 10. Cannot miss or crit.'''
    self.stats['str'] += 10
    self.stats['dex'] += 10
    self.stats['acc'] += 10
    return (0, -8, 1, self.name + ' is more focused, and is bolstered with newfound energy. *')
MOVES['concentrate'] = [concentrate, 2, 10]

def stomp(self, tempo, enemy):
    '''Stomp is a powerful, basic move which deasl a base 80 damage plus your strength. Costs 20 tempo.'''
    dmg = self.stats['str'] + 80
    crit = Rodent.crit(self.stats['acc'])
    dmg *= crit
    return (dmg, -10, crit, '')
MOVES['stomp'] = [stomp, 3, 15]

def stab(self, tempo, enemy):
    '''Stab is a 70% damage, -5 tempo attack, with 25% chance to crit and triple crit damage.'''
    dmg = self.stats['str']*.7
    crit = Rodent.crit(self.stats['acc'], crit_chance=25, crit_dmg=4.286)
    dmg *= crit
    return (dmg, -5, crit, '')
MOVES['stab'] = [stab, 6, 7]

def curbstomp(self, tempo, enemy):
    '''Curbstomp is a move which has a lower miss chance and higher crit chance based on how high your tempo is. Deals 200% damage. -30 tempo. Will miss automatically if behind on tempo, and crit automatically if ahead by 40. Triple crit damage.'''
    dmg = self.stats['str']*2
    if tempo < 0:
        crit = 0
    if tempo > 40:
        crit = 3
    crit = Rodent.crit(self.stats['acc'], crit_chance=tempo*1.7, miss_chance=40-tempo, crit_dmg=3)
    dmg *= crit
    return (dmg, -30, crit, '')
MOVES['curbstomp'] = [curbstomp, 2, 20]

def bop(self, tempo, enemy):
    '''Bop is a quick weak move, which costs 0 tempo. Recovers 50% of tempo if behind.'''
    dmg = self.stats['str']*.7
    if tempo < 0:
        tc = tempo * -.5
    else:
        tc = 0
    crit = Rodent.crit(self.stats['acc'])
    dmg *= crit
    return (dmg, tc, crit, '')
MOVES['bop'] = [bop, 10, 8]

def choke(self, tempo, enemy):
    '''Choke deals 1.5x damage, and has crit chance corresponding to your strength, rather than accuracy. Costs 25 tempo. 10% miss chance, 10% crit chance.'''
    dmg = self.stats['str']*1.5
    crit = Rodent.crit(self.stats['str'], miss_chance=10, crit_chance=10)
    dmg *= crit
    return (dmg, -25, crit, '')
MOVES['choke'] = [choke, 3, 12]
    
def five_finger_death_punch(self, tempo, enemy):
    '''Five finger death punch is an extremely difficult move. Deals 10% damage. However, on a crit (2.5% chance) deals 2000% damage. (0 tempo)'''
    dmg = self.stats['str']*.1
    crit = Rodent.crit(self.stats['str'], crit_chance=2.5, crit_dmg=200)
    dmg *= crit
    if crit > 1:
        return (dmg, -10, 1, 'Woah! Five finger death punch critical hit! ' + enemy.name + '\'s heart explodes!')
    return (dmg, -10, crit, '')
MOVES['five finger death punch'] = [five_finger_death_punch, 2, 25]

def intimidate(self, tempo, enemy):
    '''Intimidate lowers the opponents strength by 10% of YOUR strength. Costs 0 tempo.'''
    dmg = 0
    crit = Rodent.crit(self.stats['str'], crit_chance=0)
    if crit >= 1:
        enemy.stats['str'] -= self.stats['str']*.1
        return (dmg, 0, crit, enemy.name + ' is scared.\n' + repr(enemy))
    else:
        return (dmg, 0, crit, '')
MOVES['intimidate'] = [intimidate, 1, 6]

def uppercut(self, tempo, enemy):
    '''Uppercut is a simple, powerful finishing move which costs 40 tempo, and must be used only if you have the tempo. Deals massive damage. Crit chance = 20%.'''
    if tempo <= 0:
        return (0, 0, 'Whiff! You cannot uppercut without positive tempo.')
    dmg = self.stats['str']**1.5 / 2
    crit = Rodent.crit(self.stats['acc'], crit_chance=20)
    dmg *= crit
    return (dmg, -40, crit, '')
MOVES['uppercut'] = [uppercut, 2, 25]

def slap(self: Rodent, tempo, enemy):
    '''Slap is a quick, half damaging move which gains 10 tempo. Deals more damage if you are ahead on tempo.'''
    dmg = self.stats['str']*.5
    if tempo > 0:
        dmg = self.stats['str'] * .75
    crit = Rodent.crit(self.stats['acc'])
    dmg *= crit
    return (dmg, 10, crit, '')
MOVES['slap'] = [slap, 8, 12]

def blood_sacrifice(self, tempo, enemy):
    '''Blood Sacrifice uses 25% of your max health and deals damage equal to the health subtracted. Costs 0 tempo. 10% crit, 10% miss'''
    dmg = self.stats['str']*.25
    self.health -= dmg
    crit = Rodent.crit(self.stats['acc'], 10, 10)
    dmg *= crit
    return (dmg, 0, crit, self.name + ' draws a portion of their own blood, taking ' + dmg + ' damage, leaving them with ' + self.health + ' hp.')
