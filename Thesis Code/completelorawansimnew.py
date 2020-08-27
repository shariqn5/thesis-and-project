from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super,
         filter, map, zip)
import simpy
import random
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import json
import time
import six
from six.moves import html_parser
import statistics
import simpy.rt

sf7 = np.array([7,-126.5,-124.25])
sf8 = np.array([8,-129,-126.75])
sf9 = np.array([9,-131.5,-128.25])
sf10 = np.array([10,-134,-130.25])
sf11 = np.array([11,-136.5,-132.75])
sf12 = np.array([12,-139.5,-132.25])
## spreading factor sensitivity
sensi = np.array([sf7,sf8,sf9,sf10,sf11,sf12])
full_collision = False
graphics = 0


def checkcollision(packet):
    col = 0 # flag needed since there might be several collisions for packet
    # lost packets don't collide
    if packet.lost:
       return 0
    if packetsAtBS[packet.bs]:
        for other in packetsAtBS[packet.bs]:
            if (other.id != packet.nodeid) :
               # simple collision
               if sfCollision(packet, other.packet[packet.bs]):
                   
                   
                    packet.collided = 1
                    other.packet[packet.bs].collided = 1  # other also got lost, if it wasn't lost already
                    col = 1
        return col
    return 0

#
# frequencyCollision, conditions
#

#        |f1-f2| <= 60 kHz if f1 or f2 has bw 250
#        |f1-f2| <= 30 kHz if f1 or f2 has bw 125
def frequencyCollision(p1,p2):
    
    if (abs(p1.freq-p2.freq)<=60 and (p1.bw==250 or p2.freq==250)):
        return True
    else:
        if (abs(p1.freq-p2.freq)<=30):
            return True
    return False

def sfCollision(p1, p2):
    print(p1.sf)
    print("node",p1.nodeid)
    print(p2.sf)
    print("node",p2.nodeid)
    if (p1.sf == p2.sf) and (p1.channel==p2.channel):
        print("sf collided")
        # p2 may have been lost too, will be marked by other checks
        return True
        

    return False


def airtime(sf,cr,pl,bw):
    H = 0        # implicit header disabled (H=0) or not (H=1)
    DE = 0       # low data rate optimization enabled (=1) or not (=0)
    Npream = 8   # number of preamble symbol (12.25  from Utz paper)

    if bw == 125 and sf in [11, 12]:
        # low data rate optimization mandated for BW125 with SF11 and SF12
        DE = 1
    if sf == 6:
        # can only have implicit header with SF6
        H = 1

    Tsym = (2.0**sf)/bw
    Tpream = (Npream + 4.25)*Tsym
    payloadSymbNB = 8 + max(math.ceil((8.0*pl-4.0*sf+28+16-20*H)/(4.0*(sf-2*DE)))*(cr+4),0)
    Tpayload = payloadSymbNB * Tsym
    return Tpream + Tpayload



class myBS():
    def __init__(self, id,BSX,BSY):
        self.id = id
        
        self.bsx=BSX
        self.bsy=BSY

        


        print ('bsnode %d' %self.id,"BSx:", self.bsx, "BSy:", self.bsy)

        global graphics
        if (graphics):
            global ax
            # XXX should be base station position
            ax.add_artist(plt.Circle((self.bsx, self.bsy), 3, fill=True, color='green'))
            ax.add_artist(plt.Circle((self.bsx, self.bsy), 20, fill=False, color='green'))





class myNode():
    def __init__(self, id, packetlen,xloction,ylocation,height):
        self.id = id
        # self.period = period
        self.dist = []
        self.packet = []
        self.x = xloction
        self.y = ylocation
        self.height =height
        global counter
        self.spread=random.randint(7,12)
        self.period=random.choice(avg)








        if (experiment==3) or (experiment==4) or(experiment==2):
            if a==[]:
                self.spread==self.spread
            else:
                self.spread=checksf(a)


        if (experiment==3) :
            nodelist.append(self.id)
            if len(nodelist)>6:
                nodelist.clear()
                counter=counter+1
                nodelist.append(self.id)
            if counter==8:
                counter=0



        global nrBS
        for i in range(0,nrBS):
            d = np.sqrt((self.x-bs[i].bsx)*(self.x-bs[i].bsx)+(self.y-bs[i].bsy)*(self.y-bs[i].bsy))
            self.dist.append(d)
            if sys.argv[1] == 'fixed':
                self.packet.append(myPacket(self.id, packetlen, self.dist[i],self.height, i,bsminheight[i],self.spread))
            elif sys.argv[1] == 'notfixed':
                self.packet.append(myPacket(self.id, packetlen, self.dist[i],self.height, i,bsavgheight[i],self.spread))


           
        

        print('node %d' %id, "x", self.x, "y", self.y, "dist: ", self.dist,self.height)
      

        self.sent = 0




class myPacket():
    def __init__(self, nodeid, plen, distance,height,bs,bsheight,sf):
        global experiment
        global Ptx
        global gamma
        global d0
        global var
        global Lpld0
        global GL

        self.nodeid = nodeid
        self.height=height
        # self.freq = random.choice(frequency)
        self.dist=distance
        self.bs=bs
        self.bsheight=bsheight
        self.freq = random.choice(frequency)
        self.sf=sf
        self.cr=0
        self.bw=0
        # self.cr = random.randint(1,4)
        # self.bw = random.choice([sensor["min_bw"],sensor["max_bw"]])

        # for certain experiments override these
        if experiment==1 or experiment == 0:
            self.sf = spreadingfactor
            self.cr = 1
            self.bw = sensor["min_bw"]

            self.freq=frequency[0]
            self.channel=mychannel(self.freq,self.bw)

        # # # for certain experiments override these
        if experiment==2:
           
            self.cr = 1
            self.bw = sensor["min_bw"]
            self.freq=frequency[0]
            self.channel=mychannel(self.freq,self.bw)
        # # # lorawan
        if experiment == 3:
            self.bw = sensor["min_bw"]
            self.cr = 1
            if counter==0:
                self.freq=frequency[0]
                self.channel=1
                print("channel1")
            elif counter==1:
                self.freq=frequency[1]
                self.channel=2
                print("channel2")
            elif counter==2:
                self.freq=frequency[2]
                self.channel=3
                print("channel3")
            elif counter ==3:
                self.freq=frequency[3]
                self.channel=4
                print("channel4")
            elif counter==4:
                self.freq=frequency[4]
                self.channel=5
                print("channel5")
            elif counter==5:
                self.freq=frequency[5]
                self.channel=6
                print("channel6")
            elif counter==6:
                self.freq=frequency[6]
                self.channel=7
                print("channel7")
            elif counter==7:
                self.freq=frequency[7]
                self.channel=8
                print("channel8")


        if experiment == 4:
            self.bw = sensor["min_bw"]
            self.cr = 1
            self.freq = random.choice(frequency)
            self.channel=mychannel(self.freq,self.bw)


        if experiment == 3 or experiment == 4:
            if self.sf==7:
                self.subchannel=1
            elif self.sf==8:
                self.subchannel=2
            elif self.sf==9:
                self.subchannel=3
            elif self.sf==10:
                self.subchannel=4
            elif self.sf==11:
                self.subchannel=5
            elif self.sf==12:
                self.subchannel=6






        




        self.txpow = random.choice(range(sensor["min_transmit_power"],sensor["max_transmit_power"]))
        # self.txpow = random.choice(range(sensor["sensor_configuration"]["min_transmit_power"],sensor["sensor_configuration"]["max_transmit_power"]))

        print(self.txpow)

        # randomize configuration values
        # self.sf = random.randint(7,12)
        # self.sf=12
        self.sensor_antenna_gain=random.choice(range(sensor["min_antenna_gain"],sensor["max_antenna_gain"]))
        self.basestation_antenna_gain=random.choice(range(data["simulation"]["basestation_configuration"]["min_antenna_gain"],data["simulation"]["basestation_configuration"]["max_antenna_gain"]))

        



        print('node %d' %nodeid, "bs", self.bs, "freq", self.freq,"bw", self.bw,"cr", self.cr,"sf", self.sf, "dist: ", self.dist,self.height,self.bsheight)
        # self.bw = random.choice([sensor["sensor_configuration"]["min_bw"],sensor["sensor_configuration"]["max_bw"]])
        # self.bw=125
        # self.channel=mychannel(self.freq,self.bw,self.sf)
        ## Cost 231 pathloss calculations
        ruralareachecking=areacheck(self.bsheight)
        
        a=69.55+26.16*math.log10(int(self.freq))-13.83*math.log10(int(self.bsheight))
        b=(44.9-6.55*math.log10(self.bsheight))
        if ruralareachecking==True:
            ah=((1.1*math.log10(self.freq)-0.7)*self.height)-(1.56*math.log10(self.freq)-0.8)
            at=a-ah
            pathloss3=at+b*math.log10(int(self.dist))
            print(pathloss3)
        else:
            ah=(3.20*(math.log10(11.75*self.height))**2)-4.97
            at=a-ah
            pathloss3=at+b*math.log10(int(self.dist))+3
            print(pathloss3)


         
        
        
        ## link budgeting and resetting antenna gains to avoid packet loss
        
        if (self.sf>9) :
            if (pathloss3<=124):
                Prx=self.txpow-pathloss3+self.sensor_antenna_gain+self.basestation_antenna_gain 
            elif(124<pathloss3<160):
                Prx=sensor["max_transmit_power"]-pathloss3+sensor["max_antenna_gain"]+data["simulation"]["basestation_configuration"]["max_antenna_gain"]
            elif(pathloss3>=160):
                Prx=sensor["max_transmit_power"]-pathloss3+sensor["max_antenna_gain"]+9+data["simulation"]["basestation_configuration"]["max_antenna_gain"]+3

        else :
           Prx=sensor["max_transmit_power"]-pathloss3+sensor["max_antenna_gain"]+9+data["simulation"]["basestation_configuration"]["max_antenna_gain"]+9
          

           
       

        
        # print(self.freq)
        print(pathloss3)
        print(Prx)

        

#        
#             

        # transmission range, needs update XXX
        # self.transRange = 150
        self.pl = plen
        self.symTime = (2.0**self.sf)/self.bw
        self.arriveTime = 0
        self.rssi = Prx

        print ("frequency" ,self.freq, "symTime ", self.symTime)
        print ("bw", self.bw, "sf", self.sf, "cr", self.cr, "rssi", self.rssi)
        self.rectime = airtime(self.sf,self.cr,self.pl,self.bw)
        # self.channel= mychannel(self.freq,self.bw,self.sf)
        print ("rectime node ", self.nodeid, "  ", self.rectime)
    


        print ("frequency" ,self.freq, "symTime ", self.symTime)
        sensitivity = sensi[self.sf- 7, [125,250].index(self.bw) + 1]
#         # denote if packet is collided
        self.collided = 0
        self.processed = 0
        self.lost = self.rssi < sensitivity

## channel assignment for exxperiment 4
def mychannel(freq,bw):
    if ((freq==868.1) and(bw==125)):
        x=1
        
        print("channel 1")
    elif((freq==868.3) and(bw==125)):
        print("channel 2")
        x=2
        
        if((sf==7) and(bw==250)):
            print("channel 2")
                

    elif((freq==868.5) and(bw==125)):
        print("channel 3")
        x=3
        
            
    elif((freq==867.1) and(bw==125)):
        print("channel 4")
        x=4
        
            
    elif((freq==867.3) and(bw==125)):
        print("channel 5")
        x=5
        
            
    elif((freq==867.5) and(bw==125)):
        print("channel 6")
        x=6
        
            
    elif((freq==867.7) and(bw==125)):
        print("channel 7")
        x=7
        
            
    elif((freq==867.9) and(bw==125)):
        print("channel 8")
        x=8
    return x    
        




def transmit(env,node):
    while True:
        yield env.timeout(random.expovariate(1.0/float(node.period)))

        # time sending and receiving
        # packet arrives -> add to base station

        node.sent = node.sent + 1
        
        global packetSeq
        packetSeq = packetSeq + 1

        global nrBS
        for bs in range(0,nrBS):
           if (node in packetsAtBS[bs]):
                print ("ERROR: packet already in")
           else:
                # adding packet if no collision
                if (checkcollision(node.packet[bs])==1):
                    node.packet[bs].collided = 1
                    
                   
                else:
                    node.packet[bs].collided = 0
                packetsAtBS[bs].append(node)
                node.packet[bs].addTime = env.now
                node.packet[bs].seqNr = packetSeq

        # take first packet rectime
        yield env.timeout(node.packet[0].rectime)

        # if packet did not collide, add it in list of received packets
        # unless it is already in
        for bs in range(0, nrBS):
            if node.packet[bs].lost:
                lostPackets.append(node.packet[bs].seqNr)
            else:
                if node.packet[bs].collided == 0:
                    packetsRecBS[bs].append(node.packet[bs].seqNr)
                    if (recPackets):
                        if (recPackets[-1] != node.packet[bs].seqNr):
                            recPackets.append(node.packet[bs].seqNr)
                    else:
                        recPackets.append(node.packet[bs].seqNr)
                # else:
                #     if (collidedPackets):
                #         if (collidedPackets[-1] != node.packet[bs].seqNr):
                #             collidedPackets.append(node.packet[bs].seqNr)
                else:
                    # XXX only for debugging
                    collidedPackets.append(node.packet[bs].seqNr)
                            


                    

        # complete packet has been received by base station
        # can remove it
        for bs in range(0, nrBS):
            if (node in packetsAtBS[bs]):
                packetsAtBS[bs].remove(node)
                # reset the packet
                node.packet[bs].collided = 0
                node.packet[bs].processed = 0

## function for storing spreadingfactor auto assigned to node            
def sf(node):
    
    return node.spread
## function to ensure each node gets a unique spreding factor    
def checksf(a):
    if len(a)==6:
        newa=a[5]
        a.clear()
        
        difference = np.setdiff1d(spf,a,assume_unique=True)
        y=random.choice(difference)
    else:
        difference = np.setdiff1d(spf,a,assume_unique=True)
        # print(difference)
        y=random.choice(difference)
    

    return y

## area check for rural and metropolitan
def areacheck(i):
    
  for k in rural:
      if i==k:
          a=rural.remove(i)
          return True

nodes=[]
packetsAtBS = []
env = simpy.Environment()
# env = simpy.rt.RealtimeEnvironment(factor=0.5)           


bsx=[]
different=[]

bsy=[]
bs=[]
rural=[]
nodelist=[]
metropolitan=[]
sensor_height=[]
bsminheight=[]
bsmaxheight=[]
frequency=[]
distan=[]
# packetsRecBS=[]
# packetscollideBS=[]
packetSeq = 0
nrCollisions = 0
nrReceived = 0
nrProcessed = 0
counter=0
spf=[]
a=[]
# nrLost = 0

recPackets=[]
collidedPackets=[]
lostPackets = []
# avg=[30000,86400000]
avg=[1000000]
maxBSReceives = 8
different.append(0)

for sdb in range(7,13):
    spf.append(sdb)

if (graphics == 1):
    plt.ion()
    plt.figure()
    
    ax = plt.gcf().gca()

    ax.add_patch(Rectangle((0, 0), 20, 20, fill=None, alpha=1))
    


if len(sys.argv)>1 :
    
    experiment = int(sys.argv[2])
    simtime = int(sys.argv[3])
    nrBS = int(sys.argv[4])
    sensornodes = int(sys.argv[5])
    PayLoad = int(sys.argv[6])
    
    if len(sys.argv)>7 :
        spreadingfactor = int(sys.argv[7])

        
    



   


    if sys.argv[1] == 'fixed':
        for data in open('parameters__settings__of__fixedbasestion.json','r') :
            data=json.loads(data)
        for sensor in open('parameters__settings__of__fixedsensor_configuration.json','r') :
            sensor=json.loads(sensor)
    elif sys.argv[1] == 'notfixed':
        for data in open('parameters__settings__of__notfixedbasestion.json','r') :
            data=json.loads(data)
        for sensor in open('parameters__settings__of__notfixedsensor_configuration.json','r') :
            sensor=json.loads(sensor)

           



            
       

height=[]
ind_height=[]
bsavgheight=[]
rural=[]
metropolitan=[]
g=[]
i=[]
enor=[]
tz=[]
totalreceivedperbasestation=[]
for j in sensor["sensor_placement"]["sensor_x_y"]:
    g.append(j["slocx"])
    
# print(g[0])
# print(g[1])
# print(g[2])
# print(g[3])
x=sensor["max_number_sensors"]

## the below for loops assign sensors x and y location to a list

for k in g[0:x]:
    # print(k)
    enor.append(k)

print(enor)
for b in sensor["sensor_placement"]["sensor_x_y"]:
    i.append(b["slocy"])

for er in i[0:x]:
    # print(k)
    tz.append(er)

print(tz)

## the below loop selects the height and adds to list

if sys.argv[1] == 'fixed':
    for j in sensor["sensor_placement"]["sensor_x_y"]:
        height.append(j["sheight"])
        
    for ey in height[0:x]:
        
        ind_height.append(ey)
elif sys.argv[1] == 'notfixed':
    for x in sensor["sensor_placement"]["sensor_x_y"]:
        x.update({"sheight":random.randint(1,10)})
    for j in sensor["sensor_placement"]["sensor_x_y"]:
        height.append(j["sheight"])
    for ey in height[0:sensor["max_number_sensors"]]:
        ind_height.append(ey)     

# basestation=1

for z in data["basestations_placement"]:
    bsx.append(z["xloction"])
    bsy.append(z["ylocation"])
    bsminheight.append(z["min_height"])
    rural.append(z["min_height"])
    bsmaxheight.append(z["max_height"])
    if sys.argv[1] == 'notfixed':
        bsavgheight.append(round((z["min_height"]+z["max_height"])/2))
        avg.clear()
        for sendtime in sensor["averagesendtime"]["selectedtime"]:
            avg.append(sendtime)

        if (z["area_type"]=='rural'):
            ruralheight=round((z["min_height"]+z["max_height"])/2)
            rural.append(ruralheight)
        elif(z["area_type"]=='metropolitan'):
            metropolitanheight=round((z["min_height"]+z["max_height"])/2)
            metropolitan.append(metropolitanheight)


      



            

       

            

        
        





# bsx1=bsx[basestation-1]+0
# bsy1=bsy[basestation-1]+0

for freq in sensor["Frequencyalocation"]["frequency_EUstandard"]:
    frequency.append(freq)

packetsAtBS=[]
packetsRecBS=[]
for i in range(0, nrBS):
    b = myBS(i,bsx[i],bsy[i])
    bs.append(b)
    packetsAtBS.append([])
    packetsRecBS.append([])
   


for i in range(0,sensornodes):
    node = myNode(i,PayLoad,enor[i],tz[i],ind_height[i])

    nodes.append(node)
    a.append(sf(node))
    print(a)
    
    env.process(transmit(env,node))    


if (graphics == 1):
    plt.xlim([0, 100])
    plt.ylim([0, 100])
    plt.draw()
    plt.show()

env.run(until=simtime)
sent=0
for i in range(0,sensornodes):
#    print "sent ", nodes[i].sent         
    sent = sent + nodes[i].sent


for i in range(0,nrBS):
    print ("packets at BS",i, ":", len(packetsRecBS[i]))
    totalreceivedperbasestation.append(len(packetsRecBS[i]))


    # print ("collided at BS",i, ":", len(packetscollideBS[i]))
    # 


print(totalreceivedperbasestation)
packetsrec=math.ceil(statistics.mean(totalreceivedperbasestation))
nrCollisions=sent-packetsrec
print ("nr received packets",(recPackets))
# print ("nr received packets",len(recPackets))
print ("nr received packets",packetsrec)

# print ("nr collided packets", (collidedPackets))
print ("nrCollisions ", nrCollisions)
# print ("nr collided packets", len(collidedPackets))     packetsRecBS
print ("nr lost packets", len(lostPackets))  


print ("sent packets: ", sent)





print ("sent packets: ", packetSeq)

## add the below commented to fname is case of experiment 1
# str(spreadingfactor) +


if (graphics == 1):
    input('Press Enter to continue ...')    


## for saving in a text file uncomment to check

# fname = "lorascheduledMBS_subchannel200sensorsscheduled"+str(sys.argv[1])+ str(experiment) + ".txt"
# print (fname)
# if os.path.isfile(fname):
#     res = "\n" + str(nrCollisions) + " "  + str(sent) + " " + str(packetsrec)
# else:
#     res = "\n" + str(nrCollisions) + " "  + str(sent) + " " + str(packetsrec)
# with open(fname, "a") as myfile:
#     myfile.write(res)
# myfile.close()


# the below commented calculates energy and stores in a file uncommnet to check energy (best observed when setting average sendime to 10mins)
# energy = 0.0
# mA = 125    # current draw for TX = 17 dBm
# V = 3     # voltage XXX
# sent = 0
# tdx=[]
# lpc=[]
# for i in range(0,sensornodes):
#     for b in range(0,nrBS):
#         sent=sent + nodes[i].sent
#         energy = (energy + nodes[i].packet[b].rectime * mA * V * nodes[i].sent)/1000.0
#         tdx.append(nodes[i].packet[b].rectime)
#         lpc.append(nodes[i].sent)

# print(lpc)
# print(tdx) 
# print ("energy (in mJ): ", energy)

# fname = "lorascheduledMBS_energy"+str(sys.argv[1])+ str(experiment)+ str(spreadingfactor) + ".txt"
# print (fname)
# if os.path.isfile(fname):
#     res = "\n" + str(energy)
# else:
#     res = "\n" + str(energy)
# with open(fname, "a") as myfile:
#     myfile.write(res)
# myfile.close()