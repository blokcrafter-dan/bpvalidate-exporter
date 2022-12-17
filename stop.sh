#!/bin/bash

starting_dir="${PWD}"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}"

if [ -n "$(docker ps | grep bpvalidate-wax)" ]; then
  docker stop bpvalidate-wax
fi
if [ -n "$(docker ps | grep bpvalidate-waxtest)" ]; then
  docker stop bpvalidate-waxtest
fi

cd "${starting_dir}"

exit 0
