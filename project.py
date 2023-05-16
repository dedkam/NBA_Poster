import sys
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playergamelog
import pandas as pd
from tabulate import tabulate
import requests
import shutil
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import dataframe_image as dfi

def main():
    player1, player2, season = validate_arguments()
    player1_dict = validate_player(player1)
    player2_dict = validate_player(player2)
    if validate_season(player1_dict[0]["id"], season) and validate_season(
        player2_dict[0]["id"], season
        ):
        get_stats(player1_dict, season)
        get_stats(player2_dict, season)
    else:
        if validate_season(player1_dict[0]["id"],season) == False:
            sys.exit(f"{player1} does not play in NBA in {season} season")
        else:
            sys.exit(sys.exit(f"{player2} does not play in NBA in {season} season"))

    player1_gamelog_mean = get_stats(player1_dict, season)
    player2_gamelog_mean = get_stats(player2_dict, season)
    comparison_df =pd.concat([player1_gamelog_mean, player2_gamelog_mean], ignore_index=True)
    print(tabulate(comparison_df, headers=comparison_df.columns, showindex=False, tablefmt="grid"))
    comparison_df.to_csv("comparison.csv")

    # save player images
    get_image(player1_dict)
    get_image(player2_dict)
    
    #create and save plot
    create_plot(player1_dict, player2_dict, season)

    #create table image
    create_table_image(comparison_df)
    
    #create an comparison PDF file
    create_comparison_pdf(player1_dict, player2_dict, season, comparison_df)

# validate command-line argument
# expected input name of 2 NBA players as "First Last" and optional season year XXXX format (if not default = 2022)
def validate_arguments():
    if len(sys.argv) < 3:
        sys.exit("Too few argument")
    elif 3 <= len(sys.argv) <= 4:
        player1 = sys.argv[1]
        player2 = sys.argv[2]
        if len(sys.argv) == 4:
            season = sys.argv[3]
        else:
            season = 2022
        return (player1, player2, season)
    else:
        sys.exit("Too many arguments")


# check if players exist in database
def validate_player(player):
    player_dict = players.find_players_by_full_name(player)
    if len(player_dict) < 1:
        sys.exit(f"Player {player} do not exist in database")
    return player_dict

def validate_season(player_id, year):
    # get list of season
    player_info = commonplayerinfo.CommonPlayerInfo(player_id)
    player_info_dict = player_info.available_seasons.get_dict()
    lists = player_info_dict["data"]
    seasons = []
    for list in lists:
        if list[0][1:] not in seasons:
            seasons.append(list[0][1:])
    if str(year) in seasons:
        return True
    else:
        return False

def get_stats(player_dict, year):
    player_gamelog = playergamelog.PlayerGameLog(player_dict[0]["id"], year)
    player_gamelog_df = player_gamelog.get_data_frames()[0]
    player_gamelog_mean = player_gamelog_df[["PTS", "AST", "REB", "BLK", "MIN","FG_PCT", "FG3_PCT"]].describe().iloc[1:2]
    player_gamelog_mean["Name"] = f"{player_dict[0]['full_name']}"
    return player_gamelog_mean

def get_image(player_dict):
    player_id = player_dict[0]["id"]
    url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(f"{player_id}.png", "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def create_plot(player1_dict, player2_dict, season):
    player1_full_name = player1_dict[0]["full_name"]
    player2_full_name = player2_dict[0]["full_name"]
    df = pd.read_csv("comparison.csv")

    df = df[["PTS", "AST", "REB"]]
    columns = df.columns.tolist()

    X_axis = np.arange(3)
    player1_y = df.iloc[0].tolist()  
    player2_y = df.iloc[1].tolist()
    plt.rcParams.update({"font.size": 12, "font.weight": "bold", "axes.edgecolor": "white"})
    plt.bar(X_axis - 0.2, player1_y, 0.4, label = f"{player1_full_name}")
    plt.bar(X_axis + 0.2, player2_y, 0.4, label = f"{player2_full_name}")
    plt.xticks(X_axis, columns)
    plt.tick_params(axis="x", colors="white")
    plt.tick_params(axis="y", colors="white")
    plt.xlabel("Game Elements",color="white")
    plt.ylabel("Value", color = "white")
    plt.title(f"Average in season {season}", color="white")
    plt.legend()
    plt.savefig(f"{player1_full_name}_vs_{player2_full_name}_in_season_{season}.png", transparent=True)

def create_comparison_pdf(player1_dict, player2_dict, season, comparison_df):
    
    player1_id = player1_dict[0]["id"]
    player2_id = player2_dict[0]["id"]
    player1_full_name = player1_dict[0]["full_name"]
    player2_full_name = player2_dict[0]["full_name"]
    pdf = FPDF(orientation="L")
    pdf.add_page()
    pdf.image("background.jpg", x=0,y=0, w=298, h=210)
    pdf.image(f"{player1_id}.png", x= 10, y = 40, w = 80)
    pdf.image(f"{player2_id}.png", x= 187, y = 40, w = 80)
    pdf.set_font("Helvetica", "b", 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(10, 25)
    pdf.cell(80, 20, f"{player1_full_name}", align="C")
    pdf.set_xy(187,25)
    pdf.cell(80, 20, f"{player2_full_name}", align="C")

    #print comparison table
    pdf.image("table.png", x=25, y=130,w = 250)
     
    #add plot
    pdf.image(f"{player1_full_name}_vs_{player2_full_name}_in_season_{season}.png", x=90, y=40, w=100)

    #create output PDF file
    pdf.output("comparison.pdf")

def create_table_image(comparison_df):
    comparison_df = comparison_df.style.hide().background_gradient(axis=None, vmin=1, vmax=40, cmap="plasma_r")
    dfi.export(comparison_df, "table.png", table_conversion="matplotlib")




if __name__ == "__main__":
    main()
