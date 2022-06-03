# giannis mparzas 2765
import sys
import math
import time


############### some functions i need ################
def myFuncx(e):
  return e[1][0]
def myFuncy(e):
  return e[1][2]


def find_avg_mbr(lev):
    lev_start=0
    sum_mbr=0
   
    for i in range(lev):
        lev_start+=nodes_per_level[i]
    lev_nodes=nodes_per_level[lev]
    
    for i in range(lev_start,lev_start+lev_nodes):
        for j in range(len(R_tree[i])):
            m=( R_tree[i][j][1][1]-R_tree[i][j][1][0])*(R_tree[i][j][1][3]-R_tree[i][j][1][2])
            sum_mbr+=m
    return (sum_mbr/lev_nodes)
  
def initial():
  global minx
  global maxx
  global miny
  global maxy
  minx=100
  maxx=0
  miny=100
  maxy=0
  
def find_mbr(nod):
    minx=1000
    miny=1000
    maxx=0
    maxy=0
    mbr=[]
    
    for element in R_tree[nod]:
        
        if (minx>element[1][0]):
            minx=element[1][0]
        if (maxx<element[1][1]):
            maxx=element[1][1]
        if(miny>element[1][2]):
            miny=element[1][2]
        if(maxy<element[1][3]):
            maxy=element[1][3]
    mbr.append(minx)
    mbr.append(maxx)
    mbr.append(miny)
    mbr.append(maxy)
    return mbr




####  x2,x2m,y2,y2m is query window m->max
def intersection_q(x1,x1m,y1,y1m,x2,x2m,y2,y2m):
    if(x1m<x2 or x2m<x1):
        return False
    if(y1m<y2 or y2m<y1):
        return False
    #if(inside_q(x1,x1m,y1,y1m,x2,x2m,y2,y2m) or containment_q(x1,x1m,y1,y1m,x2,x2m,y2,y2m) ):
        #return False
    return True
  
def  inside_q (x1,x1m,y1,y1m,x2,x2m,y2,y2m):
    if( x1>=x2 and x1<=x2m and x1m>=x2 and x1m<=x2m):
        if(y1>=y2 and y1<=y2m and y1m>=y2 and y1m<=y2m):
            return True
    return False

def  containment_q (x1,x1m,y1,y1m,x2,x2m,y2,y2m):
    if( x2>=x1 and x2<=x1m and x2m>=x1 and x2m<=x1m):
        if(y2>=y1 and y1<=y1m and y2m>=y1 and y2m<=y1m):
            return True
    return False
  
     
###################### Read data file ################################


#input_file=sys.argv[1]
input_file="data_rectangles.txt" ######## data file input
f = open(input_file, "r")
all_rectangles=[]
R_tree=[]
nodes_per_level=[]
start_level=[]
stop_level=[]
for line in f.readlines():
     rectangle=[]
     mbr=[]
     line_i=line.split("\t")
     
     mbr.append(float(line_i[1]))
     mbr.append(float(line_i[2]))
     mbr.append(float(line_i[3]))
     mbr.append(float(line_i[4]))
     
     rectangle.append(int(line_i[0]))
     rectangle.append(mbr)
     
     all_rectangles.append(rectangle)
    
rectangles=len(all_rectangles)
print("rectangles found: ",rectangles)

################## Create R tree ################################

node_capacity=math.floor(1024/36)

leave_number=math.ceil(rectangles/node_capacity)
n=math.ceil(math.sqrt(leave_number))
nodes_per_level.append(leave_number)


all_rectangles.sort(key=myFuncx)## sort by x min axis


n_next=[]
take=n*node_capacity


################## Create Level 0 ###############################
print("node_capacity: ",node_capacity)
print("leave_number: ",leave_number)
print("n: ",n)
print("take (n*node_capacity) triangles to order by y :  ",take)
end=0
for rectangle in range(len(all_rectangles)):
    if(rectangle==(len(all_rectangles)-1)):
        end=1
    n_next.append(all_rectangles[rectangle])
    if((rectangle+1)%take==0 or end==1):
          
        node=[]
        #print(n_next[0])
        #print("\n $$$$$")
        n_next.sort(key=myFuncy)## sort by y min  axis
          
        for nod in range(len(n_next)):
            node.append(n_next[nod])
            if((nod+1)%node_capacity==0 ):
                    
                  R_tree.append(node)
                  node=[]
        if( len(node)!=0):
            R_tree.append(node)
        n_next=[]
          




################## Create above Levels ##########################
start=-1
stop=0
komvoi_epipedou=0
minx=100
maxx=0
miny=100
maxy=0
nodes=[]

height=1

while(komvoi_epipedou!=1):
    entries=0
    start=stop
    stop=len(R_tree)
    height+=1
    komvoi_epipedou=0
    taken=[]
    
    for i in range(start,stop):
        

        take=math.ceil(math.sqrt(leave_number))
        for j in range(len(R_tree[i]) ):
                
            ptr=[]
            
            if(j==len(R_tree[i])-1):
              
                maxmbr=find_mbr(i)   
                ptr.append(i)
                ptr.append(maxmbr)
                nodes.append(ptr)
                initial()
                
                entries+=1
                
            if(( entries%take==0 or (i+1)==stop ) and  j==len(R_tree[i])-1 ):#( (i+1)%node_capacity==0 or (i+1)==stop )
                
                entries=0
                    
                if(len(taken)==take or (i+1)==stop):
                    print("###",node[0])
                    nodes.sort(key=myFuncy)## sort by y  min axis
                        
                    for i in nodes:
                        R_tree.append(i)
                    
                initial()
                nodes=[]
                komvoi_epipedou+=1
            
    
    nodes_per_level.append(komvoi_epipedou)
    
print("\n")
print("height of R tree: ",height)
print("\n")
for i in range(len(nodes_per_level)):
    print("in level ",i,"found ",nodes_per_level[i]," nodes")
    print("The avg mbr in level ",i," is ",find_avg_mbr(i))

    

########## Save R tree in txt file #############################


f = open("rtree.txt", "w+")
f.write(str(len(R_tree)-1)+"\n")
f.write(str(len(nodes_per_level))+" \n")
f.write("\n")
for i in range(len(R_tree)):
    f.write(str(i)+","+str(len(R_tree[i])))
    for j in range(len(R_tree[i])):
        f.write(","+str(R_tree[i][j]))
        
    f.write("\n")
    f.write("\n")
    if(len(R_tree[i])<node_capacity):
        f.write("################## TELOS EPIPEDOU ######################## \n")
        f.write("################## TELOS EPIPEDOU ######################## \n\n")

f.close()

################################# [PART 2] Search in  the R tree ##########################



################################# Read Queries #############
#input_queries=sys.argv[2]
input_queries="query_rectangles.txt"
f = open(input_queries, "r") ### query file input
queries=[]

for line in f.readlines():
  
     lin_e=[]
     line_i=line.split("\t")
     
     lin_e.append(float(line_i[1]))
     lin_e.append(float(line_i[2]))
     lin_e.append(float(line_i[3]))
     lin_e.append(float(line_i[4]))
     
     queries.append(lin_e)

#################################### Search in R tree ####################################


def intersection_search(s,q):
    node_accesses_1[0]+=1
    for el in R_tree[s]:
        
        if(s>=leave_number):
            if(intersection_q(el[1][0],el[1][1],el[1][2],el[1][3],queries[q][0],queries[q][1],queries[q][2],queries[q][3])):
                intersection_search(el[0],q)
                  
        else:
          if(intersection_q(el[1][0],el[1][1],el[1][2],el[1][3],queries[q][0],queries[q][1],queries[q][2],queries[q][3])):
              intersection_results.append(el)
              
    
def inside_search(s,q):
    node_accesses_2[0]+=1
    for el in R_tree[s]:
        
        if(s>=leave_number):
            if(intersection_q(el[1][0],el[1][1],el[1][2],el[1][3],queries[q][0],queries[q][1],queries[q][2],queries[q][3])):
                inside_search(el[0],q)
                  
        else:
          if(inside_q(el[1][0],el[1][1],el[1][2],el[1][3],queries[q][0],queries[q][1],queries[q][2],queries[q][3])):
              inside_results.append(el)
              

def containment_search(s,q):
    node_accesses_3[0]+=1
    for el in R_tree[s]:
        
        if(s>=leave_number):
            if(containment_q(el[1][0],el[1][1],el[1][2],el[1][3],queries[q][0],queries[q][1],queries[q][2],queries[q][3])):
                containment_search(el[0],q)
                     
        else:
          if(containment_q(el[1][0],el[1][1],el[1][2],el[1][3],queries[q][0],queries[q][1],queries[q][2],queries[q][3])):
              containment_results.append(el)

      
print("\n")
time0=time.time()
print("-Results for intersection search query")
print("\n")
for i in range(len(queries)):
    intersection_results=[]
    node_accesses_1=[0]
    intersection_search(len(R_tree)-1,i)
    print("Query ",i,"accesses ",node_accesses_1," nodes and find ",len(intersection_results)," rectangles")
    
   
print("-----------------------------------------------------")

print("-Results for inside search query")
print("\n")
for i in range(len(queries)):
    
    inside_results=[]
    node_accesses_2=[0]
    inside_search(len(R_tree)-1,i)
    print("Query ",i,"accesses ",node_accesses_2," nodes and find ",len(inside_results)," rectangles")
    
    
print("-----------------------------------------------------")

print("-Results for containment search query")
print("\n")
for i in range(len(queries)):
   
    containment_results=[]
    node_accesses_3=[0]
    containment_search(len(R_tree)-1,i)
    print("Query ",i,"accesses ",node_accesses_3," nodes and find ",len(containment_results)," rectangles")
    


time1=time.time()
print("-----------------------------------------------------")
print("execute time: ",time1-time0,"sec\n")
print(R_tree[len(R_tree)-1])



