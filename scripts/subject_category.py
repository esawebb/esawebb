#
# -*- coding: utf-8 -*-
#
# eso.org
# Copyright 2011 ESO
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#
#
# Mantis ESO 3065, now for spacetelescope
# this time Video and Images are take care off in the same go
# Tag all images with subject category and remove temporary taxonomy items.
# 2011 Apr 18
#*************************************************************************************************************

import pprint

from djangoplicity.media.models import Image
from djangoplicity.media.models import ImageExposure


# do I need this TODO?
from djangoplicity.metadata.models import TaxonomyHierarchy
from djangoplicity.metadata.models import SubjectName

def show_taxonomy():
    print 'trying to find good matches for these locally used taxonomies with X'
    for xth in TaxonomyHierarchy.objects.filter(top_level = 'X'):
        print xth.avm_code(),';', xth.name
    print '--------------------------------------------------------------------------------------------'
    for xth in TaxonomyHierarchy.objects.filter(top_level = 'X'):
        level = 10
        for th in TaxonomyHierarchy.objects.exclude(top_level = 'X'):
            # first try to find the x.name in the taxonomy
            if th.name.find(xth.name) > -1: 
                if len(th.avm_code().split('.')) <= level:
                    level = len(th.avm_code().split('.'))
                    print level, xth.avm_code(), xth.name, '\t ; \t',th.name, th.avm_code()
                #break
            # split the localy used name and try to find its integredients
#            sloppy = -10
#            xths = xth.name.split()
#            n_words = len(xths)
#            matching = 0
#            splitter = ''    
#            if n_words > 1:
#                for splitter in xths:
#                    if th.name.find(splitter) > -1: 
#                        matching = matching + 1
#                    if matching >= n_words - sloppy:     
#                        print xth.avm_code(), xth.name, splitter, '\t; \t',th.name, th.avm_code()
#                        break            
#                
    return

def show_subjectnames():
    sns = SubjectName.objects.all()
    for sn in sns:
        print sn
    return

def analyse_taxonomy(generate_code = False):
    '''
    see which X.tags are used
    and generate sceleton for the code
    '''
    # 1 build dictionary
    X_Tags = {}


    for xth in TaxonomyHierarchy.objects.filter(top_level = 'X'):
        X_Tags[xth.avm_code()] = [xth.name,0]    
    #pprint.pprint(X_Tags) 
        
    for Img in Image.objects.all():#.filter(pk = 'eso9212d'):
        x_tag  = False
        n_tags = len(Img.subject_category.all()) 
        for sc in  Img.subject_category.all():
            if sc.top_level == 'X': x_tag = True
        if x_tag:
            [name, number] = X_Tags[sc.avm_code()]
            X_Tags[sc.avm_code()] = [name, number + 1]
            # print X_Tags[sc.avm_code()] 

    if generate_code:  
        keys = X_Tags.keys()
        keys.sort()
        for key in keys:
            print "    elif tag == '%s':" % key
            print "        # '%s' %d" % (X_Tags[key][0], X_Tags[key][1]) 
            print "        print object.id ,';', sc.name ,';', object.title.encode('utf-8'),';', object.distance"
        print '-----------------------'
    
    pprint.pprint(X_Tags) 
    return  


def scan_tags(object, name):
    found = False
    for sc in  object.subject_category.exclude(top_level = 'X'):
        if sc.name.find(name) > -1: found = True   
    return found

def get_toplevel(object):
    toplevel = None
    for sc in  object.subject_category.exclude(top_level = 'X'):
        toplevel = sc.top_level
        print toplevel,
    print   
    return toplevel


def print_tags(object):
    scs = object.subject_category.exclude(top_level = 'X')
#    if len(scs) > 0: print object.id,
    for sc in  scs:
        print sc.name,
    print
    return 

def print_alltags(object):
    scs = object.subject_category.all()
#    if len(scs) > 0: print object.id,
    for sc in  scs:
        print sc.name,
    print
    return 

def scan_subjectnames(object, name):
    found = False
    for sn in  object.subject_name.all():
        print sn, sn.name.find(name)
        if sn.name.find(name) > -1: found = True   
    return found

def treat_x(sc, object, remove = True): 
    tag = sc.avm_code()
    save_changes = False
    #    
    #A. Solar System: local to our Solar System 
    #Typical taxonomy types: 1-3, 7-8 
    #B. Milky Way: contained within the Milky Way Galaxy 
    #Typical taxonomy types: 1-4 
    #C. Local Universe: current era of the Universe (z <= 0.1) 
    #Typical taxonomy types: 3-5 
    #D. Early Universe: distant galaxies and cosmological epochs (z > 0.1) 
    #Typical taxonomy types: 5-6 
    #E. Unspecified: for generic instance of subject 
    #Typical taxonomy types: any 

    if tag == 'X.101.10':
        # 'Extrasolar Planets Videos' 1
        # not treated
        print object.id ,';', sc.name ,';', object.title.encode('utf-8'),';', object.distance, '; TAGS: ', print_alltags(object)
    elif tag == 'X.101.11':
        # 'JWST Images/Videos' 24
        # add subject_name JWST
        if not scan_subjectnames(object,'JWST'): 
            print 'add subject_name JWST to ', object.id
            new_name = SubjectName.objects.get(name = 'JWST')
            object.subject_name.add(new_name)
        # set image.type = 'Artwork'
        print object.id, sc.name,' set object.type = "Artwork" ;', object.title.encode('utf-8')
        object.type = 'Artwork'
        if remove: object.subject_category.remove(sc)
        save_changes = True
        
    elif tag == 'X.101.12':
        # 'Spacecraft Images/Videos' 20
        # replace with 8.2 Spacecraft 
        print object.id ,';', sc.name ,';', object.title.encode('utf-8'),';', object.distance, '; TAGS: ', print_alltags(object)
        if not scan_tags(object, 'Spacecraft'):
            new_tag = TaxonomyHierarchy.objects.get( top_level = 'E', level1 = 8, level2 = 2, level3 = None, level4 = None)
            print object.id, 'replace', sc.name, 'with', new_tag.avm_code(), new_tag.name, '; ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(new_tag)    
        if remove: object.subject_category.remove(sc)
        save_changes = True        

    elif tag == 'X.101.13':
        # 'Miscellaneous  Images/Videos' 165
        # remove tag
        print object.id ,';', sc.name ,';', object.title.encode('utf-8'),';', object.distance, '; TAGS: ', print_alltags(object)
        if remove: object.subject_category.remove(sc)
        save_changes = True     
    elif tag == 'X.101.21':
        # 'Illustration Images' 237
        print object.id ,';', sc.name ,';', object.title.encode('utf-8'),';', object.distance, object.type        
        # set type to artwork and remove tag
        print object.id, sc.name,' set object.type = "Artwork" ;', object.title.encode('utf-8')
        object.type = 'Artwork'
        if remove: object.subject_category.remove(sc)
        save_changes = True
        
    elif tag == 'X.101.22':
        # 'Mission' 132     E.8.1.2 Telescope, E.9.2 Astronaut, subject_name Hubble?
        # replace with 8.2 Spacecraft
        print object.id ,';', sc.name ,';', object.title.encode('utf-8'),';', object.distance, '; TAGS: ', print_alltags(object)
        if not scan_tags(object, 'Spacecraft'):
            new_tag = TaxonomyHierarchy.objects.get( top_level = 'E', level1 = 8, level2 = 2, level3 = None, level4 = None)
            print object.id, 'replace', sc.name, 'with', new_tag.avm_code(), new_tag.name, '; ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(new_tag)    
        if remove: object.subject_category.remove(sc)
        save_changes = True 
    
    elif tag == 'X.101.3':
        # 'Solar System Images/Videos' 577
        if not scan_tags(object, 'Solar System'):
            new_tag = TaxonomyHierarchy.objects.get( top_level = 'A', level1 = None)
            print object.id, 'replace', sc.name, 'with', new_tag.avm_code(), new_tag.name, '; ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(new_tag)    
        if remove: object.subject_category.remove(sc)
        save_changes = True        

    elif tag == 'X.101.4':
        # 'Stars Images/Videos' 206
        # make B.3, change to C afterwards if necessary
        print object.id ,';', sc.name ,';', object.title.encode('utf-8'),';', object.distance
        if not scan_tags(object, 'Star'):
            toplevel = get_toplevel(object)
            if not toplevel: toplevel = 'B'
            new_tag = TaxonomyHierarchy.objects.get( top_level = toplevel, level1 = 3, level2 = None)
            print object.id, 'replace', sc.name, 'with', new_tag.avm_code(), new_tag.name, '; ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(new_tag)  
        # remove local-use tag 
        if remove: object.subject_category.remove(sc)
        
    elif tag == 'X.101.5':
        # 'Star Clusters Images/Videos' 100
        # B.3.6.4. 
        if not scan_tags(object, 'Cluster'):
            new_tag = TaxonomyHierarchy.objects.get( top_level = 'B', level1 = 3, level2 = 6, level3 = 4, level4 = None)
            print object.id, 'replace', sc.name, 'with', new_tag.avm_code(), new_tag.name, '; ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(new_tag)  
        # remove local-use tag 
        if remove: object.subject_category.remove(sc)
    
    elif tag == 'X.101.6':
        # 'Nebulae Images/Videos' 330
        # B.4, change to C afterwards if necessary
        if not scan_tags(object, 'Nebula'):
            print object.id ,';', sc.name ,';', object.title.encode('utf-8'),';', object.distance 
            new_tag = TaxonomyHierarchy.objects.get( top_level = 'B', level1 = 4, level2 = None, level3 = None)
            print object.id, 'replace', sc.name, 'with', new_tag.avm_code(), new_tag.name, '; ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(new_tag)      
        # remove local-use tag               
        if remove: object.subject_category.remove(sc)
        save_changes = True           
    
    elif tag == 'X.101.7':
        # 'Galaxies Images/Videos' 474
        Ds = ['opo9228b',''] # Cosmology
        D = False
        Cs = [] # local universe
        C = False
        Bs = [] # Milky Way
        B = False
        type = ''
        #if there is not already a Galaxy tag:
        if not scan_tags(object, 'Galax'):
            # check if there is a tag for Milky Way => B
            if scan_tags(object, 'ilky'):
                B = True
                type = 'B'
            # or maybe a tag for Cosmology => D
            elif scan_tags(object, 'Cosmology'): 
                D = True
                type = 'D'
            elif object.id in Ds: 
                D = True  
                type = 'D'
            else: 
                C = True
                type = 'C'
            print sc.name,';',type, object.id,';', object.title.encode('utf-8'),';', object.distance
            new_tag = TaxonomyHierarchy.objects.get( top_level = type, level1 = 5, level2 = None)
            print object.id, 'replace', sc.name, 'with', new_tag.avm_code(), new_tag.name, '; ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(new_tag)
        if remove: object.subject_category.remove(sc)
        save_changes = True
        
    elif tag == 'X.101.8':
        # 'Quasars/AGN/Black Hole Images/Videos' 85
        added = False
        # 1. determine top_level
        print object.id, sc.name,
        type = ''
        if object.distance > 0.1 and object.distance < 11:
            type = 'D'
           # print object.distance,'=>',type
           
        # maybe there is a tag for Cosmology => D
        elif scan_tags(object, 'Cosmology'): 
            type = 'D'
           # print 'TAG: Cosmology =>', type
            
        # check if there is a tag for Milky Way => B
        elif scan_tags(object, 'ilky'):
            type = 'B'
           # print 'TAG: Milky Way =>', type
        else: type = ''

        # determin level1

            
        TITLE = str(object.title).upper()   
        if TITLE.find('MILKY WAY') > -1:
            if type == '': type = 'B'
            black_hole = TaxonomyHierarchy.objects.get( top_level = type, level1 = 5, level2 = 4, level3 = 6, level4 = None)
            print 'add', black_hole.avm_code(), black_hole.name, ' to ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(black_hole)
            added = True 
        if TITLE.find('GALACTIC CENTRE') > -1:
            if type == '': type = 'B'
            black_hole = TaxonomyHierarchy.objects.get( top_level = type, level1 = 5, level2 = 4, level3 = 6, level4 = None)
            print 'add', black_hole.avm_code(), black_hole.name, ' to ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(black_hole)
            added = True 
        if TITLE.find('BLACK HOLE') > -1:
            if type == '': type = 'C'
            black_hole = TaxonomyHierarchy.objects.get( top_level = type, level1 = 5, level2 = 4, level3 = 6, level4 = None)
            print 'add', black_hole.avm_code(), black_hole.name, ' to ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(black_hole)
            added = True
        if TITLE.find('NUCLE') > -1:
            if type == '': type = 'C'
            agn = TaxonomyHierarchy.objects.get( top_level = type, level1 = 5, level2 = 3, level3 =2, level4 = None)
            print 'add', agn.avm_code(), agn.name, ' to ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(agn)
            added = True
        if TITLE.find('ACTIVE') > -1:
            if type == '': type = 'C'
            agn = TaxonomyHierarchy.objects.get( top_level = type, level1 = 5, level2 = 3, level3 =2, level4 = None)
            print 'add', agn.avm_code(), agn.name, ' to ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(agn)
            added = True    
        if TITLE.find('QUASAR') > -1:
            if type == '': type = 'D'
            quasar = TaxonomyHierarchy.objects.get( top_level = type, level1 = 5, level2 = 3, level3 =2, level4 = 1, level5 = None)
            print 'add', quasar.avm_code(), quasar.name, ' to ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(quasar)        
            added = True
            
        if remove and added: object.subject_category.remove(sc)
        if added == False: print object.id, object.title, 'NOTHING added'
        save_changes = True
        
    elif tag == 'X.101.9':
        # 'Cosmology Images/Videos' 241
        # D
        if not scan_tags(object, 'Cosmology'):
            print object.id ,';', sc.name ,';', object.title.encode('utf-8'),';', object.distance 
            new_tag = TaxonomyHierarchy.objects.get( top_level = 'D', level1 = None, level2 = None, level3 = None)
            print object.id, 'replace', sc.name, 'with', new_tag.avm_code(), new_tag.name, '; ', object.id,  object.title.encode('utf-8') 
            object.subject_category.add(new_tag)      
        # remove local-use tag               
        if remove: object.subject_category.remove(sc)
        save_changes = True            
      
#---------------------------------------------------------------------------
 
    if save_changes:
        try: 
            object.save() # force_insert=True
            print "saved changes for tag %s in %s" % (sc.name, object.id)
        except:
            print "save failed with %s in %s" % (sc.name, object.id)        
    return

if __name__ == '__main__':
    #print "TEST"
    #analyse_taxonomy() 
    #show_taxonomy()
    #show_subjectnames()
    
    #exit()
    
    
    
# 'X.101.1': [u'Hubble Images Videos', 0],
# 'X.101.10': [u'Extrasolar Planets Videos', 1],
# O.K. 'X.101.11': [u'JWST Images/Videos', 24],
# O.K. 'X.101.12': [u'Spacecraft Images/Videos', 20],
# ? remove tag ? 'X.101.13': [u'Hubble DVD Videos', 165],
# O.K. 'X.101.21': [u'Illustration Images', 228],
# 'X.101.22': [u'Mission', 124],
# O.K. 'X.101.3': [u'Solar System Images/Videos', 518],
# O.K. 'X.101.4': [u'Stars Images/Videos', 166],
# O.K. 'X.101.5': [u'Star Clusters Images/Videos', 84],
# O.K. 'X.101.6': [u'Nebulae Images/Videos', 249],
# O.K. 'X.101.7': [u'Galaxies Images/Videos', 379],
# if there is no Milky Way tag (B) use C for BH and AGN and D for Quasar 'X.101.8': [u'Quasars/AGN/Black Hole Images/Videos', 72],
# O.K.'X.101.9': [u'Cosmology Images/Videos', 205]




    images = True
    count = 0
    #  First process the easier tags, then in 2. round the newly created tags can be used to check the top_level
    print 'Images 1. round'
    for Obj in Image.objects.all():
        x_tag = False
        n_tags = len(Obj.subject_category.all()) 
        for sc in  Obj.subject_category.all():
            if sc.top_level == 'X': 
                if sc.avm_code() == 'X.101.8' or sc.avm_code() == 'X.101.7': continue   
                count = count + 1
                treat_x(sc, Obj)
    
    print 'Images 2. round, AGN BH Quasare and Galaxies'
    for Obj in Image.objects.all(): 
        x_tag = False
        n_tags = len(Obj.subject_category.all()) 
        for sc in  Obj.subject_category.all():
            if sc.top_level == 'X': 
                if sc.avm_code() == 'X.101.8' or sc.avm_code() == 'X.101.7': 
                    count = count + 1
                    treat_x(sc, Obj)
    
    print 'treated', count, 'tags'
    
    
    
