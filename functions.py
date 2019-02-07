#!/usr/bin/env python
# coding: utf-8

# Parsing json data 
# CoojaJsonImporter(dir) imports jsons from the dir in a list
# dict2df(dict) imports one json and return a df 
# dict2df_list(dict) import one json and return a list of df

# In[9]:


import os
import pandas as pd
import numpy as np
import json

#Object idea= List of nodes
#Node has (ip,hop,min_rtt,max_rtt,pkts,responses)
#pkt is a dataframe with packets
#hop is from 64-ttl


class node(object):
    ip = ""
    hop= 0
    min_rtt= 0
    max_rtt= 0
    pkts=pd.DataFrame()
    pktsC=pd.DataFrame()
    responses=0
    
    
    # The class "constructor" - It's actually an initializer 
    def __init__(self,ip,hop,min_rtt,max_rtt,pkts,responses,pktsC):
        self.ip = ip
        self.hop=hop
        self.min_rtt=min_rtt
        self.max_rtt=max_rtt
        self.pkts=pkts
        self.responses=responses
        self.pktsC=pktsC

    def make_node(ip,hop,min_rtt,max_rtt,pkts,responses,pktsC):
        node= node(ip,hop,min_rtt,max_rtt,pkts,responses,pktsC)
        return node
    
    
class packet(object):
    rtt=np.NaN
    pkt=np.NaN
    ttl=np.NaN   
    def __init__(self,rtt,pkt,ttl):
        self.rtt=rtt
        self.pkt=pkt
        self.ttl=ttl
    
    
    def make_packet(rtt,pkt,ttl):
        package=package(rtt,pkt,ttl)

def coojaJsonImporter(dir):
        
        dataList=[]

        for file in os.listdir(dir):
            print("Importing "+ file)
            with open(dir+"/" + file, 'r') as f:

                dataList.append(json.load(f))

        return dataList

def dict2df(dict):
    dfList=[]
    bigdata=pd.DataFrame()
    for key in dict.keys():
        df=pd.DataFrame(dict[key]['pkts'])
        df['ip']=key
        
        #dfList.append(df)
        #print(df)
        bigdata=bigdata.append(df,ignore_index=True)

    return bigdata
        
def dict2df_list(dict):
    dfList=[]
    #dfList(pd.DataFrame(dict))
    for key in dict.keys():
        df=pd.DataFrame(dict[key]['pkts'])
        df['ip']=key
        df['hop']=64-(df['ttl'])
        dfList.append(df)
        #print(df)
    return dfList


###Function to create nodes, create a list of nodes
### 
    
def createNodes(dict):
    nodeList=[]
    #dfList(pd.DataFrame(dict))
    for ip in dict.keys():
        pkts=pd.DataFrame(dict[ip]['pkts'])
        #(ip,hop,min_rtt,max_rtt,pkts,responses)
        #print(dict.get(ip).get("max_rtt"))
        #findMissingPackets(dict.get(ip))
        pkts1=dict.get(ip).get("pkts")
        pktsList=[]
        for p in pkts1:
            #print(p.get("rtt"))
             #make_packet(rtt,pkt,ttl)
            rtt=p.get("rtt")
            pkt=p.get("pkt")
            ttl=p.get("ttl")
            pack=packet(rtt,pkt,ttl)
            pktsList.append(pack)
        min_rtt=dict.get(ip).get("min_rtt")
        max_rtt=dict.get(ip).get("max_rtt")
        responses=dict.get(ip).get("responses")
        hop=64-(int(pkts[0:1]["ttl"]))
        #print(type(pkts[0:1]["ttl"]))
        #print(pkts[0:1]["ttl"])
        n=node(ip,hop,min_rtt,max_rtt,pkts,responses,pkts)
        
        nodeList.append(n)
        #print(type(nodeList[0].pkts[0]))
        
    return nodeList



def findMissingPackets(node):
    #print(node.pkts["pkt"])
    print("Executed")
    maxP=-1
    
    for el in node.pkts["pkt"]:
        if(el>maxP): maxP=int(el)
    #print(maxP)
    pkt=[None]*(maxP+1)
    for i in range(len(node.pkts["pkt"])):
        index=int(node.pkts["pkt"][i])
        #print(index)
        pkt[index]=node.pkts["rtt"][i]
        #pkt[)]=node.pkts["pkt"][i]
    return pkt
    
    


    
def getIps(list):
    ips=[]
    for n in list:
        ips.append(n.ip)
    return ips


def MLPreparation(data):
    # Calculate all the statistics
    statistics = {}	# <node_id, statistics of the node>
    
    for network in data:
        for node in network:
            print(node.pkts["rtt"].describe())
  
    
def getOutliers(df):
    df1=df["rtt"]
    std=df1.std()
    mean=df1.mean()
    a1=df["rtt"]>mean+(2*std)
    a2=df["rtt"]<mean-(2*std)
    return(df[a1 | a2])

def getStdValues(df):
    df1=df["rtt"]
    std=df1.std()
    mean=df1.mean()
    a1=df["rtt"]<mean+(2*std)
    a2=df["rtt"]>mean-(2*std)
    return(df[a1 & a2])   

def getPings(data):
    pings=[]
    for i in range(len(data)):
        packetN=-1
        for j in range(len(data[i])):
            if(len(data[i][j].pkts)>packetN): packetN=len(data[i][j].pkts)
        pings.append(packetN)
    return pings
