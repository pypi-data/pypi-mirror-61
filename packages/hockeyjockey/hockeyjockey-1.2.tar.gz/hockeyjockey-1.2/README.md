# hockeyjockey
A menu-driven console-based application for analyzing NHL hockey games.

## Purpose
This app was created to assist with making hockey pics for a so-called 'confidence pool' (such as this [NHL Pick 'Em Pool](https://www.officepooljunkie.com/info-nhl-hockey-pools.php)), where a pool participant must pick the outcome of several games and rank them in order of how confident they are that the chosen team in each matchup will win.

## Requirements:
 - Python >= 3.6
 - decorest
 - ansicolors


## Installation:
```bash
pip install hockeyjockey
```

## Usage
```python
from hockeyjockey import Jockey

# hockeyjockey will automatically download stats and games from the internet
jockey = Jockey()
jockey.menu_main.display_menu()

# you can choose to load the cached copy of games and stats data from disk
# by answering the prompts
jockey = Jockey(suppress_prompt=False)
jockey.menu_main.display_menu()
```

## Documentation
When hockeyjockey first loads, you will be given the option to load NHL statistics and games which have been cached to disk. If the local cache does not exist, or you elect not to use cached data, new data will be fetched from the internet.  

The default is to fetch hockey games for the closest Friday and Saturday.

### Games Menu
1. Load Today's Games - Loads the NHL games that are taking place today into memory.
2. Load Upcoming Friday/Saturday - If today is a Friday or Saturday, loads the current Friday/Saturday's games, otherwise loads next weekend's Friday/Saturday games.
3. Load Custom Date Range - Prompts for a start and end date and loads the games between those dates inclusive.
4. Print Games - Echoes the currently loaded games to the console.

### Teams Menu
1. Print Teams - Prints a list of the NHL teams in alphabetical order.

### Stats Menu
1. Reload Stats - Fetches a fresh copy of the latest NHL statistics for all teams and stores it in memory. The stats stored in memory are the basis for hockeyjockey's ranking analysis.
2. Rank Games by Single Statistic - Requires that a set of NHL games and statistics have been loaded. This option provides the main purpose for hockeyjockey - ranking a set of NHL games by a single stat which is chosen from the stats provided. For example, if the user of the program chooses 'wins', hockey jockey will output a list of games with the team with the most wins in each matchup highlighted green. The amplitude difference between the team with the greater number of wins and the team with the lesser number of wins is the key on which the games are ranked.  
3. Rank Games by All Statistics - The same as the above option, but will rank the games by every statistic in memory.
4. Print Stats - Echoes the currently loaded NHL statistics for all teams to the console.

### Statistics
Special thanks to Drew Hynes for documenting the NHL Stats API, [here](https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md).

### License
[GNU GPLv3](LICENSE.TXT) 
