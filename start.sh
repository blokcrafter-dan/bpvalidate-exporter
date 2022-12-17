#!/bin/bash

starting_dir="${PWD}"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}"

if [ -z "$(docker images -q bpvalidate-exporter:latest)" ]; then
  ./build.sh
fi
if [ -z "$(docker ps | grep bpvalidate-exporter)" ]; then
  ./run.sh
fi

cd "${starting_dir}"

exit 0
