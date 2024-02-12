from crawler import scamletterinfo
from crawler import scamsurvivors


def fetch_all():
    scamletterinfo.fetch()
    scamsurvivors.fetch()
