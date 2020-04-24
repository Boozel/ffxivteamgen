import xml.etree.ElementTree as et
import os, random, sys

mode = 'default'
dungeonlevel = 50

if '-l' in sys.argv:
    dungeonlevel = sys.argv[sys.argv.index('-l') + 1]
if '-c' in sys.argv:
    mode = 'chaos'

playerxmls = []
loadedplayernames = []
playerdict = {}
tanksMaster = []
tanks = []
healers = []
healersMaster = []
dps = []
dpsMaster = []
rolesdict = {'tank': tanks, 'healer': healers, 'dps': dps}
ortanks = []
orhealers = []
ordps = []
dictOneRolePlayers = {'tank': ortanks, 'healer': orhealers, 'dps': ordps}
supergrouptanks = []
supergrouphealers = []
supergroupdps = []
dictsupergroup = {'tank': supergrouptanks, 'healer': supergrouphealers, 'dps': supergroupdps}
groups = []

### Helper Methods ###

def ValidatePlayer(player, role):
    allowed = True
    if role is not 'tank' and len(dictsupergroup['tank']) < 2:
        if player in rolesdict['tank']:
            if len(rolesdict['tank']) <= 2 - len(dictsupergroup['tank']):
                    allowed = False
                    print("Can't allow " + player + " into role " + role + ": Would run out of tanks.")

    if role is not 'healer' and len(dictsupergroup['healer']) < 2:
        if player in rolesdict['healer']:
            if len(rolesdict['healer']) <= 2 - len(dictsupergroup['healer']):
                allowed = False
                print("Can't allow " + player + " into role " + role + ": Would run out of healers.")
    if role is not 'dps' and len(dictsupergroup['dps']) < 4:
        if player in rolesdict['dps']:
            if len(rolesdict['dps']) <= 4 - len(dictsupergroup['dps']):
                allowed = False
                print("Can't allow " + player + " into role " + role + ": Would run out of DPS.")
    #if(allowed == False):
        #print(group)
        #print(tanks)
        #print(healers)
        #print(dps)
        #input("waiting")
    return allowed

def AssignPlayer(player, role):
    dictsupergroup[role].append(player)
    if player in rolesdict['tank']:
        rolesdict['tank'].pop(rolesdict['tank'].index(player))
        if player in dictOneRolePlayers['tank']:
            dictOneRolePlayers['tank'].pop(dictOneRolePlayers['tank'].index(player))
    if player in rolesdict['healer']:
        rolesdict['healer'].pop(rolesdict['healer'].index(player))
        if player in dictOneRolePlayers['healer']:
            dictOneRolePlayers['healer'].pop(dictOneRolePlayers['healer'].index(player))
    if player in rolesdict['dps']:
        rolesdict['dps'].pop(rolesdict['dps'].index(player))
        if player in dictOneRolePlayers['dps']:
            dictOneRolePlayers['dps'].pop(dictOneRolePlayers['dps'].index(player))

def ListPlayersOneRole():
    for player in loadedplayernames:
        CheckPlayerOneRole(player)
            

def CheckPlayerOneRole(player):
    roles = 0x00
    if player in tanks:
        roles = roles | 0x01
    if player in healers:
        roles = roles | 0x02
    if player in dps:
        roles = roles | 0x04

    if roles == 0x01:
        dictOneRolePlayers['tank'].append(player)
    elif roles == 0x02:
        dictOneRolePlayers['healer'].append(player)
    elif roles == 0x04:
        dictOneRolePlayers['dps'].append(player)

def CreateRoster():
    # Get the Tank
    groupdict = {}
    player = ""
    breaklimit = 0
    resetRoster = True

    while(resetRoster == True):
        ListPlayersOneRole()
        resetRoster = False
        for tanker in range (2,0,-1):
            if len(rolesdict['tank']) >= 1:
                movingon = False
                while movingon == False and breaklimit < 10:
                    breaklimit += 1
                    #print(tanks)
                    #print(healers)
                    #print(dps)
                    #input("waiting")
                    if len(dictOneRolePlayers['tank']) > 0:
                        player = random.choice(dictOneRolePlayers['tank'])
                    else:
                        player = random.choice(rolesdict['tank'])
                    if ValidatePlayer(player, 'tank'):
                        movingon = True
                        AssignPlayer(player, 'tank')
                if breaklimit >= 10:
                    resetRoster = True 
            else:
                print("Ran out of tanks.")
                exit()
        breaklimit = 0
        for healer in range(2,0,-1):
            if len(rolesdict['healer']) >= 1:
                movingon = False
                while movingon == False and breaklimit < 10:
                    breaklimit += 1
                    #print(tanks)
                    #print(healers)
                    #print(dps)
                    #input("waitingi")
                    if len(dictOneRolePlayers['healer']) > 0:
                        player = random.choice(dictOneRolePlayers['healer'])
                    else:
                        player = random.choice(rolesdict['healer'])
                    if ValidatePlayer(player, 'healer'):
                        movingon = True
                        AssignPlayer(player, 'healer')
                if breaklimit >= 10:
                    resetRoster = True
            else:
                print("Ran out of healers.")
                exit()
    
        breaklimit = 0
        for dpser in range(4,0,-1):
            if len(rolesdict['dps']) >= 1:
                movingon = False
                while movingon == False and breaklimit < 10:
                    breaklimit += 1
                    #print(tanks)
                    #print(healers)
                    #print(dps)
                    #input("waiting")
                    if len(dictOneRolePlayers['dps']) > 0:
                        player = random.choice(dictOneRolePlayers['dps'])
                    else:
                        player = random.choice(rolesdict['dps'])
                    if ValidatePlayer(player, 'dps'):
                        movingon = True
                        AssignPlayer(player, 'dps')
                if breaklimit >= 10:
                    resetRoster = True 
            else:
                print("Ran out of DPSers")
                exit()

        if resetRoster == True:
            ResetRoster()

def ResetRoster():
    print("I fucked up. Starting over...")
    dictsupergroup['tank'].clear()
    dictsupergroup['healer'].clear()
    dictsupergroup['dps'].clear()

    dictOneRolePlayers['tank'].clear()
    dictOneRolePlayers['healer'].clear()
    dictOneRolePlayers['dps'].clear()

    rolesdict['tank'].clear()
    rolesdict['healer'].clear()
    rolesdict['dps'].clear()

    rolesdict['tank'] = tanksMaster.copy()
    rolesdict['healer'] = healersMaster.copy()
    rolesdict['dps'] = dpsMaster.copy()
    
def DefaultPopulate(player):
    rolesdict[player['default']].append(player['name'])

def ChaosPopulate(player):
    if int(player['tank']) >= int(dungeonlevel):
        rolesdict['tank'].append(player['name'])
    if int(player['dps']) >= int(dungeonlevel):
        rolesdict['dps'].append(player['name'])
    if int(player['healer']) >= int(dungeonlevel):
        rolesdict['healer'].append(tempdict['name'])

def GetPlayers(player):
    tree = et.parse(player)
    root = tree.getroot()
    playerdict = {'name': root.attrib['name'], 'tank': root.attrib['tank'], 'dps': root.attrib['dps'], 'healer': root.attrib['healer'], 'default': root.attrib['default']}
    return playerdict

def PrintGroup(group, number):
    print("\nTeam " + str(number) + ":")
    print("\tTank:\t" + group[0])
    print("\tHealer:\t" + group[1])
    print("\tDPS 1:\t" + group[2])
    print("\tDPS 2:\t" + group[3])

### Main ###

for root, dirs, files in os.walk('./players/', topdown=False):
    for filename in files:
        if '.swp' not in filename and '.xml' in filename:
            playerxmls.append(os.path.join(root, filename))

for player in playerxmls:
    tempdict = GetPlayers(player)
    playerdict[tempdict['name']] = tempdict
    loadedplayernames.append(tempdict['name'])
    if mode is 'default':
        DefaultPopulate(tempdict)
    if mode is 'chaos':
        ChaosPopulate(tempdict)

if len(tanks) < 2 or len(healers) < 2 or len(dps) < 4:
    print("Not enough players to build a group. Aborting.")
    exit()

tanksMaster = tanks.copy()
healersMaster = healers.copy()
dpsMaster = dps.copy()

CreateRoster()

group1 = [dictsupergroup['tank'].pop(), dictsupergroup['healer'].pop(), dictsupergroup['dps'].pop(), dictsupergroup['dps'].pop()]
group2 = [dictsupergroup['tank'].pop(), dictsupergroup['healer'].pop(), dictsupergroup['dps'].pop(), dictsupergroup['dps'].pop()]

PrintGroup(group1, 1)
PrintGroup(group2, 2)
