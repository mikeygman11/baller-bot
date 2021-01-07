# Baller-Bot

This application utilizes ESPN's basketball and football API's (more to be added in later versions) to retrieve updated scores and standings for the respective leagues. The Python script is integrated with Discord's API to include various commands that can be called in any discord channel that has Baller-Bot in it. 

# Getting Started

I spent a decent amount of time searching for an API that would provide me the type of information I was looking for. Ultimately, I found a repository with detailed documentation about ESPN's Hidden API and the endpoints for specific data. For those interested, here's the url: https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b

After this was done, I began setting up my bot by travelling to Discord's website, signing in, selecting New Application, and going through the process of specifying what I wanted my bot to do.

# Installing

Before anything, I made sure I had the latest version of Python's package manager, Pip by running `sudo -H pip3 install --upgrade pip`

After finding the API with the content needed to gather info like scores and matchups for the NBA and NFL I ran the following command to install the Python Requests library: `python -m pip install requests`

Once I finished setting up the bot and including it in my server, I ran `python3 -m pip install -U discord.py` to get access to the Discord API.

Finally, to allow formatting the data into nice-looking tables, I installed Tabulate by running `pip install tabulate`. Now, I was ready to begin programming my bot.

# The Process

I began the programming process by setting up the Discord development environment. This included retrieving a key/token that let me connect to the bot and use the API. I then read up on Discord's Python docmentation and researched the @tags as well as the headers on Discord's Python classes. Once I became familiar with the API, I knew I needed to use @client.command() for most of the functions I'd be creating.

Once I set up the general skeleton for programming Discord commands, I started exploring the ESPN API that I had decided to use. My first goal was to be able to parse the HTML text from the endpoints into JSON text for easy processing later on. In order to do this, I utilized the Requests library in Pyton and json.loads(text_variable_name). Once I got the data into a large Python dictionary, I was able to explore the patterns of ESPN's JSON text to extract the information I needed.

As I progressed with retrieving data I wanted, I realized I wanted to display information (like standings) in a nice, readable format. As such, I used the Python Tabulate library which displays lists of lists, iterables of iterables, etc into visually appealing tables. For each NFL division, once I sorted the teams and their data by playoff seed, I wanted to turn the list of tuple pairs into something Tabulate could process. Therefore, I created the below algorithm to do so:

`    fin = []
    fin.append(["Team", "Record", "Win Percentage", "Playoff Seed"])
    for item in sorted_nfc_west:
        print(item[0])
        fin.append([item[0], item[1][0], item[1][1], item[1][2]])
    fin_tab = tabulate(fin, headers = 'firstrow', tablefmt = "fancy_grid")`
    

Essentially, given the list `[('Pittsburgh Steelers', ('12-4', '.750', '3')), ('Baltimore Ravens', ('11-5', '.688', '5')), ('Cleveland Browns', ('11-5', '.688', '6')), ('Cincinnati Bengals', ('4-11-1', '.281', '13'))]`, where the first element in the tuple is the Team Name and the second element is another tuple of statistics, this algorithm creates a list of lists with the team name and statistics and passes this info to the tabulate function so it can process the data into a table.

Besides this, a lot of the process was using the JSON text to pull information into a readable format to send to the Discord Server.

# Documentation

At the moment, the various commands are available for Baller-Bot:

## NFL Functions

###### -nfceast (prints the standings of the NFL's NFC East Division - uses Python Tabulate library to print in table format)
###### -nfcwest (same for NFC West)
###### -nfcsouth
###### -nfcnorth
###### -afceast
###### -afcwest
###### -afcsouth
###### -afcnorth
###### -nflscores (prints scores of current week of games)
###### -nfcschedule (prints games to be played this week)

## NBA Functions

###### -nbascores (prints scores of today's games)
###### -nbaschedule (prints games to be played today)

Thank you for taking the time to check out my work!

# Built With

##### Languages used
Python

#### API's used
Discord.py, ESPN API

# Authors
##### Michael Galanaugh - New Jersey Institute of Technology 2022
##### Email
michael.galanaugh11@gmail.com
