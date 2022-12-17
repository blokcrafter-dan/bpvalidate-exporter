#!/bin/bash

starting_dir="${PWD}"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}"

if [ -n "$(docker ps | grep bpvalidate-exporter)" ]; then
  docker stop bpvalidate-exporter
fi

cd "${starting_dir}"

exit 0
