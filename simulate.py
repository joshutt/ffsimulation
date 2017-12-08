#!/usr/bin/python

import copy
import numpy
import random


pts = { 'CRU' : (67,76,113,94,110,117,104,57,74,70,63,84,148), \
        'FS' : (69,52,112,111,98,82,75,55,69,64,135,69,69), \
        'GW' : (59,90,120,79,67,61,88,79,56,86,115,125,76), \
        'AE' : (61,98,75,88,61,125,106,148,82,78,83, 119,65), \
        'RL' : (39,95,60,65,59,40,59,79,66,77,106,59,81), \
        'MM' : (74,85,113,96,102,76,83,75,71,82,79,106,101), \
        'NOR' : (63,60,46,95,53,95,36,71,61,92,105,90,95), \
        'FBB' : (79,97,70,103,98,92,107,127,82,80,91,112,103), \
        'SOB' : (85,81,125,105,82,91,86,82,78,123,130,113,104), \
        'STA' : (51,87,101,61,56,71,70,56,506,65,68,58,56), \
        'TPL' : (59,81,99,119,104,93,72,56,93,104,88,87,70), \
        'WR' : (93,83,83,97,134,81,120,77,59,42,75,90,87)}

divisions = { 'Burgundy' : ('AE','NOR','RL','STA'), 'Gold' : ('CRU', 'FS', 'GW', 'TPL'), 'White' : ('MM', 'SOB', 'FBB', 'WR') }

crossDiv = { 'CRU' : 'Gold', 'FS':'Gold', 'GW':'Gold', 'TPL':'Gold', 'AE':'Burgundy', 'RL':'Burgundy', 'NOR':'Burgundy', 'STA':'Burgundy',
            'MM':'White', 'SOB':'White', 'FBB':'White', 'WR':'White'}


record = { 'CRU' : [0,0,0], 'FS' : [0,0,0], 'GW': [0,0,0], 'TPL':[0,0,0], 'AE':[0,0,0], 'RL':[0,0,0], 'NOR':[0,0,0], 'STA':[0,0,0],
           'MM' : [0,0,0], 'SOB':[0,0,0], 'FBB':[0,0,0], 'WR':[0,0,0] }

games = { 'CRU' : {}, 'FS':{}, 'GW':{}, 'TPL':{}, 'AE':{}, 'RL':{}, 'NOR':{}, 'STA':{}, 'MM':{}, 'SOB':{}, 'FBB':{}, 'WR':{}}


titles = { 'CRU' : {'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0},
            'FS':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}, 
            'GW':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}, 
            'TPL':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}, 
            'AE':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}, 
            'RL':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}, 
            'NOR':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}, 
            'STA':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}, 
            'MM':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}, 
            'SOB':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}, 
            'FBB':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}, 
            'WR':{'Division' : 0, 'Wild Card' : 0, 'Toliet Bowl' : 0, 'In Finals':0, 'Champion':0, 'TB Win':0}
            }

cumrecord = { 'CRU' : [0,0,0], 'FS' : [0,0,0], 'GW': [0,0,0], 'TPL':[0,0,0], 'AE':[0,0,0], 'RL':[0,0,0], 'NOR':[0,0,0], 'STA':[0,0,0],
           'MM' : [0,0,0], 'SOB':[0,0,0], 'FBB':[0,0,0], 'WR':[0,0,0] }


def addWin(record, winTeam, loseTeam) :
    record[winTeam][0] += 1
    record[loseTeam][1] += 1
    if loseTeam in games[winTeam] :
        games[winTeam][loseTeam] += 1
    else :
        games[winTeam][loseTeam] = 1
    if winTeam in games[loseTeam] :
        games[loseTeam][winTeam] -= 1
    else :
        games[loseTeam][winTeam] = -1


def addTie(record, teama, teamb) :
    record[teama][2] += 1
    record[teamb][2] += 1
    if teama not in games[teamb] :
        games[teamb][teama] = 0
    if teamb not in games[teama] :
        games[teama][teamb] = 0


def readFile() :
    scheduleFile = open("schedule.csv")
    lines = []
    for line in scheduleFile :
        lines.append(line)
    scheduleFile.close()

    toSimulate = []
    for line in lines :
        pieces = line.strip().split(",")
        if len(pieces) == 3 :
            if (pieces[2] == 'W') :
                addWin(record, pieces[0], pieces[1])
                #record[pieces[0]][0] += 1
                #record[pieces[1]][1] += 1
            elif (pieces[2] == 'L') :
                addWin(record, pieces[1], pieces[0])
                #record[pieces[1]][0] += 1
                #record[pieces[0]][1] += 1
            elif (pieces[2] == 'T') :
                addTie(record, pieces[0], pieces[1])
                #record[pieces[0]][2] += 1
                #record[pieces[1]][2] += 1
        else :
            toSimulate.append(pieces)
    return (record, toSimulate)


def singleGame(team1Name, team2Name) :
    team1 = pts[team1Name]
    team2 = pts[team2Name]
    score1 = round(random.gauss(numpy.average(team1), numpy.std(team1, ddof=1)))
    score2 = round(random.gauss(numpy.average(team2), numpy.std(team2, ddof=1)))
    return (score1, score2)


def simulateGames(simulatedRecord) :
    for x in toSimulate :
        #team1 = pts[x[0]]
        #team2 = pts[x[1]]
        #score1 = round(random.gauss(numpy.average(team1), numpy.std(team1, ddof=1)))
        #score2 = round(random.gauss(numpy.average(team2), numpy.std(team2, ddof=1)))
        (score1, score2) = singleGame(x[0], x[1])
        if (score1 > score2) :
            addWin(simulatedRecord, x[0], x[1])
            #simulatedRecord[x[0]][0] += 1
            #simulatedRecord[x[1]][1] += 1
        elif (score1 < score2) :
            addWin(simulatedRecord, x[1], x[0])
            #simulatedRecord[x[1]][0] += 1
            #simulatedRecord[x[0]][1] += 1
        elif (score1 == score2) :
            addTie(simulatedRecord, x[0], x[1])
            #simulatedRecord[x[0]][2] += 1
            #simulatedRecord[x[1]][2] += 1


def postSeason(teamA, teamB, titleName) :
    score1 = 0
    score2 = 0
    while score1==score2 :
        (score1, score2) = singleGame(teamA, teamB)
    if score1 > score2 :
        titles[teamA][titleName] += 1
        return teamA
    elif score2 > score1 :
        titles[teamB][titleName] += 1
        return teamB


def printOutput(record) :
    for divName in divisions :
        print "------ %s ------" % divName
        for team in divisions[divName] :
            print "%3s = %4.1f - %4.1f - %4.1f " % (team, record[team][0]/float(numIter), record[team][1]/float(numIter), record[team][2]/float(numIter))


def printTitles(titles) :
    print "------ TITLES -----"
    for team in titles :
        print "%3s = Division - %5.1f,  WildCard - %5.1f,  Playoffs - %5.1f, In Finals - %5.1f, Champion - %5.1f" % (team, titles[team]["Division"]/float(numIter)*100, titles[team]["Wild Card"]/float(numIter)*100, (titles[team]["Division"] + titles[team]["Wild Card"])/float(numIter)*100, titles[team]["In Finals"]/float(numIter)*100, titles[team]["Champion"]/float(numIter)*100)

    print
    print "------ TOLIET BOWL -----"
    for team in titles :
        print "%3s = In Toliet Bowl - %5.1f,  Winner - %5.1f" % (team, titles[team]["Toliet Bowl"]/float(numIter)*100, titles[team]["TB Win"]/float(numIter)*100)


def checkOrder(divOrder, record, team) :
    wins = record[team][0] + record[team][2]/2.0
    for x in range(0, len(divOrder)) :
        othTeam = divOrder[x][0]
        if wins > divOrder[x][1] :
            divOrder.insert(x, (team, wins))
            return
        elif wins == divOrder[x][1] :
            if (games[team][othTeam] > 0) :
                divOrder[x] = (othTeam, divOrder[x][1], '1st TB')
                divOrder.insert(x, (team,wins,"1st TB"))
                return
            elif (games[team][othTeam] < 0) :
                divOrder[x] = (othTeam, divOrder[x][1], '1st TB')
                divOrder.insert(x+1, (team,wins,"1st TB"))
                return

            if (crossDiv[team] == crossDiv[othTeam]) :
                teamDivWin = reduce(lambda x,y: x+y, map(lambda x: games[team][x] , filter(lambda x: x in divisions[crossDiv[team]], games[team])))
                othTeamDivWin = reduce(lambda x,y: x+y, map(lambda x: games[othTeam][x] , filter(lambda x: x in divisions[crossDiv[team]], games[othTeam])))
                if teamDivWin > othTeamDivWin :
                    divOrder[x] = (othTeam, divOrder[x][1], '2nd TB')
                    divOrder.insert(x, (team,wins,"2nd TB"))
                    return
                elif teamDivWin < othTeamDivWin :
                    divOrder[x] = (othTeam, divOrder[x][1], '2nd TB')
                    divOrder.insert(x+1, (team,wins,"2nd TB"))
                    return

            divOrder[x] = (othTeam, divOrder[x][1], 'TIE')
            divOrder.insert(x, (team, wins, 'TIE'))
            return
    divOrder.append((team,wins))



def rankDivisions(record) :
    for divName in divisions:
        divLeader = ('', 0)
        divOrder = []
        for team in divisions[divName] :
            checkOrder(divOrder, record, team)
        print divOrder


## Sort only by record
def firstRank(record, teamList, time=0) :
    #print len(teamList)
    if len(teamList) == 1 :
        return list(teamList)
    if len(teamList) == 0 :
        return []

    if time > 12 :
        print "Time Exceeded %s" % time
        return

    wins = map(lambda x: record[x][0] + record[x][2]/2.0, teamList)
    #print wins
    maxWins = None
    topTeams = []
    for x in range(0, len(wins)) :
        if (wins[x] > maxWins) :
            maxWins = wins[x]
            #print maxWins
            topTeams = [teamList[x]]
            #print topTeams
        elif (wins[x] == maxWins) :
            topTeams.append(teamList[x])

    remainList = filter(lambda t: t not in topTeams, teamList)
    #print "%s - %s " %(time, remainList)
    #print "%s - %s " %(time, topTeams)
    #sys.exit(0)
    rankTheRest = firstRank(record, remainList, time+1)
    #print rankTheRest
    if len(topTeams) == 1 :
        topTeams.extend(rankTheRest)
        return topTeams
        #return list(topTeams, firstRank(record, remainList))
    else :
        returnTeams = secondRank(record, topTeams)
        returnTeams.extend(rankTheRest)
        return returnTeams
        #return list(secondRank(record, topTeams), firstRank(record, remainList))


# Return sort by head to head
def secondRank(record, teamList) :
    if len(teamList) == 2 :
        #print games
        if (games[teamList[0]][teamList[1]] > 0) :
            return [teamList[0], teamList[1]]
        elif (games[teamList[0]][teamList[1]] < 0) :
            return [teamList[1], teamList[0]]
        elif (games[teamList[0]][teamList[1]] == 0) :
            return thirdRank(record, teamList)

    maxDiff = -99999
    topTeams = []
    for team in teamList :
        myGames = filter(lambda x: x in teamList, games[team])
        netDiff = sum(map(lambda x: games[team][x], myGames))
        if netDiff > maxDiff :
            maxDiff = netDiff
            topTeams = [team]
        elif netDiff == maxDiff :
            topTeams.append(team)

    remainList = filter(lambda t: t not in topTeams, teamList)
    rankTheRest = firstRank(record, remainList)
    if len(topTeams) == 1 :
        topTeams.extend(rankTheRest)
        return topTeams
    else :
        returnTeams = thirdRank(record, topTeams)
        returnTeams.extend(rankTheRest)
        return returnTeams



# Division record if in same division
def thirdRank(record, teamList):
    div = crossDiv[teamList[0]]
    maxDiff = -9999
    topTeams = []
    for team in teamList :
        if div != crossDiv[team] :
            return fourthRank(record, teamList)
        myGames = filter(lambda t: t in divisions[div], games[team])
        netDiff = sum(map(lambda t: games[team][t], myGames))
        if netDiff > maxDiff :
            maxDiff = netDiff
            topTeams = [team]
        elif netDiff == maxDiff :
            topTeams.append(team)

    # After loop get the top teams
    remainList = filter(lambda t: t not in topTeams, teamList)
    rankTheRest = firstRank(record, remainList)
    if len(topTeams) == 1 :
        topTeams.extend(rankTheRest)
        return topTeams
    else :
        returnTeams = fourthRank(record, topTeams)
        returnTeams.extend(rankTheRest)
        return returnTeams
    return teamList


# Strength of victory
def fourthRank(record, teamList):
    for team in teamList :
        for game in games[team] :
            pass 

    return teamList


(record, toSimulate) = readFile()
baseGames = copy.deepcopy(games)
numIter = 1000

for numTimes in range(numIter) :
    simulatedRecord = copy.deepcopy(record)
    games = copy.deepcopy(baseGames)
    simulateGames(simulatedRecord)
#printOutput(simulatedRecord)

#newRec = { 'A' : (10,3,1), 'B':(4,10,0), 'C':(10,3,1), 'D':(10,3,1)}
#testTeams = ('A','B','D')
#games = {'A' : {'B' : -2, 'D':0}, 'B':{'A':2, 'D':-2}, 'D':{'A':0, 'B':2}}
#print secondRank(newRec, testTeams)

    gold = firstRank(simulatedRecord, divisions["Gold"])
    burgundy = firstRank(simulatedRecord, divisions["Burgundy"])
    white = firstRank(simulatedRecord, divisions["White"])

    divWinners = firstRank(simulatedRecord, [gold[0], burgundy[0], white[0]])
    wildCard = firstRank(simulatedRecord, [gold[1], burgundy[1], white[1]])
    tolietBowl = firstRank(simulatedRecord, [gold[3], burgundy[3], white[3]])

    titles[divWinners[0]]['Division'] += 1
    titles[divWinners[1]]['Division'] += 1
    titles[divWinners[2]]['Division'] += 1
    titles[wildCard[0]]['Wild Card'] += 1
    titles[tolietBowl[1]]['Toliet Bowl'] += 1
    titles[tolietBowl[2]]['Toliet Bowl'] += 1

    for rec in simulatedRecord :
        cumrecord[rec][0] += simulatedRecord[rec][0]
        cumrecord[rec][1] += simulatedRecord[rec][1]
        cumrecord[rec][2] += simulatedRecord[rec][2]

    postSeason(tolietBowl[1], tolietBowl[2], 'TB Win')
    if crossDiv[divWinners[0]] == crossDiv[wildCard[0]] :
        winA = postSeason(divWinners[0], divWinners[2], 'In Finals')
        winB = postSeason(divWinners[1], wildCard[0], 'In Finals')
    else :
        winA = postSeason(divWinners[0], wildCard[0], 'In Finals')
        winB = postSeason(divWinners[1], divWinners[2], 'In Finals')
    postSeason(winA, winB, 'Champion')


#print gold
#print burgundy
#print white
#print divWinners
#print wildCard[0]
#print [tolietBowl[1], tolietBowl[2]]
#print titles
#print cumrecord

printOutput(cumrecord)
print
printTitles(titles)
#rankDivisions(simulatedRecord)


#print games
#print record
#print simulatedRecord
#print dir(record)
