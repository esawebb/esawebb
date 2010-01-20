filename = "/Volumes/webdocs/spacetelescope/docs/images/index.html"
f = open( filename )
s = f.read()
f.close()

import re
import xml.dom.minidom

def extract( s, p, group=1 ):
	m = p.search( s, re.MULTILINE)
	print m
	if m:
		return m.group(group)
	else:
		return None

sectionp = re.compile( '<!-- InstanceParam name="SelectedSection" type="text" value="([a-z]+)" -->')
titlep = re.compile("<title>(.+)</title>", re.MULTILINE)
contentp = re.compile('<!-- InstanceBeginEditable name="ContentArea" -->(.+)<!-- InstanceEndEditable -->', re.MULTILINE )
pagecontentp = re.compile('<!-- InstanceBeginEditable name="PageContent" -->(.+)<!-- InstanceEndEditable -->', re.MULTILINE )
headlinep = re.compile( '!-- InstanceBeginEditable name="Headline" -->(.+)<!-- InstanceEndEditable -->', re.MULTILINE )


#<!-- InstanceBeginEditable name="PageContent" -->' )


data = {
	'section' : extract(s,sectionp),
	'title' : extract(s,titlep),
	'content' : extract(s,contentp),
	'headline' : extract(s,headlinep),
	'pagecontent' : extract(s,pagecontentp),
	}

import pprint
pprint.pprint(data)



print xml.dom.minidom.parse(filename)
