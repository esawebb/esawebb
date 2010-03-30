from spacetelescope.migration.archives import SpacetelescopeCSVDataSource

import sys


for f in sys.argv:
    ds = SpacetelescopeCSVDataSource( filename = f )
    found = False
   
    list = []
    for line in ds:
        haskey = line.has_key('topic')
        topic = line.get('topic',None)
        if topic:
            found = True
            tops = topic.split(',')
            for t in tops:
                if t:
                    list.append(t.lstrip())
            
    keyset = set(list)    
    
    if found:
        print "Found topics in file %s:" % f
        print keyset
    elif haskey:
        print "Didn't find topics in file %s, but key 'topic' exists" % f
    else:
        print "Didn't find topics in file %s." % f
        