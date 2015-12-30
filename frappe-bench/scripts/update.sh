#!/usr/bin/env bash

set -e

if [[ -f .update_bench ]]
then
	git pull
fi

for app in apps/*
do
	cd $app
	echo updating $app
	git pull --rebase upstream HEAD
	cd -
done

source ./env/bin/activate
frappe --latest all --sites_path sites
frappe --build --sites_path sites


if [[ -f .run_post_update && -f scripts/post_update.sh ]]
then
	scripts/post_update.sh
else
	echo "Please restart all processes"
fi

