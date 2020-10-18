import os
import subprocess
from sys import path

from pip._vendor import requests


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


def getname(url):
    debut = url.rindex("/")
    fin = url.rindex(".git")
    return url[debut + 1:fin]


def updateAllBranches(rep, url):
    os.chdir(rep)
    tab = ["git", "branch", "--all"]
    result = subprocess.run(tab, stdout=subprocess.PIPE)
    print("res=", result)
    print("The exit code was: %d" % result.returncode)
    if result.returncode != 0:
        raise Error(f"Le branch all a plante pour {rep} (url={url})")
    s = result.stdout.decode('utf-8')
    print("res=", s)
    lines = s.splitlines()
    print("res lines=", lines)
    lines2 = []
    for line in lines:
        line02=line.strip()
        if(line02.startswith('*')):
            line02=line02[1:]
            line02 = line02.strip()
        lines2.append(line02)
    for line in lines2:
        s2 = line
        if s2.find('->') != -1 and s2.find('HEAD') != -1:
            pass
        elif s2.find('remotes/origin') != -1:
            print('branch', s2)
            s3 = s2
            begin = "remotes/origin/"
            if s3.startswith(begin):
                s3 = s3[len(begin):]
            brancheExisteDeja = False
            if s3 in lines2 or s3 == 'master':
                print(f"la branche {s3} existe déjà en local")
                pass
            else:
                # tab2 = ["git", "branch", "--track", s2, s3]
                tab2 = ["git", "branch", s3]
                print('branch tab', tab2)
                result2 = subprocess.run(tab2)
                if result2.returncode != 0:
                    raise Error(f"Le branch track a plante pour {rep} {s2} (url={url})")
            print('fetch', s2)
            tab3 = ["git", "fetch", "--all"]
            print('fetch tab', tab3)
            result3 = subprocess.run(tab3)
            if result3.returncode != 0:
                raise Error(f"Le fetch a plante pour {rep} {s2} (url={url})")


def updateGit(rep_racine, url):
    name = getname(url)

    rep = rep_racine + name

    if (os.path.exists(rep)):
        print("pull", rep)
        tab = ["git", "-C", rep, "pull", "--all"]
        print("exec", tab)
        list_files = subprocess.run(tab)
        print("The exit code was: %d" % list_files.returncode)
        if list_files.returncode != 0:
            raise Error(f"Le pull a plante pour {rep} (url={url})")
    else:
        print("clone", url, rep)
        # mirror fait un repository baremetal qui ne fonctionne pas correctement
        # tab = ["git", "clone", "--mirror", url, rep]
        tab = ["git", "clone", url, rep]
        print("exec", tab)
        list_files = subprocess.run(tab)
        print("The exit code was: %d" % list_files.returncode)
        if list_files.returncode != 0:
            raise Error(f"Le clone a plante pour {rep} (url={url})")

    updateAllBranches(rep, url)

    print('fin')
