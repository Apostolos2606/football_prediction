
import pathlib
import pathlib
import random
from turtle import home
import pymysql 
from pathlib import Path

def xscore(ashot1,ashot2,xGps1,xGps2,Gpxg1,Gpxg2):
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

class Team:
    def __init__(self, name, gf, ga, xGf, xGa, ashotf, ashota):
        self.name = name
        self.xGf = xGf
        self.xGa = xGa
        self.gf = gf
        self.ga = ga
        self.ashotf = ashotf
        self.ashota = ashota

def menu():
    print("________________________________________")
    print("1--> Add Match")
    print("2--> Predict Matches")
    print("3--> Exit")
    print("________________________________________")
    choice=int(input("Enter your choice: "))
    return choice

def add_match():
    date=input("Date (YYYY-MM-DD): ")
    home_team=input("Home Team: ")
    away_team=input("Away Team: ")
    home_formation=input("Home Formation: ")
    away_formation=input("Away Formation: ")
    home_goals =int(input("Home Goals: "))
    away_goals = int(input("Away Goals: "))
    home_xg = float(input("Home xG: "))
    away_xg = float(input("Away xG: "))
    home_shots = int(input("Home Shots: "))
    away_shots = int(input("Away Shots: ")) 
    querry = "INSERT INTO season25_26 (date, home_team, away_team, h_formation, a_formation, h_goals, a_goals, h_xg, a_xg, h_shot, a_shot) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
    values = (date, home_team, away_team, home_formation, away_formation, home_goals, away_goals, home_xg, away_xg, home_shots, away_shots)
    cursor.execute(querry, values)
    connection.commit() 

def predict_matches():
    cursor.execute("select distinct(home_team) from season25_26 union select distinct(away_team) from season25_26")
    names = [row[0] for row in cursor.fetchall()]
    cursor.execute("""SELECT 
                                team_name,
                                AVG(goals_for) AS avg_goals_for,
                                AVG(goals_against) AS avg_goals_against,
                                AVG(xg_for) AS avg_xg_for,
                                AVG(xg_against) AS avg_xg_against,
                                AVG(shots_for) AS avg_shots_for,
                                AVG(shots_against) AS avg_shots_against
                        FROM (
                                SELECT home_team AS team_name, h_goals AS goals_for, a_goals AS goals_against, h_xg AS xg_for, a_xg AS xg_against, h_shot AS shots_for, a_shot AS shots_against FROM `season25_26`
                        UNION ALL
                            SELECT away_team AS team_name, a_goals AS goals_for, h_goals AS goals_against, a_xg AS xg_for, h_xg AS xg_against, a_shot AS shots_for, h_shot AS shots_against FROM `season25_26`
                             ) AS combined_data
                        GROUP BY team_name""")
    result = cursor.fetchall()
    teams=[]
    for row in result:
        team = Team(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        teams.append(team)
    
    epana = int(input("Πόσες επαναλήψεις: "))
    n = int(input("Πόσα ματς: "))
    print("________________________________________")
    hometeams = []
    awayteams = []
    for i in range(n):
        home_team_name = input("Home team name: ")
        while home_team_name not in names:
            home_team_name = input("Home team name: ")  
        away_team_name = input("Away team name: ")
        while away_team_name not in names:
            away_team_name = input("Away team name: ")
        hometeams.append(home_team_name)
        awayteams.append(away_team_name)
        print("________________________________________")
    for i in range(n):
        home_team = next((team for team in teams if team.name == hometeams[i]), None)
        away_team = next((team for team in teams if team.name == awayteams[i]), None)
        #xG home team
        xG1 = (home_team.xGf + away_team.xGa)/2
        #xG away team
        xG2 = (away_team.xGf + home_team.xGa)/2
        #same for goals and shots   
        g1 = float((home_team.gf + away_team.ga)/2)
        g2 = float((away_team.gf + home_team.ga)/2)
        ashot1 = int((home_team.ashotf + away_team.ashota)/2)
        ashot2 = int((home_team.ashota + away_team.ashotf)/2)
        #xG per shot
        xGps1 = int(round(xG1/ashot1*1000))
        xGps2 = int(round(xG2/ashot2*1000))
        #Goals per expected xG
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
            a = xscore(ashot1,ashot2,xGps1,xGps2,Gpxg1,Gpxg2)
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

        script_dir = pathlib.Path(__file__).parent
        file_path = script_dir / "results.txt"
        if not file_path.exists():
            file_path.touch()
  
        with file_path.open("a") as file:
            file.write("\n----------------------------------------------------------------------------------- \n")
            file.write(f"{home_team.name} {round(homew/epana*100,2)}% Draw {round(draww/epana*100,2)}% {away_team.name} {round(awayw/epana*100,2)}%\n")
            for i in range(len(scHOME)):
                if(((plithosHOME[i]/epana)*100)>20):
                    file.write(f"{scHOME[i]} {round(((plithosHOME[i]/epana)*100),2)}%//")
            for i in range(len(scDRAW)):
                if(((plithosDRAW[i]/epana)*100)>20):
                    file.write(f"{scDRAW[i]} {round(((plithosDRAW[i]/epana)*100),2)}%//")   
            for i in range(len(scAWAY)):
                if(((plithosAWAY[i]/epana)*100)>20):
                    file.write(f"{scAWAY[i]} {round(((plithosAWAY[i]/epana)*100),2)}%//")

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='0626',
        database='premier',
        charset='utf8mb4'
    )
    cursor = connection.cursor()
    choice=menu()
    while choice!=3:
        if choice==1:
            add_match()
        elif choice==2:
            predict_matches()
        else:
           pass
        choice=menu()
except pymysql.MySQLError as e:
    print(f"Σφάλμα σύνδεσης: {e}")
finally:
    if 'connection' in locals():
        connection.close()
        print("Η σύνδεση με τη βάση δεδομένων έκλεισε.")







   
