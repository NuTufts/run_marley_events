import os,sys
import ROOT as rt
import numpy as np

"""
we load the marley simulation data for cc and NC events.
we have fixed true neutrino energy, so we need to interpolate.
"""

def make_matrix_cc( cc_anafolder, cc_stemname, nbins, xmin, xmax, outroot ):

    outroot.cd()
    
    energies = [5,15,20,30,35,40,50,55]
    ly = 5.0*1000.0

    tnbins = 100
    txmin  = 0.0
    txmax  = 100.0

    matrix  = rt.TH2F( "hcc_pmt",";true energy; reco energy (scint)", tnbins,txmin,txmax,nbins,xmin,xmax)
    matrix2 = rt.TH2F( "hcc_sipm",";true energy; reco energy (cherenkov)",tnbins,txmin,txmax,nbins,xmin,xmax)    
    hlist_pmt  = {}
    hlist_sipm = {}    

    truebins = [1]

    hlist_pmt[1]  = rt.TH1F("hcc_pmt_energy%d"%(0),";reco energy",nbins,xmin,xmax)
    hlist_sipm[1] = rt.TH1F("hcc_sipm_energy%d"%(0),";reco energy",nbins,xmin,xmax)    
        
    for energy in energies:
        ienergy = int(energy)
        #ccfilename=cc_anafolder+"/cc_marleyana_Ev%02d_gen.root"%(ienergy)
        ccfilename=cc_anafolder+"/"+cc_stemname%(ienergy)

        if not os.path.exists(ccfilename):
            print "could not find CC ana file: ",ccfilename
            continue
        print "Loading: ",ccfilename
        
        ccfile = rt.TFile( ccfilename )
        cctree = ccfile.Get("hittotals")

        outroot.cd()
        hreco_pmt  = rt.TH1F("hcc_pmt_energy%d"%(ienergy),";reco energy",nbins,xmin,xmax)
        hreco_sipm = rt.TH1F("hcc_sipm_energy%d"%(ienergy),";reco energy",nbins,xmin,xmax)        
        
        reduct_factor = 10.0
        if ienergy in [10]:
            reduct_factor = 1.0

        cctree.Draw("(totals[0][0]*10.0+totals[0][1])/%.3f>>hcc_pmt_energy%d"%(ly,ienergy))
        cctree.Draw("(totals[1][0]*10.0+totals[1][1])/%.3f>>hcc_sipm_energy%d"%(25.0,ienergy)) 
        
        truebin = matrix.GetXaxis().FindBin( energy )
        hlist_pmt[truebin]  = hreco_pmt
        hlist_sipm[truebin] = hreco_sipm

        if truebin not in truebins:
            truebins.append( truebin )

    # do interpolation
    lobin = truebins[0]
    hibin = truebins[1]
    lowtruebin = 0
    
    for tbin in xrange(1,tnbins+1):
        if tbin in truebins:
            continue
        # find the bounding true bins
        while tbin > hibin:
            lowtruebin += 1
            if lowtruebin+1>=len(truebins):
                break
            lobin = truebins[lowtruebin]
            hibin = truebins[lowtruebin+1]
        if lowtruebin+1>=len(truebins):
            break
        print "true bin ",tbin," of ",tnbins," from lobin=",lobin," hibin=",hibin
        x   = float(tbin-lobin)/float(hibin-lobin)        
        # reco bin interpolations
        tot  = 0.0
        tot2 = 0.0
        for rbin in xrange(1,nbins+1):
            # pmt values
            val = (1.0-x)*hlist_pmt[lobin].GetBinContent(rbin) + x*hlist_pmt[hibin].GetBinContent(rbin)
            tot += val
            matrix.SetBinContent( tbin, rbin, val )
            # sipm values
            val = (1.0-x)*hlist_sipm[lobin].GetBinContent(rbin) + x*hlist_sipm[hibin].GetBinContent(rbin)
            tot2 += val
            matrix2.SetBinContent( tbin, rbin, val )
            
        if tot>0:
            for rbin in xrange(1,nbins+1):
                val = matrix.GetBinContent( tbin, rbin )
                val /= tot
                matrix.SetBinContent( tbin, rbin, val )
        if tot2>0:
            for rbin in xrange(1,nbins+1):
                val = matrix2.GetBinContent( tbin, rbin )
                val /= tot2
                matrix2.SetBinContent( tbin, rbin, val )

    for tbin in truebins[1:]:
        tot = hlist_pmt[tbin].Integral()
        for rbin in xrange(1,nbins+1):
            matrix.SetBinContent(  tbin, rbin, hlist_pmt[tbin].GetBinContent(rbin)/tot )
            matrix2.SetBinContent( tbin, rbin, hlist_sipm[tbin].GetBinContent(rbin)/tot )            

    for tbin in xrange(truebins[-1]+1,tnbins+1):
        for rbin in xrange(1,nbins+1):
            matrix.SetBinContent(  tbin, rbin, matrix.GetBinContent(truebins[-1],rbin) )
            matrix2.SetBinContent( tbin, rbin, matrix2.GetBinContent(truebins[-1],rbin) )            
                
    for truebin,hist in hlist_pmt.items():
        if hist is not None:
            hist.Write()

    for truebin,hist in hlist_sipm.items():
        if hist is not None:
            hist.Write()

    matrix.Write()
    matrix2.Write()
            
    return matrix,matrix2

if __name__ == "__main__":

    rt.gStyle.SetOptStat(0)
    
    out = rt.TFile("out_smearing_matrix.root","recreate")
    
    matrix,matrix2 = make_matrix_cc( "cc_anaout","cc_marleyana_Ev%02d_gen.root",20, 0, 100.0, out )

    c = rt.TCanvas("c","c",1400,600)
    c.Divide(2,1)
    c.cd(1)
    matrix.Draw("colz")
    c.cd(2)
    matrix2.Draw("colz")
    c.Update()
    c.Draw()
    raw_input()
    
    out.Close()


