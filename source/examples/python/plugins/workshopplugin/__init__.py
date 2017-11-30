from workshop import Workshop

def name():
	return "name"
	
def description():
	return "beschreibung"
	
def qgisMiniumVersion():
	return "1.6"

def authorName():
	return "me"
	
def icon():
	return "icon1.png"

def classFactory(iface):
	return Workshop(iface)