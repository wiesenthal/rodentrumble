from rodent import Rodent

class Capybara(Rodent):
	'''Capybaras are the world's largest rodent, making them super heavy, and high health. Very slow.'''
	def __init__(self, name, health=90.0, strength=60.0, dexterity=20.0, accuracy=30.0, charisma=50.0, ai=False):
		Rodent.__init__(self, name, health, strength, dexterity, accuracy, charisma, ai)
		self.moves['headbutt'] = [self.headbutt, 7]
		self.moves['slam'] = [self.slam, 5]
		self.moves['chomp'] = [self.chomp, 3]
	
	@staticmethod
	def headbutt(self, tempo, enemy):
		'''Headbutt is a regular damage, 5 tempo cost attack, with zero chance to crit. Deals extra damage when behind on tempo.'''
		dmg = self.stats['str']
		if tempo < 0:
			dmg += tempo*-.8
		crit = Rodent.crit(self.stats['acc'], crit_chance=0)
		dmg *= crit
		return (dmg, -5, crit, '')
	
	@staticmethod
	def slam(self, tempo, enemy):
		'''Slam is a powerful but costly move. It deals triple damage, but costs 45 tempo. Crit damage: * 1.5. Miss chance: 10%.'''
		dmg = self.stats['str'] * 3
		crit = Rodent.crit(self.stats['acc'], crit_dmg=1.5, miss_chance=10)
		dmg *= crit
		return (dmg, -45, crit, '')
	
	@staticmethod
	def chomp(self, tempo, enemy):
		'''Chomp is a very risky move, with 30% chance to miss. -17 tempo. On hit, you lift the enemy up with your jaws, dealing high damage and decreasing their accuracy by 10.'''
		dmg = self.stats['str'] * 2
		crit = Rodent.crit(self.stats['acc'], miss_chance=30)
		if crit > 0:
			enemy.stats['acc'] -= 10
			return (dmg, -17, crit, enemy.name + ' is lifted into the air!\n' + repr(enemy))
		dmg *= crit
		return (dmg, -17, crit, '')