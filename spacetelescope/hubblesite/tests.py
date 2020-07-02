# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
import unittest
from django.core import mail
from avm import *
from utils import *
from django.test import TestCase
from django.conf import settings

#Tests for avm.py

class EmailTest(TestCase):
	def test_video_rename(self):
		data = load_json('spacetelescope/hubblesite/test_clients.json')
		self.assertEqual(data['clients'][0]['first name'], "Pepito")	

	@classmethod
	def setUpjsonmapper(cls):
		#Set up non-modified objects used by all test methods
		test_jm = jsonmapper()

	def test_strings2stringlist(self):
		test_jm = jsonmapper()
		test_string = "a,b,c;d,e,f"
		test_list = test_jm.strings2stringlist(test_string)
		self.assertEqual(test_list[0], "a")

	def test_semicolonstrings2stringlist(self):
		test_jm = jsonmapper()
		test_string = "a,b,c;d,e,f"
		test_list = test_jm.semicolonstrings2stringlist(test_string)
		self.assertEqual(test_list[0], "a,b,c")

	def test_listdistances(self):
		test_jm = jsonmapper()
		test_string = "z=c;e"
		test_list = test_jm.listdistances(test_string)
		self.assertEqual(test_list[1], "c")

	def test_replace_html(self):
		test_jm = jsonmapper()
		test_string = "test&gt;tost"
		test_list = test_jm.replace_html(test_string)
		self.assertEqual(test_list, "test>tost")

	def test_subjectcategories(self):
		test_jm = jsonmapper()
		test_string = "Xtest&gt;tost;test&gt;tost"
		test_list = test_jm.subjectcategories(test_string)
		self.assertEqual(test_list[0],u'test>tost')

	def test_cet_datetime(self):
		test_jm = jsonmapper()
		""" test conversion of local time to specific timezone """
		settings.TIME_ZONE = 'Europe/Berlin'

		est = datetime(2011, 3, 10, 12, 00 ) # Eastern Standard Time
		edt = datetime(2011, 3, 15, 12, 00 ) # Eastern Daylight Time
		cet = datetime(2011, 3, 24, 12, 00 ) # Central European Time
		cest = datetime(2011, 3, 30, 12, 00 ) # Central European Summer Time

		assert test_jm.cet_datetime(est).isoformat() == '2011-03-10T12:00:00+01:00'
		assert test_jm.cet_datetime(edt).isoformat() == '2011-03-15T12:00:00+01:00'
		assert test_jm.cet_datetime(cet).isoformat() == '2011-03-24T12:00:00+01:00'
		assert test_jm.cet_datetime(cest).isoformat() == '2011-03-30T12:00:00+02:00'
	
	def test_datestring2datetime(self):
		test_jm = jsonmapper()
		datestring = "2011-03-23"
		self.assertEqual(test_jm.datestring2datetime(datestring).isoformat(),"2011-03-23T05:00:00+01:00")


	def test_datetimestring2datetime(self):
		test_jm = jsonmapper()
		datestring = '2011-03-23 20:15:11'
		dt2d = test_jm.datetimestring2datetime(datestring)
		self.assertEqual(dt2d.isoformat(),'2011-03-24T01:15:11+01:00')

	def test_starttimes2datetimelist(self):
		test_jm = jsonmapper()
		starttimes = '2005-03-23;2007-06-14;2002-06-15;2002-06-14;2002-06-13;2002-06-12'
		st2dl = test_jm.starttimes2datetimelist(starttimes)
		self.assertEqual(st2dl[0].isoformat(),"2005-03-23T06:00:00+01:00")

	def test_string2coordinateframeCV(self):
		test_jm = jsonmapper()
		frameCV = test_jm.string2coordinateframeCV("icrs")
		frameCV2 = test_jm.string2coordinateframeCV("2tp")
		self.assertEqual(frameCV,"ICRS")
		self.assertEqual(frameCV2,None)
		
	def test_string2filetypeCV(self):
		test_jm = jsonmapper()
		frameCV = test_jm.string2filetypeCV("image/tiff")
		frameCV2 = test_jm.string2filetypeCV("toff")
		self.assertEqual(frameCV,"TIFF")
		self.assertEqual(frameCV2,None)		

	def test_string2spatialqualityCV(self):
		test_jm = jsonmapper()
		frameCV = test_jm.string2spatialqualityCV("Full")
		frameCV2 = test_jm.string2spatialqualityCV("toff")
		self.assertEqual(frameCV,"Full")
		self.assertEqual(frameCV2,{'Full': 'Full','Position': 'Position'})	

	def test_string2coordprojectionsCV(self):
		test_jm = jsonmapper()
		frameCV = test_jm.string2coordprojectionsCV("TAN")
		frameCV2 = test_jm.string2coordprojectionsCV("toff")
		self.assertEqual(frameCV,"TAN")
		CV = {'TAN': 'TAN',
              'SIN': 'SIN',
              'ARC': 'ARC',
              'AIT': 'AIT',
              'CAR': 'CAR',
              'CEA': 'CEA',
              }
		self.assertEqual(frameCV2,CV)

	#There are issues with this couple of tests
	"""
	def test_avmdict(self):
		test_jm = jsonmapper()
		avm = test_jm.avmdict()
	
	def test_remove_duplicates(self):
		json_data = None
		try:
			fp = open('/home/hubbleadm/spacetelescope/hubblesite/test_clients.json','r')
			json_data = remove_duplicates(fp)
			print(json_data)
			fp.close()
		except IOError, (errno, strerror):
			logger.error("I/O error(%s): %s" % (errno, strerror))
			logger.error("Problem opening file %s, returning None" % json_file )   

		
		print(json_data)
	"""	
#Tests for utils.py

class UtilsTest(TestCase):
	
	def test_get_url_content(self):
		url = "http://hubblesite.org/newscenter/archive/releases/2005/37/image/"
		a,b = get_url_content(url)
		self.assertEqual(b,"https://hubblesite.org/contents/news-releases/2005/news-2005-37.html")

	def test_remove_void(self):
		text = "Here is a jump \n and a tab \r and multiple space"
		test_text = remove_void(text)
		text2 = "Here is a jump and a tab and multiple space"
		self.assertEqual(test_text, text2)
