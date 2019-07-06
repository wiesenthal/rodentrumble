from myprompt import select, wait, clear
from rodent import Rodent
import random
import moves

class ShadyRoach:
    dojo_dict = {}
    
    @staticmethod
    def drugs(rod: Rodent):
        print('Roach: So you would like to buy some drugs eh? 10 bucks.')
        print('Roach: How much money do you have?')
        print('You take out a knapsack with ' + str(rod.money) + ' shiny objects.')
        wait()
        if rod.money < 10:
            print('Roach: Hey, you can\'t buy anything with that chump change! Stop wasting my time.')
            ShadyRoach.main(rod, False)
        else:
            clear()
            print('Roach: Alright, that\'s what I\'m talking about!')
            print(repr(rod))
            info = {}
            info['hp'] = 'Higher hp means more health.', -1
            info['str'] = 'Higher strength means your attacks do more damage.', -1
            info['dex'] = 'With higher dexterity the threshold for you to fall behind on tempo is higher, and it is easier for your opponent to skip a turn.', -1
            info['acc'] = 'Higher accuracy means you are less likely to miss, and more likely to perform a critical hit.', -1
            info['chr'] = 'Your charisma determines how good you are at making friends.', -1
            
            c = select('Roach: Would you like to buy Morphine(health), Steroids(strength), Meth(dexterity), Adderall(accuracy), Weed(charisma)', 'hp', 'str', 'dex', 'acc', 'chr', info_full = info)
            rod.level += 1
            rod.stats[c] += 10
            rod.money -= 10
            print('Roach: Okay fantastic, your new ' + c + ' is: ' + str(rod.stats[c]) + '.')
            ShadyRoach.main(rod, False)
    
    @staticmethod
    def dojo(rod: Rodent):
        print('You enter the dojo, and see four red pandas each practicing different moves, as well as some mice meditating in the corner.')
        
        #generate moves
        while len(ShadyRoach.dojo_dict) < 4:
            r_move = random.choice(list(moves.MOVES.keys()))
            while r_move in ShadyRoach.dojo_dict:
                r_move = random.choice(list(moves.MOVES.keys()))
            ShadyRoach.dojo_dict[r_move] = moves.MOVES[r_move]
        
        if len(rod.moves.keys()) >= 5:
            print('Looks like you have maximum capacity moves.')
            c = select('Would you like to meditate or leave?', 'meditate', 'leave')
        else:
            c = select('Would you like to meditate or learn a new move?', 'meditate', 'learn')
        if c == 'learn':
            h_dict = {}
            for name, (f, num, cost) in ShadyRoach.dojo_dict.items():
                h_dict[name] = (f.__doc__ + "\ncost = $" + str(cost), num)
            m = select('What move would you like to learn?', *ShadyRoach.dojo_dict.keys(), info_full = h_dict)
            if rod.money >= ShadyRoach.dojo_dict[m][2]:
                rod.money -= ShadyRoach.dojo_dict[m][2]
                print('Learned ' + m + '! new balance: $' + str(rod.money))
                rod.moves[m] = ShadyRoach.dojo_dict[m][0:2]
                ShadyRoach.dojo_dict.clear()
            else:
                print('You do not have enough money for that move.')
            wait()
        elif c == 'meditate':
            h_dict = {}
            for name, (f, num) in rod.moves.items():
                h_dict[name] = (f.__doc__, num)
            c = select('Which move would you like to forget?', *rod.moves.keys(), info_full = h_dict)
            del(rod.moves[c])
        else:
            wait('You leave the dojo')
        

    @staticmethod
    def main(rod: Rodent, greeting = True):
        if greeting:
            print('Roach: Welcome back, ' + rod.name + '! Balance: $' + str(rod.money))
        c = select('Roach: Would you like to buy some performance enhancing drugs, or go to the dojo to learn a new move?', 'drugs', 'dojo', 'leave')
        if c == 'drugs':
            ShadyRoach.drugs(rod)
        elif c == 'dojo':
            ShadyRoach.dojo(rod)
            
    @staticmethod
    def intro():
        clear()
        print('Roach: Welcome my store, The Shady Roach!')
        print("Roach: I haven't seen you around before, you must be new. Let me show you around.")
        wait()
        clear()
        print("The cockroach leads you to the left side of his shop, to a shelf displaying a wide variety of powders, crystals, and fluids.")
        print('Roach: These are all the drugs I sell.')
        wait()
        clear()
        print('Roach: Most are performance enhancing: I have drugs that make you have more health, make you stronger, faster, smarter, and funnier.')
        print('Roach: These rodent fighting arenas are chock-full of juiced-up, roided-out mice so if you want to have a chance, you better fight dirty.')
        wait()  
        clear()
        print('The cockroach guides you to the back of his shop, to what looks to be some type of dojo.')
        print('Roach: This is my fighting studio, where for some special coin I can teach you new fighting moves.')
        print('Roach: Of course, you can only have a maximum of five moves, so you can also meditate in my dojo to forget a move.')
        wait()
        clear()
        print('Roach: So that\'s about all I sell here.')
        print('Roach: Be sure to come back and spend your money.')
        wait()
        clear()
        
    @staticmethod
    def random_lvl(rod: Rodent, num_lvl: int):
        rod.level += num_lvl
        for i in range(num_lvl):
            pick = random.choice(sorted(rod.stats.keys()))
            rod.stats[pick] += 10
            



