#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export $(cat ${DIR}/variables.env | xargs)
source /usr/local/bin/tc_variables.sh

venvdir="${venvDirectory}/${DJANGO_APP_NAME}_venv"
source "${venvdir}/bin/activate"

pip install -r "${DIR}/requirements.txt"

_int() {
    for job in `jobs -p`
    do
        kill -TERM "$job" 2>/dev/null
    done

    exit 130
}

_term() {
    for job in `jobs -p`
    do
        kill -TERM "$job" 2>/dev/null
    done
    exit 0
}

trap _int SIGINT
trap _term SIGTERM

FAIL=0
export PYTHONPATH=${DIR}

python -m application.manage makemigrations
python -m application.manage migrate
mkdir -p "${DIR}/static"
mkdir -p "${DIR}/medias"
python -m application.manage collectstatic --clear --no-input

if [[ "$#" -gt 0 ]] && [[ "$1" == "loadexampledata" ]]
then
    fileList=$(find "${DIR}/fixtures/" -name *.json -printf "%f")
    for file in ${fileList}; do
        python -m application.manage loaddata "${DIR}/fixtures/${file}"
    done
fi

python -m application.manage runserver 0.0.0.0:${WEBSERVER_PORT} &
python -m application.asyncmsg.main &

for job in `jobs -p`
do
    wait ${job} || let "FAIL+=1"
done

if [[ "$FAIL" == "0" ]];
then
    exit 0
else
    exit 1
fi