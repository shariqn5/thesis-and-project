

import sys
import copy

def readNetlist(file):
	totalports = int(file.readline())
	inputs  = file.readline().split()
	inputs.sort()
	outputs = file.readline().split()
	outputs.sort()
	#mapping1apping
	mapping = {}
	while True:
		line = file.readline().strip()
		if not line:
			break

		net,name = line.split()
		mapping[name] = int(net)

	# read gates
	gates = []
	for line in file.readlines():
		bits = line.split()
		gate = bits.pop(0)
		ports = list(map(int,bits))
		gates.extend([(gate,ports)])
		
	return inputs,outputs,mapping,gates,totalports

# read netlists
inputs1, outputs1, mapping1, gates1, totalports1 = readNetlist(open(sys.argv[1],"r"))
inputs2, outputs2, mapping2, gates2, totalports2 = readNetlist(open(sys.argv[2],"r"))
# add your code here!

##mapping of ports (map2)
for z in mapping2:
	mapping2[z]=mapping2.get(z, 1) + totalports1


#print(mapping2)

#updating gate 2 ports
new_gate=len(gates2)
#print(new_gate)
j=0
i=0
while new_gate>0:
	new_gate1=len(gates2[i][1])
	while new_gate1>0:
		gates2[i][1][j]+=totalports1
		j=j+1
		new_gate1=new_gate1-1
	i=i+1
	j=0
	new_gate=new_gate-1	
#concatenate gates1 and gates 2 and to form new gates 3
gates3 = list(gates1)
gates3.extend(gates2)

#print(gates3)

outputsneew = []
#meiter circuit
outputsneew=[]
for i,value in enumerate(outputs1):
	gates3.insert(3,('xor',[mapping1[outputs1[i]],mapping2[outputs2[i]],totalports2+totalports1+i+1]))
	outputsneew.extend([totalports2+totalports1+i+1])

#adding final or gate
gates3.extend([('finalor', outputsneew)])
#print(gates3)

#connecting equivalency circuit
for i in inputs1:
	z=i
	a=mapping1[i]
	for j in inputs2:
		x=j
		b=mapping2[j]
		if z==x:
			gates3.extend([( 'equiv', [a,b])])
		else:
			pass	
if len(inputs2)>len(inputs1):
	gates3.extend([('equiv',[mapping1[inputs1[0]],mapping2[inputs2[0]]])])
	gates3.extend([('equiv',[mapping1[inputs1[1]],mapping2[inputs2[1]]])])
else:
	pass
######creating CNF
def cnf(a):
	CNF=[]
	cnf_len=len(a)
	#condition verification 
	while cnf_len>0:
		#for storing 0th element and then removing
		x=a.pop(0)
		if x[0] == 'xor':  
			CNF.extend([(-x[1][0], x[1][1], x[1][2])])
			CNF.extend([(x[1][0], -x[1][1], x[1][2])])
			CNF.extend([(x[1][0], x[1][1], -x[1][2])])
			CNF.extend([(-x[1][0], -x[1][1], -x[1][2])])  
		elif x[0] =='and':
			CNF.extend([(x[1][0],-x[1][2])])
			CNF.extend([(x[1][1],-x[1][2])])
			CNF.extend([(-x[1][0],-x[1][1],x[1][2])])
		  
		elif x[0]=='or':
			CNF.extend([(-x[1][0],x[1][2])])
			CNF.extend([(-x[1][1],x[1][2])])
			CNF.extend([(x[1][0],x[1][1],-x[1][2])])
		elif x[0]=='inv':
			CNF.extend([(x[1][0],x[1][1])])
			CNF.extend([(-x[1][0],-x[1][1])])
		elif x[0]=='finalor':
			CNF.extend([outputsneew])
		elif x[0]=='equiv':
			CNF.extend([(-x[1][0],x[1][1])])
			CNF.extend([(x[1][0],-x[1][1])])
		cnf_len=cnf_len-1	
	# returning new Generated CNF	
	return CNF
#calling of CNF function					
CNF=cnf(gates3)
#print(CNF)
listofcnf = []
#converting cnf into list
listofcnf=list(map(list, CNF))

print('orignal cnf')
print(listofcnf)
#loop for checking Satisfiable or Not Satisfiable
def repeatloop(a):
 	abc=backtracking(a)
 	if len(abc)==0:
 		s='Satisfiable,Circuits are not equivalent'
 		return s
 	elif len(abc)>0:
 		for i in abc:
 			if len(i)==0:
 				t='Not Satisfiable,Circuits are equivalent'
 				return t
 		
 		previouscnf=copy.deepcopy(abc)
 		answer=posbacktracking(abc)		
 		solution=repeatloop(answer)		
 		#print(solution)
 		if solution=='Not Satisfiable,Circuits are equivalent':
 			answer=negbacktracking(previouscnf)
 			solution=repeatloop(answer)
 		return solution
#appending with positive value
def posbacktracking(positive_value):
	value=abs(positive_value[-1][-1])
	positive_value.extend([[value]])
	return positive_value
#appending with negative value	
def negbacktracking(negative_value):
	value=abs(negative_value[-1][-1])
	negative_value.extend([[-value]])
	return negative_value
#creating dicitionary for counter example
counter={}
#function for cancelling clause and litreals and unit clause 
def backtracking (listofcnfback):
	print(listofcnfback)
	for x in listofcnfback :
		#print(x)
		if len(x)==1:
			#print(x)
			for back_clause in reversed (listofcnfback):
				for back_litreal in back_clause:
					if back_litreal==x[0] and x[0]>0:
						counter[abs(x[0])]=1
						listofcnfback.remove(back_clause)
					elif back_litreal==-x[0] and x[0]>0:
						counter[abs(x[0])]=1
						back_clause.remove(back_litreal)
					if back_litreal==x[0] and x[0]<0:
						counter[abs(x[0])]=0
						listofcnfback.remove(back_clause)
					elif -back_litreal==x[0] and x[0]<0:
						counter[abs(x[0])]=0
						back_clause.remove(back_litreal)	
	# list comprehension method for sending back CNF for unit clause removal				
	[backtracking(listofcnfback) for j in listofcnfback if len(j)==1]
	
	print(listofcnfback)		
	return listofcnfback
#After cnf generation main task start from here
solution=repeatloop(listofcnf) 
print(solution)
if solution=='Satisfiable,Circuits are not equivalent':
	print('counter example is:')
	print('input1')
	for x in counter:
		for inputs in inputs1:
			if x == mapping1[inputs]:
				y=counter.get(x)
				print(inputs,'=',y)

		
	print('output1')
	for x in counter:
		for output in outputs1:
			if x == mapping1[output]:
				y=counter.get(x)
				print(output,'=',y)

	print('output2')	
	for x in counter:
		for output in outputs2:
			if x == mapping2[output]:
				y=counter.get(x)
				print(output,'=',y)
