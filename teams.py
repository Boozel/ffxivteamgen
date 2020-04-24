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
tanks = []
healers = []
dps = []
rolesdict = {'tank': tanks, 'healer': healers, 'dps': dps}
groups = []

### Helper Methods ###

def ValidatePlayer(player, role, group, teamnum):
    allowed = True
    if role is not 'tank' and 'tank' not in group:
        if player in rolesdict['tank']:
            if len(rolesdict['tank']) <= (1 * teamnum):
                    allowed = False
                    print("Can't allow " + player + " into role " + role + ": Would run out of tanks.")

    if role is not 'healer' and 'healer' not in group:
        if player in rolesdict['healer']:
            if len(rolesdict['healer']) <= (1 * teamnum):
                allowed = False
                print("Can't allow " + player + " into role " + role + ": Would run out of healers.")
    if role is not 'dps':
        if player in rolesdict['dps']:
            if len(rolesdict['dps']) <= (2 * teamnum):
                allowed = False
                print("Can't allow " + player + " into role " + role + ": Would run out of DPS.")
    #if(allowed == False):
        #print(group)
        #print(tanks)
        #print(healers)
        #print(dps)
        #input("waiting")
    return allowed

def AssignPlayer(player, role, group):
    group[role] = player
    if player in rolesdict['tank']:
        rolesdict['tank'].pop(rolesdict['tank'].index(player))
    if player in rolesdict['healer']:
        rolesdict['healer'].pop(rolesdict['healer'].index(player))
    if player in rolesdict['dps']:
        rolesdict['dps'].pop(rolesdict['dps'].index(player)) 

def FindPlayersWithOneRole()
    roles = 0x01
    for player in loadedplayernames:
        if player in tanks:
            roles << 1
        if player in healers:
            roles << 1
        if player in dps:
            roles << 1
    if roles > 0x02:
        return False
    else:
        return True

def CreateTeam(teamnum):
    # Get the Tank
    groupdict = {}
    player = ""

    if len(rolesdict['tank']) >= 1:
        movingon = False
        while movingon == False:
            #print(tanks)
            #print(healers)
            #print(dps)
            #input("waiting")
            player = random.choice(rolesdict['tank'])
            if ValidatePlayer(player, 'tank', groupdict, teamnum):
                movingon = True
                AssignPlayer(player, 'tank', groupdict) 
    else:
        print("Ran out of tanks.")
        exit()

    if len(rolesdict['healer']) >= 1:
        movingon = False
        while movingon == False:
            #print(tanks)
            #print(healers)
            #print(dps)
            #input("waiting")   
            player = random.choice(rolesdict['healer'])
            if ValidatePlayer(player, 'healer', groupdict, teamnum):
                movingon = True
                AssignPlayer(player, 'healer', groupdict)
    else:
        print("Ran out of healers.")
        exit()

    for dpser in range(0,2):
        if len(rolesdict['dps']) >= 1:
            movingon = False
            while movingon == False:
                #print(tanks)
                #print(healers)
                #print(dps)
                #input("waiting")
                player = random.choice(rolesdict['dps'])
                if ValidatePlayer(player, 'dps', groupdict, teamnum):
                    movingon = True
                    AssignPlayer(player, 'dps'+str(dpser+1), groupdict) 
        else:
            print("Ran out of DPSers")
            exit()
    return groupdict
    
def DefaultPopulate(player):
    rolesdict[player['default']].append(player['name'])

def ChaosPopulate(player):
    if int(player['tank']) >= dungeonlevel:
        rolesdict['tank'].append(player['name'])
    if int(player['dps']) >= dungeonlevel:
        rolesdict['dps'].append(player['name'])
    if int(player['healer']) >= dungeonlevel:
        rolesdict['healer'].append(tempdict['name'])

def GetPlayers(player):
    tree = et.parse(player)
    root = tree.getroot()
    playerdict = {'name': root.attrib['name'], 'tank': root.attrib['tank'], 'dps': root.attrib['dps'], 'healer': root.attrib['healer'], 'default': root.attrib['default']}
    return playerdict

### Main ###

for root, dirs, files in os.walk('./players/', topdown=False):
    for filename in files:
        if '.swp' not in filename and '.xml' in filename:
            playerxmls.append(os.path.join(root, filename))

for player in playerxmls:
    print(player)
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

print(CreateTeam(2))
print("\nGroup 2\n")
print(CreateTeam(1))

completegroup = False
#while(completegroup is False):
    
    #print(playerdict['Boozel Vivarin']['name'])
