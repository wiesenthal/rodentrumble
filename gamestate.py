import rodent
from rodents import mouse, rat, chinchilla, capybara, mole, porcupine, squirrel
from moves import MOVES
from shadyroach import ShadyRoach

class Gamestate:
    
    def __init__(self):
        self.player = None
        self.pre_lvl = 0
    
    def save(self, play, pl):
        self.player = play
        self.pre_lvl = pl
        f = open("save.txt", "w")
        def s(x): # for ease
            f.write(str(x) + ';')
        p = self.player # for ease
        #RODENT SAVING
        #Order: Name, type, id, level, money, friends, stats
        s(p.name)
        print(type(p).__qualname__)
        s(type(p).__qualname__)
        s(p.id)
        s(p.level)
        s(p.money)
        m_string = "$" + '~'.join([k + '=' + v1.__qualname__ + ':' + str(v2) for k, (v1, v2) in p.moves.items()])
        s(m_string)
        f_string = "$" + '~'.join([f.name + '&' + str(f.level) + '&' + str(f.money) + '&' + type(f).__qualname__ + '&' + ':'.join([str(v) for k, v in f.stats.items()]) for f in p.friends])
        s(f_string)
        stat_string = "$" + ':'.join([str(v) for k, v in p.stats.items()])
        s(stat_string)
        f.write('\n')
        
        f.write(str(self.pre_lvl) + '\n')
        f.close()
    
    def load(self):
        f = open("save.txt", "r")
        lines = []
        for line in f:
            lines.append(line.rstrip('\n'))
        
        first, moves, friends, stats = lines[0].split('$')
        name, rodent, id, level, money = first.rstrip(';').split(';')
        id, level, money = int(id), int(level), int(money)
        
        moves = moves.rstrip(';').split('~')
        new_moves = [m.split('=')[0] for m in moves]
        
        new_friends = []
        if len(friends) > 1:
            friends = friends.rstrip(';').split('~')
            for friend in friends:
                namef, levelf, moneyf, rodf, statsf = friend.split('&')
                levelf, moneyf = int(levelf), int(moneyf)
                statsf = statsf.split(':')
                statsf = [float(x) for x in statsf]
                f = eval(rodf.lower() + '.' + rodf + '(namef, *statsf)')
                f.level = levelf
                f.money = moneyf
                new_friends.append(f)
        
        stats = stats.rstrip(';').split(':')
        stats = [float(x) for x in stats]
        p = eval(rodent.lower() + '.' + rodent + '(name, *stats)')
        p.id = id
        p.level = level
        p.money = money
        p.friends = new_friends
        
        ldel = [m for m in p.moves.keys() if m not in new_moves]
        for m in ldel:
            del(p.moves[m])
        
        for m in new_moves:
            if m not in p.moves.keys():
                p.moves[m] = MOVES[m][0:2]
        
        return p
    