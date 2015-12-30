#! /bin/bash
set -e

add_mariadb_repo() {
	echo "
# MariaDB 5.5 CentOS repository list - created 2014-06-06 06:02 UTC
# http://mariadb.org/mariadb/repositories/
[mariadb]
name = MariaDB
baseurl = http://yum.mariadb.org/5.5/centos6-amd64
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1
" > /etc/yum.repos.d/mariadb.repo
}

read_msq_password() {
	echo Enter mysql root password to set:
	read -s MSQ_PASS
	export $MSQ_PASS
}

add_ius_repo() {
# HARDCODED!!!
	wget http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/epel-release-6-5.noarch.rpm
	wget http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-11.ius.centos6.noarch.rpm
	rpm -Uvh epel-release-6-5.noarch.rpm
	rpm -Uvh ius-release-1.0-11.ius.centos6.noarch.rpm
}

install_packages() {
	yum groupinstall -y "Development tools"
	yum install -y sudo yum install MariaDB-server MariaDB-client MariaDB-compat python-setuptools nginx zlib-devel bzip2-devel openssl-devel memcached postfix python27-devel python27 libxml2 libxml2-devel libxslt libxslt-devel redis MariaDB-devel
	useradd -m -d /home/erpnext -s $SHELL erpnext
	chmod o+x /home/erpnext
	chmod o+r /home/erpnext
	wget http://downloads.sourceforge.net/project/wkhtmltopdf/0.12.1/wkhtmltox-0.12.1_linux-centos6-amd64.rpm
	rpm -Uvh wkhtmltox-0.12.1_linux-centos6-amd64.rpm
}

install_erpnext() {
	su erpnext -c "cd /home/erpnext && git clone https://github.com/frappe/frappe-bench"
	su erpnext -c "cd /home/erpnext/frappe-bench && ./scripts/install.sh single"
	su erpnext -c "touch /home/erpnext/frappe-bench/.run_post_update"
}

add_backup_crontab() {
	su erpnext -c "echo \"`crontab -l`\" | uniq | sed -e \"a0 */6 * * * cd /home/erpnext/frappe-bench/sites &&  /home/erpnext/frappe-bench/env/bin/frappe --backup all\" | crontab"
}

install_supervisor() {
	easy_install supervisor
	curl https://raw.githubusercontent.com/pdvyas/supervisor-initscripts/master/redhat-init-jkoppe > /etc/init.d/supervisord
	curl https://raw.githubusercontent.com/pdvyas/supervisor-initscripts/master/redhat-sysconfig-jkoppe > /etc/sysconfig/supervisord
	curl https://raw.githubusercontent.com/pdvyas/supervisor-initscripts/master/supervisord.conf > /etc/supervisord.conf
	mkdir /etc/supervisor.d
	chmod +x /etc/init.d/supervisord
	bash -c "service supervisord start || true"
}

start_services() {
	service mysql start
	service redis start
	service postfix start
	service nginx start
	service memcached start
}

configure_services() {
	chkconfig --add supervisord 
	chkconfig redis on
	chkconfig mysql on
	chkconfig nginx on
	chkconfig supervisord on
	echo "erpnext ALL=(ALL) NOPASSWD: /usr/bin/supervisorctl restart frappe\:" > /etc/sudoers.d/erpnext
}

configure_mysql() {
	mysqladmin -u root password $MSQ_PASS
}

link_config() {
	ln -s  /home/erpnext/frappe-bench/config/nginx.conf /etc/nginx/conf.d/frappe.conf
	ln -s  /home/erpnext/frappe-bench/config/supervisor.conf /etc/supervisor.d/frappe.conf
	rm /etc/nginx/conf.d/default.conf
}

reload_config() {
	supervisorctl reload
	service nginx reload
}

read_msq_password
yum install wget -y
add_ius_repo
add_mariadb_repo
install_packages
start_services
configure_mysql
install_erpnext
install_supervisor
add_backup_crontab
configure_services
link_config
reload_config
