import datetime
from selenium.webdriver.common.by import By
from celery import shared_task
from celery.exceptions import Ignore
import time

from tasks.scraper.base.base_scraper import DataScraper


class GithubScraper(DataScraper):
    def __init__(self, login_url, username, password, submit, redirect_url):
        super(GithubScraper, self).__init__(login_url, username, password, submit, redirect_url)


@shared_task
def github_scraper():
    login_url = 'https://github.com/login'
    username = {
        'by': (By.ID, 'login_field'),
        'text': 'boris.allen127@outlook.com'
    }
    password = {
        'by': (By.ID, 'password'),
        'text': 'Barhfu1028'
    }
    submit = (By.XPATH, '//input[@type="submit"]')
    redirect_url = 'https://github.com'

    page_url = 'https://github.com/settings/profile'
    elements = [
        {
            'name': 'name',
            'by': (By.ID, 'user_profile_name')
        },
        {
            'name': 'email',
            'by': (By.ID, 'user_profile_email')
        }
    ]

    scraper = GithubScraper(login_url, username, password, submit, redirect_url)
    data = scraper.run(page_url, elements)
    if not data:
        raise Exception('Scrape Failed')
    return True
