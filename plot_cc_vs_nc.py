import ROOT as rt

rt.gStyle.SetOptStat(0)

def make_pmt_v_sipm( energy, outroot, cc_anafolder="cc_anaout", nc_anafolder="nc_anaout" ):
    ienergy = int(energy)

    ccfilename=cc_anafolder+"/cc_marleyana_Ev%02d_gen.root"%(ienergy)
    ncfilename=nc_anafolder+"/nc_ana_Ev%02d_00_gen.root"%(ienergy)

    
    ccfile = rt.TFile( ccfilename )
    ncfile = rt.TFile( ncfilename )

    print ccfilename,": ",ccfile
    print ncfilename,": ",ncfile

    cctree = ccfile.Get("hittotals")
    nctree = ncfile.Get("hittotals")

    outroot.cd()

    reduct_factor = 10.0
    if ienergy in [10]:
        reduct_factor = 1.0

    cchist = rt.TH2D("hpmt_v_sipm_cc_en%02d"%(ienergy),"CC-#nu_{e} @ true E_{#nu}=%d MeV;num PMT hits; num SiPM hits"%(ienergy),50,0,3e5,50,0,3000)
    nchist = rt.TH2D("hpmt_v_sipm_nc_en%02d"%(ienergy),"NC-#nu @ true E_{#nu}=%d MeV;num PMT hits; num SiPM hits"%(ienergy),    50,0,3e5,50,0,3000)

    cctree.Draw("(totals[1][0]*10+totals[1][1]):(totals[0][0]*10.0+totals[0][1])>>hpmt_v_sipm_cc_en%02d"%(ienergy))
    nctree.Draw("(totals[1][0]*%.2f+totals[1][1]):(totals[0][0]*%.2f+totals[0][1])>>hpmt_v_sipm_nc_en%02d"%(reduct_factor,reduct_factor,ienergy))

    return cchist,nchist


if __name__ == "__main__":

    out = rt.TFile("tempana.root","recreate")

    energies = [5,15,20,30,35,40,50,55]

    ccombo = rt.TCanvas("call","call",1200,1200)
    ccombo.Divide( 4, 4 )

    hists = {}

    ctemp = rt.TCanvas("c","c",800,400)

    for i,energy in enumerate(energies):

        ctemp.cd()
        cc,nc = make_pmt_v_sipm( energy, out )

        #c = rt.TCanvas("c","c",1200,500)
        #c.Divide(2,1)
        ccombo.cd( 4*i/2 + 1 )
        cc.Draw("colz")
        ccombo.cd( 4*i/2 + 2 )
        nc.Draw("colz")
            

        ccombo.Update()

        hists[("cc",energy)] = cc
        hists[("nc",energy)] = nc

    ctemp.cd()
    ctemp.Clear()
    ctemp.Divide(2,1)
    ctemp.cd(1)
    hists[("cc",5)].Draw("colz")
    ctemp.cd(2)
    hists[("nc",5)].Draw("colz")

    raw_input()
