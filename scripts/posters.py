from djangoplicity.products.models import *


#cps = ConferencePoster.objects.all()
#
#for cp in cps:
#    p = Poster()
#    p.type = 'C'
#    for key,value in cp.__dict__.iteritems():
#       p.__dict__[key] = value
#       
#    p.save()

ps = Poster.objects.exclude(type='C')

for p in ps:
    print p.type
    #p.type = 'P'
    #p.save()