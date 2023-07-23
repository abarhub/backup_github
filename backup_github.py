import datetime
import json
import os
import subprocess
from pathlib import Path
from sys import path
from os import listdir
from os.path import isfile, join, isdir

from pip._vendor import requests

import git_utils

# from git import Repo

# from pydriller import RepositoryMining

# class Error(Exception):
#     """Base class for exceptions in this module."""
#     pass


def getListeRepo(user, rep_destination):
    no_page=1
    list_url = []
    dateCourante = datetime.datetime.now().timestamp()

    while True:
        print(f'page={no_page}')
        url=f"https://api.github.com/users/{user}/repos?per_page=100&page={no_page}"
        print(f'url={url}')
        response = requests.get(url)

        value_jon=response.json()
        if no_page==1 or len(value_jon)>0:

            rep_destination2 = rep_destination + '/github_metadata'
            Path(rep_destination2).mkdir(parents=True, exist_ok=True)
            # print(response.content)
            # print(response.json())
            val = rep_destination2 + '/github_meta_{0}_{1}.json'.format(int(dateCourante * 1000), no_page)
            with open(val, 'w') as f:
                json_data = json.loads(response.text)
                f.write(json.dumps(json_data, indent=4))
            print('enregistrement du fichier {0}'.format(val))

            contenu = response.text

            for repo in response.json():
                # print('repo:',repo)
                # print('clone:',repo['clone_url'])
                if repo['clone_url']:
                    list_url.append(repo['clone_url'])
        else:
            break

        no_page=no_page+1


    print("nb:", len(list_url))
    print("liste:", list_url)
    return (contenu, list_url)


def enregistre_starred(user, rep_destination, dateCourante):

    no_page=1

    while True:
        url_starred = f"https://api.github.com/users/{user}/starred?per_page=100&page={no_page}"

        rep_destination2 = rep_destination + '/starred'
        Path(rep_destination2).mkdir(parents=True, exist_ok=True)
        print(f'url_starred={url_starred}')
        response = requests.get(url_starred)

        if len(response.json())>0:
            val = rep_destination2 + '/starred_{0}_{1}.json'.format(int(dateCourante * 1000), no_page)
            with open(val, 'w') as f:
                json_data = json.loads(response.text)
                f.write(json.dumps(json_data, indent=4))
            print('enregistrement du fichier {0}'.format(val))
        else:
            break
        no_page=no_page+1


def enregistre_info_user(user, rep_destination):
    dateCourante = datetime.datetime.now().timestamp()
    url = f"https://api.github.com/users/{user}"
    print(f'url={url}')
    response = requests.get(url)

    rep_destination2 = rep_destination + '/github_user'
    Path(rep_destination2).mkdir(parents=True, exist_ok=True)

    val = rep_destination2 + '/github_user_{0}.json'.format(int(dateCourante * 1000))
    with open(val, 'w') as f:
        json_data = json.loads(response.text)
        f.write(json.dumps(json_data, indent=4))
    print('enregistrement du fichier {0}'.format(val))

    enregistre_starred(user, rep_destination2, dateCourante)

def affiche_difference_repo(liste,rep_racine):

    liste_projet_github=[]

    for url in liste:
        debut = url.rindex("/")
        fin = url.rindex(".git")
        liste_projet_github.append(url[debut + 1:fin])

    liste_projet_github.sort()

    print(f"liste projets github : {liste_projet_github}")

    onlydir = [f for f in listdir(rep_racine) if isdir(join(rep_racine, f))]

    onlydir.sort()

    print(f"liste projets local : {onlydir}")

    trop_github=list(set(liste_projet_github) - set(onlydir))
    print(f"liste en trop sur github : {trop_github}")


    trop_local=list(set(onlydir) - set(liste_projet_github))
    print(f"liste en trop en local : {trop_local}")



def backup_github(rep_destination, user):
    print("coucou")

    enregistre_info_user(user,rep_destination)

    contenu, liste = getListeRepo(user, rep_destination)

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

    # affiche les projets qui sont en trop soit sur github, soit en local
    affiche_difference_repo(liste,rep_racine)

    for url_repo in liste:
        print("update", url_repo, "...")
        git_utils.updateGit(rep_racine, url_repo)
        print("update", url_repo, "OK")

