import random,time,pathlib

epana = int(input("Πόσες επαναλήψεις: "))
n = int(input("Πόσα ματς: "))
class Team:
    def __init__(self, name, xGf, xGa, gf, ga, ashotf, ashota):
        self.name = name
        self.xGf = xGf
        self.xGa = xGa
        self.gf = gf
        self.ga = ga
        self.ashotf = ashotf
        self.ashota = ashota

def xscore():
        #shots
        asho1 = random.randint(int(round(ashot1))- random.randint(1,4),int(round(ashot1))+random.randint(1,4))
        asho2 = random.randint(int(round(ashot2))- random.randint(1,4),int(round(ashot2))+random.randint(1,4))
        #xGs per shot
        xGpsA = random.randint(xGps1-random.randint(1,4),xGps1+random.randint(1,4))
        xGpsB = random.randint(xGps2-random.randint(1,4),xGps2+random.randint(1,4))
        #expected goals for 
        xpGA = asho1*xGpsA 
        xpGB = asho2*xGpsB
        #Goals for every xG
        gcount1 = 1000/Gpxg1
        gcount2 = 1000/Gpxg2
        #Goals 
        goals1 = int(xpGA/gcount1/1000)
        goals2 = int(xpGB/gcount2/1000)
        posa = ((xpGA/gcount1)%1000)/10
        posb = ((xpGB/gcount1)%1000)/10
        a = random.randint(1,100)
        gop = random.sample(range(1, 101), round(posa))
        if a in gop:
          goals1 += 1
        b = random.randint(1,100)
        gop = random.sample(range(1, 101), round(posb))
        if b in gop:
          goals2 += 1
        return(str(goals1) + "-" + str(goals2))

teams =[]
hometeams =[]
awayteams =[]
for i in range(2*n):
    name = str(input(f'Team name {i+1}: '))
    xGf = float(input(f'xG for {name}: '))
    xGa = float(input(f'xG against {name}: '))
    gf = float(input(f'goals for {name}: '))
    ga = float(input(f'goals against {name}: '))
    ashotf = float(input(f'avg shots for {name}: '))
    ashota = float(input(f'avg shots against {name}: '))
    team = Team(name, xGf, xGa, gf, ga, ashotf, ashota)
    teams.append(team)

for i in range(n):
    home_name = str(input('Home team name: '))
    away_name = str(input('Away team name: '))

    home = next((team for team in teams if team.name == home_name), None)
    while home is None:
        home_name = str(input('Home team name: '))
        home = next((team for team in teams if team.name == home_name), None)
    away = next((team for team in teams if team.name == away_name), None) 
    while away is None:
        away_name = str(input('Away team name: '))
        away = next((team for team in teams if team.name == away_name), None)
    hometeams.append(home)
    awayteams.append(away)

for i in range(n):
    home = hometeams[i]
    away = awayteams[i]
    xG1 = (home.xGf + away.xGa)/2
    xG2 = (away.xGf + home.xGa)/2   
    g1 = (home.gf + away.ga)/2
    g2 = (away.gf + home.ga)/2
    ashot1 = int((home.ashotf + away.ashota)/2)
    ashot2 = int((home.ashota + away.ashotf)/2)
    xGps1 = int(round(xG1/ashot1*1000))
    xGps2 = int(round(xG2/ashot2*1000))
    Gpxg1 = round(g1/xG1*1000)
    Gpxg2 = round(g2/xG2*1000)
    scHOME=["1-0","2-0","2-1","3-0","3-1","3-2","4-0","4-1","4-2","4-3","5-0","5-1","5-2","5-3","5-4"]
    plithosHOME=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    scAWAY=["0-1","0-2","1-2","0-3","1-3","2-3","0-4","1-4","2-4","3-4","0-5","1-5","2-5","3-5","4-5"]
    plithosAWAY=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    scDRAW=["0-0","1-1","2-2","3-3","4-4","5-5"]
    plithosDRAW=[0,0,0,0,0,0]
    homew=0
    awayw=0
    draww=0
    for i in range(epana):
        a = xscore()
        for i in range(len(scHOME)):
            if a==scHOME[i]:
                plithosHOME[i]+=1
                homew+=1
        for i in range(len(scAWAY)):
            if a==scAWAY[i]:
                plithosAWAY[i]+=1
                awayw+=1
        for i in range(len(scDRAW)):
            if a==scDRAW[i]:
                plithosDRAW[i]+=1
                draww+=1

    file_path = pathlib.Path("C:\\Users\\apost\\Downloads\\Desktop\\Premier League\\results.txt")
    if not file_path.exists():
        file_path.touch()
  
    with file_path.open("a") as file:
        file.write("\n----------------------------------------------------------------------------------- \n")
        file.write(f"{home.name} {round(homew/epana*100,2)}% Draw {round(draww/epana*100,2)}% {away.name} {round(awayw/epana*100,2)}%\n")
        for i in range(len(scHOME)):
            if(((plithosHOME[i]/epana)*100)>20):
                file.write(f"{scHOME[i]} {round(((plithosHOME[i]/epana)*100),2)}%//")
        for i in range(len(scDRAW)):
            if(((plithosDRAW[i]/epana)*100)>20):
                file.write(f"{scDRAW[i]} {round(((plithosDRAW[i]/epana)*100),2)}%//")   
        for i in range(len(scAWAY)):
            if(((plithosAWAY[i]/epana)*100)>20):
                file.write(f"{scAWAY[i]} {round(((plithosAWAY[i]/epana)*100),2)}%//")


