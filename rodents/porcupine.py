from rodent import Rodent

class Porcupine(Rodent):
	'''Porcupines are highly dangerous rodents, with very low charisma (it's hard to make friends while surrounded with spikes).'''
	def __init__(self, name, health=60.0, strength=80.0, dexterity=40.0, accuracy=50.0, charisma=10.0, ai=False):
		Rodent.__init__(self, name, health, strength, dexterity, accuracy, charisma, ai)
		self.moves['bump'] = [self.bump, 7]
		self.moves['whirlwind'] = [self.whirlwind, 5]
		self.moves['defensive stance'] = [self.defensive_stance, 5]
	
	@staticmethod
	def bump(self, tempo, enemy):
		'''Bump is a quick ram into the enemy. 1.35x damage, 13.5% chance to crit, only 1.35x damage on crit. Loses 15 tempo.'''
		dmg = self.stats['str'] * 1.35
		crit = Rodent.crit(self.stats['acc'], crit_chance=13.5, crit_dmg = 1.35)
		dmg *= crit
		return (dmg, -15, crit, '')

	@staticmethod
	def whirlwind(self, tempo, enemy):
		'''Whirlwind is a wild spin move, launching quills all around. Deals 2.5x damage, but reduces your own strength by 15%. 20% chance to miss. (-30 tempo)'''
		dmg = self.stats['str'] *2.5
		crit = Rodent.crit(self.stats['acc'], miss_chance=20)
		dmg *= crit
		self.stats['str'] *= .85
		return (dmg, -30, crit, 'The porcupine lost some of its spikes. *')

	@staticmethod
	def defensive_stance(self, tempo, enemy):
		'''Defensive stance uses your quills to reflect damage equal to your opponents strength against him. 10 tempo cost.'''
		dmg = enemy.stats['str']
		crit = Rodent.crit(self.stats['acc'])
		dmg *= crit
		return (dmg, -10, crit, '')