import sys
import os
import numpy as np
import random as RD
from ROOT import *
from array import array
from CMS_style import setTDRStyle

def DrawCanv(name, graph1, graph2, graph3):
  setTDRStyle()

  gStyle.SetLegendBorderSize(0)
  gStyle.SetLegendFont(42)
  gStyle.SetLegendTextSize(0.04)
  gStyle.SetErrorX(0.0)

  colors = [kOrange+1, kGreen+2, kRed] # 5 pt in total
#  sizes  = [1.4, 1.2, 1.0, 0.8, 0.6] # 5 pt in total

  print ('drawing %s'%name)
  canv = TCanvas(name, name, 600, 600)
  canv.cd()
  frame = canv.DrawFrame(0, 0, 1800, 160)
  frame.GetXaxis().SetTitle('E_{#mu} (GeV)')
  frame.GetYaxis().SetTitle('#sigma (fb)')
  canv.SetGrid()

  leg = TLegend(0.2, 0.53, 0.5, 0.73)
  leg.AddEntry(graph1, 'total', 'l')
  leg.AddEntry(graph2, 'CC', 'l')
  leg.AddEntry(graph3, 'NC', 'l')
  leg.SetMargin(0.5)
  leg.SetFillStyle(0)

  text_label = TLatex()
  text_label.SetTextSize(0.035)
  text_label.DrawLatexNDC(0.18, 0.85, '#scale[1.4]{MuIC #bf{#it{Prospective}}}')
  text_label.Draw("same")

  graph1.SetMaximum(140)
  graph1.SetMinimum(0)
  graph1.SetLineColor(colors[0])
  graph2.SetLineColor(colors[1])
  graph3.SetLineColor(colors[2])
  graph1.SetLineWidth(2)
  graph2.SetLineWidth(2)
  graph3.SetLineWidth(2)
  graph1.SetFillColor(colors[0])
  graph2.SetFillColor(colors[1])
  graph3.SetFillColor(colors[2])
  graph1.SetFillStyle(3010)
  graph2.SetFillStyle(3010)
  graph3.SetFillStyle(3010)
  graph1.Draw("L3 same")
  graph2.Draw("L3 same")
  graph3.Draw("L3 same")

  mark_nom = TMarker(960, 76.7, 20)
  mark_nom.SetMarkerColor(kOrange+2)
  mark_nom.SetMarkerSize(1.5)
  leg.AddEntry(mark_nom, 'E_{#mu} = 960 GeV', 'P')
  mark_nom.Draw('same')

  leg.Draw('same')

  canv.Write()
  canv.SaveAs(name+'.pdf')

def main():

  out_file = TFile('Higgs_xsec.root', 'RECREATE')
  out_file.cd()

  muE = array('f', [
         14., 16., 20., 40., 
         60., 80., 100., 200., 
         300., 500., 700., 730., 
         800., 900., 960., 1000., 
         1200., 1300., 1390., 1500.])

  xsec_CC = array('f', [
             0, 9.8e-11, 1.4e-6, 9.7e-3, 
             0.104, 0.359, 0.791, 5.15,   
             11.6,  27.3,  43.8,  46.3,   
             52.0,  60.3,  65.1,  68.3,   
             84.2,  92.1,  99.3, 107.2])

  uncert_up_CC = array('f', [
             0, 103, 67.6, 29.3,
             21.8, 18.6, 16.5, 12.2,
             10.4, 8.49, 7.44, 7.37,
             7.10, 6.70, 6.57, 6.49,
             6.01, 5.80, 5.62, 5.36])

  uncert_dn_CC = array('f', [
             0, -45.0, -34.5, -19.6,
             -15.6, -13.7, -12.5, -9.62,
             -8.37, -7.02, -6.24, -6.18,
             -5.97, -5.68, -5.58, -5.51,
             -5.15, -4.98, -4.84, -4.64])

  xsec_NC = array('f', [0, 6.0e-12, 9.9e-8, 9.2e-4, 
             1.1e-2, 4.2e-2, 9.9e-2, 0.74,
             1.79,   4.51,   7.52,   7.95,
             9.06,   10.7,   11.6,   12.2,
             15.4,   16.9,   18.3,   20.0])

  uncert_up_NC = array('f', [
                      0, 102, 68.1, 29.8,
                      22.5, 19.1, 17.0, 12.3,
                      10.3, 8.34, 7.21, 7.06,
                      6.73, 6.37, 6.17, 6.06,
                      5.48, 5.25, 5.03, 4.81])

  uncert_dn_NC = array('f', [
                      0, -44.8, -34.7, -19.0,
                      -16.0, -14.1, -12.8, -9.73,
                      -8.35, -6.93, -6.10, -5.98,
                      -5.73, -5.45, -5.31, -5.18,
                      -4.78, -4.60, -4.44, -4.26])

  unc_CC_up = np.multiply(xsec_CC, uncert_up_CC) * 0.01
  unc_CC_dn = np.multiply(xsec_CC, uncert_dn_CC) * -0.01
  unc_NC_up = np.multiply(xsec_NC, uncert_up_NC) * 0.01
  unc_NC_dn = np.multiply(xsec_NC, uncert_dn_NC) * -0.01

  xsec_tot = np.add(xsec_CC, xsec_NC)
  unc_tot_up = np.add(unc_CC_up, unc_NC_up)
  unc_tot_dn = np.add(unc_CC_dn, unc_NC_dn)
  
  graph_CC = TGraphAsymmErrors()
  graph_CC.SetName('graph_CC')
  graph_NC = TGraphAsymmErrors()
  graph_NC.SetName('graph_NC')
  graph_tot = TGraphAsymmErrors()
  graph_tot.SetName('graph_tot')

  for i in range(len(muE)):
    graph_CC. SetPoint(i, muE[i], xsec_CC[i])
    graph_NC. SetPoint(i, muE[i], xsec_NC[i])
    graph_tot.SetPoint(i, muE[i], xsec_tot[i])

    graph_CC. SetPointError(i, 0, 0, unc_CC_up[i],  unc_CC_dn[i])
    graph_NC. SetPointError(i, 0, 0, unc_NC_up[i],  unc_NC_dn[i])
    graph_tot.SetPointError(i, 0, 0, unc_tot_up[i], unc_tot_dn[i])

  DrawCanv('muNeg', graph_tot, graph_CC, graph_NC)
  out_file.Close()

main()
