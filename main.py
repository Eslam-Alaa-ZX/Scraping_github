import requests
import csv
from itertools import zip_longest
from bs4 import BeautifulSoup
import re


def repoScraping():
    username = str(input("Enter GitHub username: "))
    repoInfo = []
    names = []
    urls = []
    stars = []
    forks = []
    issues = []

    url = "https://github.com/" + username + "?tab=repositories"

    while True:

        getWeb = requests.get(url)
        webContent = getWeb.content
        soup = BeautifulSoup(webContent, "lxml")
        listOfRipo = soup.find_all("ul", {"data-filterable-for": "your-repos-filter"})

        for listItem in listOfRipo:
            repo = listItem.find_all("li", {
                "class": re.compile("^col-12 d-flex width-full py-4 border-bottom color-border-muted public")})
            for repoTitel in repo:
                repoName = repoTitel.find_all("h3", {"class": "wb-break-all"})
                for link in repoName:
                    repoUrl = link.find_all("a", {"itemprop": "name codeRepository"})
                    for repoUrlInfo in repoUrl:
                        names.append((""+repoUrlInfo.text).replace("\n        ",""))
                        repoPageUrl = str(repoUrlInfo.get("href"))
                        urls.append("https://github.com/" + repoPageUrl)

                        getWeb = requests.get("https://github.com/" + repoPageUrl)
                        webContent = getWeb.content
                        soup = BeautifulSoup(webContent, "lxml")

                        star = soup.find_all("span", {"id": "repo-stars-counter-star"})
                        for starInfo in range(len(star)):
                            stars.append(star[starInfo].text)

                        fork = soup.find_all("span", {"id": "repo-network-counter"})
                        for forkInfo in range(len(fork)):
                            forks.append(fork[forkInfo].text)

                        issue = soup.find("span", {"id": "issues-repo-tab-count"})
                        if issue is not None:
                            issues.append(issue.text)
                        else:
                            issues.append('0')

        repoInfo = [names, urls, stars, forks, issues]
        summaryFile = zip_longest(*repoInfo)
        with open("repos.csv", "w") as file:
            write = csv.writer(file)
            write.writerow(
                ["Repositorie Name", "Repositorie URL", "Number Of Stars", "Number Of Forks", "Number Of Issues"])
            write.writerows(summaryFile)

        getWeb = requests.get(url)
        webContent = getWeb.content
        soup = BeautifulSoup(webContent, "lxml")
        nextPage = soup.find_all('div', {'class':'paginate-container'})
        if(len(nextPage)==0):
          break
        nextPageCheck = nextPage[0]
        for nextPageInfo in nextPage:
            nextPageUrl = nextPageInfo.find_all('a', {'rel': 'nofollow'})
            for nextPageUrlInfo in nextPageUrl:
                if nextPageUrlInfo.text == "Next":
                    nextPageCheck = nextPageUrlInfo
                else:
                    nextPageCheck = None

        if nextPageCheck is not None:
            url = nextPageCheck.get('href')
        else:
            break

    for completRepoInfo in repoInfo:
        print(completRepoInfo)




repoScraping()