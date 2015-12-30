#! env python

import os
import getpass
from jinja2 import Environment, FileSystemLoader
loader = FileSystemLoader(os.getcwd())
env = Environment(loader=loader, trim_blocks=True)


def generate_config(application, template_name):
	template = env.get_template(template_name)
	bench_dir = os.getcwd()
	sites_dir = os.path.join(bench_dir, "sites")
	user = getpass.getuser()
	with open("sites/currentsite.txt") as f:
		site = f.read().strip()

	config = template.render(**{
		"bench_dir": bench_dir,
		"sites_dir": sites_dir,
		"user": user,
		"site": site
	})
	with open("config/{}.conf".format(application), 'w') as f:
		f.write(config)

if __name__ == "__main__":
	generate_config('supervisor', 'templates/supervisor.conf')
	generate_config('nginx', 'templates/nginx.conf')
	
