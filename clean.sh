#!/bin/bash

starting_dir="${PWD}"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}"

./stop.sh

docker rmi bpvalidate-wax
docker rmi bpvalidate-waxtest
docker rmi python:3.9

cd "${starting_dir}"

exit 0
