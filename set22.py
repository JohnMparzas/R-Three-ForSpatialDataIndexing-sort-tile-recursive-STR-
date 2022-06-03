# Stefanos Tononidis 2833

import sys
import time
import math

t = time.time()
t1 = time.time()

########################## Reading the data ##########################

# If you have a diffrent name you can specify it as a command line argument
try:

    rectangles_fp = open(sys.argv[1], 'r')

except IndexError:

    rectangles_fp = open('data_rectangles.txt', 'r')

except FileNotFoundError:

    rectangles_fp = open('data_rectangles.txt', 'r')


rectanglesList = []

rectangles_line = rectangles_fp.readline()

while rectangles_line:

    rectangles_split = rectangles_line.split('\t')

    id_ = int(rectangles_split[0])
    x_low = float(rectangles_split[1])
    x_high = float(rectangles_split[2])
    y_low = float(rectangles_split[3])
    y_high = float(rectangles_split[4])

    rectanglesList.append((id_, x_low, x_high, y_low, y_high))

    rectangles_line = rectangles_fp.readline()

NODE_BYTES_CAPACITY = 1024
RECTANGLES_BYTES = 36
ratio = math.floor(NODE_BYTES_CAPACITY / RECTANGLES_BYTES)


########################## Finding the r tree ##########################

tree = []
statisticsList = []
idCounter = 0

def sortTileRecursive(rectanglesList):
    
    global tree
    global statisticsList
    global idCounter

	#sort by x
    rectanglesList = sorted(rectanglesList, key=lambda x: x[1])

	#exit condition
    if len(rectanglesList) == 1:

        return

    number_of_rectangles = len(rectanglesList)
    number_of_leaf_nodes = math.ceil(number_of_rectangles / ratio)
    rectangles_list_band = math.ceil(math.sqrt(number_of_leaf_nodes))

	# y ordering
    yOrderList = []

    j = 0
    step = ratio * rectangles_list_band
    for i in range(step, number_of_rectangles + step, step):

        yOrderList.append(sorted(rectanglesList[j:i], key=lambda x: x[3]))

        j = i

    totalArea = 0
    nodeList = []
    nextList = []

	# creating nodes
    for y in yOrderList:

        j = 0
        for i in range(ratio, len(y) + ratio, ratio):

            nodeList.append(y[j:i])

            xmin = min(y[j:i], key=lambda x: x[1])[1]
            xmax = max(y[j:i], key=lambda x: x[2])[2]
            ymin = min(y[j:i], key=lambda x: x[3])[3]
            ymax = max(y[j:i], key=lambda x: x[4])[4]
            
            totalArea = totalArea + (xmax-xmin)*(ymax-ymin)

            nextList.append((idCounter, xmin, xmax, ymin, ymax))
            idCounter = idCounter + 1

            j = i

    tree = tree + nodeList
    statisticsList.append((len(nodeList), totalArea / len(nodeList)))
    
    sortTileRecursive(nextList)

sortTileRecursive(rectanglesList)

elapsed = time.time() - t1
print("Time to create the r tree :\t" + str(elapsed))
print()

print("Number of levels in tree: ", len(statisticsList))


# Print tree statistics
l = 1
for s in statisticsList:
    print("Level ", l, "has ", s[0], "number of nodes and ", s[1], "avarage area")
    l = l + 1
print()

########################## Saving the r tree as txt ##########################

output_fp = open('rTree.txt', 'w')

output_fp.write(str(tree[len(tree) - 1]).strip('[]') + '\n')

output_fp.write("Number of levels: " + str(len(statisticsList)) + '\n')

for nodeId in range(len(tree)):

    line = str(nodeId) + ', ' + str(len(tree[nodeId])) + ', '

    for rectangle in range(len(tree[nodeId])):

        id = str(tree[nodeId][rectangle][0])
        xmin = str(tree[nodeId][rectangle][1])
        xmax = str(tree[nodeId][rectangle][2])
        ymin = str(tree[nodeId][rectangle][3])
        ymax = str(tree[nodeId][rectangle][4])

        line = line + ('(' + id + ', ' + xmin + ', ' +
                       xmax + ', ' + ymin + ', ' + ymax + ')' + ', ')

    output_fp.write(line[0:len(line)-2] + '\n')


########################## Creating the testing rectangles list ##########################
t2 = time.time()

query_fp = open('query_rectangles.txt', 'r')

query = []

query_line = query_fp.readline()

while query_line:

    query_split = query_line.split('\t')

    id_ = int(query_split[0])
    x_low = float(query_split[1])
    x_high = float(query_split[2])
    y_low = float(query_split[3])
    y_high = float(query_split[4])

    query.append((id_, x_low, x_high, y_low, y_high))

    query_line = query_fp.readline()


########################## Finding the intersections ##########################

# Cheack if rectangle is intersected with other
def isIntersected(rectangle, other):

    if((rectangle[1] > other[2]) or (rectangle[2] < other[1])):

        return False

    else:

        if ((rectangle[3] > other[4]) or (rectangle[4] < other[3])):

            return False

        else:

            return True


# Find the results for the query
intersectedRectangles = []
nodesViseted = 0
def findIntesections(rectangle, startLocation):

    global nodesViseted
    nodesViseted = nodesViseted + 1

    for r in tree[startLocation]:

        if startLocation in range(math.ceil(len(rectanglesList) / ratio)):

            if (isIntersected(rectangle, r)):

                intersectedRectangles.append(r)

        else:

            if (isIntersected(rectangle, r)):

                findIntesections(rectangle, r[0])

    return


# Find the results for the query
intersectedResults = []
nodesVisetedList1 = []
for q in query:

    intersectedRectangles = []
    nodesViseted = 0
    findIntesections(q, startLocation = len(tree) - 1)
    intersectedResults.append(intersectedRectangles)
    nodesVisetedList1.append(nodesViseted)


########################## Finding the inside rectangles ##########################

# Cheack if other is inside in rectangle (for the oposide swap the arguments)
def isInside(rectangle, other):

    if((rectangle[1] <= other[1]) and (rectangle[2] >= other[2])):

        if ((rectangle[3] <= other[3]) and (rectangle[4] >= other[4])):

            return True

        else:

            return False

    else:

        return False

    

insideRectangles = []
nodesViseted = 0
def findInside(rectangle, startLocation):

    global nodesViseted

    nodesViseted = nodesViseted + 1
    
    for r in tree[startLocation]:

        if startLocation in range(math.ceil(len(rectanglesList) / ratio)):

            if (isInside(rectangle, r)):

                insideRectangles.append(r)

        else:

            if (isIntersected(rectangle, r)):

                findInside(rectangle, r[0])

    return


# Find the results for the query
insideResults = []
nodesVisetedList2 = []
for q in query:

    insideRectangles = []
    nodesViseted = 0
    findInside(q, startLocation = len(tree) - 1)
    insideResults.append(insideRectangles)
    nodesVisetedList2.append(nodesViseted)


########################## Finding the contained rectangles ##########################

containedRectangles = []
nodesViseted = 0
def findContained(rectangle, startLocation):

    global nodesViseted
    
    nodesViseted = nodesViseted + 1

    for r in tree[startLocation]:

        if startLocation in range(math.ceil(len(rectanglesList) / ratio)):

            if (isInside(r, rectangle)):

                containedRectangles.append(r)

        else:

            if (isInside(r, rectangle)):

                findContained(rectangle, r[0])

    return


containedResults = []
nodesVisetedList3 = []
for q in query:

    containedRectangles = []
    nodesViseted = 0
    findContained(q, startLocation = len(tree) - 1)
    containedResults.append(containedRectangles)
    nodesVisetedList3.append(nodesViseted)

elapsed = time.time() - t2
print("Time to search the r tree :\t" + str(elapsed))
print()
    
########################## Print results ##########################

l = 0
for r in range(len(query)):
    
    print("Intersetions results for query", r, ":", "matched results =", len(intersectedResults[r]), "and nodes searched =", nodesVisetedList1[r])
    print("Inside results for query", r, ":", "matched results =", len(insideResults[r]), "and nodes searched =", nodesVisetedList2[r])
    print("Contained results for query", r, ":", "matched results =", len(containedResults[r]), "and nodes searched =", nodesVisetedList3[r])
    print()
    

elapsed = time.time() - t
print("Time to complete :\t" + str(elapsed))