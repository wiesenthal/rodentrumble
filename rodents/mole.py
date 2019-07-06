from rodent import Rodent

class Mole(Rodent):
	'''Moles are high damage fighters with decent dexterity, often specializing in buffing themselves. However, they are blind, giving them terrible accuracy.'''
	def __init__(self, name, health=70.0, strength=70.0, dexterity=60.0, accuracy=20.0, charisma=40.0, ai=False):
		Rodent.__init__(self, name, health, strength, dexterity, accuracy, charisma, ai)
		self.moves['power punch'] = [self.power_punch, 5]
		self.moves['burrow'] = [self.burrow, 4]
		self.moves['double swipe'] = [self.double_swipe, 3]
	
	@staticmethod
	def power_punch(self, tempo, enemy):
		'''Power punch is a high damage, -20 tempo move, which increases your strength by 10. 15% chance to miss, 10% chance to crit.'''
		dmg = self.stats['str'] * 1.6
		crit = Rodent.crit(self.stats['acc'], crit_chance=10, miss_chance=15)
		dmg *= crit
		if crit > 0:
			self.stats['str'] += 10
			return (dmg, -20, crit, 'The mole is motivated by the power!\n*')
		else:
			return (dmg, -20, crit, '')
	
	@staticmethod
	def burrow(self, tempo, enemy):
		'''Burrow is a low damage move which throws your opponent off, gaining 10 tempo, and 10 dexterity. (Even on a miss)'''
		dmg = self.stats['str']*.4
		crit = Rodent.crit(self.stats['acc'])
		dmg *= crit
		self.stats['dex'] += 10
		return (dmg, 10, crit, 'The mole got into an advantageous position!\n*')

	@staticmethod
	def double_swipe(self, tempo, enemy):
		'''Double swipe is an attack using both your claws, giving you two opportunities to miss, or crit. Each attack does regular damage. 20% miss, 5% crit. Loses 20 tempo.'''
		dmg1, dmg2 = self.stats['str'], self.stats['str']
		crit1 = Rodent.crit(self.stats['acc'], miss_chance=20)
		crit2 = Rodent.crit(self.stats['acc'], miss_chance=20)
		dmg1 *= crit1
		dmg2 *= crit2
		sp = ''
		if crit1 == 0:
			sp += 'First hit missed!\n'
		elif crit1 == 2:
			sp += 'First hit crit!\n'
		if crit2 == 0:
			sp += 'Second hit missed!\n'
		elif crit2 == 2:
			sp += 'Second hit crit!\n'
		return (dmg1 + dmg2, -20, 1, sp)