## Warning: Deprecated

Please use the new [Frappe Bench](https://github.com/frappe/bench)

---

## Frappe bench (Archived)

This repository helps you setup an isolated environment (bench) to run and
develop ERPNext. A virtualenv is installed in the env directory. You can
activate it by running `source ./env/bin/activate` or use execute using
absolute/relative path (eg, `./env/bin/frappe`).

#### Pre requisites

* Add MariaDB repository from https://downloads.mariadb.org/mariadb/repositories/

* Install packages
```
sudo apt-get install python-dev build-essential python-mysqldb git memcached ntp vim screen htop mariadb-server mariadb-common libmariadbclient-dev  libxslt1.1 libxslt1-dev redis-server libssl-dev libcrypto++-dev postfix
```

#### Usage

Note: Please do not run the following commands as root.

```
git clone https://github.com/frappe/frappe-bench
cd frappe-bench
./scripts/install.sh single [sitename [dbname]]
```

#### Migrating from ERPNext version 3

Make sure that you have updated your site for the latest version of 3.x.x and take a database backup.
```
git clone https://github.com/frappe/frappe-bench
cd frappe-bench
./scripts/install.sh migrate_3_to_4 /path/to/old/erpnext
```

### Development
```
./env/bin/honcho start
```

### Default Login

username: Administrator

password: admin

Please change this once you complete setup.

### Updating

```
./scripts/update.sh
```

### Production Deployment
* Install nginx and supervisor
* `cp config/nginx.conf /etc/nginx/conf.d/frappe.conf`
* `cp config/supervisor.conf /etc/supervisor/conf.d/frappe.conf`
