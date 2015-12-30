#! /bin/bash 
set -e

sudo apt-get update

# Add mariadb repos
sudo apt-get install software-properties-common -y
sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xcbcb082a1bb943db
sudo add-apt-repository 'deb http://download.nus.edu.sg/mirror/mariadb/repo/5.5/ubuntu trusty main'

sudo apt-get update

# install system deps
sudo apt-get install python-dev build-essential python-mysqldb git memcached ntp vim screen htop mariadb-server mariadb-common libmariadbclient-dev  libxslt1.1 libxslt1-dev redis-server libssl-dev libcrypto++-dev postfix supervisor nginx -y
useradd -m -d /home/erpnext -s $SHELL erpnext

su erpnext -c "cd /home/erpnext && git clone https://github.com/frappe/frappe-bench"
su erpnext -c "cd /home/erpnext/frappe-bench && ./scripts/install.sh single"
su erpnext -c "touch /home/erpnext/frappe-bench/.run_post_update"

sudo ln -s  /home/erpnext/frappe-bench/config/nginx.conf /etc/nginx/conf.d/frappe.conf
sudo ln -s  /home/erpnext/frappe-bench/config/supervisor.conf /etc/supervisor/conf.d/frappe.conf

if [[ -e /etc/nginx/sites-enabled && -e /etc/nginx/sites-enabled/default ]] 
then
    unlink /etc/nginx/sites-enabled/default
fi

sudo service nginx restart
sudo service supervisor restart
