#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}"

if ! docker network inspect eosio-exporters >/dev/null 2>&1; then
  docker network create eosio-exporters || exit 1
fi

docker run -d --rm --name bpvalidate-wax --network eosio-exporters bpvalidate-wax
docker run -d --rm --name bpvalidate-waxtest --network eosio-exporters bpvalidate-waxtest
