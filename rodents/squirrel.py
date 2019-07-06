from rodent import Rodent

class Squirrel(Rodent):
	'''Squirrels are extremely quick, low damage fighters which try to out-tempo their opponent and skip their turn.'''
	def __init__(self, name, health=20.0, strength=30.0, dexterity=90.0, accuracy=50.0, charisma=60.0, ai=False):
		Rodent.__init__(self, name, health, strength, dexterity, accuracy, charisma, ai)
		self.moves['bite'] = [self.bite, -1]
		self.moves['quick slash'] = [self.quick_slash, 12]
		self.moves['leap'] = [self.leap, 6]
		self.moves['flurry'] = [self.flurry, 4]
		
	@staticmethod
	def bite(self, tempo, enemy):
		'''For squirrels, bite deals 1.25x damage, and costs 0 tempo.'''
		d, _, c, s = Rodent.bite(self, tempo, enemy)
		return (d*1.25, 0, c, s)
	
	@staticmethod
	def quick_slash(self, tempo, enemy):
		'''Quick slash is a slightly less damaging move, which gains 15 tempo. 20% chance to crit.'''
		dmg = self.stats['str'] * .8
		crit = Rodent.crit(self.stats['acc'], crit_chance=20)
		dmg *= crit
		return (dmg, 15, crit, '')
	
	@staticmethod
	def leap(self, tempo, enemy):
		'''leap is a risky move which has 30% to miss and 30% to crit. On a miss, lose 30 tempo, on a crit gain 30 tempo. Otherwise, gain 20.'''
		dmg = self.stats['str']
		crit = Rodent.crit(self.stats['acc'], miss_chance=30, crit_chance=30)
		dmg *= crit
		tc = 20
		if crit == 0:
			tc = -30
		if crit == 2:
			tc = 30
		return (dmg, tc, crit, '')
	
	@staticmethod
	def flurry(self, tempo, enemy):
		'''Flurry consists of a series of lightning-fast attacks, dealing damage based on your strength. The higher your dexterity is, the more attacks you get. Each has a 15% chance to miss or crit. -40 tempo.'''
		dmg = self.stats['str']
		total = 0
		misses = 0
		crits = 0
		for i in range(int(self.stats['dex']//12)):
			crit = Rodent.crit(self.stats['acc'], miss_chance=15, crit_chance=15)
			total += dmg*crit
			if crit == 0:
				misses += 1
			if crit == 2:
				crits += 1
		return (total, -40, 1, str(int(self.stats['dex']//10)) + ' swipes of the claw! ' + str(misses) + ' misses, and ' + str(crits) + ' critical hits.' )