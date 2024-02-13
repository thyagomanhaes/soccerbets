import time
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup  # Optionally for parsing HTML
from selenium.webdriver.support import expected_conditions as EC

from webscraping.soccervital.database import Connection

urls = [
    "https://www.soccervital.com/ad-grecia-vs-herediano-soccer-prediction-jggj526a4.html",
    "https://www.soccervital.com/morton-vs-arbroath-soccer-prediction-jggj5j992.html"
]


def start():

    for url in urls:
        driver.get(url)
        result_div = driver.find_element(By.XPATH, '//*[@id="loadresult"]/div[1]')
        result = result_div.text
        print("Valor: ", result)

connec = Connection()

cursor = connec.cursor

sql = f"SELECT * FROM soccer_vista.all_matches WHERE RESULT IS NULL OR RESULT = '' AND DAY(MATCH_DATE) <= DAY(GETDATE()) ORDER BY MATCH_DATE"


# Result:  1 - 1 Pen (4 - 5)
# Result:  0 - 0 Abandoned
# Postponed
# Abandoned
# Result:  1 - 2 AET
ts_now_brazil = datetime.now(pytz.timezone('Brazil/East'))

try:
    cursor.execute(sql)

    # Fetch the results
    results = cursor.fetchall()

    # Print the results
    driver = webdriver.Chrome()  # Replace with your browser's WebDriver
    for row in results:
        id_match = row[0]
        match_date = row[4]
        url = row[9]
        strategy = row[11]
        print(strategy, url, match_date)
        try:
            driver.get(url)
            #driver.implicitly_wait(10)
            result_div = driver.find_element(By.XPATH, '//*[@id="loadresult"]/div[1]')
            timeresult_div = driver.find_element(By.XPATH, '//*[@id="loadresult"]/div[2]')

            result = result_div.text
            timeresult = timeresult_div.text
            print(f"Result: [{result}], timeresult: [{timeresult}]")

            segue = False
            final_result = None

            if result != '':
                if timeresult == 'FT' or 'Pen' in timeresult:
                    final_result = result
                elif timeresult == 'AET' and '-' in result:
                    home_goals = result.split('-')[0].strip()
                    away_goals = result.split('-')[1].strip()
                    min_score = min(home_goals, away_goals)
                    final_result = f"{min_score} - {min_score}"
                    print(final_result)
            elif result == '' and timeresult.strip() == 'Postponed' in timeresult or 'Abandoned' in timeresult:
                final_result = 'PSTP'

            if strategy == 'Banker Bets':
                table = 'banker_bets_matches'
            elif strategy == 'Value Bets':
                table = 'value_bets_matches'
            else:
                table = 'draw_bets_matches'

            if final_result is not None:
                sql = f"UPDATE soccer_vista.{table} SET RESULT = '{final_result}' where ID_MATCH = '{id_match}'"
                print(sql)
                cursor.execute(sql)
                cursor.commit()
                print("Atualizado com sucesso!\n")
        except Exception as es:
            print(es)
            pass
except Exception as e:
    print(e)

# start()





