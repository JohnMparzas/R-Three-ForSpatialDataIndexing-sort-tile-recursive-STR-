import time


### x2,x2m,y2,y2m is query window
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

######## read Queries #############
f = open("query_rectangles.txt", "r")
queries=[]

for line in f.readlines():
     lin_e=[]
     line_i=line.split("\t")
     #print(line_i)
     lin_e.append(float(line_i[1]))
     lin_e.append(float(line_i[2]))
     lin_e.append(float(line_i[3]))
     lin_e.append(float(line_i[4]))
     #print(int(line_i[0]))
     #rectangle.append(int(line_i[0]))
     queries.append(lin_e)
     

####### serial

input_file="data_rectangles.txt"
f = open(input_file, "r")

sum_1=[0 for i in range(len(queries))]
sum_2=[0 for i in range(len(queries))]
sum_3=[0 for i in range(len(queries))]
sum_4=[0 for i in range(len(queries))]

time0=time.time()

for line in f.readlines():
     rectangle=[]
     mbr=[]
     line_i=line.split("\t")
     #print(line_i)
     for i in range(len(queries)):
          if(intersection_q(float(line_i[1]),float(line_i[2]),float(line_i[3]),float(line_i[4]),queries[i][0],queries[i][1],queries[i][2],queries[i][3])):
               sum_1[i]+=1  

          if(inside_q(float(line_i[1]),float(line_i[2]),float(line_i[3]),float(line_i[4]),queries[i][0],queries[i][1],queries[i][2],queries[i][3])):
               sum_2[i]+=1
          if(containment_q(float(line_i[1]),float(line_i[2]),float(line_i[3]),float(line_i[4]),queries[i][0],queries[i][1],queries[i][2],queries[i][3])):
               sum_3[i]+=1
          if(inside_q(queries[i][0],queries[i][1],queries[i][2],queries[i][3],float(line_i[1]),float(line_i[2]),float(line_i[3]),float(line_i[4]))):
               sum_4[i]+=1

time1=time.time()
print("execute time: ",time1-time0,"sec\n")
for i in range(len(queries)):         
     print("gia thn query",i," intersection_q ",sum_1[i])  
     print("gia thn query ",i,"inside_q ",sum_2[i])    
     print("gia thn query ",i,"containment_q ",sum_3[i])













     
