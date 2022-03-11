import sys
import os
import argparse
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

LUMI = 400.0

SAMPLES = ['H_NC', 'H_CC', 'Z_CC', 'Z_NC_loPT', 'Z_NC_hiPT', 
           'DIS_loPT1', 'DIS_loPT2', 'DIS_loPT3', 'DIS_loPT4', 'DIS_loPT5', 'DIS_loPT6', 
           'DIS_hiPT1', 'DIS_hiPT2', 'DIS_hiPT3', 'DIS_hiPT4']

FILES = {}
FILES["H_CC"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/Hbb_CC/Hbb_CC_50kevt.root'
FILES["H_NC"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/Hbb_NC/Hbb_NC_50kevt.root'
FILES["Z_CC"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/Znuj_Zbb/Znuj_Zbb_100kevt.root'
FILES["Z_NC_loPT"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/Zmuj_Zbb/Zmuj_Zbb_loPT_100kevt.root'
FILES["Z_NC_hiPT"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/Zmuj_Zbb/Zmuj_Zbb_hiPT_100kevt.root'

FILES["DIS_loPT1"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/DIS_bb/DIS_bb_loPT_tuple1_200kevt.root'
FILES["DIS_loPT2"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/DIS_bb/DIS_bb_loPT_tuple2_200kevt.root'
FILES["DIS_loPT3"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/DIS_bb/DIS_bb_loPT_tuple3_200kevt.root'
FILES["DIS_loPT4"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/DIS_bb/DIS_bb_loPT_tuple4_200kevt.root'
FILES["DIS_loPT5"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/DIS_bb/DIS_bb_loPT_tuple5_200kevt.root'
FILES["DIS_loPT6"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/DIS_bb/DIS_bb_loPT_tuple6_200kevt.root'
 
FILES["DIS_hiPT1"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/DIS_bb/DIS_bb_hiPT_tuple1_150kevt.root'
FILES["DIS_hiPT2"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/DIS_bb/DIS_bb_hiPT_tuple2_150kevt.root'
FILES["DIS_hiPT3"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/DIS_bb/DIS_bb_hiPT_tuple3_150kevt.root'
FILES["DIS_hiPT4"] = '/eos/cms/store/user/xzuo/MuIC/samples/tuples/DIS_bb/DIS_bb_hiPT_tuple4_150kevt.root'

XSECS = {}
XSECS["H_CC"] = 37.5
XSECS["H_NC"] = 6.74
XSECS["Z_CC"] = 51.2
XSECS["Z_NC_loPT"] = 390.0
XSECS["Z_NC_hiPT"] = 108.0

XSECS["DIS_loPT1"] = 56000.0 / 6.0
XSECS["DIS_loPT2"] = 56000.0 / 6.0
XSECS["DIS_loPT3"] = 56000.0 / 6.0
XSECS["DIS_loPT4"] = 56000.0 / 6.0
XSECS["DIS_loPT5"] = 56000.0 / 6.0
XSECS["DIS_loPT6"] = 56000.0 / 6.0

XSECS["DIS_hiPT1"] = 21130.0 / 4.0
XSECS["DIS_hiPT2"] = 21130.0 / 4.0
XSECS["DIS_hiPT3"] = 21130.0 / 4.0
XSECS["DIS_hiPT4"] = 21130.0 / 4.0

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


def EventLoop(in_file, hists, nom, selections):
  in_tree = in_file.Get("Delphes")
  treeReader = ExRootTreeReader(in_tree)

  jets      = treeReader.UseBranch("Jet")
  muons     = treeReader.UseBranch("Muon")
  MET       = treeReader.UseBranch("MissingET")
  event     = treeReader.UseBranch("Event")

  for iEvt in range(treeReader.GetEntries()):
    if iEvt % 10000 == 0: print ("processing event %d"%iEvt)
    treeReader.ReadEntry(iEvt)
    evt_wgt = event[0].Weight
    reco_MET = MET[0].MET

    for sel in selections:
      pass_sel = True
      vec_b1 = TLorentzVector(0, 0, 0, 0)
      vec_b2 = TLorentzVector(0, 0, 0, 0)
      vec_lq = TLorentzVector(0, 0, 0, 0)
      vec_mu = TLorentzVector(0, 0, 0, 0)
      for jet in jets:
        # baseline bJet selection
        if jet.PT < 25: continue
        if jet.BTag == 0: 
          if vec_lq.Pt() < jet.PT: vec_lq.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
          continue
        if jet.Eta < -4 or jet.Eta > 2.4: continue
        if   vec_b1.M() < jet.Mass: vec_b1.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
        elif vec_b2.M() < jet.Mass: vec_b2.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
      if 'bJet' in sel:
        if vec_b1.Pt() == 0 or vec_b2.Pt() == 0: pass_sel = False
      if 'lightq' in sel:
        if vec_lq.Pt() == 0: pass_sel = False
      for muon in muons:
        if muon.Eta > 0 or muon.Eta < -7: continue
        if muon.Eta > -4 and muon.PT < 5: continue
        temp_vec = TLorentzVector(0, 0, 0, 0)
        temp_vec.SetPtEtaPhiM(muon.PT, muon.Eta, muon.Phi, 0.105)
        if vec_b1.Pt() > 0 and temp_vec.DeltaR(vec_b1) < 0.4: continue
        if vec_b2.Pt() > 0 and temp_vec.DeltaR(vec_b2) < 0.4: continue
        if vec_mu.Pt() < temp_vec.Pt(): vec_mu = temp_vec
      if 'noMu' in sel: 
        if vec_mu.Pt() > 0: pass_sel = False
      if 'Hpt20' in sel:
        vec_H = vec_b1 + vec_b2
        if vec_H.Pt() < 20: pass_sel = False
      if 'MET30' in sel:
        if reco_MET < 30: pass_sel = False

      if not pass_sel: continue

      # passed selection, fill plots
      vec_H = vec_b1 + vec_b2
      if vec_b1.Pt() != 0:
        hists['b_pt'][sel] .Fill(vec_b1.Pt(),  evt_wgt * nom)
        hists['b_eta'][sel].Fill(vec_b1.Eta(), evt_wgt * nom)
      if vec_b2.Pt() != 0:
        hists['b_pt'][sel] .Fill(vec_b2.Pt(),  evt_wgt * nom)
        hists['b_eta'][sel].Fill(vec_b2.Eta(), evt_wgt * nom)
      if vec_lq.Pt() != 0:
        hists['q_pt'][sel] .Fill(vec_lq.Pt(),  evt_wgt * nom)
        hists['q_eta'][sel].Fill(vec_lq.Eta(), evt_wgt * nom)
  
      hists['H_mass'][sel].Fill(vec_H.M(),    evt_wgt * nom)
      hists['H_pt'][sel]  .Fill(vec_H.Pt(),   evt_wgt * nom)
      hists['H_eta'][sel] .Fill(vec_H.Eta(),  evt_wgt * nom)
      hists['MET'][sel]   .Fill(reco_MET,     evt_wgt * nom)
      if vec_mu.Pt() != 0:
        hists['mu_pt'][sel] .Fill(vec_mu.Pt(),  evt_wgt * nom)
        hists['mu_eta'][sel].Fill(vec_mu.Eta(), evt_wgt * nom)

  for sel in selections:
    hists['b_pt'][sel]  .Write()
    hists['b_eta'][sel] .Write()
    hists['q_pt'][sel]  .Write()
    hists['q_eta'][sel] .Write()
    hists['H_mass'][sel].Write()
    hists['H_pt'][sel]  .Write()
    hists['H_eta'][sel] .Write()
    hists['mu_pt'][sel] .Write()
    hists['mu_eta'][sel].Write()
    hists['MET'][sel]   .Write()


def GetTitle(var_name):
  if   var_name == 'H_mass': return 'm(bb) (GeV)'
  elif var_name == 'H_pt':   return 'p_{T}(bb) (GeV)'
  elif var_name == 'H_eta':  return '#eta_{}(bb)'
  elif var_name == 'b_pt':   return 'p_{T}(b) (GeV)'
  elif var_name == 'b_eta':  return '#eta_{}(b)'
  elif var_name == 'q_pt':   return 'p_{T}(q) (GeV)'
  elif var_name == 'q_eta':  return '#eta_{}(q)'
  elif var_name == 'mu_pt':  return 'p_{T}(#mu) (GeV)'
  elif var_name == 'mu_eta': return '#eta_{}(#mu)'
  elif var_name == 'MET':    return 'E^{miss}_{T} (GeV)'
  else: return ''

def DrawCanv(var_name, hists, sel, stacks, sigs, bkgs):
  setTDRStyle()

  gStyle.SetLegendBorderSize(0)
  gStyle.SetLegendFont(42)
  gStyle.SetLegendTextSize(0.035)
  gStyle.SetErrorX(0.0)

  bkg_colors = {'Z_NC': kAzure + 7, 'Z_CC': kYellow - 9, 'DIS_bb': kSpring -1}
  sig_colors = {'H_NC': kGreen+2, 'H_CC': kOrange+1}

  print ('drawing %s'%var_name)
  canv = TCanvas(var_name+'_'+sel, var_name+'_'+sel, 600, 600)
  canv.cd()

  leg = TLegend(0.68, 0.63, 0.86, 0.85)
  leg.SetMargin(0.5)
  leg.SetFillStyle(0)

  for sig in sigs:
    leg.AddEntry(hists[var_name][sig][sel], sig, 'l')
    hists[var_name][sig][sel].SetLineColor(sig_colors[sig])
    hists[var_name][sig][sel].SetLineWidth(2)
  for bkg in bkgs:
    leg.AddEntry(hists[var_name][bkg][sel], bkg, 'f')
    hists[var_name][bkg][sel].SetFillColor(bkg_colors[bkg]) 
    hists[var_name][bkg][sel].SetLineWidth(0)

  stacks[var_name+sel] = THStack(f"h_stack_{var_name}_{sel}", f'{var_name}_{sel}')
  if sel == 'bJets':
    stacks[var_name+sel].Add(hists[var_name]['Z_CC'][sel])
    stacks[var_name+sel].Add(hists[var_name]['Z_NC'][sel])
    stacks[var_name+sel].Add(hists[var_name]['DIS_bb'][sel])
  elif sel == 'bJets_lightq_Hpt20_noMu_MET30':
    stacks[var_name+sel].Add(hists[var_name]['Z_NC'][sel])
    stacks[var_name+sel].Add(hists[var_name]['Z_CC'][sel])
    stacks[var_name+sel].Add(hists[var_name]['DIS_bb'][sel])

  yscale = 1.4
  ymin = 0
  if sel == 'bJets':
    yscale = 500
    ymin = 0.1
    canv.SetLogy()

  frame = canv.DrawFrame( hists[var_name]['H_NC'][sel].GetBinLowEdge(1),  # xmin
                          ymin,                                         # ymin
                          hists[var_name]['H_NC'][sel].GetBinLowEdge(1) + hists[var_name]['H_NC'][sel].GetNbinsX() * hists[var_name]['H_NC'][sel].GetBinWidth(0), # xmax
                          stacks[var_name+sel].GetMaximum() * yscale)   # ymax
  frame.GetXaxis().SetTitle(GetTitle(var_name))
  frame.GetYaxis().SetTitle('Events / bin')
  frame.GetXaxis().SetTitleSize(0.04)
  frame.GetYaxis().SetTitleSize(0.04)
  frame.GetXaxis().SetTitleOffset(1.0)
  frame.GetYaxis().SetTitleOffset(1.5)
  canv.SetGrid()

  stacks[var_name+sel].Draw('HISTSAME')
  for sig in sigs:
    hists[var_name][sig][sel].Draw('HISTSAME')

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
  lumi_label.DrawLatexNDC(0.73, 0.94, '#bf{(Scaled to %.1f fb^{-1})}'%LUMI)
  lumi_label.Draw("same")

  canv.Write()
  canv.SaveAs(f'Hbb_{var_name}_{sel}.png')
  canv.SaveAs(f'Hbb_{var_name}_{sel}.pdf')

# To perform this analysis, run this script 3 times (steps)
# eg: python toy_analysis_Hbb.py --step nom
# eg: python toy_analysis_Hbb.py --step ana --sample H_CC
# for the second steps, run several times (parallel) for different samples.
def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("--step", choices=['nom', 'ana', 'plot'], required=True, help="choose analysis step: calculate nomalization, or analyze each sample, or make plots")
  parser.add_argument("--sample", choices=SAMPLES, required=False, help="only matters for step ana", default="H_CC")
  args = parser.parse_args()
  samp = args.sample

  samples = SAMPLES
#  samples = ['H_NC', 'H_CC', 'Z_CC', 'Z_NC_loPT', 'Z_NC_hiPT']
#  samples = ['DIS_loPT1', 'DIS_loPT2', 'DIS_loPT3', 'DIS_loPT4', 'DIS_loPT5', 'DIS_loPT6',
#             'DIS_hiPT1', 'DIS_hiPT2', 'DIS_hiPT3', 'DIS_hiPT4']

  var_names = ['H_mass', 'H_pt', 'H_eta', 'b_pt', 'b_eta', 'mu_pt', 'mu_eta', 'q_pt', 'q_eta', 'MET']
  # noms calculated with LUMI = 200
  noms = { 'H_CC': 3.350393, 'H_NC': 3.2659266, 'Z_CC': 1.8986719, 'Z_NC_loPT': 4.4001990, 'Z_NC_hiPT': 2.0194102,
           'DIS_loPT1': 0.2367412, 'DIS_loPT2': 0.2368015, 'DIS_loPT3': 0.23669445, 'DIS_loPT4': 0.2368718, 'DIS_loPT5': 0.2371298, 'DIS_loPT6': 0.23687889,
           'DIS_hiPT1': 0.2971800, 'DIS_hiPT2': 0.2968244, 'DIS_hiPT3': 0.29674328, 'DIS_hiPT4': 0.2966269 }

  selections = ['bJets', 'bJets_lightq_Hpt20_noMu_MET30']
    
  # run step 'nom'
  if args.step == 'nom':
    in_files = {}
    for sam in samples:
      in_files[sam] = TFile.Open(FILES[sam], 'READ')
    for sam in samples:
      nom = getTotalNom(in_files[sam], XSECS[sam])
      print (f"{sam} nom: {nom}")

  # run step 'ana'
  elif args.step == 'ana':
    in_file = TFile.Open(FILES[samp], 'READ')

    out_file = TFile(f'Hbb_dist_{samp}.root', 'RECREATE')
    out_file.cd()
    # declare histograms
    hists = {}
    for var_name in var_names:
      hists[var_name] = {}
    for sel in selections:
      hists['H_mass'][sel] = TH1D(f'H_mass_{samp}_{sel}', f'H_mass_{samp}_{sel}', 40, 0, 200)
      hists['H_pt'][sel]   = TH1D(f'H_pt_{samp}_{sel}',   f'H_pt_{samp}_{sel}',   40, 0, 200)
      hists['H_eta'][sel]  = TH1D(f'H_eta_{samp}_{sel}',  f'H_eta_{samp}_{sel}',  40, -8, 8)
      hists['b_pt'][sel]   = TH1D(f'b_pt_{samp}_{sel}',   f'b_pt_{samp}_{sel}',   40, 0, 200)
      hists['b_eta'][sel]  = TH1D(f'b_eta_{samp}_{sel}',  f'b_eta_{samp}_{sel}',  40, -8, 8)
      hists['mu_pt'][sel]  = TH1D(f'mu_pt_{samp}_{sel}',  f'mu_pt_{samp}_{sel}',  40, 0, 200)
      hists['mu_eta'][sel] = TH1D(f'mu_eta_{samp}_{sel}', f'mu_eta_{samp}_{sel}', 40, -10, 2)
      hists['q_pt'][sel]   = TH1D(f'q_pt_{samp}_{sel}',   f'q_pt_{samp}_{sel}',   40, 0, 200)
      hists['q_eta'][sel]  = TH1D(f'q_eta_{samp}_{sel}',  f'q_eta_{samp}_{sel}',  40, -8, 8)
      hists['MET'][sel]    = TH1D(f'MET_{samp}_{sel}',    f'MET_{samp}_{sel}',    40, 0, 200)

    EventLoop(in_file, hists, noms[samp], selections)
    out_file.Close()

  # run step 'plot'
  elif args.step == 'plot':
    hists = {}
    in_files = {}
    out_file = TFile(f'Hbb_plots.root', 'RECREATE')
    for var_name in var_names:
      hists[var_name] = {}
      for sam in samples:
        in_files[sam] = TFile.Open(f'Hbb_dist_{sam}.root', 'READ')
        hists[var_name][sam] = {}
        for sel in selections:
          hists[var_name][sam][sel] = in_files[sam].Get(f'{var_name}_{sam}_{sel}').Clone(f'h_{var_name}_{sam}_{sel}')
          hists[var_name][sam][sel].SetDirectory(0)
          hists[var_name][sam][sel].Scale(2) # only needed for lumi = 400

    stacks = {}
    out_file.cd()
    for var_name in var_names:
      hists[var_name]['Z_NC'] = {}
      hists[var_name]['DIS_bb'] = {}
      for sel in selections:
        hists[var_name]['Z_NC'][sel] = hists[var_name]['Z_NC_loPT'][sel].Clone(var_name + '_Z_NC_' + sel)
        hists[var_name]['Z_NC'][sel].Add(hists[var_name]['Z_NC_hiPT'][sel]) 
        hists[var_name]['DIS_bb'][sel] = hists[var_name]['DIS_loPT1'][sel].Clone(var_name + '_DIS_' + sel)
        hists[var_name]['DIS_bb'][sel].Add(hists[var_name]['DIS_loPT2'][sel])
        hists[var_name]['DIS_bb'][sel].Add(hists[var_name]['DIS_loPT3'][sel])
        hists[var_name]['DIS_bb'][sel].Add(hists[var_name]['DIS_loPT4'][sel])
        hists[var_name]['DIS_bb'][sel].Add(hists[var_name]['DIS_loPT5'][sel])
        hists[var_name]['DIS_bb'][sel].Add(hists[var_name]['DIS_loPT6'][sel])
        hists[var_name]['DIS_bb'][sel].Add(hists[var_name]['DIS_hiPT1'][sel])
        hists[var_name]['DIS_bb'][sel].Add(hists[var_name]['DIS_hiPT2'][sel]) 
        hists[var_name]['DIS_bb'][sel].Add(hists[var_name]['DIS_hiPT3'][sel])
        hists[var_name]['DIS_bb'][sel].Add(hists[var_name]['DIS_hiPT4'][sel])
        DrawCanv(var_name, hists, sel, stacks, ['H_NC', 'H_CC'], ['Z_NC', 'Z_CC', 'DIS_bb'] )
        # need to fix DrawCanv
  
    out_file.Close()

main()
