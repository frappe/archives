#!/usr/bin/env bash

set -e

python2.7 ./scripts/virtualenv.py env

SITES_PATH='sites'
ENV_PATH='env'

# args

CMD=$1
SINGLE_SITE_NAME=$2
DB_NAME=$3

SITE_PATH=$2

if [ -z "$SINGLE_SITE_NAME" ]
then
   SINGLE_SITE_NAME="erpnext.`hostname`"
fi

if [ -z "$DB_NAME" ]
then
   DB_NAME="erpnext"
fi

#commands

if [[ $CMD = "single" ]]
then
    . ./env/bin/activate
    frappe --install $DB_NAME $SINGLE_SITE_NAME --sites_path $SITES_PATH
    cat sites/apps.txt | xargs -n1 -I {} frappe --install_app {} $SINGLE_SITE_NAME --sites_path $SITES_PATH
    frappe --build  $SINGLE_SITE_NAME --sites_path $SITES_PATH
    echo please run "\``which frappe` --serve $SINGLE_SITE_NAME --sites_path `pwd`/$SITES_PATH\`" to start erpnext
    frappe --use $SINGLE_SITE_NAME --sites_path $SITES_PATH
	python scripts/generate_config.py
    deactivate
fi


if [[ $CMD = "migrate_3_to_4" ]]
then
    if [[ -z $SITE_PATH ]]
    then
        echo 'Please provide site path'
        exit 1
    fi

    site=`basename $SITE_PATH`

    if [[ -d $SITES_PATH/$site ]]
    then
        echo site $site already exists
        exit 1
    fi

    mkdir $SITES_PATH/$site

    . ./env/bin/activate
    if [[ -d $SITE_PATH/public ]]
    then
        cp -r $SITE_PATH/public $SITES_PATH/$site/public
    fi

    if [[ -f $SITE_PATH/conf.py ]]
    then
        python scripts/module_to_json.py $SITE_PATH/conf.py > $SITES_PATH/$site/site_config.json
    fi

    if [[ -f $SITE_PATH/site_config.json ]]
    then
        cp $SITE_PATH/site_config.json $SITES_PATH/$site/site_config.json
    fi

    frappe --build --sites_path $SITES_PATH
    python scripts/3to4.py $site
    frappe --use $SINGLE_SITE_NAME --sites_path $SITES_PATH
	python scripts/generate_config.py
    echo please run "`which frappe` --serve $site --sites_path `pwd`/$SITES_PATH" to start erpnext
fi
