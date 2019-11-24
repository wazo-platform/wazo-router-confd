#!/bin/sh
date
if ! [ -z "$POSTGRES_URI" ]; then
    wait-for -t 60 $POSTGRES_URI
fi
if ! [ -z "$CONSUL_URI" ]; then
    wait-for -t 60 $CONSUL_URI
    sleep 2
fi

exec $@
