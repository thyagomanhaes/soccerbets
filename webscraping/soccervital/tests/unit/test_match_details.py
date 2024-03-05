import pytest
from bs4 import BeautifulSoup

from utils.utils import convert_to_datetime
from webscraping.soccervital.tests.stubs import HTML_TABLE_GAME_DETAILS
from webscraping.soccervital.scrape_new_matches_v2 import SoccerVitalScraper
from datetime import datetime


class TestScraperMatchDetails:

    @pytest.fixture
    def setup_mock_page(self):
        """
        Simulates the HTML for a match details page used for testing.
        """
        html_content = HTML_TABLE_GAME_DETAILS
        return BeautifulSoup(html_content, "html.parser")

    def test_should_return_game_details_info(self, setup_mock_page):
        scraper = SoccerVitalScraper()
        soup_table_match_game_details = setup_mock_page

        response = scraper.parse_match_game_details(soup_table_match_game_details)

        keys_to_check = ['HomeTeam', 'AwayTeam', 'OddHome', 'OddDraw', 'OddAway', 'Date', 'Time']

        assert response is not None
        assert isinstance(response, dict)
        assert all(elem in response.keys() for elem in keys_to_check) is True

    @pytest.mark.parametrize('date, time, day, month, year, hour, minute',
                             [
                                 ('Tuesday 5th March 2024', '20:00', 5, 3, 2024, 20, 0),
                                 ('Tuesday 1st March 2024', '23:30', 1, 3, 2024, 23, 30),
                                 ('Tuesday 3rd October 2024', '11:15', 3, 10, 2024, 11, 15)
                             ])
    def test_should_convert_date_and_time_to_datetime(self, date, time, day, month, year, hour, minute):
        match_date = convert_to_datetime(date, time)

        assert isinstance(match_date, datetime)
        assert match_date.day == day
        assert match_date.month == month
        assert match_date.year == year
        assert match_date.hour == hour
        assert match_date.minute == minute
