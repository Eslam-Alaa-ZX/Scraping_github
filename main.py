from requests.api import get
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urlparse
import http.cookiejar
import requests
from lxml import html
from lxml import etree
import csv
from itertools import zip_longest
from bs4 import BeautifulSoup
import re
import operator


def openWebsite():
    username = str(input("enter GitHub username: "))
    repo_info = []
    stars = []
    names = []
    urls = []
    stars = []
    forks = []
    issues = []

    while True:

        url = "https://github.com/" + username + "?tab=repositories"
        web_url = requests.get(url)
        result = web_url.content
        soup = BeautifulSoup(result, "lxml")
        listOfRipo = soup.find_all("ul", {"data-filterable-for": "your-repos-filter"})
        for repo in listOfRipo:
            a_repo = repo.find_all("li", {
                "class": "col-12 d-flex width-full py-4 border-bottom color-border-muted public source"}) + repo.find_all(
                "li", {"class": "col-12 d-flex width-full py-4 border-bottom color-border-muted public fork"})

            # temp=repo.find_all("li", {"class": "col-12 d-flex width-full py-4 border-bottom color-border-muted public fork"})
            # a_repo.append()
            for repoN in a_repo:
                name = repoN.find_all("h3", {"class": "wb-break-all"})
                for link in name:
                    l = link.find_all("a", {"itemprop": "name codeRepository"})
                    for r in l:
                        names.append(r.text)
                        url2 = str(r.get("href"))
                        urls.append("https://github.com/" + url2)

                        web_url = requests.get("https://github.com/" + url2)
                        result = web_url.content
                        soup = BeautifulSoup(result, "lxml")
                        sta = soup.find_all("span", {"id": "repo-stars-counter-star"})
                        for rs in range(len(sta)):
                            stars.append(sta[rs].text)

                        fok = soup.find_all("span", {"id": "repo-network-counter"})
                        for fo in range(len(fok)):
                            forks.append(fok[fo].text)

                        iss = soup.find("span", {"id": "issues-repo-tab-count"})

                        if iss is not None:
                            issues.append(iss.text)
                        else:
                            issues.append('0')

        repo_info = [names, urls, stars, forks, issues]
        export_file = zip_longest(*repo_info)
        with open("C:/Users/future/PycharmProjects/Network_project/repos.csv", "w") as myfile:
            wr = csv.writer(myfile)
            wr.writerow(["Repositorie Name", "Repositorie URL", "Number Of Stars", "Number Of Forks", "Number Of Issues"])
            wr.writerows(export_file)

        div = soup.find('a', {'rel': 'n'})

        if div is not None:
            url = div.get('href')
            url = "https://github.com/" + url
        else:
            # if there is no next repository
            # page, then exit loop
            break

    for y in repo_info:
        print(y);


# Driver program
if __name__ == "__main__":
    openWebsite()