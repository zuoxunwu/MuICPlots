import sys
import os
import numpy as np
import random as RD
from ROOT import *
from array import array
from CMS_style import setTDRStyle

gSystem.Load('/afs/cern.ch/work/x/xzuo/MadGraph5/MG5_aMC_v3_3_1/Delphes/libDelphes')

try:
  ROOT.gInterpreter.Declare('#include "/afs/cern.ch/work/x/xzuo/MadGraph5/MG5_aMC_v3_3_1/Delphes/classes/DelphesClasses.h"')
  ROOT.gInterpreter.Declare('#include "/afs/cern.ch/work/x/xzuo/MadGraph5/MG5_aMC_v3_3_1/Delphes/external/ExRootAnalysis/ExRootTreeReader.h"')
except:
  pass


from ROOT import *


IN_FILE = '/afs/cern.ch/work/x/xzuo/MadGraph5/MG5_aMC_v3_3_1/sim_muNp_CC_LO_Hbb/Events/run_02/delphes_MuIC.root'


def DrawCanv(name, graph1, graph2, graph3, graph4):
  setTDRStyle()

  gStyle.SetLegendBorderSize(0)
  gStyle.SetLegendFont(42)
  gStyle.SetLegendTextSize(0.035)
  gStyle.SetErrorX(0.0)

  colors = [kRed, kOrange+1, kGreen+2, kBlue] # 5 pt in total

  print ('drawing %s'%name)
  canv = TCanvas(name, name, 600, 600)
  canv.cd()
  frame = canv.DrawFrame(-10, 0, 10, 350)
  frame.GetXaxis().SetTitle('#eta')
  frame.GetYaxis().SetTitle('a.u.')
  canv.SetGrid()

  leg = TLegend(0.52, 0.56, 0.8, 0.8)
  leg.SetMargin(0.5)
  leg.SetFillStyle(0)

  text_label = TLatex()
  text_label.SetTextSize(0.035)
  text_label.DrawLatexNDC(0.18, 0.85, '#scale[1.4]{MuIC #bf{#it{Prospective}}}')
  text_label.Draw("same")

  mu_det = TPave(-7, 0, 0, 230, 0, 'NB')
  tk_det = TPave(-4, 0, 2.4, 250, 0, 'NB')
  mu_det.SetFillColor(kAzure-2)
  mu_det.SetFillStyle(3004)
  tk_det.SetFillColor(kOrange)
  tk_det.SetFillStyle(3005)
  mu_det.Draw('same')
  tk_det.Draw('same')
  leg.AddEntry(mu_det, 'Muon acceptance', 'f')
  leg.AddEntry(tk_det, 'Track acceptance', 'f')
 
  leg.AddEntry(graph1, 'Higgs', 'l')
  leg.AddEntry(graph2, 'Decay products', 'l')
  leg.AddEntry(graph3, 'Struck quark', 'l')
  leg.AddEntry(graph4, 'Scattered lepton', 'l')

  graph1.SetLineColor(colors[0])
  graph2.SetLineColor(colors[1])
  graph3.SetLineColor(colors[2])
  graph4.SetLineColor(colors[3])
  graph1.SetLineWidth(2)
  graph2.SetLineWidth(2)
  graph3.SetLineWidth(2)
  graph4.SetLineWidth(2)
  graph1.Draw("Chist same")
  graph2.Draw("Chist same")
  graph3.Draw("Chist same")
  graph4.Draw("Chist same")

  leg.Draw('same')

  canv.Write()
  canv.SaveAs(name+'.pdf')

def DrawMET(name, graph1, graph2):
  setTDRStyle()

  gStyle.SetLegendBorderSize(0)
  gStyle.SetLegendFont(42)
  gStyle.SetLegendTextSize(0.035)
  gStyle.SetErrorX(0.0)

  colors = [kRed, kOrange+1, kGreen+2, kBlue] # 5 pt in total

  print ('drawing %s'%name)
  canv = TCanvas(name, name, 600, 600)
  canv.cd()
  frame = canv.DrawFrame(0, 0, 300, 150)
  frame.GetXaxis().SetTitle('MET (GeV)')
  frame.GetYaxis().SetTitle('a.u.')
  canv.SetGrid()

  leg = TLegend(0.52, 0.57, 0.8, 0.8)
  leg.SetMargin(0.5)
  leg.SetFillStyle(0)

  text_label = TLatex()
  text_label.SetTextSize(0.035)
  text_label.DrawLatexNDC(0.18, 0.85, '#scale[1.4]{MuIC #bf{#it{Prospective}}}')
  text_label.Draw("same")

  leg.AddEntry(graph1, 'Real MET', 'l')
  leg.AddEntry(graph2, 'Reco MET', 'l')
#  leg.AddEntry(graph3, 'Struck quark', 'l')
#  leg.AddEntry(graph4, 'Scattered lepton', 'l')

  graph1.SetLineColor(colors[0])
  graph2.SetLineColor(colors[1])
#  graph3.SetLineColor(colors[2])
#  graph4.SetLineColor(colors[3])
  graph1.SetLineWidth(2)
  graph2.SetLineWidth(2)
#  graph3.SetLineWidth(2)
#  graph4.SetLineWidth(2)
  graph1.Draw("Chist same")
  graph2.Draw("Chist same")
#  graph3.Draw("Chist same")
#  graph4.Draw("Chist same")

  leg.Draw('same')

  canv.Write()
  canv.SaveAs(name+'.pdf')


def main():

  in_file = TFile.Open(IN_FILE, 'READ')
  out_file = TFile('Higgs_xsec.root', 'RECREATE')
  out_file.cd()

  eta_H = TH1D('eta_H', 'eta_H', 100, -10, 10)
  eta_b = TH1D('eta_b', 'eta_b', 100, -10, 10)
  eta_p = TH1D('eta_p', 'eta_p', 100, -10, 10)
  eta_m = TH1D('eta_m', 'eta_m', 100, -10, 10)

  real_met = TH1D('real_met', 'real_met', 100, 0, 300)
  reco_met = TH1D('reco_met', 'reco_met', 100, 0, 300)

  in_tree = in_file.Get("Delphes")
  treeReader = ExRootTreeReader(in_tree)

  gen_parts = treeReader.UseBranch("Particle")
  tracks    = treeReader.UseBranch("Track")
  gen_jets  = treeReader.UseBranch("GenJet")
  jets      = treeReader.UseBranch("Jet")
  eles      = treeReader.UseBranch("Electron")
  phots     = treeReader.UseBranch("Photon")
  muons     = treeReader.UseBranch("Muon")
  gen_MET   = treeReader.UseBranch("GenMissingET")
  MET       = treeReader.UseBranch("MissingET")

  event     = treeReader.UseBranch("Event")  
  

  for iEvt in range(treeReader.GetEntries()):
    if iEvt % 10000 == 0: print ("processing event %d"%iEvt)
    treeReader.ReadEntry(iEvt)
    evt_wgt = event[0].Weight   

    for gen_p in gen_parts:
      if gen_p.Status < 20: continue
      # Higgs
      elif gen_p.Status == 22:
          eta_H.Fill(gen_p.Eta, evt_wgt)
      # other primary products
      elif gen_p.Status == 23:
        # bb from Higgs
        if abs(gen_p.PID) == 5:
          eta_b.Fill(gen_p.Eta, evt_wgt * 0.5)
        # struct parton
        elif gen_p.PID == 1 or gen_p.PID == 3 or gen_p.PID == -2 or gen_p.PID == -4:
          eta_p.Fill(gen_p.Eta, evt_wgt)
        # vmu
        elif gen_p.PID == 14:
          eta_m.Fill(gen_p.Eta, evt_wgt)

    real_MET = gen_MET[0].MET
    reco_MET = MET[0].MET
    real_met.Fill(real_MET, evt_wgt)
    reco_met.Fill(reco_MET, evt_wgt)

  # End of event loop

  eta_H.Write() 
  eta_b.Write()
  eta_p.Write()
  eta_m.Write()
  real_met.Write()
  reco_met.Write()

  DrawCanv('eta_dist', eta_H, eta_b, eta_p, eta_m)
  DrawMET('met_dist', real_met, reco_met)

  out_file.Close()

main()
