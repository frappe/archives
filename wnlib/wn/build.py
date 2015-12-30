"""
build client app

1. builds 4 files
  - app.js
  - web.js
  - app.css 
  - web.css

2. Makes pages (views) from view.html template

3. Makes other pages from database

Setup file bundle in conf.py
"""

import sys
sys.path.append('lib')
sys.path.append('controllers')

import wn, os, conf, shutil, codecs
from itertools import chain
from jinja2 import Template
from wn.translate import _

def build():
	make_folders()
	build_app()
	copy_files()
	for lang in conf.languages:
		print 'building for %s...' % lang
		langdir = os.path.join('public', lang)
		if not os.path.exists(langdir):
			os.makedirs(langdir)
		symlink_common_folders(lang)
		copy_core_app(lang)
		make_views(lang)
	
def make_folders():
	"""make public folders"""
	def make(folder):
		if not os.path.exists(folder):
			os.makedirs(folder)
		
	make('public/common/js')
	make('public/common/css')
	make('public/common/img')
	make('public/common/files')

	# symlink client libs
	if not os.path.exists('public/common/js/lib'):
		os.symlink(os.path.abspath('lib/client'), 'public/common/js/lib')
				
def build_app():
	"""build files from conf"""
	from wn.utils.jsmin import minify
	for fpath in conf.build:
			outfile = u""
			for srcpath in conf.build[fpath]:
				with codecs.open(srcpath, "r", "utf-8") as src:
					outfile += '/*\n%s\n*/\n' % srcpath
					if fpath.endswith('.js') and (not '.min.' in srcpath):
						fcontent = minify(src.read())
					else:
						fcontent = src.read()
					
					try:
						outfile += unicode(fcontent)
					except UnicodeDecodeError, e:
						position = int(str(e).split('position')[-1].split(':')[0].strip())
						print 'Cannot decode in file %s: position %s' % (srcpath, position)
						print
						print fcontent[position-10:position+10]
						print
						print '--------------------------------------'
						raise e
						
					if fpath.endswith('.js'):
						# add missing semicolon
						if outfile.strip()[-1]!=';':
							outfile += ';\n'
						else:
							outfile += '\n'
							
			outpath = os.path.join('public', 'common', fpath)
			outfile = outfile.encode('utf-8')
			
			with open(outpath, 'w') as tarfile:
				tarfile.write(outfile)
				print "wrote %s %sk" % (outpath, str(int(float(len(outfile))/1024)))

def translate(content, lang):
	return unicode(Template(content).render(_=_, lang=lang)).encode('utf-8')
	
def copy_files():
	"""copy image and other files"""
	for src in conf.copy_files:
		shutil.copyfile(src, os.path.join('public', 'common', conf.copy_files[src]))
		
def copy_core_app(lang):
	"""copy server.cgi"""
	shutil.copyfile(os.path.join('lib', 'files', 'server.cgi'), 
		os.path.join('public', lang, 'server.cgi'))
	os.system('chmod a+x %s' % os.path.join('public', lang, 'server.cgi'))
		

def symlink_common_folders(lang):
	"""symlink js/css/img/files folders for each language"""
	for f in ('js', 'css', 'img', 'files'):
		if not os.path.exists(os.path.join('public', lang, f)):
			os.symlink(os.path.abspath(os.path.join('public', 'common', f)), 
				os.path.join('public', lang, f))
	
def make_views(lang):
	"""make view html files from `views` and `lib/views` folders"""
	
	wn.lang = lang

	def write_public_file(fname, content):
		with open(os.path.join('public', lang, fname), 'w') as viewfile:
			viewfile.write(translate(content, lang))
			
	if os.path.exists(os.path.join('views', 'template.html')):	
		with open('views/template.html', 'r') as templatefile:
			template = Template(templatefile.read())
	else:
		with open('lib/views/template.html', 'r') as templatefile:
			template = Template(templatefile.read())
		
	for wt in chain(os.walk('lib/views'), os.walk('views')):
		for fname in filter(lambda n: n.endswith('.html'), wt[2]):

			# ignore template.html
			if fname == 'template.html': 
				continue
				
			with open(os.path.join(wt[0], fname), 'r') as viewfile:
				content = viewfile.read()
				
			# if starts with <!-- content -->
			# then put in in views/template.html
			if content.startswith('<!-- public'):
				write_public_file(fname, unicode(template.render(content=content, _=_, lang=lang)))
											
				# write private file also
				if content.startswith('<!-- public+private'):
					write_public_file('_' + fname, content)

			else:
				write_public_file(fname, content)

if __name__=='__main__':
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option('-w', '--watch',help="Watch: Watch files and rebuild if updated.", nargs=0)
	options, args = parser.parse_args()
	
	if options.watch is not None:
		from itertools import chain
		import os, time
		files = {}
		while True:
			do_build = False
			for wt in chain(os.walk('./views'), os.walk('./lib/client/wn'), os.walk('./lib/views')):
				for fname in wt[2]:
					fpath = os.path.join(wt[0], fname)
					mtime = os.path.getmtime(fpath)
					if mtime != files.get(fpath):
						files[fpath] = mtime
						do_build = True
			if do_build:
				build()
			time.sleep(2)
	else:
		build()	
