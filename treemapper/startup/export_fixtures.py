if __name__=="__main__":
	import webnotes, os, shutil
	webnotes.connect()
	
	from core.page.data_import_tool.data_import_tool import export_json, export_csv
	export_json("Website Settings", None, "app/startup/install_fixtures/website_settings.json")
	export_json("Style Settings", None, "app/startup/install_fixtures/style_settings.json")
	export_csv("Tree Species", "app/startup/install_fixtures/Tree_Species.csv")
	export_csv("Tree Family", "app/startup/install_fixtures/Tree_Family.csv")
	shutil.rmtree("app/startup/install_fixtures/files/tree_species")
	os.makedirs("app/startup/install_fixtures/files/tree_species")
	os.system("cp -R public/files/tree_species app/startup/install_fixtures/files")
