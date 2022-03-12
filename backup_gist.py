import datetime
import json
import os
from pathlib import Path

import requests
import sys
from subprocess import call

import git_utils


def backup_gist(rep_destination, user):
    rep_racine = rep_destination + f"/gist_{user}/"
    Path(rep_racine).mkdir(parents=True, exist_ok=True)

    dateCourante = datetime.datetime.now().timestamp()
    rep = rep_racine + '/json_meta'
    Path(rep).mkdir(parents=True, exist_ok=True)
    no = 1

    while True:
        print('page=',no)
        url = 'https://api.github.com/users/{0}/gists?page={1}'.format(user, no)
        print('url={0}'.format(url))
        r = requests.get(url)
        valeur_json = r.json()
        if no == 1 or len(valeur_json) > 0:

            val = rep + '/gist_meta_{0}_{1}.json'.format(int(dateCourante * 1000), no)
            with open(val, 'w') as f:
                json_data = json.loads(r.text)
                f.write(json.dumps(json_data, indent=4))
            print('enregistrement du fichier {0}'.format(val))

            for i in r.json():
                # call(['git', 'clone', i['git_pull_url']])

                git_utils.updateGit(rep_racine, i['git_pull_url'])

                description_file = rep_racine + '/{0}/description.txt'.format(i['id'])
                print("ecriture dans ", description_file)
                print("json", i)
                with open(description_file, 'w') as f:
                    f.write('{0}\n'.format(i['description']))
        else:
            break
        no = no + 1
