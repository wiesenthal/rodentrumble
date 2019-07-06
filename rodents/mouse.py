from rodent import Rodent

class Mouse(Rodent):
	'''Mice are versatile, well rounded rodents, which specialize in well-timed, reliable attacks.'''
	def __init__(self, name, health=50.0, strength=50.0, dexterity=50.0, accuracy=50.0, charisma=50.0, ai=False):
		Rodent.__init__(self, name, health, strength, dexterity, accuracy, charisma, ai)
		self.moves['scratch'] = [self.scratch, 12]
		self.moves['timed stab'] = [self.timed_stab, 4]
		self.moves['gnaw'] = [self.gnaw, 3]
	
	@staticmethod
	def scratch(self, tempo, enemy):
		'''Scratch is a reliable, yet weak move which gains 10 tempo. Deals 90% damage. 1% miss chance, 1% crit chance.'''
		dmg = self.stats['str'] * .5
		crit = Rodent.crit(self.stats['acc'], crit_chance=1, miss_chance=1)
		dmg *= crit
		return (dmg, 10, crit, '')
	
	@staticmethod
	def timed_stab(self, tempo, enemy):
		'''Timed stab is a precise move with 15 tempo loss, which deals extra damage based on your current tempo. 0% miss chance, crit chance equal to tempo.'''
		dmg = self.stats['str']
		if tempo > 0:
			dmg += tempo * 2
		if tempo > 100:
			tempo = 100
		crit = Rodent.crit(self.stats['acc'], miss_chance=0, crit_chance=tempo)
		dmg *= crit
		return (dmg, -15, crit, '')
	
	@staticmethod
	def gnaw(self, tempo, enemy):
		'''Gnaw is a slow, high damaging move. 23 tempo loss, and deals double damage.'''
		dmg = self.stats['str'] * 2
		crit = Rodent.crit(self.stats['acc'])
		dmg *= crit
		return (dmg, -23, crit, '')