#!/bin/bash

set -e

error(){
    echo "ERREUR : paramètres invalides !" >&2
    echo "Usage : create_fixtures.sh NOM_DE_LA_FIXTURE" >&2
    exit 1
}

[[ $# -ne 1 ]] && error


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export $(cat ${DIR}/variables.env | xargs)
source /usr/local/bin/tc_variables.sh

venvdir="${venvDirectory}/${DJANGO_APP_NAME}_venv"
source "${venvdir}/bin/activate"

pip install -r "${DIR}/requirements.txt"

export PYTHONPATH=${DIR}
python -m application.manage dumpdata | sed '/^ \[x\] /d' > "${DIR}/fixtures/${1}.json"

echo "La fixture a été créé à l'endroit suivant : ${DIR}/fixtures/${1}.json"
exit 0