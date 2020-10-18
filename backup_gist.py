import os
from pathlib import Path

import requests
import sys
from subprocess import call

import git_utils


def backup_gist(rep_destination, user):

    rep_racine=rep_destination+f"/gist_{user}/"
    Path(rep_racine).mkdir(parents=True, exist_ok=True)

    r = requests.get('https://api.github.com/users/{0}/gists'.format(user))

    for i in r.json():
        #call(['git', 'clone', i['git_pull_url']])

        git_utils.updateGit(rep_racine, i['git_pull_url'])

        description_file = rep_racine+'/{0}/description.txt'.format(i['id'])
        print("ecriture dans ",description_file)
        print("json", i)
        with open(description_file, 'w') as f:
            f.write('{0}\n'.format(i['description']))
