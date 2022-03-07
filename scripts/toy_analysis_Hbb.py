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

LUMI = 10.0

H_CC_FILE = '/afs/cern.ch/work/x/xzuo/MadGraph5/MG5_aMC_v3_3_1/sim_muNp_CC_LO_Hbb/Events/run_02/delphes_MuIC.root'
H_NC_FILE = '/afs/cern.ch/work/x/xzuo/MadGraph5/MG5_aMC_v3_3_1/sim_muNp_NC_LO_Hbb/Events/run_02/delphes_MuIC.root'
Z_CC_FILE = '/afs/cern.ch/work/x/xzuo/MadGraph5/MG5_aMC_v3_3_1/sm_processes/Znuj_Zbb/Events/run_01/delphes.root'
Z_NC_loPT = '/afs/cern.ch/work/x/xzuo/MadGraph5/MG5_aMC_v3_3_1/sm_processes/Zmuj_Zbb/Events/run_02_ptl0p01_1/delphes.root'
Z_NC_hiPT = '/afs/cern.ch/work/x/xzuo/MadGraph5/MG5_aMC_v3_3_1/sm_processes/Zmuj_Zbb/Events/run_01_ptl1/delphes.root'

H_CC_xsec = 37.5
H_NC_xsec = 6.74
Z_CC_xsec = 51.2
Z_NC_loPT_xsec = 390.0
Z_NC_hiPT_xsec = 108.0

H_CC_nom = 0.163296
H_NC_nom = 0.167520
Z_CC_nom = 0.094934
Z_NC_loPT_nom = 0.220010
Z_NC_hiPT_nom = 0.100971

def getTotalNom(in_file, xsec):
  in_tree = in_file.Get("Delphes")
  treeReader = ExRootTreeReader(in_tree)

  event     = treeReader.UseBranch("Event")
  tot_wgt = 0
  for iEvt in range(treeReader.GetEntries()):
    if iEvt % 10000 == 0: print ("processing event %d"%iEvt)
    treeReader.ReadEntry(iEvt)
    evt_wgt = event[0].Weight
    tot_wgt += evt_wgt

  tot_nom = xsec * LUMI / tot_wgt
  return tot_nom


def EventLoop(in_file, hists, samp, nom):
  in_tree = in_file.Get("Delphes")
  treeReader = ExRootTreeReader(in_tree)

  jets      = treeReader.UseBranch("Jet")
  event     = treeReader.UseBranch("Event")

  for iEvt in range(treeReader.GetEntries()):
    if iEvt % 10000 == 0: print ("processing event %d"%iEvt)
    treeReader.ReadEntry(iEvt)
    evt_wgt = event[0].Weight

    vec_b1 = TLorentzVector(0, 0, 0, 0)
    vec_b2 = TLorentzVector(0, 0, 0, 0)
    for jet in jets:
      if jet.BTag == 0: continue
      if   vec_b1.Pt() == 0: vec_b1.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
      elif vec_b2.Pt() == 0: vec_b2.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

    if vec_b1.Pt() == 0 or vec_b2.Pt() == 0: continue
    vec_H = vec_b1 + vec_b2
    hists['b_pt'][samp] .Fill(vec_b1.Pt(),  evt_wgt * nom)
    hists['b_pt'][samp] .Fill(vec_b2.Pt(),  evt_wgt * nom)
    hists['b_eta'][samp].Fill(vec_b1.Eta(), evt_wgt * nom)
    hists['b_eta'][samp].Fill(vec_b2.Eta(), evt_wgt * nom)

    hists['H_mass'][samp].Fill(vec_H.M(), evt_wgt * nom)
    hists['H_pt'][samp]  .Fill(vec_H.Pt(),   evt_wgt * nom)
    hists['H_eta'][samp] .Fill(vec_H.Eta(),  evt_wgt * nom)

    hists['b_pt'][samp] .Write()
    hists['b_eta'][samp].Write()
    hists['H_mass'][samp].Write()
    hists['H_pt'][samp]  .Write()
    hists['H_eta'][samp] .Write()


def GetTitle(var_name):
  if   var_name == 'H_mass': return 'm(bb) (GeV)'
  elif var_name == 'H_pt':   return 'p_{T}(bb) (GeV)'
  elif var_name == 'H_eta':  return '#eta_{}(bb) (GeV)'
  elif var_name == 'b_pt':   return 'p_{T}(b) (GeV)'
  elif var_name == 'b_eta':  return '#eta_{}(b) (GeV)'
  else: return ''

def DrawCanv(var_name, hists, stacks, samples):
  setTDRStyle()

  gStyle.SetLegendBorderSize(0)
  gStyle.SetLegendFont(42)
  gStyle.SetLegendTextSize(0.035)
  gStyle.SetErrorX(0.0)

  bkg_colors = [kAzure + 7, kYellow - 9]
  sig_colors = [kGreen+2, kOrange+1]

  print ('drawing %s'%var_name)
  canv = TCanvas(var_name, var_name, 600, 600)
  canv.cd()
#  frame = canv.DrawFrame(0, 0, 5, 160)
#  frame.GetXaxis().SetTitle('#Delta^{}R')
#  frame.GetYaxis().SetTitle('a.u.')

  leg = TLegend(0.68, 0.63, 0.86, 0.85)
  leg.SetMargin(0.5)
  leg.SetFillStyle(0)

  leg.AddEntry(hists[var_name]['H_NC'], 'H_NC', 'l')
  leg.AddEntry(hists[var_name]['H_CC'], 'H_CC', 'l')
  leg.AddEntry(hists[var_name]['Z_NC'], 'Z_NC', 'f')
  leg.AddEntry(hists[var_name]['Z_CC'], 'Z_CC', 'f')

  hists[var_name]['H_NC'].SetLineColor(sig_colors[0])
  hists[var_name]['H_CC'].SetLineColor(sig_colors[1])
  hists[var_name]['H_NC'].SetLineWidth(2)
  hists[var_name]['H_CC'].SetLineWidth(2)

  hists[var_name]['Z_NC'].SetLineWidth(0)
  hists[var_name]['Z_CC'].SetLineWidth(0)
  hists[var_name]['Z_NC'].SetFillColor(bkg_colors[0])
  hists[var_name]['Z_CC'].SetFillColor(bkg_colors[1])

  stacks[var_name] = THStack("h_stack_"+var_name, var_name)
  for samp in ['Z_CC', 'Z_NC']:
        stacks[var_name].Add(hists[var_name][samp])

#  stacks[var_name].SetMaximum(stacks[var_name].GetMaximum() * 1.3)

  frame = canv.DrawFrame( hists[var_name]['H_NC'].GetBinLowEdge(1),  # xmin
                          0,                                         # ymin
                          hists[var_name]['H_NC'].GetBinLowEdge(1) + hists[var_name]['H_NC'].GetNbinsX() * hists[var_name]['H_NC'].GetBinWidth(0), # xmax
                          stacks[var_name].GetMaximum() * 1.4)       # ymax
  frame.GetXaxis().SetTitle(GetTitle(var_name))
  frame.GetYaxis().SetTitle('Events / bin')
  frame.GetXaxis().SetTitleSize(0.04)
  frame.GetYaxis().SetTitleSize(0.04)
  frame.GetXaxis().SetTitleOffset(1.0)
  frame.GetYaxis().SetTitleOffset(1.5)
  canv.SetGrid()

  stacks[var_name].Draw('HISTSAME')
  hists[var_name]['H_NC'].Draw('HISTSAME')
  hists[var_name]['H_CC'].Draw('HISTSAME')

  leg.Draw('same')

  text_label = TLatex()
  text_label.SetTextSize(0.035)
  text_label.DrawLatexNDC(0.18, 0.85, '#scale[1.4]{MuIC #bf{#it{Prospective}}}')
  text_label.Draw("same")

  e_label = TLatex()
  e_label.SetTextSize(0.035)
  e_label.DrawLatexNDC(0.18, 0.78, '#bf{275 GeV #it{p} X 960 GeV #mu^{-}}')
  e_label.Draw("same")

  lumi_label = TLatex()
  lumi_label.SetTextSize(0.028)
  lumi_label.DrawLatexNDC(0.75, 0.94, '#bf{(Scaled to 10 fb^{-1})}')
  lumi_label.Draw("same")

  canv.Write()
  canv.SaveAs('Hbb_' + var_name+'.pdf')

def main():

  samples = ['H_NC', 'H_CC', 'Z_CC', 'Z_NC_loPT', 'Z_NC_hiPT']
  in_files = {}

  in_files['H_NC'] = TFile.Open(H_NC_FILE, 'READ')
  in_files['H_CC'] = TFile.Open(H_CC_FILE, 'READ')
  in_files['Z_CC'] = TFile.Open(Z_CC_FILE, 'READ')
  in_files['Z_NC_loPT'] = TFile.Open(Z_NC_loPT, 'READ')
  in_files['Z_NC_hiPT'] = TFile.Open(Z_NC_hiPT, 'READ')
  out_file = TFile('Hbb_dist.root', 'RECREATE')
  out_file.cd()

  var_names = ['H_mass', 'H_pt', 'H_eta', 'b_pt', 'b_eta']
  # declare histograms
  hists = {}
  for var_name in var_names:
    hists[var_name] = {}
  for samp in samples:
    hists['H_mass'][samp] = TH1D('H_mass_' + samp, 'H_mass_' + samp, 40, 0, 200)
    hists['H_pt'][samp]   = TH1D('H_pt_' + samp,   'H_pt_' + samp,   40, 0, 200)
    hists['H_eta'][samp]  = TH1D('H_eta_' + samp,  'H_eta_' + samp,  40, -8, 8)
    hists['b_pt'][samp]   = TH1D('b_pt_' + samp,   'b_pt_' + samp,   40, 0, 200)
    hists['b_eta'][samp]  = TH1D('b_eta_' + samp,  'b_eta_' + samp,  40, -8, 8)

#  # calculate normalization for samples
#  H_NC_nom = getTotalNom(in_files['H_NC'], H_NC_xsec)
#  print ("H_NC_nom: %f" %H_NC_nom)
#  H_CC_nom = getTotalNom(in_files['H_CC'], H_CC_xsec)
#  print ("H_CC_nom: %f" %H_CC_nom)
#  Z_CC_nom = getTotalNom(in_files['Z_CC'], Z_CC_xsec)
#  print ("Z_CC_nom: %f" %Z_CC_nom)
#  Z_NC_loPT_nom = getTotalNom(in_files['Z_NC_loPT'], Z_NC_loPT_xsec)
#  print ("Z_NC_loPT_nom: %f" %Z_NC_loPT_nom)
#  Z_NC_hiPT_nom = getTotalNom(in_files['Z_NC_hiPT'], Z_NC_hiPT_xsec)
#  print ("Z_NC_hiPT_nom: %f" %Z_NC_hiPT_nom)

  noms = { 'H_CC': 0.163296, 'H_NC': 0.167520, 'Z_CC': 0.094934, 'Z_NC_loPT': 0.220010, 'Z_NC_hiPT': 0.100971}

  hist_dir = out_file.mkdir('raw_plots')
  hist_dir.cd()
  for samp in samples:
    EventLoop(in_files[samp], hists, samp, noms[samp])

  stacks = {}
  out_file.cd()
  for var_name in var_names:
    hists[var_name]['Z_NC'] = hists[var_name]['Z_NC_loPT'].Clone(var_name + '_Z_NC')
    hists[var_name]['Z_NC'].Add(hists[var_name]['Z_NC_hiPT']) 
    DrawCanv(var_name, hists, stacks, ['H_NC', 'H_CC', 'Z_CC', 'Z_NC'] )
  

  out_file.Close()

main()
