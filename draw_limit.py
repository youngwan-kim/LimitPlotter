#!/usr/bin/env python3

import os
import sys
import array
import argparse
import ROOT
import rootconfig

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--output", dest="output", default="limit")
parser.add_argument("-c", "--channel", dest="channel", default="Muon")

channels = ["Muon", "Electron"]
models = ["Majorana", "Dirac"]

def draw_limits(channel, model, final):

    #x_grids = array.array('d')
    #y_grids_exp_2sig_up = array.array('d')
    #y_grids_exp_1sig_up = array.array('d')
    #y_grids_exp = array.array('d')
    #y_grids_exp_1sig_down = array.array('d')
    #y_grids_exp_2sig_down = array.array('d')

    y_grids_obs = array.array('d')
    y_grids_dilepton = array.array('d')
    y_grids_trilepton = array.array('d')
    y_grids_SSWW = array.array('d')

    #masses = list(limits_exp.keys())

    #for mass in masses:
    #    x_grids.append(mass)
    #    y_grids_exp_2sig_up.append(limits_exp[mass]["Combined"]["97.5%"] - limits_exp[mass]["Combined"]["50.0%"])
    #    y_grids_exp_1sig_up.append(limits_exp[mass]["Combined"]["84.0%"] - limits_exp[mass]["Combined"]["50.0%"])
    #    y_grids_exp.append(limits_exp[mass]["Combined"]["50.0%"])
    #    y_grids_exp_1sig_down.append(limits_exp[mass]["Combined"]["50.0%"] - limits_exp[mass]["Combined"]["16.0%"])
    #    y_grids_exp_2sig_down.append(limits_exp[mass]["Combined"]["50.0%"] - limits_exp[mass]["Combined"]["2.5%"])
    #    y_grids_obs.append(limits_obs[mass]["Combined"]["50.0%"])

    x_grids_dilepton = array.array('d')
    with open(f"./dilepton_{channel}.txt") as openfile :
        ll = openfile.readlines()
        for l in ll:
            l = l.strip()
            mass = float(l.split(" ")[0])
            x_grids_dilepton.append(mass)
            limit = float(l.split(" ")[1])
            y_grids_dilepton.append(limit)

    x_grids_trilepton = array.array('d')
    with open(f"./trilepton_{channel}.txt") as openfile :
        ll = openfile.readlines()
        for l in ll:
            l = l.strip()
            mass = float(l.split(" ")[0])
            x_grids_trilepton.append(mass)
            limit = float(l.split(" ")[1])
            y_grids_trilepton.append(limit)

    if channel == "Muon" : 
        x_grids_SSWW = array.array('d')
        with open(f"./SSWW_{channel}.txt") as openfile :
            ll = openfile.readlines()
            for l in ll:
                l = l.strip()
                mass = float(l.split(" ")[0])
                x_grids_SSWW.append(mass)
                limit = float(l.split(" ")[1])
                y_grids_SSWW.append(limit)

    graph_dilepton = ROOT.TGraphAsymmErrors(len(x_grids_dilepton), x_grids_dilepton, y_grids_dilepton, 0, 0, 0, 0)
    graph_dilepton.SetLineColor(ROOT.kBlue-4)
    graph_dilepton.SetLineWidth(3)

    graph_trilepton = ROOT.TGraphAsymmErrors(len(x_grids_trilepton), x_grids_trilepton, y_grids_trilepton, 0, 0, 0, 0)
    graph_trilepton.SetLineColor(ROOT.kRed-4)
    graph_trilepton.SetLineWidth(3)

    if channel == "Muon" : 
        graph_SSWW = ROOT.TGraphAsymmErrors(len(x_grids_SSWW), x_grids_SSWW, y_grids_SSWW, 0, 0, 0, 0)
        graph_SSWW.SetLineColor(ROOT.kGreen+1)
        graph_SSWW.SetLineWidth(3)

    #graph_exp = ROOT.TGraphAsymmErrors(len(masses), x_grids, y_grids_exp, 0, 0, 0, 0)
    #graph_exp.SetLineColor(ROOT.kBlack)
    #graph_exp.SetLineStyle(2)
    #graph_exp.SetLineWidth(5)
    #graph_obs = ROOT.TGraphAsymmErrors(len(masses), x_grids, y_grids_obs, 0, 0, 0, 0)
    #graph_obs.SetLineColor(ROOT.kBlack)
    #graph_obs.SetLineWidth(5)

    #graph_exp_1sig = ROOT.TGraphAsymmErrors(len(masses), x_grids, y_grids_exp, 0, 0, y_grids_exp_1sig_down, y_grids_exp_1sig_up)
    #graph_exp_1sig.SetLineColor(ROOT.kGreen+1)
    #graph_exp_1sig.SetFillColor(ROOT.kGreen+1)
    #graph_exp_1sig.SetMarkerColor(ROOT.kGreen+1)

    #graph_exp_2sig = ROOT.TGraphAsymmErrors(len(masses), x_grids, y_grids_exp, 0, 0, y_grids_exp_2sig_down, y_grids_exp_2sig_up)
    #graph_exp_2sig.SetLineColor(ROOT.kOrange)
    #graph_exp_2sig.SetFillColor(ROOT.kOrange)
    #graph_exp_2sig.SetMarkerColor(ROOT.kOrange)

    canvas = ROOT.TCanvas()
    hist_dummy = ROOT.TH1D("hist_dummy", "hist_dummy", 50000, 0., 50000.)
    hist_dummy.SetTitle("")
    hist_dummy.Draw("hist")
    hist_dummy.GetXaxis().SetTitle("m_{N} [GeV]")
    if channel == "Muon":
        hist_dummy.GetYaxis().SetTitle("#left|V_{#muN}#right|^{2}")
    elif channel == "Electron":
        hist_dummy.GetYaxis().SetTitle("#left|V_{eN}#right|^{2}")
    hist_dummy.GetYaxis().SetTitleSize(0.0565)
    #hist_dummy.GetYaxis().SetTitleOffset(0.0)
    hist_dummy.GetYaxis().SetLabelSize(0.04)
    hist_dummy.GetXaxis().SetLabelSize(0.04)
    hist_dummy.GetXaxis().SetRangeUser(1., 50000.)
    hist_dummy.GetXaxis().SetNdivisions(505)
    hist_dummy.GetYaxis().SetRangeUser(5.e-06, 1.0)
    hist_dummy.GetYaxis().SetNdivisions(505)

    #graph_exp_2sig.Draw("3same")
    #graph_exp_1sig.Draw("3same")
    #graph_exp.Draw("lsame")
    if channel == "Muon" : graph_SSWW.Draw("lsame")
    graph_dilepton.Draw("lsame")
    graph_trilepton.Draw("lsame")
    #graph_obs.Draw("lsame")

    legend = ROOT.TLegend(0.58, 0.16, 0.93, 0.575)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.035)
    #legend.AddEntry(graph_obs, "Observed", "l")
    if channel == "Muon" : legend.AddEntry(graph_SSWW, "#splitline{SSWW VBF}{#scale[0.85]{#it{arXiv:2206.08956}}}", "l")
    legend.AddEntry(graph_dilepton, "#splitline{Same-Sign Dilepton}{#scale[0.85]{#it{JHEP} 01(2019)122}}", "l")
    legend.AddEntry(graph_trilepton, "#splitline{Trilepton}{#scale[0.85]{#it{PRL} 120(2018)221801}}", "l")
    #legend.AddEntry(graph_exp, "Expected", "l")
    #legend.AddEntry(graph_exp_1sig, "68% expected", "f")
    #legend.AddEntry(graph_exp_2sig, "95% expected", "f")

    hist_dummy.Draw("axissame")

    latex_cms = ROOT.TLatex()
    latex_cms.SetNDC()
    latex_cms.SetTextSize(0.07)
    latex_cms.DrawLatex(0.18, 0.89, "#font[62]{CMS}")

    latex_cms_wip = ROOT.TLatex()
    latex_cms_wip.SetNDC()
    latex_cms_wip.SetTextSize(0.0375)
    latex_cms_wip.DrawLatex(0.18, 0.85, "#font[42]{#it{Work in progress}}")


    latex_lumi = ROOT.TLatex()
    latex_lumi.SetNDC()
    latex_lumi.SetTextSize(0.0425)
    latex_lumi.SetTextFont(42)
    #latex_lumi.DrawLatex(0.7, 0.93, "138 fb^{-1} (13 TeV)")

    legend.Draw("same")


    output = f"limit_{channel}"
    canvas.SetLogx()
    canvas.SetLogy()
    if not os.path.exists("plotter/outputs/hists/limits/"):
        os.system("mkdir -p plotter/outputs/hists/limits/")
    if final:
        canvas.SaveAs(f"plotter/outputs/hists/limits/Obs_comparison_{output}_{model}.pdf")
        canvas.SaveAs(f"plotter/outputs/hists/limits/Obs_comparison_{output}_{model}.png")
    else:
        canvas.SaveAs(f"plotter/outputs/hists/limits/Exp_{output}_{model}.pdf")

def get_crossing_point(limits, channel, model):

    masses = list(limits.keys())

    left_mass = -1
    left_limit = -1
    right_mass = -1
    right_limit = -1
    for mass in masses :
        if (limits[mass]["Combined"]["50.0%"] < 1.0):
            left_mass = float(mass)
            left_limit = limits[mass]["Combined"]["50.0%"]

    masses.reverse()
    for mass in masses :
        if (limits[mass]["Combined"]["50.0%"] > 1.0):
            right_mass = float(mass)
            right_limit = limits[mass]["Combined"]["50.0%"]
    masses.reverse()

    this_mass = ((right_mass - left_mass) + (right_limit * left_mass - left_limit * right_mass)) / (right_limit - left_limit)

    print (f"{channel} {model} : Mixing 1.0 at {this_mass} GeV")

def main():

    for model in models:
        for channel in channels :
            if model == "Dirac" : continue

            #limits_exp, limits_obs = get_expected_limits(channel, model)
            for final in [True]:
                draw_limits(channel, model, final)
            #print ("Expected ===============")
            #get_crossing_point(limits_exp, channel, model)
            #print ("Observed ===============")
            #get_crossing_point(limits_obs, channel, model)

if __name__ == "__main__":

    main()
