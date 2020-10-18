import os
import subprocess
from sys import path

from pip._vendor import requests

import git_utils

# from git import Repo

# from pydriller import RepositoryMining

# class Error(Exception):
#     """Base class for exceptions in this module."""
#     pass


def getListeRepo(user):
    response = requests.get(f"https://api.github.com/users/{user}/repos?per_page=100")

    # print(response.content)
    # print(response.json())

    contenu = response.text

    list_url = []
    for repo in response.json():
        # print('repo:',repo)
        # print('clone:',repo['clone_url'])
        if repo['clone_url']:
            list_url.append(repo['clone_url'])

    print("nb:", len(list_url))
    print("liste:", list_url)
    return (contenu, list_url)



def backup_github(rep_destination, user):
    print("coucou")

    contenu, liste = getListeRepo(user)

    print("repos:", liste)

    os.system("echo Hello from the other side!")

    os.system("git --version")

    # rep_racine ="D:/backup/repo_github2/"
    # rep_racine = "D:/temp/test_git2/"
    rep_racine = rep_destination

    print(f"backup github vers le répertoire {rep_racine}")

    # os.system("git clone $url $rep")

    os.system(f"echo test {rep_racine}")

    # res=os.system(f"git clone {url} {rep}")

    # print(f"res={res}")

    for url_repo in liste:
        print("update", url_repo, "...")
        git_utils.updateGit(rep_racine, url_repo)
        print("update", url_repo, "OK")

