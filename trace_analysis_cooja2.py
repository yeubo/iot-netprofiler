import pandas as pd
import matplotlib.pyplot as plt
import os
from node import *
from functions import *
from plots import *
from plots_analysis import *
from sklearn.metrics import confusion_matrix
from sklearn.cluster import KMeans
import sklearn.metrics as sm
from sklearn.decomposition import PCA
import random
random.seed(6666)
#Import for Kmeans

def import_Cooja2(plots):
    data=[]
    node_defaults = {
        "aaaa::212:7403:3:303": 1,
        "aaaa::212:7402:2:202": 2,
        "aaaa::212:7404:4:404": 2,
        "aaaa::212:7406:6:606": 2,
        "aaaa::212:7405:5:505": 3,
        "aaaa::212:7407:7:707": 3,
        "aaaa::212:7409:9:909": 3,
        "aaaa::212:7408:8:808": 4,
        "aaaa::212:740a:a:a0a": 4}
    for row in plots:

        #print("Importing ./"+row[0]+"/"+row[1])
        nodeList=import_nodes_Cooja_2(row[0],row[1],node_defaults)
        data.append(nodeList)

    return data
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


def analyze_network(directory,plots,pings,window):
    cases=[]
    casesAccuracy=[]
    for row in plots:
        cases.append(row[1])
        casesAccuracy.append(row[2])
        data=import_Cooja2(plots)
    #pings=getPings(data)
    #All data collection is in variable node that is a list of list of nodes
    #3 nets input x 9 nodes by net
    print("Processing...")
    d={ "label":[],
       "type":[],
        "count":[],
        "std":  [],
        "mean": [],
        "var":  [],
        "hop":[],

       "packet loss":[],
       "outliers":[],
       "node":[]
    }
    #count=[]
    labels=[]
    var=[]
    #window=100
    #stats=pd.DataFrame(columns=columns)
    n=pings

    for i in range(len(data)):
        #window=pings[i]

        for j in range(len(data[i])):
            #n=pings[i]

            #print(n)
            for z in range(0,n,int(window)):
                #if(z+window>n):break
                #print(z,z+window)

                #df1 = df1.assign(e=p.Series(np.random.randn(sLength)).values)
                node=data[i][j].pkts
                name=str(j)+" "+cases[i]
                nodeWindow=node[(node["seq"]<z+window) & (node["seq"]>=z)]
                nodeWindowP=nodeWindow["rtt"]
                d["count"].append(nodeWindowP.count())
                #Case without outliers
                #Case with outliers
                std=0
                if (nodeWindowP.std()>10):
                    std=1
                    std=nodeWindowP.std()

                d["std"].append(std)
                mean=nodeWindowP.mean()
                #if(mean<1):print(mean)
                d["mean"].append(mean)
                var=0
                if (nodeWindowP.var()>var): var=nodeWindowP.var()
                d["var"].append(var)
                d["label"].append(cases[i])
                d["hop"].append(data[i][j].hop)
                d["type"].append(casesAccuracy[i])
                d["outliers"].append(getOutliers(nodeWindow)["rtt"].count())
                missing=window-nodeWindow.count()
                d["node"].append(data[i][j].ip)
                mP=getPercentageMissingPackets(nodeWindow,window)
                PL=0
                if(mP>30):
                    PL=1
                    PL=mP
                d["packet loss"].append(mP)



    stats=pd.DataFrame(d)

    dataK=stats.drop([
        "label",
        "mean",
        "var",
        "std",
        #"packet loss",
        "outliers",
        "hop",
        "count",
        "node",
        #"type"
    ],axis=1)
    dataK=dataK.fillna(0)

    #print(dataK)
    correction=[]
    correction_alt=[]
    col=np.array(dataK["type"])
    dataK=dataK.drop(["type"],axis=1)
    #Creating simple array to correct unsupervised learning
    #NB as it is unsupervised could happen that the correction are inverted
    for i in range(len(col)):
        el=d["type"][i]
        if el=="normal":
            correction.append(1)
            correction_alt.append(0)

        else:

            correction.append(0)
            correction_alt.append(1)


    dataC=stats["label"]
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(dataK)
    labels = kmeans.predict(dataK)
    centroids = kmeans.cluster_centers_
    labels=accuracy_score_corrected(correction,labels)
    predicted=[]
    for i in range(len(labels)):

        if(labels[i]==1):
            predicted.append("normal")
        else: predicted.append("BH")

    #print(len(predicted))
    stats["predicted"]=pd.Series(np.array(predicted))
    stats["predicted number"]=pd.Series(np.array(labels))
    stats["correction number"]=pd.Series(np.array(correction))
    stats_csv=stats[[
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
    stats_csv.to_csv("results_kmeans.csv", sep='\t', encoding='utf-8')
    stats.head()
    net_results={
       "case":[],
        "predicted":[],
        "real":[]
    }
    #print(stats["predicted number"])
    for case in range(len(cases)):
        subset=stats[stats["label"]==cases[case]]
        mean_predicted=str(subset["predicted number"].mean()*100)+"% normal"
        net_results["case"].append(cases[case])
        net_results["predicted"].append(mean_predicted)
        net_results["real"].append(casesAccuracy[case])



    results=pd.DataFrame(net_results)
    results.to_csv("results_network_kmeans.csv", sep='\t', encoding='utf-8')
    print(results)


#End functions from cooja2 -> nodes for kmeans
