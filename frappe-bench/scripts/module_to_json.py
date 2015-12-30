import argparse

def module_to_json(module_path, indent=None, keys=None):
	import imp
	import json
	module = imp.load_source('tempmod', module_path)
	json_keys = [x for x in dir(module) if not x.startswith('_')]
	if keys:
		json_keys = [x for x in json_keys if x in keys]
	if 'unicode_literals' in json_keys:
		json_keys.remove('unicode_literals')
	module = {x:getattr(module, x) for x in json_keys}
	return json.dumps(module, indent=indent)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('path')
	parser.add_argument('--indent', nargs='?', type=int, default=4)
	args = parser.parse_args()
	print module_to_json(args.path, indent=args.indent)
