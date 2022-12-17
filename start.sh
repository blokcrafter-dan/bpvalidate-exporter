#!/bin/bash

starting_dir="${PWD}"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}"

if [ -z "$(docker images -q bpvalidate-wax:latest)" ] || [ -z "$(docker images -q bpvalidate-waxtest:latest)" ]; then
  ./build.sh
fi
if [ -z "$(docker ps | grep bpvalidate-wax)" ] || [ -z "$(docker ps | grep bpvalidate-waxtest)" ]; then
  ./run.sh
fi

cd "${starting_dir}"

exit 0
