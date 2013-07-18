# Code to convert .spm files to the Triangle format as described by the fluidity manual. Output is .node, .ele and .face files. 
# Code also produces .vtu files. 
# Must type .spm file you wish to convert into command line when executing program
# .spm file must have 7 face selections named 'Face1', 'Face2',....'Face6', 'Interface' and 1 material selection named 'mat1'




def MakeFile(file_name):	#Function to create new files
	file = open(file_name, 'w')
	file.write(' ')
	file.close()

import sys					#importing useful modules
import vtk
from numpy import array

points = []					#creating empty lists for .vtu files
tets = []
tris = []




# ---------------Creating .node file for mesh--------------- #

MakeFile('mesh_with_interface.node')

with open(sys.argv[1],"r") as infile:				#open up file given in command line
	headerline = infile.readline()
	header2 = infile.readline()						#ignore first few lines
	no_vertices = infile.readline()
	vert_coordinates = infile.readline()			#collecting coordinates of vertices
	xyz = vert_coordinates.split("    ")			#split line into sets of coordinates
	xyz.remove('\n')								#remove newline symbol from list 



with open('mesh_with_interface.node', 'w') as file:
	line1 = no_vertices.strip() + " 3 0 0"			
	file.write(line1 + '\n')						#add first line (number of vertices, dimensions(3) and 0 0) to .node file
	count = 0
	for string in xyz:
		count += 1									#count vertice number
		countst = repr(count)
		file.write(countst + ' ' + string + '\n')	#add vertice number, its coordinates and newline to .node file
		points.append([float(x) for x in string.split()])

# -------------------.node file finished------------------- #




# ---------------Creating .ele file for mesh--------------- #

MakeFile('mesh_with_interface.ele')

with open(sys.argv[1],"r") as f:
	lines = f.readlines()[6:]										#ignore first few lines
	no_ele = lines[0]
	node_per_ele = lines[1]
	line1 = no_ele.strip() + " " + node_per_ele.strip() + " 1"		#creating first line (total number of elements, nodes per element)
	
	for i in lines:
       	   
        	if i.strip() == "mat1":									#find lines with selection info	
            		start = lines.index(i)  
			selectionlines = [item.rstrip('\n') for item in lines[start:start + 4]] #lines of interest into list               
			
			mat1 = ([int(i) for i in selectionlines[3].split()])	#split line up so elements are separated		
			
				
			
			
			
    	
	with open('mesh_with_interface.ele', 'w') as f2:
		
		f2.write(line1 + '\n')				#adding first line to .ele file
		count = 0
								
		nodes_list = []						#create list for .face file later
		
		
		for i in lines[2:]:
			if i != lines[1] and i != lines[0] and i != " ":		#ignore blank lines and nodes per element lines	
				I = i.strip('\n')			#remove newline character
				I2 = I.lstrip()				#remove white space			
				count += 1					#count element number
				
				I3 = I2.split()
				I3 = [int(x) for x in I3]	#convert to integers 
				I3 = [x+1 for x in I3]		#so that 1 can be added to all (.spm counts from 0)
				I3 = [str(x) for x in I3]	#convert back to string and join so can easily be added to file
				node_string = ' '.join(I3)
				tets.append([int(x) for x in node_string.split()])	#entering info into list for .vtu file
				nodes_list.append(I3)		#adding node and element info for .face file later)
				countstr = repr(count)
												
				if count-1 in mat1:			#assign material ID
					matID = "1"
					f2.write(countstr + " " + node_string + " " + matID + '\n')
				
				
				
				if count == float(no_ele):
					break					#stop loop when total number of elements has been reached


# --------------------.ele file finished-------------------- #




# ---------------Creating .face file for mesh--------------- #


MakeFile('mesh_with_interface.face')

			
def WriteNodes(list,ID): 							#Function to enter face number, its nodes and surface ID into the file
		global count
		for i in list:
			count += 1								#count face number
			countstr = repr(count)
			if i[1] == 0:							#2nd number in each pair gives orientation info (0=012, 1=103, 2=213, 3=023)
				nodes = nodes_list[i[0]]			#extract nodes from list
				nodes2 = [nodes[j] for j in 0,1,2] 	#add face nodes to list (0=012, 1=103, 2=213, 3=023)
				tris.append(nodes2)			
				NODES = " ".join(nodes2)	
				f4.write(countstr + " " + NODES + " " + ID + '\n') 	#add face number, nodes, and face ID to file
			elif i[1] == 1:
				nodes = nodes_list[i[0]] 
				nodes2 = nodes[:]
				nodes2 = [nodes[j] for j in 1,0,3]
				tris.append(nodes2)
				NODES = " ".join(nodes2)	
				f4.write(countstr + " " + NODES + " " + ID + '\n')
			elif i[1] == 2:
				nodes = nodes_list[i[0]]
                                nodes2 = [nodes[j] for j in 2,1,3]
				tris.append(nodes2)
				NODES = " ".join(nodes2)	
				f4.write(countstr + " " + NODES + " " + ID + '\n')
			elif i[1] == 3:
				nodes = nodes_list[i[0]] 
				nodes2 = [nodes[j] for j in 0,2,3]
				tris.append(nodes2)
				NODES = " ".join(nodes2)	
				f4.write(countstr + " " + NODES + " " + ID + '\n')	


I3 = [str(x) for x in I3]		

with open(sys.argv[1],"r") as f3:				#open up file given in command line and read
    	f3lines = f3.readlines()
    	for i in f3lines:
        	       
        	if i.strip() == "Face1":			#find index of first line of interest
            		startline = f3lines.index(i)                   
    	facelines = [item.rstrip('\n') for item in f3lines[startline:startline + 39]] #put lines of interest into list
    	total_faces = str((int(facelines[2]) + int(facelines[9]) + int(facelines[16]) + int(facelines[23]) + int(facelines[30]) + int(facelines[37])) / 2)		#find total number of faces (half the values given in .spm file due to 									additional orientation info)
	
			
    	face1 = ([int(i) for i in facelines[3].split()])		
	Face1 = [[face1[i],face1[i+1]] for i in range(0,len(face1)-1,2)]	#pair each element face with orientation information

	face2 = ([int(i) for i in facelines[10].split()])
	Face2 = [[face2[i],face2[i+1]] for i in range(0,len(face2)-1,2)]

	face3 = ([int(i) for i in facelines[17].split()])
	Face3 = [[face3[i],face3[i+1]] for i in range(0,len(face3)-1,2)]
	
	face4 = ([int(i) for i in facelines[24].split()])
	Face4 = [[face4[i],face4[i+1]] for i in range(0,len(face4)-1,2)]

	face5 = ([int(i) for i in facelines[31].split()])
	Face5 = [[face5[i],face5[i+1]] for i in range(0,len(face5)-1,2)]

	face6 = ([int(i) for i in facelines[38].split()])
	Face6 = [[face6[i],face6[i+1]] for i in range(0,len(face6)-1,2)]
	
	
	count = 0
	
	with open('mesh_with_interface.face','w') as f4:
		f4.write(total_faces + " 1" + '\n')		#add first line to .face file (total number of faces, and 1)	
		   
		WriteNodes(Face1,"1")					#add nodes for all 6 faces to file
		WriteNodes(Face2,"2")
		WriteNodes(Face3,"3")
		WriteNodes(Face4,"4")
		WriteNodes(Face5,"5")
		WriteNodes(Face6,"6")
		

# --------------------.face file finished-------------------- #




# --------------------Creating .vtu files-------------------- #

pts = vtk.vtkPoints()

pts.SetNumberOfPoints(len(points))
for p in range(len(points)):
	pts.SetPoint(p, points[p][0], points[p][1], points[p][2])


ug_tets = vtk.vtkUnstructuredGrid()
ug_tets.SetPoints(pts)
for cell in tets:
	c = vtk.vtkIdList()
	for i in cell:
		c.InsertNextId(i-1)
	ug_tets.InsertNextCell(10, c)

tet_writer = vtk.vtkXMLUnstructuredGridWriter()
tet_writer.SetFileName("elements.vtu")
tet_writer.SetInput(ug_tets)
tet_writer.Write()


ug_tris = vtk.vtkUnstructuredGrid()
ug_tris.SetPoints(pts)
for cell in tris:
	c = vtk.vtkIdList()
	for i in cell:
		c.InsertNextId(int(i)-1)
	ug_tris.InsertNextCell(5, c)


tri_writer = vtk.vtkXMLUnstructuredGridWriter()
tri_writer.SetFileName("facets.vtu")
tri_writer.SetInput(ug_tris)
tri_writer.Write()

# --------------------.vtu files finished-------------------- #
