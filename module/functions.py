#Modules to install via pip pandas,ipynb
import os
import sys
import time

from lib import trace_classification

sys.path.append('../')

import os
import pandas as pd
import numpy as np
import json
#Modules to install via pip pandas,ipynb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from pprint import pprint
import os
#import import_ipynb
import sys
sys.path.append('../')
from pandas.plotting import scatter_matrix
from lib import trace_analysis 
from node import *
import sklearn.metrics as sm
import pandas as pd
import matplotlib.pyplot as plt
import os
from node import *


from lib import plots_analysis 
from sklearn.metrics import confusion_matrix
from sklearn.cluster import KMeans
import sklearn.metrics as sm
from sklearn.decomposition import PCA
import random


#Modules to install via pip pandas,ipynb
import sys

sys.path.append('../')

from lib import plots_analysis 
from sklearn.cluster import KMeans
import pandas as pd
# scipy
import sklearn.metrics as sm


class node(object):
    ip = ""
    hop= 0
    pkts=pd.DataFrame()


    # The class "constructor" - It's actually an initializer
    def __init__(self,ip,hop,pkts):
        self.ip = ip
        self.hop=hop
        self.pkts=pkts

    def make_node(ip,hop,pkts):
        node= node(ip,hop,pkts)
        return node


#######
#Plotting Graphs
#####

def saveFileFigures(fig,directory,namefile):
    directory=directory+"figures/"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(directory)
    fig.savefig(directory+namefile+".pdf")   # save the figure to file
    #plt.show()


#Prints on a file the big matrix (asked by professor)
def printBigPlot(directory,data,figsize,namefile,colors,cases):
    print("Printing Big Plot for "+directory)
    fig, axs= plt.subplots(len(data),len(data[0]), figsize=figsize,sharey=True, )

    for i in range(len(data)):
        for j in range(len(data[i])):
        #print(i,j)
            ax=axs[i][j]
            d=data[i][j].pkts["rtt"]
            ax.set_ylabel("Density")
            ax.set_title("Node "+ str(data[i][j].ip) )
            ax.set_xlabel("Time (ms)")
            if not d.empty  | len(d)<2 :
                d.plot.kde(
                    ax=ax,
                    label="Case " +str(cases[i]),
                    color=colors[i]

                )


                d.hist(density=True,alpha=0.3,color=colors[i], ax=ax)

                ax.legend()
            #ax.set_xlim([-500, 8000])
    plt.tight_layout()
    saveFileFigures(fig,directory,namefile)

#Print on a file density by Hop (asked by professor)
def printDensityByHop(directory,dataHop,hops,figsize,namefile,colors,cases):

    print("Printing Density by Hop for "+directory)
    #dataHop=hopPreparation(data)
    fig, axs= plt.subplots(len(dataHop[0]),1, figsize=(15,20),sharey=True, )
    #print(len(dataHop),len(dataHop[0]))
    for i in range(len(dataHop)):
        for j in range(len(dataHop[i])):
            #print(i,j)
            d=dataHop[i][j].pkts['rtt']
            axs[j].set_xlabel("Time (ms)")
            axs[j].set_title("Hop "+ str(j+1))
            if not d.empty | len(d)<2 :
                d.plot.kde(
                    ax=axs[j],
                    label=cases[i],color=colors[i]
                )

                d.hist(density=True,alpha=0.3, ax=axs[j],color=colors[i])


                axs[j].legend()

            #axs[j].set_xlim([-40, 6000])
    plt.tight_layout()
    saveFileFigures(fig,directory,namefile)

#Print on a file density by Case (asked by professor)
def printDensityByCase(directory,data,hops,figsize,namefile,colors,cases):

    print("Printing Density by case for "+directory)
    #print(len(data),len(data[0]))

    #data1=hopPreparation(data)
    dataHopT=[*zip(*hops)]

    #print(len(data1),len(data1[0]))
    #print(len(dataHopT),len(dataHopT[0]))
    fig, axs= plt.subplots(len(dataHopT[0]),1, figsize=(15,20),sharey=True, )
    for i in range(len(dataHopT)):
        for j in range(len(dataHopT[0])):
            d=dataHopT[i][j]

            axs[j].set_title(""+ cases[i])
            axs[j].set_xlabel("Time (ms)")
            axs[j].set_ylabel("Density")
            if not d.empty | len(d)<2 :
                #print(dataHopT[i][j])
                #print(colors[i])
                d=d["rtt"]
                try:
                    d.plot.kde(
                        ax=axs[j],
                        label="Hop "+str(i),
                        color=colors[i]
                    )

                    d.hist(density=True,alpha=0.3, ax=axs[j],color=colors[i])

                    axs[j].legend()
                except:pass

    plt.tight_layout()
    #axs[j].set_xlim([-40, 6000])
    saveFileFigures(fig,directory,namefile)

#Print Density of delay without outliers in every node by Case
def densityOfDelayByCaseNoOutliers(directory,data,figsize,namefile,colors,cases):
    print("Printing Density of delay without outliers in every node by Case for "+directory)
    fig, axs= plt.subplots(len(data[0]),1, figsize=figsize,sharey=True, )
    for i in range(len(data)):
        for j in range(len(data[i])):
            out=getStdValues(data[i][j].pkts)
            if not out.empty :
                ax=axs[j]
                out["rtt"].plot.kde(
                ax=ax,
                label=cases[i],
                     color=colors[i]
            )
                ax.set_ylabel("Density")
                out["rtt"].hist(density=True,alpha=0.3, ax=ax, color=colors[i])
                ax.set_title("Node "+ str(data[i][j].ip))
                ax.set_xlabel("Time (ms)")
                ax.legend()
    plt.tight_layout()
    saveFileFigures(fig,directory,namefile)

#Density of outliers in every node by Case
def densityOutliersByCase(directory,data,figsize,namefile,colors,cases):
    print("Printing Density of outliers in every node by Case for "+directory)
    fig, axs= plt.subplots(len(data),len(data[0]), figsize=figsize,sharey=True, )
    for i in range(len(data)):
        for j in range(len(data[i])):
            out=getOutliers(data[i][j].pkts)
            ax=axs[i][j]
            ax.set_ylabel("Density")
            ax.set_title("Node "+ str(data[i][j].ip))
            ax.set_xlabel("Time (ms)")
            if not out.empty | len(out)<2 :

                out["rtt"].plot.kde(
                ax=ax,
                label=cases[i],
                 color=colors[i]
            )

                out["rtt"].hist(density=True,alpha=0.3, ax=ax, color=colors[i])
                ax.legend()

    plt.tight_layout()
    saveFileFigures(fig,directory,namefile)


#Distibution of the delay divided by Node in the differents Cases
def densityOfDelayByCase(directory,data,figsize,namefile,colors,cases):
    print("Printing Density of delay in every node by Case for "+directory)
    fig, axs= plt.subplots(len(data[0]),1, figsize=figsize,sharey=True, )
    for i in range(len(data)):
        for j in range(len(data[i])):
            d=data[i][j].pkts["rtt"]
            axs[j].set_title("Node "+ str(data[i][j].ip))
            axs[j].set_xlabel("Time (ms)")
            axs[j].set_ylabel("Density")
            if not d.empty | len(d)<2 :

                try:
                    d.plot.kde(
                        ax=axs[j],
                        label=cases[i],color=colors[i]
                    )

                    d.hist(density=True,alpha=0.3, ax=axs[j],color=colors[i])

                    axs[j].legend()
                except:
                    pass
    plt.tight_layout()
    saveFileFigures(fig,directory,namefile)


#RTT Graph
def RTTGraph(directory,data,figsize,namefile,colors,cases):
    print("Printing RTT Graph for "+directory)
    # fig, axs= plt.subplots(len(data[0]),1, figsize=figsize,sharey=True, )
    # for i in range(len(data)):
    #     for j in range(len(data[i])):
    #         axs[j].plot(data[i][j].pkts["seq"],data[i][j].pkts["rtt"],label=cases[i],color=colors[i]   )
    #         axs[j].set_title("Node "+ str(data[i][j].ip))
    #         axs[j].set_xlabel("Packet Number")
    #         axs[j].set_ylabel("Time (ms)")
    #         axs[j].legend()
    # plt.tight_layout()
    # saveFileFigures(fig,directory,namefile)
    fig, axs= plt.subplots(len(data),len(data[0]), figsize=figsize,sharey=True, )

    for i in range(len(data)):
        for j in range(len(data[i])):
        #print(i,j)
            ax=axs[i][j]
            d=data[i][j].pkts["rtt"]
            ax.set_ylabel("Time (ms)")
            ax.set_title("Node "+ str(data[i][j].ip))
            ax.set_xlabel("Packet Number")
            if not d.empty  | len(d)<2 :
                 ax.plot(data[i][j].pkts["seq"],data[i][j].pkts["rtt"],label=cases[i]
                 #,color=colors[i]
                   )

                 ax.legend()
            #ax.set_xlim([-500, 8000])
    plt.tight_layout()
    saveFileFigures(fig,directory,namefile)




#Not used anymore
def coojaJsonImporter(dir):

        dataList=[]

        for file in os.listdir(dir):
            print("Importing "+ file)
            with open(dir+"/" + file, 'r') as f:

                dataList.append(json.load(f))

        return dataList


###Function to create nodes, create a list of nodes
###

def createNodes(dict):
    nodeList=[]
    #dfList(pd.DataFrame(dict))
    for ip in dict.keys():
        pkts=pd.DataFrame(dict[ip]['pkts'])

        hop=64-(int(pkts[0:1]["ttl"]))
        pkts = pkts.drop(['ttl'], axis=1)
        pkts=pkts.rename(columns={"pkt":"seq"})
        #print(type(pkts[0:1]["ttl"]))
        #print(pkts[0:1]["ttl"])
        n=node(ip,hop,pkts)

        nodeList.append(n)

    return nodeList



def findMissingPackets(node):
    #print(node.pkts["pkt"])
    print("Executed")
    maxP=-1

    for el in node.pkts["seq"]:
        if(el>maxP): maxP=int(el)
    #print(maxP)
    pkt=[None]*(maxP+1)
    for i in range(len(node.pkts["seq"])):
        index=int(node.pkts["seq"][i])
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

def get_IQR_Outliers(df):
    df1 = df["rtt"]
    lower = df1.quantile(.25)
    upper = df1.quantile(.75)
    a1 = df["rtt"]>upper
    a2 = df["rtt"]<lower
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



#Prepare the hop data
def hopPreparation(data):
    hoplist=[]
    df_a = pd.DataFrame( )
    dataHop=[]

    listoflists = []
    #print("Hop Preparation")
    #print(len(data),len(data[0]))

    maxHopCase=[]
    for i in range(len(data)):
        maxHop=-1
        for j in range(len(data[i])):
            if(data[i][j].hop>maxHop):
                maxHop=data[i][j].hop
        maxHopCase.append(maxHop)
    #print(maxHopCase)

    for i in range(len(data)):
        sublist = []
        for j in range(maxHopCase[i]):
            sublist.append((df_a))
        dataHop.append(sublist)
    #print (listoflists)

    for i in range(len(data)):
        col=[]
        for j in range(len(data[i])):
            hop=data[i][j].hop-1

            dataHop[i][hop]= pd.concat([dataHop[i][hop],data[i][j].pkts],sort=True)
    #print(len(dataHop),len(dataHop[0]))

    return dataHop


def getPercentageMissingPackets(node,lenght):
    missing=0
    #print(len(node.pkts))
    missing=lenght-len(node)
    #print(lenght,missing)
    if(missing!=0):
        result=missing/lenght
    else: result=0
    #print(maxS/missing)
    return result*100


def accuracy_score_corrected(correction,labels):
    #print(np.array(correction))
    labels_alt=[]
    sum_labels=0
    sum_labels_alt=0
    for el in labels:
        if (el==0):
            labels_alt.append(1)
            sum_labels_alt+=1
        elif el==1:
            labels_alt.append(0)
            sum_labels+=1

    accuracy=sm.accuracy_score(correction, labels)
    accuracy_alt=sm.accuracy_score(correction, labels_alt)
    #print(correction)


    if (sum_labels>sum_labels_alt):
        #print(accuracy)
        None

    else:
        #print(accuracy_alt)
        labels=labels_alt
    #print(np.array(labels))
    confusionMatrix=sm.confusion_matrix(correction, labels)

    #pprint(confusionMatrix)
    return labels



def ReplaceMissingPackets(node):
    #print(node.pkts["pkt"])
    print("Executed")
    maxP=-1

    for el in node.pkts["seq"]:
        if(el>maxP): maxP=int(el)
    #print(maxP)
    pkt=[None]*(maxP+1)
    for i in range(len(node.pkts["seq"])):
        index=int(node.pkts["seq"][i])
        #print(index)
        pkt[index]=node.pkts["rtt"][i]
        #pkt[)]=node.pkts["pkt"][i]
    return pkt

#Import from pings files to a dataframe
def import_nodes_Cooja_2(directory,tracemask,node_defaults):
    #print(directory)
    #print(tracemask)
    files = []

    # load all files and extract IPs of nodes
    for file in os.listdir(directory):
        try:
            if file.startswith(tracemask) and file.index("routes"):
                continue
        except:
            files.append(file)

    nodes = pd.DataFrame(columns=['node_id', 'rank'])
    packets_node = {}

    # Load the ICMP traces
    for file in files:
        packets = pd.read_csv(directory + '/' + file,
                              sep=' |icmp_seq=|ttl=|time=',
                              na_filter=True,
                              header=None,
                              skiprows=1,
                              skipfooter=4,
                              usecols=[3, 5, 7, 9],
                              names=['node_id', 'seq', 'hop', 'rtt'],
                              engine='python').dropna().drop_duplicates()

        if len(packets) < 1:
            # Nodes affected by a black hole did not receive any packet
            node_id = file[-24:-4]
            if(node_id=="aa::212:7411:11:1111"): node_id="aaaa::212:7411:11:1111"
            packets = pd.DataFrame(columns=['node_id', 'seq', 'hop', 'rtt'],
                                   data=[[node_id, 1, node_defaults[node_id], 1]])

            nodes.loc[len(nodes)] = [file[-24:-4], node_defaults[node_id]]
            packets_node[file[-24:-4]] = packets

        else:
            #print("qui")
            packets['node_id'] = packets.apply(lambda row: row['node_id'][:-1], axis=1)
            #print(packets["hop"].head())
            #print(nodes)
            #nodes.loc[len(nodes)-1] = [packets['node_id'][0], 64-packets['hop'][0]]
            #print("ciao"+ str(64-packets['hop'][0]))
            #print(nodes.loc[7])
            packets = packets.sort_values(by=['node_id', 'seq'], ascending=True, na_position='first')
            packets = packets[packets['rtt'] > 1]
            packets["hop"]=  64-packets['hop']
            packets_node[packets['node_id'][0]] = packets

    nodes=nodes.sort_values(by=['rank', 'node_id'])

    #tranformation in node
    nodeList=[]

    for n in packets_node.keys():
        #print((packets_node[n]).head())
        pkts=packets_node[n].drop(["node_id","hop"],axis=1)
        #print(pkts)
        hop=int(packets_node[n]["hop"][0])
        ip=packets_node[n]["node_id"][0]
        #print(hop)
        n=node(ip,hop,pkts)
        nodeList.append(n)


    return nodeList

#calls import nodes cooja_2
def import_Cooja2(df,directory):
    data=[]
    node_defaults = {
        "aaaa::212:7403:3:303": 10,
        "aaaa::212:7402:2:202": 10,
        "aaaa::212:7404:4:404": 10,
        "aaaa::212:7406:6:606": 10,
        "aaaa::212:7405:5:505": 10,
        "aaaa::212:7407:7:707": 10,
        "aaaa::212:7409:9:909": 10,
        "aaaa::212:7408:8:808": 10,
        "aaaa::212:740a:a:a0a": 10,
        "aaaa::212:740b:b:b0b": 10,
        "aaaa::212:740f:f:f0f":  10,
        "aaaa::212:7411:11:1111": 10,
        "aaaa::212:740d:d:d0d":    10,




    }
    #for row in plots:

        #print("Importing ./"+row[0]+"/"+row[1])
    #print(directory+df["directory"].values)

    for i in range(len(df["directory"].values)):




        nodeList=import_nodes_Cooja_2(directory+df["directory"].values[i],df["case"].values[i],node_defaults)
        data.append(nodeList)
    #print(len(data))
    #print(len(data[0]))
    return data


def analyze_network(directory, df, pings, window, features_to_drop):
    cases = []
    casesAccuracy = df["case_accuracy"].values
    casesAccuracy2 = df["case_accuracy2"].values
    #     for row in plots:
    #         cases.append(row[1])
    #         casesAccuracy.append(row[2])
    #         data=import_Cooja2(plots)
    cases = df["case"].values
    folder = df["directory"].values + directory

    data = import_Cooja2(df, directory)

    # pings=getPings(data)
    # All data collection is in variable node that is a list of list of nodes
    # 3 nets input x 9 nodes by net
    print("Processing...")
    d = {"label": [],
         "type": [],
         "count": [],
         "std": [],
         "mean": [],
         "var": [],
         "hop": [],

         "packet loss": [],
         "outliers": [],
         "node": [],
         "window": []
         }
    # count=[]
    labels = []
    var = []
    # window=100
    # stats=pd.DataFrame(columns=columns)
    n = pings

    for i in range(len(data)):
        # window=pings[i]

        for j in range(len(data[i])):
            # n=pings[i]

            # print(n)
            for z in range(0, n, int(window)):
                # if(z+window>n):break
                # print(z,z+window)

                # df1 = df1.assign(e=p.Series(np.random.randn(sLength)).values)
                node = data[i][j].pkts
                name = str(j) + " " + cases[i]
                nodeWindow = node[(node["seq"] < z + window) & (node["seq"] >= z)]
                nodeWindowP = nodeWindow["rtt"]
                d["count"].append(nodeWindowP.count())
                # Case without outliers
                # Case with outliers
                std = 0
                if (nodeWindowP.std() > 10):
                    std = 1
                    std = nodeWindowP.std()

                d["std"].append(std)
                mean = nodeWindowP.mean()
                # if(mean<1):print(mean)
                d["mean"].append(mean)
                var = 0
                if (nodeWindowP.var() > var): var = nodeWindowP.var()
                d["var"].append(var)
                d["label"].append(cases[i])
                d["hop"].append(data[i][j].hop)
                d["type"].append(casesAccuracy[i])
                d["outliers"].append(getOutliers(nodeWindow)["rtt"].count())
                missing = window - nodeWindow.count()
                d["node"].append(data[i][j].ip)
                mP = getPercentageMissingPackets(nodeWindow, window)
                PL = 0
                if (mP > 30):
                    PL = 1
                    PL = mP
                d["packet loss"].append(mP)
                d["window"].append(window)

    stats = pd.DataFrame(d)

    dataK = stats.drop(features_to_drop, axis=1)
    dataK = dataK.fillna(0)

    # print(dataK)
    correction = []
    correction_alt = []
    col = np.array(dataK["type"])
    dataK = dataK.drop(["type"], axis=1)
    # Creating simple array to correct unsupervised learning
    # NB as it is unsupervised could happen that the correction are inverted
    for i in range(len(col)):
        el = d["type"][i]
        if el == "normal":
            correction.append(1)
            correction_alt.append(0)

        else:

            correction.append(0)
            correction_alt.append(1)

    dataC = stats["label"]
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(dataK)
    labels = kmeans.predict(dataK)
    centroids = kmeans.cluster_centers_
    labels = accuracy_score_corrected(correction, labels)
    predicted = []
    for i in range(len(labels)):

        if (labels[i] == 1):
            predicted.append("normal")
        else:
            predicted.append("BH")

    # print(len(predicted))
    stats["predicted"] = pd.Series(np.array(predicted))
    stats["predicted number"] = pd.Series(np.array(labels))
    stats["correction number"] = pd.Series(np.array(correction))
    stats_csv = stats[[
        "label",
        "type",
        "predicted",
        "packet loss",
        "outliers",
        "std",
        "hop",
        "node",
        "mean"

    ]]
    # stats_csv.to_csv("results_kmeans.csv", sep='\t', encoding='utf-8')
    stats.head()
    net_results = {
        "case": [],
        "normal_behaving_nodes_percentage": [],
        "predicted": [],
        "real": [],
        "pings": [],
        "window": [],

    }
    # print(stats["predicted number"])
    correction = []
    labels = []
    for case in range(len(cases)):
        subset = stats[stats["label"] == cases[case]]
        mean_predicted = str(subset["predicted number"].mean() * 100)  # +"% normal"
        net_results["case"].append(cases[case])
        net_results["normal_behaving_nodes_percentage"].append(mean_predicted)
        net_results["pings"].append(pings)
        net_results["window"].append(window)

        if (float(mean_predicted) < 85):
            p = "abnormal"
            labels.append(0)
        else:
            p = "normal"
            labels.append(1)

        if (casesAccuracy[case] == "BH"):
            c = "abnormal"
            correction.append(0)
        elif (casesAccuracy[case] == "normal"):
            c = "normal"
            correction.append(1)

        net_results["predicted"].append(p)
        net_results["real"].append(c)

    results = pd.DataFrame(net_results)

    return results, stats, correction, labels
def create_stats(directory, df, pings, window):
    cases = []
    casesAccuracy = df["case_accuracy"].values
    casesAccuracy2 = df["case_accuracy2"].values

    cases = df["case"].values
    folder = df["directory"].values + directory

    data = import_Cooja2(df, directory)


    print("Processing...")
    d = {"experiment": [],
         "node_id": [],
         "label": [],
         "label_2":[],
         "loss": [],
         "count": [],
         "std": [],
         "mean": [],
         "var": [],
         "hop": [],
        "min":[],
         "max":[],

         "outliers": [],

         "window": []
         }
    # count=[]
    labels = []
    var = []
    # window=100
    # stats=pd.DataFrame(columns=columns)
    n = pings

    for i in range(len(data)):
        # window=pings[i]

        for j in range(len(data[i])):
            # n=pings[i]

            # print(n)
            for z in range(0, n, int(window)):
                # if(z+window>n):break
                # print(z,z+window)


                # df1 = df1.assign(e=p.Series(np.random.randn(sLength)).values)
                node = data[i][j].pkts

                name = str(j) + " " + cases[i]
                nodeWindow = node[(node["seq"] < z + window) & (node["seq"] >= z)]
                nodeWindowP = nodeWindow["rtt"]
                d["count"].append(nodeWindowP.count())
                # Case without outliers
                # Case with outliers
                std = 0
                if (nodeWindowP.std() > 10):
                    std = 1
                    std = nodeWindowP.std()

                d["std"].append(std)
                mean=0

                if(nodeWindowP.mean()>mean): mean=nodeWindowP.mean()
                # if(mean<1):print(mean)
                d["mean"].append(mean)
                var = 0
                if (nodeWindowP.var() > var): var = nodeWindowP.var()
                d["var"].append(var)
                d["experiment"].append(cases[i])
                d["hop"].append(data[i][j].hop)

                if(casesAccuracy[i]=="normal"):
                    d["label"].append("Normal")

                else:
                    d["label"].append("Attacked")

                if (casesAccuracy[i] == "normal"):
                    d["label_2"].append("Normal")
                elif(casesAccuracy[i] == "BH"):
                    d["label_2"].append("BH")
                else:
                    d["label_2"].append("GH")
                d["outliers"].append(getOutliers(nodeWindow)["rtt"].count())
                missing = window - nodeWindow.count()
                d["node_id"].append(data[i][j].ip)
                mP = getPercentageMissingPackets(nodeWindow, window)
                d["min"].append(data[i][j].pkts["rtt"].min())
                d["max"].append(data[i][j].pkts["rtt"].max())
                d["loss"].append(mP)
                d["window"].append(window)

    stats = pd.DataFrame(d)
    stats.to_csv(directory + "stats.csv", sep=',', encoding='utf-8')
    return stats



def get_traces_csv(directory):
    print("Reading Traces from " + directory)
    directory1 = directory
    directory += "traces/"
    # print(directory)
    files = []
    path = []
    case_accuracy = []
    case_accuracy2 = []
    # directory="./traces"
    # directory=os.getcwd()+"/traces/"
    d = {}
    try:

        for subdirectory in os.listdir(directory):
            # print(os.path.isdir(subdirectory))
            # print(subdirectory)

            subdirectory2 = directory + "/" + subdirectory

            if (os.path.isdir(subdirectory2)):

                for file in os.listdir(subdirectory2):

                    if ("routes" in file):
                        # print(subdirectory+"/"+file)
                        path.append("traces/" + subdirectory[:])
                        # print(file)
                        files.append(file[:-10])
                        # print(file)
                        if ("normal" in file):
                            case_accuracy.append("normal")
                            case_accuracy2.append("normal")
                        elif ("bh" in file):
                            case_accuracy.append("BH")
                            case_accuracy2.append("BH")
                        elif ("gh" in file):
                            case_accuracy.append("BH")
                            case_accuracy2.append("GH")
                        continue
        d = {
            "directory": path,
            "case": files,
            "case_accuracy": case_accuracy,
            "case_accuracy2": case_accuracy2

        }
    except:
        pass

    traces = pd.DataFrame(d)
    # print(directory)
    traces.to_csv(directory + "traces.csv", sep=',', encoding='utf-8')
    return traces


def run(directory, df):
    colors = [
        'orange', 'dodgerblue',
        'forestgreen', 'violet',
        "red", "brown",
        "pink", "aqua",
        "darkslategrey", "darkred",
        "darkblue", "darkorchid",
        "salmon", "chocolate"

    ]
    casesAccuracy = df["case_accuracy"].values

    cases = df["case"].values
    folder = df["directory"].values + directory

    data = import_Cooja2(df, directory)

    hops = hopPreparation(data)

    # Distribution of the delay in correlation with the Cases
    dataHop=hopPreparation(data)
    # Distribution of the delay in correlation with the Hops
    printDensityByCase(directory,data,hops,(15,90),"densitybyCase",colors,cases)

    # Distribution by Hop
    printDensityByHop(directory,data,hops,(30,90),"densitybyHop",colors,cases)

    # Prints on a file the big matrix (asked by professor)
    printBigPlot(directory,data,(90,90),"Big Plot",colors,cases)

    # Print Density of delay without outliers in every node by Case
    densityOfDelayByCaseNoOutliers(directory,data,(15,90),"Density of delay by Case no outliers",colors,cases)

    # Density of outliers in every node by Case
    densityOutliersByCase(directory,data,(90,90),"Density Outliers of Delay by Case",colors,cases)

    # Distibution of the delay divided by Node in the differents Cases
    densityOfDelayByCase(directory,data,(15,90),"Density of Delay by Case",colors,cases)

    # RTT Graph
    RTTGraph(directory, data, (30, 90), "RTT Graph", colors, cases)


def create_results(directory, features_to_drop):
    df = pd.read_csv(directory + "/traces/traces.csv", sep=',', encoding='utf-8')

    window_size = [25, 50, 100,200]
    results_total = pd.DataFrame()
    results_total_nodes = pd.DataFrame()
    for i in window_size:
        results_kmeans_network, results_kmeans_node, correction, labels = analyze_network(directory, df, 100, i,
                                                                                          features_to_drop)
        results_total = results_total.append(results_kmeans_network, ignore_index=True)
        results_total_nodes = results_total_nodes.append(results_kmeans_node, ignore_index=True)

        # Accuracy per node
        # labels = results_kmeans_node["predicted number"].values
        # correction = results_kmeans_node["correction number"].values
        # accuracy["Accuracy"].append(sm.accuracy_score(correction, labels))

        # Accuracy per network
        accuracy["Accuracy"].append(sm.accuracy_score(correction, labels))

        accuracy["Model"].append("Kmeans")
        accuracy["Window Size"].append(i)
        accuracy["Precision"].append(sm.precision_score(correction,labels,average='macro'))
        accuracy["Recall"].append(sm.recall_score(correction, labels,average='macro'))
        accuracy["F1-score"].append(sm.f1_score(correction, labels,average='macro'))


    accuracy = pd.DataFrame(accuracy)

    results_total.to_csv(directory + "results_total.csv", sep=',', encoding='utf-8')

    results_total_nodes.to_csv(directory + "results_total_node.csv", sep=',', encoding='utf-8')

    return results_total, accuracy, results_total_nodes


def kmeans_classification(trace_stats, features_to_drop):
    results = pd.DataFrame()
    for trace_size in trace_stats:
        #print('Computing trace {}'.format(trace_size))
        trace = trace_stats[trace_size]
        target = trace["label"].values
        correction = []
        for i in range(len(target)):
            if (i == "Normal"):
                correction.append(0)
            else:
                correction.append(1)

        features = trace.drop(columns=features_to_drop)


        t0 = time.time()  # Start a timer
        kmeans = KMeans(n_clusters=2)
        kmeans.fit(features)
        labels = kmeans.predict(features)
        labels = accuracy_score_corrected(correction, labels)

        predicted = []
        for i in range(len(labels)):
            if (labels[i] == 0):
                predicted.append("normal")
            else:
                predicted.append("abnormal")
        # kmeans["predicted"]=predicted
        # kmeans[kmeans["predicted"]=="normal"]
        results = pd.concat([results, pd.DataFrame({'Model': ['Kmeans'],
                                                    'Window Size': [trace_size],
                                                    'Mean Accuracy': [metrics.accuracy_score(correction, labels)],
                                                    #'Precision': [
                                                        #metrics.precision_score(correction, labels, average='macro')],
                                                    #'Recall': [
                                                        #metrics.recall_score(correction, labels, average='macro')],
                                                    #'F1-score': [metrics.f1_score(correction, labels, average='macro')],
                                                    #'Time (ms)': [time.time() - t0]
                                                    })])
    return results


def correct_stats(df, directory):
    df_labels = df["label"].unique().tolist()
    df_nodes = df["node"].unique().tolist()
    # print(df_nodes)

    results = pd.read_csv(directory + "results_total_node.csv")

    total = pd.DataFrame()
    for label in df_labels:
        for node in df_nodes:
            case = df.loc[df["label"] == label]
            node_case = case.loc[case["node"] == node]
            if (len(node_case) > 0):
                a = results.loc[results["label"] == label].loc[results["node"] == node]
                a["type_corrected"] = node_case["type_corrected"].iloc[0]
                a["type_corrected_2"] = node_case["type_corrected_2"].iloc[0]
                # print(node_case["type_corrected_2"].iloc[0])
                total = total.append(a, ignore_index=True)
    total = total.rename(columns={
        'label': 'experiment',

        'type_corrected': 'label',
        'type_corrected_2': 'label_2',
        'node': "node_id",
        "packet loss": "loss",

    }).drop(columns=["Unnamed: 0", "predicted number", "correction number", "predicted", "type"])
    return total

def correct_stats2(df, directory):
    df_labels = df["label"].unique().tolist()
    df_nodes = df["node"].unique().tolist()
    # print(df_nodes)

    results = pd.read_csv(directory + "stats_per_node.csv")

    total = pd.DataFrame()
    for label in df_labels:
        for node in df_nodes:
            case = df.loc[df["label"] == label]
            node_case = case.loc[case["node"] == node]
            if (len(node_case) > 0):
                a = results.loc[results["experiment"] == label].loc[results["node_id"] == node]
                a["label"] = node_case["type_corrected"].iloc[0]
                a["label_2"] = node_case["type_corrected_2"].iloc[0]
                # print(node_case["type_corrected_2"].iloc[0])
                total = total.append(a, ignore_index=True)

    total = total.rename(columns={
        #'label': 'experiment',

        #'type_corrected': 'label',
        #'type_corrected_2': 'label_2',
        #'node': "node_id",
        "packet loss": "loss",

    }).drop(columns=["Unnamed: 0", ])

    return total




def results_2_classes(trace_stats,network_stats,features_to_drop,net_features_to_drop):
    #results = pd.DataFrame()  # Results from each classification algorithm
    cv_results = pd.DataFrame()  # Cross validation results from each classification algorithm
    #net_results = pd.DataFrame()  # Results from each classification algorithm
    cv_net_results = pd.DataFrame()
    # Random Forest
    cv_results = pd.concat([cv_results,
                            trace_classification.random_forest_cross_validation(trace_stats, features_to_drop)
                            ])
    cv_results = pd.concat([cv_results,
                            trace_classification.k_nearest_neighbor_cross_validation(trace_stats, features_to_drop,
                                                                                     n_neighbors=11)
                            ])
    cv_results = pd.concat([cv_results,
                            trace_classification.support_vector_machines_cross_validation(trace_stats, features_to_drop,
                                                                                          kernel='rbf')
                            ])

    cv_results = pd.concat([cv_results,
                            kmeans_classification(trace_stats, features_to_drop)
                            ])

    if(network_stats is not None):
        cv_net_results = pd.concat([cv_net_results,
                                    trace_classification.random_forest_cross_validation(network_stats,
                                                                                        net_features_to_drop,
                                                                                        cross_val=3)
                                    ])
        cv_net_results = pd.concat([cv_net_results,
                                    trace_classification.k_nearest_neighbor_cross_validation(network_stats,
                                                                                             net_features_to_drop,
                                                                                             cross_val=3)
                                    ])

        # SVN



        cv_net_results = pd.concat([cv_net_results,
                                trace_classification.support_vector_machines_cross_validation(trace_stats, features_to_drop,
                                                                                              kernel='rbf')
                                ])
        """#One VS Rest
        
        cv_results = pd.concat([cv_results,
                             trace_classification.ensalble_svm_cross_validation(trace_stats, features_to_drop, n_estimators=15)
                            ])
        net_results = pd.concat([net_results,
                             trace_classification.ensalble_svm_classification(network_stats, net_features_to_drop)
                            ])
        """
        # Kmeans


        cv_net_results = pd.concat([cv_net_results,
                                    kmeans_classification(network_stats, net_features_to_drop)
                                    ])

    return cv_results.reset_index(drop=True),cv_net_results.reset_index(drop=True)




def create_network_stats(df):
    nodes = df["node_id"].unique().tolist()
    experiments = df["experiment"].unique().tolist()
    features = []
    a = {
        "experiment": [],
        "label": [],
        "label_2": []
    }
    for i in range(len(nodes)):
        features.append(str(i))
        a[str(i)] = []

    len_loss = 0

    for i in experiments:

        d = df[df["experiment"] == i]

        for node in range(len(nodes)):
            loss = d[d["node_id"] == nodes[node]]["loss"].tolist()
            len_loss = len(loss)
            # print(len(loss))
            # print(loss)
            for j in range(len(loss)):
                a[str(node)].append(loss[j])
                None

        for x in range(len(loss)):
            a["experiment"].append(i)
            label = 'Normal'
            label2 = 'Normal'

            # Assign a label
            if i.find('gh') >= 0:
                label = "Attacked"
                label2 = 'Gray Hole'
            elif i.find('bh') >= 0:
                label = "Attacked"
                label = 'Black Hole'
            a["label"].append(label)
            a["label_2"].append(label2)

    data = pd.DataFrame(a)

    return data

def results_3_classes(trace_stats,network_stats,features_to_drop,net_features_to_drop):
    results,net_results=results_2_classes(trace_stats,network_stats,features_to_drop,net_features_to_drop)
    #print(results)
    results=results.reset_index(drop=True)
    net_results=results.reset_index(drop=True)
    net_results=net_results[net_results["Model"]!="Kmeans"]
    results=results[results["Model"]!="Kmeans"]
    return results,net_results


#Run all tests
#Uses stats_per_node as input
#Output results_2_classes_node, results_2_classes_network , results_3_classes_node, results_3_classes_network
def run_all(directory):
    """
    df = pd.read_csv(directory + "/traces/traces.csv", sep=',', encoding='utf-8')

    win_25_stats = create_stats(directory, df, pings=100, window=25)
    win_50_stats = create_stats(directory, df, pings=100, window=50)
    win_100_stats = create_stats(directory, df, pings=100, window=100)
    win_200_stats = create_stats(directory, df, pings=200, window=200)

    stats=pd.DataFrame()
    stats=pd.concat([
        win_25_stats,
        win_50_stats,
        win_100_stats,
        win_200_stats,
    ], ignore_index=True)
    stats.to_csv(directory+"stats_per_node.csv", sep=',', encoding='utf-8')

    """
    df = pd.read_csv(directory + "stats_per_node.csv", sep=',', encoding='utf-8')
    win_25_stats = df[df["window"] == 25]
    win_50_stats = df[df["window"] == 50]
    win_100_stats= df[df["window"] == 100]
    win_200_stats = df[df["window"] == 200]

    trace_stats = {
        25: win_25_stats.drop(columns=["label_2"]),
        50: win_50_stats.drop(columns=["label_2"]),
        100: win_100_stats.drop(columns=["label_2"]),
        200: win_200_stats.drop(columns=["label_2"]),
    }

    net_win_25_stats = create_network_stats(win_25_stats).drop(columns=["label_2"])
    net_win_50_stats = create_network_stats(win_50_stats).drop(columns=["label_2"])
    net_win_100_stats = create_network_stats(win_100_stats).drop(columns=["label_2"])
    net_win_200_stats = create_network_stats(win_100_stats).drop(columns=["label_2"])

    # Create a dictionary containing all the statistics for each trace size
    network_stats = {200: net_win_200_stats, 25: net_win_25_stats, 50: net_win_50_stats, 100: net_win_100_stats}

    features_to_drop = [
        'node_id', 'experiment', 'label', "window",
        "mean",
        #'loss',
        'count',
        'outliers',
        "std",
        #"var",
        "hop",
         #"min",
        "max"
    ]
    net_features_to_drop = ['experiment', 'label']
    results_2_classes_node, results_2_classes_network = results_2_classes(trace_stats,network_stats,features_to_drop,net_features_to_drop)



    #######3 Classes

    df = pd.read_csv(directory + "stats_per_node.csv", sep=',', encoding='utf-8')
    win_25_stats = df[df["window"] == 25].drop(columns="label").rename(columns={"label_2": "label"})
    win_50_stats = df[df["window"] == 50].drop(columns="label").rename(columns={"label_2": "label"})
    win_100_stats = df[df["window"] == 100].drop(columns="label").rename(columns={"label_2": "label"})
    win_200_stats = df[df["window"] == 200].drop(columns="label").rename(columns={"label_2": "label"})
    """win_25_stats = create_stats(directory, df, pings=100, window=25).drop(columns="label").rename(
        columns={"label_2": "label"})
    win_50_stats = create_stats(directory, df, pings=100, window=50).drop(columns="label").rename(
        columns={"label_2": "label"})
    win_100_stats =create_stats(directory, df, pings=100, window=100).drop(columns="label").rename(
        columns={"label_2": "label"})
    win_200_stats = create_stats(directory, df, pings=200, window=200).drop(columns="label").rename(
        columns={"label_2": "label"})"""


    trace_stats_3_classes = {
        25: win_25_stats,
        50: win_50_stats,
        100: win_100_stats,
        200: win_200_stats
    }
    net_win_25_stats = create_network_stats(win_25_stats).drop(columns=["label_2"])
    net_win_50_stats = create_network_stats(win_50_stats).drop(columns=["label_2"])
    net_win_100_stats = create_network_stats(win_100_stats).drop(columns=["label_2"])
    net_win_200_stats = create_network_stats(win_100_stats).drop(columns=["label_2"])

    # Create a dictionary containing all the statistics for each trace size
    network_stats_3_classes = {200: net_win_200_stats, 25: net_win_25_stats, 50: net_win_50_stats,
                               100: net_win_100_stats}



    results_3_classes_node, results_3_classes_network = results_3_classes(trace_stats_3_classes,
                                                                                              network_stats_3_classes,
                                                                                              features_to_drop,
                                                                                              net_features_to_drop)
    return results_2_classes_node, results_2_classes_network , results_3_classes_node, results_3_classes_network

def run_all_corrected(directory):
    print("Processing...")
    df = pd.read_csv(directory + "stats_corrected2.csv")
    df = correct_stats2(df, directory)
    df3 = df.drop(columns="label").rename(columns={"label_2": "label"})
    df2 = df.rename(columns={"label": "label"}).drop(columns="label_2")

    win_25_stats_c = df2[df2["window"] == 25].drop(columns=["mean", "window"])
    win_50_stats_c = df2[df2["window"] == 50].drop(columns=["mean", "window"])
    win_100_stats_c = df2[df2["window"] == 100].drop(columns=["mean", "window"])
    win_200_stats_c = df2[df2["window"] == 200].drop(columns=["mean", "window"])
    trace_stats_corrected_2_classes = {25: win_25_stats_c,
                                       50: win_50_stats_c,
                                       100: win_100_stats_c,
                                       200: win_200_stats_c
                                       }

    win_25_stats_c = df3[df3["window"] == 25].drop(columns=["mean", "window"])
    win_50_stats_c = df2[df3["window"] == 50].drop(columns=["mean", "window"])
    win_100_stats_c = df3[df3["window"] == 100].drop(columns=["mean", "window"])
    win_200_stats_c = df3[df3["window"] == 200].drop(columns=["mean", "window"])
    trace_stats_corrected_3_classes = {25: win_25_stats_c,
                                       50: win_50_stats_c,
                                       100: win_100_stats_c,
                                       200: win_200_stats_c,
                                       }

    features_to_drop = ['node_id', 'experiment',

                        "std",
                         "var",
                        'label',
                        'hop',
                        # 'loss',
                        'count', 'outliers'
                        ]
    net_features_to_drop = ['experiment', 'label']

    results_2_classes_node_16_nodes_corrected, _ = results_2_classes(trace_stats_corrected_2_classes,None,
                                                                        features_to_drop, net_features_to_drop)
    results_3_classes_node_16_nodes_corrected, _ = results_3_classes(trace_stats_corrected_3_classes,
                                                                     None, features_to_drop,
                                                                     net_features_to_drop)
    return results_2_classes_node_16_nodes_corrected,results_3_classes_node_16_nodes_corrected