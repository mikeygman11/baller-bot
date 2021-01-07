#Copyright 2020 Michael Galanaugh

#a discord bot to provide real-time basketball scores, football scores, and standings
# to a discord server

import discord
import os
from discord.ext import commands
import random
from bs4 import BeautifulSoup
import pandas as pd
import nba_py as nba
import espn_scraper as espn
import json
import requests 
import lxml
import json
import operator
from datetime import date
from tabulate import tabulate


#test()
#print(display.test())
t_date = str(date.today())
client = commands.Bot(command_prefix='-')
@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    
@client.command()
async def hi(cmd):
    rand_int = random.randrange(0,5)
    hellos = ["What's up y'all", "Howdy", "Top of the mornin' to ya!", "Let's get this bread boys", "How's it hangin?", "Yo"]
    await cmd.send(hellos[rand_int])

@client.command()
async def nbateams(cmd):
    lst = []
    espn_list = espn.get_teams("nba")
    for d in espn_list:
        lst.append(d['name'])
    await cmd.send(lst)

@client.command()
async def lebron(content):
    image_array = ["lebron.jpg"]
    rand = random.choice(image_array)
    await content.send(file=discord.File(rand))


@client.command()
async def nbaschedule(sched):
    url = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    json_text = requests.get(url).text
    data = json.loads(json_text)
    schedule_string = ""
    greeting = "Here are the games being played on " + data["day"]["date"] + ":\n"
    schedule_string += greeting
    schedule_game = 0
    while True:
        try:
            schedule_string += data["events"][schedule_game]["name"] + " @ "
            time = data["events"][schedule_game]["date"]
            time = time.split("T")
            minutes = time[1][2:-1]
            hour = int(time[1][0:2])
            schedule_game+=1
            if hour > 5:
                hour = hour-5
            elif hour == 0:
                hour = 19
            elif hour == 1:
                hour = 20
            elif hour == 2:
                hour = 21
            elif hour == 3:
                hour = 22
            elif hour == 4:
                hour = 23
            elif hour == 5:
                hour = 24
            mil_hour = hour
            if mil_hour <12:
                schedule_string += str(mil_hour) + str(minutes) + " AM" "\n"
            elif mil_hour == 12:
                schedule_string += str(mil_hour) + str(minutes) + " PM" "\n"
            elif mil_hour == 24:
                mil_hour = mil_hour-12
                schedule_string += str(mil_hour) + str(minutes) + " AM" "\n"           
            else:
                mil_hour = mil_hour-12
                schedule_string += str(mil_hour) + str(minutes) + " PM" "\n"
        except IndexError:
            schedule_string += "\nThat's all for today!"			
            break
    await sched.send(schedule_string)


@client.command()
async def nbascores(score):
    url = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    json_text = requests.get(url).text
    data = json.loads(json_text)
    score_thread = ""
    score_index = 0
    while True:
        try:
            score_thread += data["events"][score_index]["competitions"][0]["competitors"][0]["team"]["shortDisplayName"] + ": " + data["events"][score_index]["competitions"][0]["competitors"][0]["score"]
            score_thread += " - " + data["events"][score_index]["competitions"][0]["competitors"][1]["team"]["shortDisplayName"] + ": " + data["events"][score_index]["competitions"][0]["competitors"][1]["score"]
            score_thread += " (" + data["events"][score_index]["competitions"][0]["status"]["type"]["detail"] + ")" + "\n"
            score_index += 1
        except IndexError:
            score_thread += "\nThese are all the active scores"
            break
    await score.send(score_thread)


@client.command()
async def nfcwest(nwest):

    #NFC WEST

    nfl = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    nfl_stand = requests.get(nfl).text
    nfl_standings = json.loads(nfl_stand)
    nfc_west = ["Los Angeles Rams", "Arizona Cardinals", "San Francisco 49ers", "Seattle Seahawks"]
    nfc_west_index = 0
    nfc_west_dict = {}
    while True:
        try:
            if nfl_standings["children"][1]["standings"]["entries"][nfc_west_index]["team"]["displayName"] in nfc_west:
                print(nfl_standings["children"][1]["standings"]["entries"][nfc_west_index]["team"]["displayName"])
                record = nfl_standings["children"][1]["standings"]["entries"][nfc_west_index]["stats"][-5]["summary"]
                win_perc = nfl_standings["children"][1]["standings"]["entries"][nfc_west_index]["stats"][3]["displayValue"]
                seed = nfl_standings["children"][1]["standings"]["entries"][nfc_west_index]["stats"][0]["displayValue"]
                nfc_west_dict[nfl_standings["children"][1]["standings"]["entries"][nfc_west_index]["team"]["displayName"]] = record, win_perc, seed
            nfc_west_index += 1
        except IndexError:
            break
    #sorted_nfc_west = {}
    #for key in nfc_west_dict:
        #print(nfc_west_dict[key][1])
    sorted_nfc_west = sorted(nfc_west_dict.items(), key = lambda nfc_west_dict: int(nfc_west_dict[1][2]), reverse = False)
    nwest_string = ""
    for i in range (len(sorted_nfc_west)):
       nwest_string += str(sorted_nfc_west[i][0]) + " | " + str(sorted_nfc_west[i][1][0]) + " | " + str(sorted_nfc_west[i][1][1]) + " | Playoff Seed: " + str(sorted_nfc_west[i][1][2]) + "\n"
    fin = []
    fin.append(["Team", "Record", "Win Percentage", "Playoff Seed"])
    for item in sorted_nfc_west:
        fin.append([item[0], item[1][0], item[1][1], item[1][2]])
    fin_tab = tabulate(fin, headers = 'firstrow', tablefmt = "fancy_grid")
    print(fin_tab)
    await nwest.send(fin_tab)

#NFC SOUTH

@client.command()
async def nfcsouth(nsouth):

    nfl = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    nfl_stand = requests.get(nfl).text
    nfl_standings = json.loads(nfl_stand)
    nfc_south = ["New Orleans Saints", "Tampa Bay Buccaneers", "Carolina Panthers", "Atlanta Falcons"]
    nfc_south_index = 0
    nfc_south_dict = {}
    while True:
        try:
            if nfl_standings["children"][1]["standings"]["entries"][nfc_south_index]["team"]["displayName"] in nfc_south:
                print(nfl_standings["children"][1]["standings"]["entries"][nfc_south_index]["team"]["displayName"])
                record = nfl_standings["children"][1]["standings"]["entries"][nfc_south_index]["stats"][-5]["summary"]
                win_perc = nfl_standings["children"][1]["standings"]["entries"][nfc_south_index]["stats"][3]["displayValue"]
                seed = nfl_standings["children"][1]["standings"]["entries"][nfc_south_index]["stats"][0]["displayValue"]
                nfc_south_dict[nfl_standings["children"][1]["standings"]["entries"][nfc_south_index]["team"]["displayName"]] = record, win_perc, seed
            nfc_south_index += 1
        except IndexError:
            break
    sorted_nfc_south = sorted(nfc_south_dict.items(), key = lambda nfc_south_dict: int(nfc_south_dict[1][2]), reverse = False)
    nsouth_string = ""
    for i in range (len(sorted_nfc_south)):
       nsouth_string += str(sorted_nfc_south[i][0]) + " | " + str(sorted_nfc_south[i][1][0]) + " | " + str(sorted_nfc_south[i][1][1]) + " | Playoff Seed: " + str(sorted_nfc_south[i][1][2]) + "\n"
    fin = []
    fin.append(["Team", "Record", "Win Percentage", "Playoff Seed"])
    for item in sorted_nfc_south:
        fin.append([item[0], item[1][0], item[1][1], item[1][2]])
    fin_tab = tabulate(fin, headers = 'firstrow', tablefmt = "fancy_grid")
    await nsouth.send(fin_tab)


#NFC EAST

@client.command()
async def nfceast(neast):

    nfl = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    nfl_stand = requests.get(nfl).text
    nfl_standings = json.loads(nfl_stand)
    nfc_east = ["New York Giants", "Dallas Cowboys", "Philadelphia Eagles", "Washington"]
    nfc_east_index = 0
    nfc_east_dict = {}
    while True:
        try:
            if nfl_standings["children"][1]["standings"]["entries"][nfc_east_index]["team"]["displayName"] in nfc_east:
                print(nfl_standings["children"][1]["standings"]["entries"][nfc_east_index]["team"]["displayName"])
                record = nfl_standings["children"][1]["standings"]["entries"][nfc_east_index]["stats"][-5]["summary"]
                win_perc = nfl_standings["children"][1]["standings"]["entries"][nfc_east_index]["stats"][3]["displayValue"]
                seed = nfl_standings["children"][1]["standings"]["entries"][nfc_east_index]["stats"][0]["displayValue"]
                nfc_east_dict[nfl_standings["children"][1]["standings"]["entries"][nfc_east_index]["team"]["displayName"]] = record, win_perc, seed
            nfc_east_index += 1
        except IndexError:
            break
    neast_string = ""
    sorted_nfc_east = sorted(nfc_east_dict.items(), key = lambda nfc_east_dict: int(nfc_east_dict[1][2]), reverse = False)
    for i in range (len(sorted_nfc_east)):
       neast_string += str(sorted_nfc_east[i][0]) + " | " + str(sorted_nfc_east[i][1][0]) + " | " + str(sorted_nfc_east[i][1][1]) + " | Playoff Seed: " + str(sorted_nfc_east[i][1][2]) + "\n"
    #print(sorted_nfc_east)
    #fin_dict = {}
    #for item in sorted_nfc_east:
        #fin_dict[item[0]] = item[1]
    #print(fin_dict)
    fin = []
    fin.append(["Team", "Record", "Win Percentage", "Playoff Seed"])
    for item in sorted_nfc_east:
        fin.append([item[0], item[1][0], item[1][1], item[1][2]])
    fin_tab = tabulate(fin, headers = 'firstrow', tablefmt = "fancy_grid")
    print(fin_tab)
    await neast.send(fin_tab)

#NFC NORTH


@client.command()
async def nfcnorth(nnorth):

    nfl = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    nfl_stand = requests.get(nfl).text
    nfl_standings = json.loads(nfl_stand)
    nfc_north = ["Minnesota Vikings", "Chicago Bears", "Detroit Lions", "Green Bay Packers"]
    nfc_north_index = 0
    nfc_north_dict = {}
    while True:
        try:
            if nfl_standings["children"][1]["standings"]["entries"][nfc_north_index]["team"]["displayName"] in nfc_north:
                print(nfl_standings["children"][1]["standings"]["entries"][nfc_north_index]["team"]["displayName"])
                record = nfl_standings["children"][1]["standings"]["entries"][nfc_north_index]["stats"][-5]["summary"]
                win_perc = nfl_standings["children"][1]["standings"]["entries"][nfc_north_index]["stats"][3]["displayValue"]
                seed = nfl_standings["children"][1]["standings"]["entries"][nfc_north_index]["stats"][0]["displayValue"]
                nfc_north_dict[nfl_standings["children"][1]["standings"]["entries"][nfc_north_index]["team"]["displayName"]] = record, win_perc, seed
            nfc_north_index += 1
        except IndexError:
            break
    sorted_nfc_north = sorted(nfc_north_dict.items(), key = lambda nfc_north_dict: int(nfc_north_dict[1][2]), reverse = False)
    nnorth_string = ""
    for i in range (len(sorted_nfc_north)):
       nnorth_string += str(sorted_nfc_north[i][0]) + " | " + str(sorted_nfc_north[i][1][0]) + " | " + str(sorted_nfc_north[i][1][1]) + " | Playoff Seed: " + str(sorted_nfc_north[i][1][2]) + "\n"
    fin = []
    fin.append(["Team", "Record", "Win Percentage", "Playoff Seed"])
    for item in sorted_nfc_north:
        fin.append([item[0], item[1][0], item[1][1], item[1][2]])
    fin_tab = tabulate(fin, headers = 'firstrow', tablefmt = "fancy_grid")
    print(fin_tab)
    await nnorth.send(fin_tab)

#AFC WEST

@client.command()
async def afcwest(awest):

    nfl = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    nfl_stand = requests.get(nfl).text
    nfl_standings = json.loads(nfl_stand)
    afc_west = ["Los Angeles Chargers", "Las Vegas Raiders", "Kansas City Chiefs", "Denver Broncos"]
    afc_west_index = 0
    afc_west_dict = {}
    while True:
        try:
            if nfl_standings["children"][0]["standings"]["entries"][afc_west_index]["team"]["displayName"] in afc_west:
                print(nfl_standings["children"][0]["standings"]["entries"][afc_west_index]["team"]["displayName"])
                record = nfl_standings["children"][0]["standings"]["entries"][afc_west_index]["stats"][-5]["summary"]
                win_perc = nfl_standings["children"][0]["standings"]["entries"][afc_west_index]["stats"][3]["displayValue"]
                seed = nfl_standings["children"][0]["standings"]["entries"][afc_west_index]["stats"][0]["displayValue"]
                afc_west_dict[nfl_standings["children"][0]["standings"]["entries"][afc_west_index]["team"]["displayName"]] = record, win_perc, seed
            afc_west_index += 1
        except IndexError:
            break

    sorted_afc_west = sorted(afc_west_dict.items(), key = lambda afc_west_dict: int(afc_west_dict[1][2]), reverse = False)
    awest_string = ""
    for i in range (len(sorted_afc_west)):
       awest_string += str(sorted_afc_west[i][0]) + " | " + str(sorted_afc_west[i][1][0]) + " | " + str(sorted_afc_west[i][1][1]) + " | Playoff Seed: " + str(sorted_afc_west[i][1][2]) + "\n"
    fin = []
    fin.append(["Team", "Record", "Win Percentage", "Playoff Seed"])
    for item in sorted_afc_west:
        fin.append([item[0], item[1][0], item[1][1], item[1][2]])
    fin_tab = tabulate(fin, headers = 'firstrow', tablefmt = "fancy_grid")
    print(fin_tab)
    await awest.send(fin_tab)



#AFC SOUTH

@client.command()
async def afcsouth(asouth):

    nfl = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    nfl_stand = requests.get(nfl).text
    nfl_standings = json.loads(nfl_stand)
    afc_south = ["Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans"]
    afc_south_index = 0
    afc_south_dict = {}
    while True:
        try:
            if nfl_standings["children"][0]["standings"]["entries"][afc_south_index]["team"]["displayName"] in afc_south:
                print(nfl_standings["children"][0]["standings"]["entries"][afc_south_index]["team"]["displayName"])
                record = nfl_standings["children"][0]["standings"]["entries"][afc_south_index]["stats"][-5]["summary"]
                win_perc = nfl_standings["children"][0]["standings"]["entries"][afc_south_index]["stats"][3]["displayValue"]
                seed = nfl_standings["children"][0]["standings"]["entries"][afc_south_index]["stats"][0]["displayValue"]
                afc_south_dict[nfl_standings["children"][0]["standings"]["entries"][afc_south_index]["team"]["displayName"]] = record, win_perc, seed
            afc_south_index += 1
        except IndexError:
            break
    sorted_afc_south = sorted(afc_south_dict.items(), key = lambda afc_south_dict: int(afc_south_dict[1][2]), reverse = False)
    asouth_string = ""
    for i in range (len(sorted_afc_south)):
       asouth_string += str(sorted_afc_south[i][0]) + " | " + str(sorted_afc_south[i][1][0]) + " | " + str(sorted_afc_south[i][1][1]) + " | Playoff Seed: " + str(sorted_afc_south[i][1][2]) + "\n"
    fin = []
    fin.append(["Team", "Record", "Win Percentage", "Playoff Seed"])
    for item in sorted_afc_south:
        fin.append([item[0], item[1][0], item[1][1], item[1][2]])
    fin_tab = tabulate(fin, headers = 'firstrow', tablefmt = "fancy_grid")
    await asouth.send(fin_tab)


#AFC EAST


@client.command()
async def afceast(aeast):

    nfl = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    nfl_stand = requests.get(nfl).text
    nfl_standings = json.loads(nfl_stand)
    afc_east = ["Buffalo Bills", "New England Patriots", "New York Jets", "Miami Dolphins"]
    afc_east_index = 0
    afc_east_dict = {}
    while True:
        try:
            if nfl_standings["children"][0]["standings"]["entries"][afc_east_index]["team"]["displayName"] in afc_east:
                print(nfl_standings["children"][0]["standings"]["entries"][afc_east_index]["team"]["displayName"])
                record = nfl_standings["children"][0]["standings"]["entries"][afc_east_index]["stats"][-5]["summary"]
                win_perc = nfl_standings["children"][0]["standings"]["entries"][afc_east_index]["stats"][3]["displayValue"]
                seed = nfl_standings["children"][0]["standings"]["entries"][afc_east_index]["stats"][0]["displayValue"]
                afc_east_dict[nfl_standings["children"][0]["standings"]["entries"][afc_east_index]["team"]["displayName"]] = record, win_perc, seed
            afc_east_index += 1
        except IndexError:
            break
    sorted_afc_east = sorted(afc_east_dict.items(), key = lambda afc_east_dict: int(afc_east_dict[1][2]), reverse = False)
    aeast_string = ""
    for i in range (len(sorted_afc_east)):
       aeast_string += str(sorted_afc_east[i][0]) + " | " + str(sorted_afc_east[i][1][0]) + " | " + str(sorted_afc_east[i][1][1]) + " | Playoff Seed: " + str(sorted_afc_east[i][1][2]) + "\n"
    fin = []
    fin.append(["Team", "Record", "Win Percentage", "Playoff Seed"])
    for item in sorted_afc_east:
        fin.append([item[0], item[1][0], item[1][1], item[1][2]])
    fin_tab = tabulate(fin, headers = 'firstrow', tablefmt = "fancy_grid")
    await aeast.send(fin_tab)


#AFC North

@client.command()
async def afcnorth(anorth):

    nfl = "https://site.api.espn.com/apis/v2/sports/football/nfl/standings"
    nfl_stand = requests.get(nfl).text
    nfl_standings = json.loads(nfl_stand)
    afc_north = ["Baltimore Ravens", "Cincinnati Bengals", "Cleveland Browns", "Pittsburgh Steelers"]
    afc_north_index = 0
    afc_north_dict = {}
    while True:
        try:
            if nfl_standings["children"][0]["standings"]["entries"][afc_north_index]["team"]["displayName"] in afc_north:
                print(nfl_standings["children"][0]["standings"]["entries"][afc_north_index]["team"]["displayName"])
                record = nfl_standings["children"][0]["standings"]["entries"][afc_north_index]["stats"][-5]["summary"]
                win_perc = nfl_standings["children"][0]["standings"]["entries"][afc_north_index]["stats"][3]["displayValue"]
                seed = nfl_standings["children"][0]["standings"]["entries"][afc_north_index]["stats"][0]["displayValue"]
                afc_north_dict[nfl_standings["children"][0]["standings"]["entries"][afc_north_index]["team"]["displayName"]] = record, win_perc, seed
            afc_north_index += 1
        except IndexError:
            break
    sorted_afc_north = sorted(afc_north_dict.items(), key = lambda afc_north_dict: int(afc_north_dict[1][2]), reverse = False)
    anorth_string = ""
    for i in range (len(sorted_afc_north)):
       anorth_string += str(sorted_afc_north[i][0]) + " | " + str(sorted_afc_north[i][1][0]) + " | " + str(sorted_afc_north[i][1][1]) + " | Playoff Seed: " + str(sorted_afc_north[i][1][2]) + "\n"
    fin = []
    fin.append(["Team", "Record", "Win Percentage", "Playoff Seed"])
    for item in sorted_afc_north:
        fin.append([item[0], item[1][0], item[1][1], item[1][2]])
    fin_tab = tabulate(fin, headers = 'firstrow', tablefmt = "fancy_grid")
    await anorth.send(fin_tab)

@client.command()
async def nflscores(nfl):
    nfl_api = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    scores = requests.get(nfl_api).text
    teams = json.loads(scores)
    nfl_game_index = 0
    nfl_scores = ""
    nfl_scores += "These are the NFL scores for " + t_date + " \n\n"
    while True:
        try:
            nfl_scores += teams["events"][nfl_game_index]["competitions"][0]["competitors"][1]["team"]["shortDisplayName"] + " "
            nfl_scores += teams["events"][nfl_game_index]["competitions"][0]["competitors"][1]["score"] + " vs "
            nfl_scores += teams["events"][nfl_game_index]["competitions"][0]["competitors"][0]["team"]["shortDisplayName"] + " "
            nfl_scores += teams["events"][nfl_game_index]["competitions"][0]["competitors"][0]["score"] + " ("
            nfl_scores += teams["events"][nfl_game_index]["status"]["type"]["detail"] + ")\n"
            nfl_game_index += 1
            continue
        except IndexError:
            nfl_scores += "\nThat's all for today!"			
            break
    await nfl.send(nfl_scores)

@client.command()
async def nflschedule(nfl):
    nfl_api = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    schedule = requests.get(nfl_api).text
    teams = json.loads(schedule)
    nfl_schedule_index = 0
    nfl_schedule = ""
    nfl_schedule += "These are the NFL games for week " + str(teams["week"]["number"]) + ": \n\n"
    while True:
        try:
            name = teams["events"][nfl_schedule_index]["name"]
            if "Washington " in name:
                nfl_schedule += name.replace("Washington ", "Washington") + " @"
            else:
                nfl_schedule += name + " @"
            date = teams["events"][nfl_schedule_index]["date"]
            new_date = date.split("T")[1][0:-1]
            hour = int(new_date[0:2])
            minutes = new_date[2:]
            if hour > 5:
                hour = hour-5
            elif hour == 0:
                hour = 19
            elif hour == 1:
                hour = 20
            elif hour == 2:
                hour = 21
            elif hour == 3:
                hour = 22
            elif hour == 4:
                hour = 23
            elif hour == 5:
                hour = 24
            mil_hour = hour
            if mil_hour <12:
                nfl_schedule += str(mil_hour) + str(minutes) + " AM" "\n"
            elif mil_hour == 12:
                nfl_schedule += str(mil_hour) + str(minutes) + " PM" "\n"
            elif mil_hour == 24:
                mil_hour = mil_hour-12
                nfl_schedule += str(mil_hour) + str(minutes) + " AM" "\n"           
            else:
                mil_hour = mil_hour-12
                nfl_schedule += str(mil_hour) + str(minutes) + " PM" "\n"
            nfl_schedule_index+=1
        except IndexError:
            nfl_schedule += "\nThat's all for today!"			
            break
    await nfl.send(nfl_schedule)



client.run(TOKEN)





'''
def ppjson(data):
    print(json.dumps(data, indent = 5, sort_keys = True))

#print(ppjson(espn.get_teams("mlb")))﻿ball/league/standings?leagueId=" + str(league_id)
html_content = requests.get("https://fantasy.espn.com/basketball/league/standings?leagueId=15662402").text
soup = BeautifulSoup(html_content, "html.parser")
print(soup.prettify()) # print the parsed data of html
standings_table = soup.find_all("meta")
#print(standings_table)
#print(soup.title.text)

'''