from datetime import datetime


class Match:
    id_match: str
    home_team: str
    away_team: str
    match_date: datetime
    pick: str
    league: str
    confidence: int

    def __init__(self,
                 id_match,
                 home_team,
                 away_team,
                 pick,
                 odd,
                 url_match_details,
                 league_name,
                 country_name,
                 oficial,
                 date_scraped_br,
                 match_date,
                 match_date_br
                 ):
        self.id_match = id_match
        self.home_team = home_team
        self.away_team = away_team
        self.pick = pick
        self.odd = odd
        self.url_match_details = url_match_details
        self.league_name = league_name
        self.country_name = country_name
        self.oficial = oficial
        self.date_scraped_br = date_scraped_br
        self.match_date = match_date
        self.match_date_br = match_date_br

    def create_msg_telegram(self):
        msg = f"{self.home_team} x {self.away_team}"
        msg += f"\n{self.odd}"
        return msg
