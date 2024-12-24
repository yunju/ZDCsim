import sys
import math

import ROOT 
from ROOT import TFile
from ROOT import TH1D
from ROOT import TH2D
from ROOT import TH3D
from ROOT import TRotation
from ROOT import TVector3
from ROOT import TCanvas
from ROOT import TLine
from ROOT import TLatex
from ROOT import TTree

class SimHits:
  def __init__(self,cellID,energy,posX,posY,posZ):
    self.cellID  = cellID;
    self.energy  = energy;
    self.posX    = posX;
    self.posY    = posY;
    self.posZ    = posZ;


#PRINT=False
PRINT=True


#====== rotation fun ==================
def rotate_y(x, y, z, theta):

    #theta in radians
    x_new = x * math.cos(theta) + z * math.sin(theta)
    y_new = y
    z_new = -x * math.sin(theta) + z * math.cos(theta)
    return (x_new, y_new, z_new)

#===== give crystal ID =================

def getEcalID(x, y):

    xMin  = -1200
    xMax  = -600
    xStep = 30

    yMin  = -300
    yMax  = 300
    yStep = 30

    # Out of range
    if x < xMin or x > xMax or y < yMin or y > yMax:

        print("Error1 : hit position is out off range!")
        return -100  

    x_id = math.ceil( (x-xMin)/xStep ) 
    y_id = math.ceil( (y-yMin)/yStep )    
    cellID = 20* (y_id-1) + (x_id-1)
    #print(x, y, x_id, y_id, cellID)
    
    if cellID<0 or cellID>399:
        print("Error2 : hit position is out off range!")
        return -100
    
    return cellID


#======= read infile and intree ============
runN = sys.argv[1]
filename = f"test.root"
#filename = f"../eic/epic/gammaAtZDC_1GeVto20GeV/outfile_steering_gamma_atZDC_1GeVto20GeV_1000evt_run{runN}.root"
#filename = f"../eic/epic/outfile_steering_gamma_atZDC_1GeV_1000evt_spreadAngle.root"
#filename = f"../eic/epic/outfile_steering_gamma_atZDC_1GeV_1000evt.root"
print("infile: ", filename)


infile = TFile(filename, "read")
#infile.ls()

tree = infile.Get("events")
#tree.Print()

#*Br  186 :EcalFarForwardZDCHits : Int_t EcalFarForwardZDCHits_               *
#*Br  187 :EcalFarForwardZDCHits.cellID :                                     *
#*Br  188 :EcalFarForwardZDCHits.energy :                                     *
#*Br  189 :EcalFarForwardZDCHits.position.x :                                 *
#*Br  190 :EcalFarForwardZDCHits.position.y :                                 *
#*Br  191 :EcalFarForwardZDCHits.position.z :                                 *
#*Br  192 :EcalFarForwardZDCHits.contributions_begin :                        *
#*Br  193 :EcalFarForwardZDCHits.contributions_end :                          *
#*Br  194 :_EcalFarForwardZDCHits_contributions :                             *
#*Br  195 :_EcalFarForwardZDCHits_contributions.index :                       *
#*Br  196 :_EcalFarForwardZDCHits_contributions.collectionID :                *
#*Br  197 :EcalFarForwardZDCHitsContributions :                               *
#*Br  198 :EcalFarForwardZDCHitsContributions.PDG :                           *
#*Br  199 :EcalFarForwardZDCHitsContributions.energy :                        *
#*Br  200 :EcalFarForwardZDCHitsContributions.time :                          *
#*Br  201 :EcalFarForwardZDCHitsContributions.stepPosition.x :                *
#*Br  202 :EcalFarForwardZDCHitsContributions.stepPosition.y :                *
#*Br  203 :EcalFarForwardZDCHitsContributions.stepPosition.z :                *
#*Br  204 :_EcalFarForwardZDCHitsContributions_particle :                     *
#*Br  205 :_EcalFarForwardZDCHitsContributions_particle.index :               *
#*Br  206 :_EcalFarForwardZDCHitsContributions_particle.collectionID :        *
#*Br  341 :HcalFarForwardZDCHits : Int_t HcalFarForwardZDCHits_               *
#*Br  342 :HcalFarForwardZDCHits.cellID :                                     *
#*Br  343 :HcalFarForwardZDCHits.energy :                                     *
#*Br  344 :HcalFarForwardZDCHits.position.x :                                 *
#*Br  345 :HcalFarForwardZDCHits.position.y :                                 *
#*Br  346 :HcalFarForwardZDCHits.position.z :                                 *
#*Br  347 :HcalFarForwardZDCHits.contributions_begin :                        *
#*Br  348 :HcalFarForwardZDCHits.contributions_end :                          *
#*Br  349 :_HcalFarForwardZDCHits_contributions :                             *
#*Br  350 :_HcalFarForwardZDCHits_contributions.index :                       *
#*Br  351 :_HcalFarForwardZDCHits_contributions.collectionID :                *
#*Br  352 :HcalFarForwardZDCHitsContributions :                               *
#*Br  353 :HcalFarForwardZDCHitsContributions.PDG :                           *
#*Br  354 :HcalFarForwardZDCHitsContributions.energy :                        *
#*Br  355 :HcalFarForwardZDCHitsContributions.time :                          *
#*Br  356 :HcalFarForwardZDCHitsContributions.stepPosition.x :                *
#*Br  357 :HcalFarForwardZDCHitsContributions.stepPosition.y :                *
#*Br  358 :HcalFarForwardZDCHitsContributions.stepPosition.z :                *
#*Br  359 :_HcalFarForwardZDCHitsContributions_particle :                     *
#*Br  360 :_HcalFarForwardZDCHitsContributions_particle.index :               *
#*Br  361 :_HcalFarForwardZDCHitsContributions_particle.collectionID :        *


##=========== MCParticles info  ==============
#*Br  419 :MCParticles : Int_t MCParticles_                                   *
#*Br  420 :MCParticles.PDG : Int_t PDG[MCParticles_]                          *
#*Br  421 :MCParticles.generatorStatus : Int_t generatorStatus[MCParticles_]  *
#*Br  422 :MCParticles.simulatorStatus : Int_t simulatorStatus[MCParticles_]  *
#*Br  423 :MCParticles.charge : Float_t charge[MCParticles_]                  *
#*Br  424 :MCParticles.time : Float_t time[MCParticles_]                      *
#*Br  425 :MCParticles.mass : Double_t mass[MCParticles_]                     *
#*Br  426 :MCParticles.vertex.x : Double_t x[MCParticles_]                    *
#*Br  427 :MCParticles.vertex.y : Double_t y[MCParticles_]                    *
#*Br  428 :MCParticles.vertex.z : Double_t z[MCParticles_]                    *
#*Br  429 :MCParticles.endpoint.x : Double_t x[MCParticles_]                  *
#*Br  430 :MCParticles.endpoint.y : Double_t y[MCParticles_]                  *
#*Br  431 :MCParticles.endpoint.z : Double_t z[MCParticles_]                  *
#*Br  432 :MCParticles.momentum.x : Float_t x[MCParticles_]                   *
#*Br  433 :MCParticles.momentum.y : Float_t y[MCParticles_]                   *
#*Br  434 :MCParticles.momentum.z : Float_t z[MCParticles_]                   *
#*Br  435 :MCParticles.momentumAtEndpoint.x : Float_t x[MCParticles_]         *
#*Br  436 :MCParticles.momentumAtEndpoint.y : Float_t y[MCParticles_]         *
#*Br  437 :MCParticles.momentumAtEndpoint.z : Float_t z[MCParticles_]         *
#*Br  438 :MCParticles.spin.x : Float_t x[MCParticles_]                       *
#*Br  439 :MCParticles.spin.y : Float_t y[MCParticles_]                       *
#*Br  440 :MCParticles.spin.z : Float_t z[MCParticles_]                       *
#*Br  441 :MCParticles.colorFlow.a : Int_t a[MCParticles_]                    *
#*Br  442 :MCParticles.colorFlow.b : Int_t b[MCParticles_]                    *
#*Br  443 :MCParticles.parents_begin : UInt_t parents_begin[MCParticles_]     *
#*Br  444 :MCParticles.parents_end : UInt_t parents_end[MCParticles_]         *
#*Br  445 :MCParticles.daughters_begin : UInt_t daughters_begin[MCParticles_] *
#*Br  446 :MCParticles.daughters_end : UInt_t daughters_end[MCParticles_]     *
#*Br  447 :_MCParticles_parents : Int_t _MCParticles_parents_                 *
#*Br  448 :_MCParticles_parents.index : Int_t index[_MCParticles_parents_]    *
#*Br  449 :_MCParticles_parents.collectionID :                                *
#*Br  450 :_MCParticles_daughters : Int_t _MCParticles_daughters_             *
#*Br  451 :_MCParticles_daughters.index : Int_t index[_MCParticles_daughters_]*
#*Br  452 :_MCParticles_daughters.collectionID :                              *

#====================== define histogram ===========
h3_ecalHitPos = TH3D("h3_ecalHitPos", "h3_ecalHitPos", 
                        22*10, -1200-30, -600+30,     # posX                     
                        22*10, -300-30, 300+30,       # posY
                        100, 35710, 35740)            # posZ

h3_ecalHitPosRot = TH3D("h3_ecalHitPosRot", "h3_ecalHitPosRot", 
                        22*10, -300-30, 300+30,       # posX                     
                        22*10, -300-30, 300+30,       # posY
                        100, 225, 255)    

h3_ecalHitPosRotEnergy = TH3D("h3_ecalHitPosRotEnergy", "h3_ecalHitPosRotEnergy", 
                              100, -400, 400,   
                              100, -400, 400,   
                              100, 225, 255)    


h2_ecalHitPos2 = TH2D("h2_ecalHitPos2", "h2_ecalHitPos2", 
                      22*10, -1200-30, -600+30,     # posX                     
                      22*10, -300-30, 300+30)       # posY


h1_ecalratio = TH1D("h1_ecalratio", "h1_ecalratio", 20, 0, 1)
h1_hcalratio = TH1D("h1_hcalratio", "h1_hcalratio", 20, 0, 1)
h1_zdcratio = TH1D("h1_zdcratio", "h1_zdcratio", 20, 0, 1)



#========== outfile  and outtree =============================
outfilename = f"myTree_test.root"
#outfilename = f"../eic/epic/gammaAtZDC_1GeVto20GeV/myTree_steering_gamma_atZDC_1GeVto20GeV_1000evt_run{runN}.root"
outfile = TFile(outfilename, "RECREATE")
print("outfile : ", outfile.GetName())

myTree = TTree("myTree", "MyTree")


ecal_cellID  = ROOT.std.vector('int')()
ecal_energy  = ROOT.std.vector('double')()
ecal_posX    = ROOT.std.vector('double')()
ecal_posY    = ROOT.std.vector('double')()
ecal_posZ    = ROOT.std.vector('double')()

hcal_cellID  = ROOT.std.vector('float')()
hcal_energy  = ROOT.std.vector('double')()
hcal_posX    = ROOT.std.vector('double')()
hcal_posY    = ROOT.std.vector('double')()
hcal_posZ    = ROOT.std.vector('double')()

mcPar_PDG    = ROOT.std.vector('int')()
mcPar_mass   = ROOT.std.vector('double')()
mcPar_momX   = ROOT.std.vector('double')()
mcPar_momY   = ROOT.std.vector('double')()
mcPar_momZ   = ROOT.std.vector('double')()
mcPar_energy = ROOT.std.vector('double')()


myTree.Branch("ecal_cellID" , ecal_cellID )
myTree.Branch("ecal_energy" , ecal_energy )
myTree.Branch("ecal_posX"   , ecal_posX   )
myTree.Branch("ecal_posY"   , ecal_posY   )
myTree.Branch("ecal_posZ"   , ecal_posZ   )

myTree.Branch("hcal_cellID" , hcal_cellID )
myTree.Branch("hcal_energy" , hcal_energy )
myTree.Branch("hcal_posX"   , hcal_posX   )
myTree.Branch("hcal_posY"   , hcal_posY   )
myTree.Branch("hcal_posZ"   , hcal_posZ   )

myTree.Branch("mcPar_PDG"   , mcPar_PDG   )
myTree.Branch("mcPar_mass"  , mcPar_mass  )
myTree.Branch("mcPar_momX"  , mcPar_momX  )
myTree.Branch("mcPar_momY"  , mcPar_momY  )
myTree.Branch("mcPar_momZ"  , mcPar_momZ  )
myTree.Branch("mcPar_energy", mcPar_energy)



##===================== loop events ================
#for ievent in range(0, 10): 
for ievent in range(tree.GetEntries()):

#reset tree
    ecal_cellID .clear()
    ecal_energy .clear()
    ecal_posX   .clear()
    ecal_posY   .clear()
    ecal_posZ   .clear()

    hcal_cellID .clear()
    hcal_energy .clear()
    hcal_posX   .clear()
    hcal_posY   .clear()
    hcal_posZ   .clear()

    mcPar_PDG   .clear()
    mcPar_mass  .clear()
    mcPar_momX  .clear()
    mcPar_momY  .clear()
    mcPar_momZ  .clear()
    mcPar_energy.clear()


# read tree
    tree.GetEntry(ievent)
    
    if(PRINT):
        print("--------------------",
              f"Event#{ievent:4.0f}",
              "--------------------")
    
#- EcalHits
    EcalHits  = tree.EcalFarForwardZDCHits
    nHit_Ecal = EcalHits.size()
    sumEcalenergy = 0 

    
    
    if(PRINT): 
        print(f"----------> Ecal nHits {nHit_Ecal:2.0f}")

    if(nHit_Ecal>0):

        vector_ecal = []

        for ihit_Ecal in range(0, nHit_Ecal):

            #- get data
            EcalHits_cell   = EcalHits[ihit_Ecal].cellID
            EcalHits_energy = EcalHits[ihit_Ecal].energy
            EcalHits_posX   = EcalHits[ihit_Ecal].position.x
            EcalHits_posY   = EcalHits[ihit_Ecal].position.y
            EcalHits_posZ   = EcalHits[ihit_Ecal].position.z
            sumEcalenergy   +=EcalHits_energy
            #EcalHits_conB   = EcalHits[ihit_Ecal].contributions_begin #?
            #EcalHits_conE   = EcalHits[ihit_Ecal].contributions_end   #?  
            
            ##- rotate hits  
            #theta = 0.025 #in radiance
            #gunPosX, gunPosY, gunPosZ = 35500*math.sin(-0.025), 0, 35500*math.cos(-0.025)
            #x, y, z = EcalHits_posX-gunPosX, EcalHits_posY-gunPosY, EcalHits_posZ-gunPosZ 
            #x_rot, y_rot, z_rot = rotate_y(x, y, z, theta)
            

            #- save in hist
            h3_ecalHitPos.Fill(EcalHits_posX, EcalHits_posY, EcalHits_posZ)
            h2_ecalHitPos2.Fill(EcalHits_posX, EcalHits_posY)            
            #h3_ecalHitPosRot.Fill(x_rot, y_rot, z_rot)
            #h3_ecalHitPosRotEnergy.Fill(x_rot, y_rot, z_rot, EcalHits_energy)
            
            
            #- get crystal id
            ecalID = getEcalID(EcalHits_posX, EcalHits_posY)

            #- save info in vector so that later to sort
            vector_ecal.append([EcalHits_energy, EcalHits_posX, EcalHits_posY, EcalHits_posZ, ecalID])

    # sort hits by its energy
    sort_vector_ecal = sorted(vector_ecal , key=lambda x: x[0], reverse=True)
    tmp_ecal_cellID = [point[4] for point in sort_vector_ecal] 
    tmp_ecal_energy = [point[0] for point in sort_vector_ecal]
    tmp_ecal_posX   = [point[1] for point in sort_vector_ecal]
    tmp_ecal_posY   = [point[2] for point in sort_vector_ecal]
    tmp_ecal_posZ   = [point[3] for point in sort_vector_ecal]

    # save hit after sort
    for ihit in range(len(sort_vector_ecal)):
              
        ecal_cellID.push_back(tmp_ecal_cellID[ihit])
        ecal_energy.push_back(tmp_ecal_energy[ihit])
        ecal_posX.push_back(tmp_ecal_posX[ihit])
        ecal_posY.push_back(tmp_ecal_posY[ihit])
        ecal_posZ.push_back(tmp_ecal_posZ[ihit])
        
        if PRINT:
            print(f"ECal Hit#{ihit:3.0f}",
                  f"| cellID {ecal_cellID[ihit]:5.0f}",
                  #f"| Energy {(ecal_energy[ihit]/0.05)*100:5.2f}",           
                  f"| Energy {ecal_energy[ihit]:5.3f}",           
                  f"| pos {tmp_ecal_posX[ihit]:8.2f} {tmp_ecal_posX[ihit]:7.2f} {tmp_ecal_posZ[ihit]:6.2f}",
                  "")


##- EcalHits : info doesn't seem to be useful
#    EcalHitsCon  = tree.EcalFarForwardZDCHitsContributions
#    nHit_EcalCon = EcalHitsCon.size()
#    if(PRINT):
#        print(f"EcalCon nHits {nHit_EcalCon:2.0f}")
#    if(nHit_EcalCon>0):
#        for ihit_EcalCon in range(0, nHit_EcalCon):
#            
#            EcalHitsCon_PDG    = EcalHitsCon[ihit_EcalCon].PDG
#            EcalHitsCon_energy = EcalHitsCon[ihit_EcalCon].energy
#            EcalHitsCon_time   = EcalHitsCon[ihit_EcalCon].time
#            EcalHitsCon_stepX  = EcalHitsCon[ihit_EcalCon].stepPosition.x
#            EcalHitsCon_stepY  = EcalHitsCon[ihit_EcalCon].stepPosition.y
#            EcalHitsCon_stepZ  = EcalHitsCon[ihit_EcalCon].stepPosition.z
#
#            if(PRINT):
#                print(f"ECalHitsCon Hit#{ihit_EcalCon:.0f}",
#                      f"| PDG {EcalHitsCon_PDG:3.0f}",  #always 0? absence of particle
#                      f"| energy {EcalHitsCon_energy:.2e}",  
#                      f"| time {EcalHitsCon_time:8.2f}",   
#                      f"| step {EcalHitsCon_stepX:8.2f} {EcalHitsCon_stepY:8.2f} {EcalHitsCon_stepZ:8.2f}", #step = 0 always
#                      "")
#            
#


#- HcalHits
    HcalHits  = tree.HcalFarForwardZDCHits
    nHit_Hcal = HcalHits.size()
    HcalSimList = [] 
    sumHcalenergy = 0 
    if(PRINT): 
        print(f"----------> Hcal nHits {nHit_Hcal:2.0f}")

    if(nHit_Hcal>0):

        vector_hcal = []

        for ihit_Hcal in range(0, nHit_Hcal):

            #- get data
            HcalHits_cell   = HcalHits[ihit_Hcal].cellID
            HcalHits_energy = HcalHits[ihit_Hcal].energy
            HcalHits_posX   = HcalHits[ihit_Hcal].position.x
            HcalHits_posY   = HcalHits[ihit_Hcal].position.y
            HcalHits_posZ   = HcalHits[ihit_Hcal].position.z
            sumHcalenergy   += HcalHits_energy 
            Hcalsim= SimHits(int(HcalHits[ihit_Hcal].cellID),float(HcalHits[ihit_Hcal].energy),float(HcalHits[ihit_Hcal].position.x),float(HcalHits[ihit_Hcal].position.y),float(HcalHits[ihit_Hcal].position.z)) 
            HcalSimList.append(Hcalsim)

            print(f"Hcal",
              f"| cellID {HcalHits_cell}",
              f"| energy {HcalHits_energy}")  
   #         #- save in hist
   #         h3_hcalHitPos.Fill(HcalHits_posX, HcalHits_posY, HcalHits_posZ)
   #         h2_hcalHitPos2.Fill(HcalHits_posX, HcalHits_posY)            
   #            
   #        #- get crystal id
   #        hcalID = getHcalID(HcalHits_posX, HcalHits_posY)
   #
   #        #- save info in vector so that later to sort
   #        vector_hcal.append([HcalHits_energy, HcalHits_posX, HcalHits_posY, HcalHits_posZ, hcalID])
   #
   ## sort hits by its energy
   #sort_vector_hcal = sorted(vector_hcal , key=lambda x: x[0], reverse=True)
   #tmp_hcal_cellID = [point[4] for point in sort_vector_hcal] 
   #tmp_hcal_energy = [point[0] for point in sort_vector_hcal]
   #tmp_hcal_posX   = [point[1] for point in sort_vector_hcal]
   #tmp_hcal_posY   = [point[2] for point in sort_vector_hcal]
   #tmp_hcal_posZ   = [point[3] for point in sort_vector_hcal]
   #
   ## save hit after sort
   #for ihit in range(len(sort_vector_hcal)):
   #          
   #    hcal_cellID.push_back(tmp_hcal_cellID[ihit])
   #    hcal_energy.push_back(tmp_hcal_energy[ihit])
   #    hcal_posX.push_back(tmp_hcal_posX[ihit])
   #    hcal_posY.push_back(tmp_hcal_posY[ihit])
   #    hcal_posZ.push_back(tmp_hcal_posZ[ihit])
   #    
   #    if PRINT:
   #        print(f"Hcal Hit#{ihit:3.0f}",
   #              f"| cellID {hcal_cellID[ihit]:5.0f}",
   #              #f"| Energy {(hcal_energy[ihit]/0.05)*100:5.2f}",           
   #              f"| Energy {hcal_energy[ihit]:5.3f}",           
   #              f"| pos {tmp_hcal_posX[ihit]:8.2f} {tmp_hcal_posX[ihit]:7.2f} {tmp_hcal_posZ[ihit]:6.2f}",
   #              "")
   # sort Hcal
    new_Hcallist = sorted(HcalSimList, key=lambda x: x.energy, reverse=True)
    for ihit in range(len(new_Hcallist)):
        hcal_cellID.push_back(new_Hcallist[ihit].cellID)
        hcal_energy.push_back(new_Hcallist[ihit].energy)
        hcal_posX.push_back(new_Hcallist[ihit].posX)
        hcal_posY.push_back(new_Hcallist[ihit].posY)
        hcal_posZ.push_back(new_Hcallist[ihit].posZ)


    if(PRINT): 
        for ihit_Hcal in range(0, nHit_Hcal):
            print(f"Hcal lsit:{HcalSimList[ihit_Hcal].cellID}"
                f"| energy {HcalSimList[ihit_Hcal].energy}"  
                f"| X {HcalSimList[ihit_Hcal].posX:8.2f}"  
                f"| Y {HcalSimList[ihit_Hcal].posY:8.2f}"  
                f"| Z {HcalSimList[ihit_Hcal].posZ:8.2f}")  

        for ihit_Hcal in range(0, nHit_Hcal):
            print(f"Hcal order lsit:{new_Hcallist[ihit_Hcal].cellID}"
                f"| energy {new_Hcallist[ihit_Hcal].energy}"  
                f"| X {new_Hcallist[ihit_Hcal].posX:8.2f}"  
                f"| Y {new_Hcallist[ihit_Hcal].posY:8.2f}"  
                f"| Z {new_Hcallist[ihit_Hcal].posZ:8.2f}")  
#- MCparticles (gun, always only one)
    MCpar  = tree.MCParticles
    if(PRINT): 
        print(f"----------> nMCpar 1")

    MCpar_PDG    = MCpar[0].PDG
    MCpar_genSta = MCpar[0].generatorStatus
    MCpar_simSta = MCpar[0].simulatorStatus
    MCpar_charge = MCpar[0].charge
    MCpar_time   = MCpar[0].time
    MCpar_mass   = MCpar[0].mass
    MCpar_vtxX   = MCpar[0].vertex.x
    MCpar_vtxY   = MCpar[0].vertex.y
    MCpar_vtxZ   = MCpar[0].vertex.z
    MCpar_endPX  = MCpar[0].endpoint.x
    MCpar_endPY  = MCpar[0].endpoint.y
    MCpar_endPZ  = MCpar[0].endpoint.z
    MCpar_momX   = MCpar[0].momentum.x
    MCpar_momY   = MCpar[0].momentum.y
    MCpar_momZ   = MCpar[0].momentum.z
    MCpar_momEPX = MCpar[0].momentumAtEndpoint.x
    MCpar_momEPY = MCpar[0].momentumAtEndpoint.y
    MCpar_momEPZ = MCpar[0].momentumAtEndpoint.z
    MCpar_spinX  = MCpar[0].spin.x
    MCpar_spinY  = MCpar[0].spin.y
    MCpar_spinZ  = MCpar[0].spin.z
    MCpar_colorA = MCpar[0].colorFlow.a
    MCpar_colorB = MCpar[0].colorFlow.b
    MCpar_parB   = MCpar[0].parents_begin   
    MCpar_parE   = MCpar[0].parents_end
    MCpar_dauB   = MCpar[0].daughters_begin 
    MCpar_dauE   = MCpar[0].daughters_end  
    MCpar_mom    = math.sqrt(MCpar_momX**2 + MCpar_momY**2 + MCpar_momZ**2)
    MCpar_energy = math.sqrt(MCpar_mass**2 + MCpar_mom**2)
    
    #-save to tree
    mcPar_PDG   .push_back(MCpar_PDG)
    mcPar_mass  .push_back(MCpar_mass)
    mcPar_momX  .push_back(MCpar_momX)
    mcPar_momY  .push_back(MCpar_momY)
    mcPar_momZ  .push_back(MCpar_momZ)
    mcPar_energy.push_back(MCpar_energy)

    if(PRINT):
        print(f"MCpar#1",
              f"| PDG {MCpar_PDG:5.0f}",  #PDG=22, gamma
              f"| energy {MCpar_energy:5.3f}"
              #f"| genSta {MCpar_genSta:1.0f}", 
              #f"| simSta {MCpar_simSta:8.0f}", 
              f"| charge {MCpar_charge:2.0f}",  
              f"| time {MCpar_time:.2f}", 
              f"| mass {MCpar_mass:.2f}", 
              f"| vtx {MCpar_vtxX:6.2f} {MCpar_vtxY:4.2f} {MCpar_vtxZ:8.2f}", 
              f"| endP {MCpar_endPX:6.2f} {MCpar_endPY:4.2f} {MCpar_endPZ:8.2f}", 
              f"| Mom {MCpar_momX:5.3f} {MCpar_momY:4.2f} {MCpar_momZ:4.2f}", 
              f"| MomEP {MCpar_momEPX:5.3f} {MCpar_momEPY:4.2f} {MCpar_momEPZ:4.2f}", 
              #f"| spin {MCpar_spinX:.2f} {MCpar_spinY:.2f} {MCpar_spinZ:.2f}", 
              #f"| color {MCpar_colorA} {MCpar_colorB}", 
              #f"| parent {MCpar_parB} {MCpar_parE}", 
              #f"| daughter {MCpar_dauB} {MCpar_dauE}",
              "")  
    if(PRINT): 
        print(f"----------> Ecal sum {sumEcalenergy}")
        print(f"----------> Ecal ratio {sumEcalenergy/MCpar_energy}")
        print(f"----------> Hcal sum {sumHcalenergy}")
        print(f"----------> Hcal ratio {sumHcalenergy/MCpar_energy}")
    h1_ecalratio.Fill(sumEcalenergy/MCpar_energy)
    h1_hcalratio.Fill(sumHcalenergy/MCpar_energy)
    h1_zdcratio.Fill((sumHcalenergy+sumEcalenergy)/MCpar_energy)
    myTree.Fill()

#========= projected histogram ==================

#- before rotation
h2_ecalHitPos_XY = h3_ecalHitPos.Project3D("xy")
h1_ecalHitPos_X  = h3_ecalHitPos.Project3D("x")
h1_ecalHitPos_Y  = h3_ecalHitPos.Project3D("y")

##- after rotation
#h2_ecalHitPosRot_XY = h3_ecalHitPosRot.Project3D("xy")
#h1_ecalHitPosRot_X  = h3_ecalHitPosRot.Project3D("x")
#h1_ecalHitPosRot_Y  = h3_ecalHitPosRot.Project3D("y")

##- after rotation, w/ energy weight
#h2_ecalHitPosRotEnergy_XY = h3_ecalHitPosRotEnergy.Project3D("xy")
#h1_ecalHitPosRotEnergy_X  = h3_ecalHitPosRotEnergy.Project3D("x")
#h1_ecalHitPosRotEnergy_Y  = h3_ecalHitPosRotEnergy.Project3D("y")


#========= cry tline on crystal ============
c = TCanvas("c", "c", 600,600)

c.cd()
h2_ecalHitPos_XY.SetStats(0) 
h2_ecalHitPos_XY.Draw("colz")

line = TLine(-300, -1200, -300, -600)
line.SetLineColor(2)

for x in range(-300, 300+1, 30):
    line.DrawLine(x, -1200, x, -600)

for y in range(-1200, -600+1, 30):
    line.DrawLine(-300, y, 300, y)


latex = TLatex()
latex.SetTextSize(0.02)
latex.SetTextColor(2)

for ix in range(-1200, -600, 30):
    for iy in range(-300, 300, 30):

        x_id = math.ceil( (ix+1200)/30 ) 
        y_id = math.ceil( (iy+300) /30 )    
        cellID = 20* y_id + x_id
        
        latex.DrawLatex(iy, ix, str(cellID))
        
        #print(ix, iy, x_id, y_id, cellID)
        

##========= crystal ID ============
#c2 = TCanvas("c2", "c2", 600,600)
#
#c2.cd()
#h2_ecalHitPosRot_XY.Draw("colz")
#
#line2 = TLine(-300, -300, -300, -300)
#line2.SetLineColor(2)
#
#for x in range(-300, 300+1, 30):
#    line2.DrawLine(x, -300, x, 300)
#
#for y in range(-300, 300+1, 30):
#    line2.DrawLine(-300, y, 300, y)


#========= cry tline on crystal ============
c3 = TCanvas("c3", "c3", 600, 600)

c3.cd()
h2_ecalHitPos2.SetStats(0) 
h2_ecalHitPos2.Draw("colz")
h2_ecalHitPos2.GetXaxis().SetTitle("x(mm)")
h2_ecalHitPos2.GetYaxis().SetTitle("y(mm)")

line3 = TLine(-300, -1200, -300, -600)
line3.SetLineColor(2)

for x in range(-1200, -600+1, 30):
    line3.DrawLine(x, -300, x, 300)

for y in range(-300, 300+1, 30):
    line3.DrawLine(-1200, y, -600, y)
    
for ix in range(-1200, -600, 30):
    for iy in range(-300, 300, 30):
        x_id = math.ceil( (ix+1200)/30 ) 
        y_id = math.ceil( (iy+300) /30 )    
        cellID = 20* y_id + x_id
        latex.DrawLatex(ix, iy, str(cellID))
        
     
#========== save output ===========
outfile.cd()

#- before rotation
#h3_ecalHitPos   .Write()
#h2_ecalHitPos_XY.Write()
#h1_ecalHitPos_X .Write()
#h1_ecalHitPos_Y .Write() 
#
##- after roation 
#h3_ecalHitPosRot   .Write()
#h2_ecalHitPosRot_XY.Write()
#h1_ecalHitPosRot_X .Write()
#h1_ecalHitPosRot_Y .Write() 
#
##- after roation, w/ energy weight 
#h3_ecalHitPosRotEnergy   .Write()
#h2_ecalHitPosRotEnergy_XY.Write()
#h1_ecalHitPosRotEnergy_X .Write()
#h1_ecalHitPosRotEnergy_Y .Write() 
#
##- canvas
#c.Write()
#c2.Write()
#c3.Write()
h1_ecalratio.Write()
h1_hcalratio.Write()
h1_zdcratio.Write()
h3_ecalHitPos.Write()
h2_ecalHitPos2.Write()
c3.Write()
myTree.Write()
outfile.Close()

