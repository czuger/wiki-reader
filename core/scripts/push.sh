#!/bin/sh

cd "$1" || exit

pwd
scp "$2" "$3"/