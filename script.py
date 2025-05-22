import sys
from rodents import mouse, rat, chinchilla, capybara, mole, porcupine, squirrel
from myprompt import wait, clear
from shadyroach import ShadyRoach
from fight import fight
from myprompt import *
from name_generator import name
from gamestate import Gamestate
import random

rodent_list = [mouse.Mouse, rat.Rat, chinchilla.Chinchilla,
               capybara.Capybara, mole.Mole, porcupine.Porcupine, squirrel.Squirrel]
rodent_names = [x.__name__.lower() for x in rodent_list]

can_save = True


def check_args():
    global can_save
    if '--nosave' in sys.argv:
        can_save = False


def pick_rodent():
    name = input('What is your name? ')
    while not name.isalpha() and len(name) < 2:
        name = input(
            'Invalid input. (Only letters, and must be length > 1) What is your name? ')

    h_dict = {}
    for cl in rodent_list:
        h_dict[cl.__name__.lower()] = cl.__doc__, -1
    c = select('What type of rodent would you like to be?',
               *rodent_names, index=True, info_full=h_dict)
    return rodent_list[c](name)


def random_enemy(level):
    n = name()
    rod = random.choice(rodent_list)(n, ai=True)
    ShadyRoach.random_lvl(rod, level-1)
    return rod


def random_death(rod):
    deaths = [' is defeated, blood pooling around it.', ' flies across the room, lifeless.',
              ' collapses, eyes rolling back.', ' is pummeled into the floor.', ' goes limp, head smacking the concrete.']
    return rod.name + random.choice(deaths)


def leave(player):
    global can_save
    if not can_save:
        quit()
    a = select('Would you like to save?', 'yes', 'no')
    if a == 'yes':
        g.player = player
        g.save(player, pre_lvl)
    quit()


def start_combat(player, enemy):
    fighter = player

    a = select('Would you like to befriend ' + enemy.name + '?', 'yes', 'no')
    if a == 'yes':
        if fighter.befriend(enemy):
            wait('You successfully befriended ' + enemy.name +
                 '!\n Friends: ' + ', '.join(fighter.get_friends()))
            return 0
        else:
            print('You failed to befriend your enemy. You must fight!')
    if len(fighter.friends) > 0:
        a = select(
            'Would you like to fight by yourself, or tap a friend in?', 'self', 'friend')
    else:
        a = 'self'
    if a == 'friend':
        h_dict = {}
        for i in fighter.friends:
            h_dict[i.name] = repr(i), -1
        f = select('Which friend?', *fighter.get_friends(),
                   info_full=h_dict, index=True)
        fighter = fighter.friends[f]
        fighter.ai = False
        print('Selected ' + str(fighter) + ' to fight.')
    else:
        print('You will fight.')
    if fight(fighter, enemy) == fighter:
        print(random_death(enemy))
        if enemy.level < fighter.level:
            loot = enemy.money
        else:
            loot = enemy.money + (enemy.level - fighter.level) * 2
        print(fighter.name + ' found ' + str(loot) +
              ' shiny trinkets from looting ' + enemy.name + '\'s corpse.')
        fighter.money += loot
        wait()
        return 1
    else:
        if fighter == player:
            print(enemy.name + ' beats you within an inch of your life.')
            if player.money < 10:
                print('You wake up, missing all ' +
                      str(player.money) + ' of your scraps.')
                player.money = 0
                wait()
            else:
                print('You wake up, $10 lighter.')
                player.money -= 10
                wait()
        else:
            print(random_death(fighter))
            del (player.friends[f])
            wait('Mourn your friend\'s passing')
        return -1


r_list = []
pre_lvl = 0


def cave(player):
    global r_list, pre_lvl
    clear()
    c = select('What would you like to do now?',
               'fight', 'shady roach', 'quit')
    if c == 'fight':
        print('You decide you want to get into the ring once again.')
        if len(r_list) == 0:
            r_list = [random_enemy(player.level), random_enemy(
                player.level + 1), random_enemy(player.level + 2)]
        elif len(r_list) < 3:
            r_list.append(random_enemy(pre_lvl))
        print('You see three opponents of varying difficulty, your reward will be based on their level. Use info to learn their stats. ' +
              ' | '.join([str(i) for i in r_list]))
        h_dict = {}
        for r in r_list:
            h_dict[r.name] = repr(r), -1
        if len(player.friends) > 0:
            h_dict['friend'] = 'Kill one of your friends to get all the money they have gathered.'
            c = select('Who would you like to fight?', *
                       [i.name for i in r_list], 'friend', info_full=h_dict, index=True)
        else:
            c = select('Who would you like to fight?', *
                       [i.name for i in r_list], info_full=h_dict, index=True)
        clear()
        if c == 3:
            h_dict = {}
            for i in player.friends:
                h_dict[i.name] = repr(i), -1
            f = select('Which friend?', *player.get_friends(),
                       info_full=h_dict, index=True)
            c = player.friends[f]
            c.ai = True
            clear()
            del (player.friends[f])
            pre_lvl = c.level + start_combat(player, c)
        else:
            pre_lvl = r_list[c].level + start_combat(player, r_list[c])
            r_list.remove(r_list[c])
        cave(player)
    elif c == 'shady roach':
        print('You decide to head over to the Shady Roach.')
        ShadyRoach.main(player)
        cave(player)
    else:
        leave(player)


if __name__ == '__main__':
    check_args()

    g = Gamestate()
    print('Welcome, to RODENT RUMBLE!')
    if can_save:
        skip = select('Load Game?', 'yes', 'no') == 'yes'
    else:
        skip = False

    if skip:
        player = g.load()
        print('You are ' + str(player) + '.')
        print(repr(player))
        wait()
        clear()
    else:
        player = pick_rodent()
        print('You are ' + str(player) + '.')
        print(repr(player))
        clear()

        print('You are scrounging for food in the sewer, when suddenly, a big current sweeps you away!')
        print('Luckily, as you are being pulled away to your doom, a large, sinewy paw reaches out and grabs you.')
        russ = rat.Rat('Russ')
        ShadyRoach.random_lvl(russ, 25)
        print('This extremely ripped, battle-scarred rat pulls you out of the current with ease.')
        print('Russ: Hey little buddy, I\'m Russ. You better be careful around these parts of the sewer.')
        wait('You ask him how to be like him')
        print('Russ: Oh you wanna know how to LIVE in these sewers? Come with me.')
        print('The rat takes you to a hidden hole underneath a trashcan, and suddenly you hear shouting, and see some torchlights.')
        wait()
        print('Russ: This is The Cave. It\'s an underground rodent fighting ring where all the cool rodents go to beat the shit out of each other.')
        wait('I want in')
        print('Russ: Well if you want to succeed, you have to learn how to fight. Each turn you select one of your moves, or type info_move, to learn more about each one.')
        print('Russ: Select carefully, because each move does something unique. The key to winning fights, however, is managing the tempo of the fight.')
        print('Russ: The tempo is sort of like this subtle tug-of-war between you and your opponent. Powerful moves will cost more tempo, causing you to fall behind your opponent.')
        print('Russ: If you fall behind the tempo limit, calculated via a ratio of each rodent\'s dexterity, your turn will be skipped, and your opponent gets a free hit, with zero tempo cost.')
        print('Russ: The same goes the other way, so try to time your moves correctly, and wear out your opponent. ')
        wait()
        print('Russ: That should be enough for now. Look at that baby there, why don\'t you challenge it to a fight, using what i told you?')
        wait('You go up and challenge the tiny mouse.')
        clear()
        if fight(player, mouse.Mouse(name(), 40, 40, 40, 40, 40, ai=True)) == player:
            print('The mouse falls to the ground, limp, covered in blood.')
            print('Russ: Nice kill! Now you\'re getting it!')
        else:
            print(
                'Russ: Wow, that\'s pretty embarassing. Well, it\'s okay. You will learn.')
        print('Russ: Here, I gotta go fight that capybara that was looking at me funny. Here are some shiny scraps, that\'s currency around here.')
        player.money += 10
        print(
            'He hands you 10 random trinkets covered in dirt. Balance: ' + str(player.money))

        wait()

        print('A cockroach beckons you over to a small hole in the wall after Russ leaves.')
        wait()
        clear()
        ShadyRoach.intro()
        clear()
        print(
            'You exit his shop, overwhelmed by possibility, heading back to the main cave.')
    cave(player)
