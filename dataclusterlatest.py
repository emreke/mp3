import os
import pandas
import numpy
from sklearn.cluster import KMeans
from Tkinter import *
from tkMessageBox import *


app=Tk()
app.geometry("1370x750+0+0")
app.configure(bg="#eeeeee")
#setting the title of the project
app.title("MINI PROJECT")
class ClusterApp(Frame):
    # the textvariables for the entries
    no_cluster=StringVar()
    no_of_times=StringVar()
    resId1=StringVar()
    resId2=StringVar()
    # the constructor
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master=master
        self.creatingWidgets()
    def creatingWidgets(self):
        #the method that creates that creates the UI
        #no of clusters label and entry
        no_cluster_frame=Frame(self.master)
        no_cluster_frame.pack(side="top",anchor="center")
        no_cluster_label=Label(no_cluster_frame,text="No of Clusters (K in KMeans):", font=("calibri",15),width=40)
        no_cluster_entry=Entry(no_cluster_frame,textvariable=self.no_cluster)
        no_cluster_label.pack(side="left")
        no_cluster_entry.pack(side="left")
        #no of clustering times label and entry
        no_clustering_frame=Frame(self.master)
        no_clustering_frame.pack(side="top",anchor="center")
        no_clustering_label=Label(no_clustering_frame,text="No of Clusterings (repeat times):", font=("calibri",15),width=40)
        no_clustering_entry=Entry(no_clustering_frame,textvariable=self.no_of_times)
        no_clustering_label.pack(side="left")
        no_clustering_entry.pack(side="left")
        #restaurant id1 label and entry
        res1_frame=Frame(self.master)
        res1_frame.pack(side="top",anchor="center")
        res1_label=Label(res1_frame,text="Restaurant1:", font=("calibri",15),width=40)
        res1_entry=Entry(res1_frame,textvariable=self.resId1)
        res1_label.pack(side="left")
        res1_entry.pack(side="left")
        # restaurant id2 label and entry
        res2_frame=Frame(self.master)
        res2_frame.pack(side="top",anchor="center")
        res2_label=Label(res2_frame,text="Restaurant2:", font=("calibri",15),width=40)
        res2_entry=Entry(res2_frame,textvariable=self.resId2)
        res2_label.pack(side="left")
        res2_entry.pack(side="left")
        #runcluster cluster button
        
        run_button=Button(self.master,text="RUN CLUSTERS",width=15,font=("calibri",12),
                          command=lambda x=self.no_of_times:self.run_cluster(x.get()) )
        run_button.pack(side="top",anchor="w")
        #output text widget
        self.output=Text(self.master,width=100,height=10,state=DISABLED,bd=0,background="#eeeeee")
        self.output.pack(side="top",anchor="w")
    def transform_column(self,input_fileName):
        #getting the current working directory where the file should be
        file_path=os.getcwd()
        print "the train.csv should be here "+file_path
        #concatenating the cwd with the filename
        file_path+="\\"+input_fileName

        #creating a data frame with pandas
        frame_of_data=pandas.read_csv(file_path)

        #using this istanbul variable to store the istanbul string containing the turkish character 
        istanbul=chr(196)+chr(176)+"stanbul"
        #big city from the column 1 is equal to 1 if Big Cities present else 0
        frame_of_data["City Group"]= (frame_of_data["City Group"]=="Big Cities").astype(int)
        #Type from the column type is equal to 1 if IL present else 0
        frame_of_data["Type"]= (frame_of_data["Type"] == "IL").astype(int)
        #city  from the column city is equal to 1 if City present else 0
        frame_of_data["City"]= (frame_of_data["City"] == istanbul).astype(int)
        #deleting the opendate column
        del frame_of_data['Open Date']
        #normalising all columns except id column
        for col in frame_of_data:
            if col!="Id":
                #selecting the max value from all columns
                col_max=numpy.max(frame_of_data[col])
                #selecting the max value from all columns
                col_min=numpy.min(frame_of_data[col])
                #normalising all columns
                frame_of_data[col]=(frame_of_data[col]-col_min)/(col_max-col_min)
        #returning the normalized dataframe
        return frame_of_data
    def create_clusters(self,dataframe,no_of_clusters):
        #the method that creates clusters given the no_of_clusters and dataframe
        #creaing an instance of the KMeans class setting the n_clusters prop to the no_of clusters given 
        clusters=KMeans(n_clusters=no_of_clusters)
        #creating the clusters
        clustered_data=clusters.fit_predict(dataframe.iloc[:,1:41])
        #concatenating the dataframe form of the cluster created to the id column
        clustered_dataframe=pandas.concat([dataframe['Id'],pandas.DataFrame(clustered_data)],axis=1)
        #renaming the columns
        clustered_dataframe.columns=["Id","Cluster"]
        #writing the concatenated data into a file
        clustered_dataframe.to_csv("clustered_dataframe.csv",header=False,index=False)
        
    def run_cluster(self,cluster_time):
        try:
            cluster_no=int(self.no_cluster.get())
            cluster_time=int(cluster_time)
            resid1=int(self.resId1.get())
            resid2=int(self.resId2.get())
        
            filename="train.csv"
            #calling the transform method to transform the data to normalized dataframe
            dataframe=self.transform_column(filename)
            #getting the clusters to be created
            no_of_clusters=int(self.no_cluster.get())
            #dict to store the coappearing rest_id counts
            coappearing_counts = {}
            #looping through the no of clustering times
            for num in range(cluster_time):
               #calling the create_clusters method
               self.create_clusters(dataframe,no_of_clusters)
               #opening the file
               open_file=open("clustered_dataframe.csv")
               lines=open_file.readlines()
               #Looping thru each lines of the file
               for line_outer in lines:
                   #restaurants id
                   res_id_outer=line_outer.split(",")[0]
                   #cluster value
                   cluster_outer=line_outer.split(",")[1]
                   for line_inner in lines:
                        #restaurants id
                       res_id_inner=line_inner.split(",")[0]
                       #cluster value
                       cluster_inner=line_inner.split(",")[1]
                       #ignoring where the res_ids are equal
                       if (res_id_outer != res_id_inner):
                           #initializing counts the corresponding ids to zero
                           coappearing_counts.setdefault(res_id_inner+","+res_id_outer,0)
                           if (cluster_inner==cluster_outer):
                               #if they belong to the same cluster the count should be incresed by zero
                               coappearing_counts[res_id_inner+","+res_id_outer]+=1
            #no of times the two ids occured in the same cluster
            text= "Restaurant %s and Restaurant %s are placed in the same cluster %d times (out of %d)\n"%(self.resId1.get(),
                                    self.resId2.get(),
                                    coappearing_counts[self.resId1.get()+","+self.resId2.get()],
                                    cluster_time)
            #initiaalising counts
            max_count=[0,0]
            max_appeared_restaurants=["",""]
            res1=self.resId1.get()
            res2=self.resId2.get()
            #getting the no of times the ids appered togeda in d same cluster
            for restaurants_ids in coappearing_counts.keys():
                #appeared together with res id1 
                if res1 in restaurants_ids.split(","):
                    if max_count[0] < coappearing_counts[restaurants_ids]:
                        max_count[0]=coappearing_counts[restaurants_ids]
                        max_appeared_restaurants[0]=restaurants_ids
                #appeared together with res id2 
                if res2 in restaurants_ids.split(","):
                    if max_count[1] < coappearing_counts[restaurants_ids]:
                        max_count[1]=coappearing_counts[restaurants_ids]
                        max_appeared_restaurants[1]=restaurants_ids

            #getting the rest_id paired with the rest_id 1
            resid1=max_appeared_restaurants[0].split(",")
            for index,res_id in enumerate(resid1):
                if self.resId1.get()!= res_id:
                    res1_id=index
                    break
             #getting the rest_id paired with the rest_id 1
            resid2=max_appeared_restaurants[1].split(",")
            for index,res_id in enumerate(resid2):
                if self.resId2.get()!= res_id:
                    res2_id=index
                    break
            #output
            text+="Restaurant %s is placed in the same cluster with Restaurant %s the most frequent (%d times).\n"%(res1,
                                    resid1[res1_id],max_count[0])
            text+="Restaurant %s is placed in the same cluster with Restaurant %s the most frequent (%d times)."%(res2,
                                   resid2[res2_id],max_count[1])
            
            #making the text widget editable so that it can be modified
            self.output.config(state=NORMAL)
            self.output.delete("1.0",END)
            self.output.insert("1.0",text)
            #making the text widget not editable so that it cannot be modified
            self.output.config(state=DISABLED)
        except(ValueError):
            msg=showerror(title="Invalid Input",message="Expecting integer values got wrong values")
            
#running the app
ClusterApp(app).mainloop()
