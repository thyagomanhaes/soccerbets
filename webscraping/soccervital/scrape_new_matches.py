import hashlib
import pytz
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

from webscraping.soccervital.database import Connection
from webscraping.soccervital.constants import URL_SOCCER_VITAL, URL_SOCCER_VITAL_DAY_MINUS_1, URL_SOCCER_VITAL_DAY_MINUS_2
from webscraping.soccervital.model.match import Match


class SoccerVitalScraper:
    def __init__(self):
        self.URLS_LEAGUES = []

    def scrape_league_page(self):
        pass

    def scrape_top_leagues(self):
        leagues_url = []

        page = requests.get(URL_SOCCER_VITAL)

        soup = BeautifulSoup(page.text, 'html.parser')

        top_leagues_ul: list = soup.find_all('ul', {"class": "navlist2"})

        if len(top_leagues_ul) > 0:
            top = top_leagues_ul[0]
            leagues = top.find_all('li')
            # print(leagues)
            for league_li in leagues:
                league_link = league_li.find('a')
                if league_link is not None:
                    league_url = league_link.get('href')
                    leagues_url.append(league_url)
            self.URLS_LEAGUES = leagues_url

    def scrape_match_details(self, match):
        page_match_details = requests.get(match.url_match_details)
        if page_match_details.status_code == 200:
            soup_match_details = BeautifulSoup(page_match_details.text, 'html.parser')
            tables_last5 = soup_match_details.find_all('table', {'class': 'gamec'})
            # print(f"Nº tabelas: {len(tables_last5)}")
            if len(tables_last5) == 8:
                start_index = 5
            else:
                start_index = 6

            table_overall_last5 = tables_last5[start_index]
            table_home_last5 = tables_last5[start_index+1]
            table_away_last5 = tables_last5[start_index+2]

            trs_overall = table_overall_last5.find_all('tr', {'class': 'twom'})
            home_trs = trs_overall[0]
            away_trs = trs_overall[1]

            home_last5_overall_win = home_trs.find_all('td')[2].text
            home_last5_overall_draw = home_trs.find_all('td')[3].text
            home_last5_overall_lose = home_trs.find_all('td')[4].text
            home_last5_overall_goals = home_trs.find_all('td')[5].text
            home_last5_overall_goals_scored = home_last5_overall_goals.split(':')[0]
            home_last5_overall_goals_conceded = home_last5_overall_goals.split(':')[1]
            home_last5_overall_pct_over25 = home_trs.find_all('td')[6].text
            home_last5_overall_pct_over25 = round(float(home_last5_overall_pct_over25.split('%')[0])/100, 2)
            home_last5_overall_pct_btts = home_trs.find_all('td')[7].text
            home_last5_overall_pct_btts = round(float(home_last5_overall_pct_btts.split('%')[0]) / 100, 2)
            home_last5_overall_power = home_trs.find_all('td')[8].text

            away_last5_overall_win = away_trs.find_all('td')[2].text
            away_last5_overall_draw = away_trs.find_all('td')[3].text
            away_last5_overall_lose = away_trs.find_all('td')[4].text
            away_last5_overall_goals = away_trs.find_all('td')[5].text
            away_last5_overall_goals_scored = away_last5_overall_goals.split(':')[0]
            away_last5_overall_goals_conceded = away_last5_overall_goals.split(':')[1]
            away_last5_overall_pct_over25 = away_trs.find_all('td')[6].text
            away_last5_overall_pct_over25 = round(float(away_last5_overall_pct_over25.split('%')[0]) / 100, 2)
            away_last5_overall_pct_btts = away_trs.find_all('td')[7].text
            away_last5_overall_pct_btts = round(float(away_last5_overall_pct_btts.split('%')[0]) / 100, 2)
            away_last5_overall_power = away_trs.find_all('td')[8].text

            trs_onlyhome = table_home_last5.find_all('tr', {'class': 'twom'})
            trs_onlyhome = trs_onlyhome[0]

            home_last5_onlyhome_win = trs_onlyhome.find_all('td')[2].text
            home_last5_onlyhome_draw = trs_onlyhome.find_all('td')[3].text
            home_last5_onlyhome_lose = trs_onlyhome.find_all('td')[4].text
            home_last5_onlyhome_goals = trs_onlyhome.find_all('td')[5].text
            home_last5_onlyhome_goals_scored = home_last5_onlyhome_goals.split(':')[0]
            home_last5_onlyhome_goals_conceded = home_last5_onlyhome_goals.split(':')[1]
            home_last5_onlyhome_pct_over25 = trs_onlyhome.find_all('td')[6].text
            home_last5_onlyhome_pct_over25 = round(float(home_last5_onlyhome_pct_over25.split('%')[0]) / 100, 2)
            home_last5_onlyhome_pct_btts = trs_onlyhome.find_all('td')[7].text
            home_last5_onlyhome_pct_btts = round(float(home_last5_onlyhome_pct_btts.split('%')[0]) / 100, 2)
            home_last5_onlyhome_power = trs_onlyhome.find_all('td')[8].text

            trs_onlyaway = table_away_last5.find_all('tr', {'class': 'twom'})
            trs_onlyaway = trs_onlyaway[0]

            away_last5_onlyaway_win = trs_onlyaway.find_all('td')[2].text
            away_last5_onlyaway_draw = trs_onlyaway.find_all('td')[3].text
            away_last5_onlyaway_lose = trs_onlyaway.find_all('td')[4].text
            away_last5_onlyaway_goals = trs_onlyaway.find_all('td')[5].text

            away_last5_onlyaway_goals_scored = away_last5_onlyaway_goals.split(':')[0]
            away_last5_onlyaway_goals_conceded = away_last5_onlyaway_goals.split(':')[1]
            away_last5_onlyaway_pct_over25 = trs_onlyaway.find_all('td')[6].text
            away_last5_onlyaway_pct_over25 = round(float(away_last5_onlyaway_pct_over25.split('%')[0]) / 100, 2)
            away_last5_onlyaway_pct_btts = trs_onlyaway.find_all('td')[7].text
            away_last5_onlyaway_pct_btts = round(float(away_last5_onlyaway_pct_btts.split('%')[0]) / 100, 2)
            away_last5_onlyaway_power = trs_onlyaway.find_all('td')[8].text


            print(home_last5_overall_win, home_last5_overall_draw, home_last5_overall_lose, home_last5_overall_goals_scored, home_last5_overall_goals_conceded, home_last5_overall_pct_over25, home_last5_overall_pct_btts, home_last5_overall_power)
            print(away_last5_overall_win, away_last5_overall_draw, away_last5_overall_lose,
                  away_last5_overall_goals_scored, away_last5_overall_goals_conceded, away_last5_overall_pct_over25,
                  away_last5_overall_pct_btts, away_last5_overall_power)
            print(home_last5_onlyhome_win, home_last5_onlyhome_draw, home_last5_onlyhome_lose, home_last5_onlyhome_goals_scored, home_last5_onlyhome_goals_conceded, home_last5_onlyhome_pct_over25, home_last5_onlyhome_pct_btts, home_last5_onlyhome_power)
            print(away_last5_onlyaway_win, away_last5_onlyaway_draw, away_last5_onlyaway_lose, away_last5_onlyaway_goals_scored, away_last5_onlyaway_goals_conceded, away_last5_onlyaway_pct_over25, away_last5_onlyaway_pct_btts, away_last5_onlyaway_power)
            # print(home_power_last5)
            # print(away_power_last5)
            print(match.country_name, match.match_date_br)

    def scrape_tables(self, table, table_name, strategy):

        all_trs = table.find_all('tr')

        league_name = None
        country_name = None
        for tr in all_trs:
            if 'headupe' in tr.attrs.get('class'):
                league_name = tr.find_all('td')[1].text
                country_name = league_name.split(' ')[0]
                continue
            if 'twom' in tr.attrs.get('class'):
                on_click_text = tr.attrs.get('onclick')
                match_url = on_click_text[on_click_text.find("location='") + 10: on_click_text.find("';")]
                # print(match_url)
                url_match_details = match_url

                tds = tr.find_all('td')
                match_hour = tds[0].text
                home_team = tds[1].text
                away_team = tds[2].text
                bet = tds[3].text
                confidence = bet.split('on')[0].strip()
                odd = bet[bet.find("(") + 1:bet.find(")")]
                bet_team = bet[bet.find("on") + 2:bet.find("(")].strip()

                div_dates = soup.find('div', {"id": "date"})

                selected_div_date = div_dates.find('a', {'class': 'strong'})
                selected_div_date = selected_div_date.text
                dates_parts = selected_div_date.split(' ')

                day = dates_parts[1][:-1]
                current_date = datetime.now()
                match_date = datetime(current_date.year, current_date.month, int(day), int(match_hour.split(":")[0]),
                                      int(match_hour.split(":")[1]))

                if table_name == 'draw_bets_matches':
                    pick = 'X'
                elif home_team in bet_team:
                    pick = '1'
                else:
                    pick = '2'

                id_match = home_team + away_team + str(match_date)
                b = id_match.encode()  # convert string to bytes
                h = hashlib.new("sha256")  # create a hash object
                h.update(b)  # update the hash object with bytes
                id_match = h.hexdigest()  # print the hexadecimal hash value

                msg = f"[{league_name}]:\n{match_date}|{home_team}|{away_team}|{pick}|{odd}|{confidence}"
                print(msg)
                # send_message_to_telegram(msg, CANAL_NOTIFICACOES_BETFAIR)
                # connec = Connection()

                # cursor = connec.cursor

                sql = f"insert into soccer_vista.{table_name} values ('{id_match}', '{home_team}', '{away_team}', " \
                      f"'{league_name}', CAST('{match_date}' as datetime2), '{pick}', {odd}, {confidence}, NULL, " \
                      f"'{url_match_details}', CAST('{current_date}' as datetime2) )"

                try:
                    ts_now_brazil = datetime.now(pytz.timezone('Brazil/East'))
                    match_date_br = match_date - timedelta(hours=3)

                    match = Match(
                        id_match=id_match,
                        home_team=home_team,
                        away_team=away_team,
                        pick=pick,
                        odd=odd,
                        oficial='S',
                        match_date=match_date,
                        match_date_br=match_date_br,
                        date_scraped_br=ts_now_brazil,
                        url_match_details=url_match_details,
                        league_name=league_name,
                        country_name=country_name
                    )

                    self.scrape_match_details(match)

                    msg_to_telegram = match.create_msg_telegram()
                    print(msg_to_telegram)
                    # cursor.execute(sql)
                    # connec.conn.commit()
                    # print(sql)
                except Exception as e:
                    print(e)
                    continue
                print("\n")


# if len(all_tables) > 0:
#     scrape_tables(all_tables[0], 'banker_bets_matches', 'Bets of the day - Bankers')
#     print("\n")
#     scrape_tables(all_tables[2], 'value_bets_matches', 'Value Bets of the day')
#     print("\n")
#     scrape_tables(all_tables[4], 'draw_bets_matches', 'DRAW bet of the day')
#     # print(all_tables[2])


soccer_vital_scraper = SoccerVitalScraper()
page = requests.get(URL_SOCCER_VITAL)
soup = BeautifulSoup(page.text, 'html.parser')

all_tables = soup.find_all('table')
soccer_vital_scraper.scrape_tables(all_tables[0], 'banker_bets_matches', 'Bets of the day - Bankers')
soccer_vital_scraper.scrape_tables(all_tables[2], 'value_bets_matches', 'Value Bets of the day')
soccer_vital_scraper.scrape_tables(all_tables[4], 'draw_bets_matches', 'DRAW bet of the day')
