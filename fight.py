from rodent import Rodent
from myprompt import *


def fight(r1: Rodent, r2: Rodent):    
    free_hit = False
    rodent1 = r1.clone()
    rodent2 = r2.clone()
    tempo = 0
    turn = 1
    rodent1.health = rodent1.stats['hp']*10
    rodent2.health = rodent2.stats['hp']*10
    print(repr(rodent1))
    print(repr(rodent2))
    print()
    
    def do_move(rod1, rod2):
        nonlocal tempo
        print(str(rod1) + ' attacking ' + str(rod2))
        if tempo >= 0:
            print('Current tempo: ' + str(tempo) + ' in the favor of ' +  rod1.name + ', out of ' + str(int(50*rod2.stats['dex']/rod1.stats['dex'])))
        else:
            print('Current tempo: ' + str(tempo*-1) + ' in the favor of ' +  rod2.name + ', out of ' + str(int(50*rod1.stats['dex']/rod2.stats['dex'])))
        print(rod1.name + ' health points: ' + str(round(rod1.health, 2)))
        print(rod2.name + ' health points: ' + str(round(rod2.health, 2)))
        print()
        damage, tempo_change, crit, special = rod1.attack(tempo, rod2)
        rod2.health -= damage
        if not free_hit:
            tempo += tempo_change
        if free_hit and tempo_change > 0:
            tempo += tempo_change
            
        print()
        if crit > 1:
            print('Critical hit!')
        if crit == 0:
            print('Swing and a miss!')
        else:
            print(rod1.name + ' dealt ' + str(round(damage, 2)) + ' points of damage.')
        
        def fix_stats(r):
            for k, v in r.stats.items():
                if v < 0:
                    r.stats[k] = 1
        fix_stats(rod1)
        fix_stats(rod2)
        
        if len(special) > 0 and special[-1] == '*':
            print(special[:-1] + repr(rod1))
        else:
            print(special)
        
        print()
    
    while rodent1.health > 0 and rodent2.health > 0:
        if turn > 0:
            if tempo*-1 >= 50*rodent1.stats['dex']/rodent2.stats['dex']:
                print(rodent1.name + ' fell behind on tempo! It\'s turn is skipped.')
                tempo += int(50*rodent1.stats['dex']/rodent2.stats['dex'])
                free_hit = True
            else:
                do_move(rodent1, rodent2)
                free_hit = False
        else:
            if tempo*-1 >= 50*rodent2.stats['dex']/rodent1.stats['dex']:
                print(rodent2.name + ' fell behind on tempo! It\'s turn is skipped.')
                tempo += int(50*rodent2.stats['dex']/rodent1.stats['dex'])
                free_hit = True
            else:
                
                do_move(rodent2, rodent1)
                free_hit = False
        turn *= -1
        tempo *= -1
        wait()
        print('\n'*5)
    if rodent1.health < rodent2.health:
        return rodent2
    else:
        return rodent1