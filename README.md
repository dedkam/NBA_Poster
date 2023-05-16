# NBA PLAYER COMPARISON
#### Video Demo: https://youtu.be/CheNzKnS1k4
#### Description
NBA PLAYER COMPARISON is a program which helps you to compare NBA players in specified game season. 
As input it requires from user to type two NBA players names and optionally season - program uses command-line arguments. If user does not specify season, as default program will provide comparison for 2022. Final result is PDF poster that present player's photos, simple graph, and table with stats for both player.
There are few steps to provide final PDF poster:
- validate players names, user should provide 2 or 3 command-line argument - at least there should be two player full names, optionally season, during which user want to compare game elements as: point, rebound, assist, block, minutes, and % in 2-points and 3-points throws
- checking if both players are active players in specified season, if not sys.exit quit program with proper information
- using NBA_API get the players stats, then using Pandas formatting and averaging statistic , and create final table
- with mathplotlib create simple plot
- with requests library scrape the players photo from nba.com
- finally create PDF comparison poster with FPDF library, contains:
    - background.jpg as a PDF page bacground - user can uses diffrent files as background, which allows to create for example posters before each games and uses it on social media like twitter or facebook
    - simple plot compares two player in 3 game elements : PTS, AST, REB
    - photos of players which are downloading from main page of nba.com
    - graphical table of dataframe, which help user to compare players in another game elements
- as a addition in terminal user can also see a table creating with tabulate library
- as a result in program directory, there should be files:
    - 2 players photo in files called player_id.png
    - comparison.csv - contains statistic for players in CSV file
    - comparison.pdf - final PDF page
    - plot image
    - table image