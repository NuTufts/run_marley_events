import os,sys

template = "cc_marley_mono_EvX.json"
ftemp = open(template,'r')
templines = ftemp.readlines()

for energy in xrange(5,60,5):
    print energy
    fnameout = template.replace("X","%02d"%(energy))
    fout = open(fnameout,'w')
    for l in templines:
        l = l.replace("\n","")
        if "XXXX" in l:
            l = l.replace("XXXX","%.3f"%(float(energy)))
        print>>fout,l
    fout.close()

