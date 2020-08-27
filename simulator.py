import sys
import json
import random

h=[]
d=[]
j=[]
b=[]
g=[]
d=[]
j=[]
b=[]
g=[]
rural=[]
metropolitan=[]
height=[]
ind_height=[]
new_file=input("create new file for fixed or not fixed ( enter yes or no) :")

if len(sys.argv)>1 :
	if sys.argv[1] == 'fixed' and new_file == "yes":
		for z in range(1,21):
			positionx=random.randint(17,21) 
			positiony=random.randint(28,36)
			dota={"bsid":z,"area_type":'rural',"xloction":(positionx),"ylocation":(positiony),"min_height":(z+30),"max_height":(z+40)}
			h.append(dota)
		
		print(h)
		for x in range(1,1000):
			y=random.randint(22,24)
			k=random.randint(24,27)
			z=random.choice(range(1,10))
			loc={"sensornumber":x,"slocx":y,"slocy":k,"sheight":z}
			j.append(loc)

		print(j)
		# print(len(j))
		data={"basestations":h,"simulation":{"basestation_configuration":{"min_nrbs":1,"max_nrbs":20,"max_distance":12,"min_distance":1,"min_antenna_gain":0,"max_antenna_gain":6}},"sensor_configuration":{"min_number_sensors":3,"max_number_sensors":1000,"min_transmit_power":0,"max_transmit_power":20,"min_antenna_gain":0,"max_antenna_gain":3,"min_bw":125,"max_bw":250},"Frequencyalocation":{"frequency_EUstandard":[868.1,868.3,868.5,867.1,867.3,867.5,867.7,867.9]}}
		z=data.pop("sensor_configuration")
		z.update({"sensor_placement":{"sensor_x_y":j}})
		z.update({"Frequencyalocation":{"frequency_EUstandard":[868.1,868.3,868.5,867.1,867.3,867.5,867.7,867.9]}})
		print(z)
		with open('parameters__settings__of__fixedbasestion.json', 'w') as ps:
			json.dump(data,ps)
		with open('parameters__settings__of__fixedsensor_configuration.json', 'w') as ps:
			json.dump(z,ps)
		
	        
	elif sys.argv[1] == 'notfixed' and new_file == "yes" :
		numberofrural=int(input("enter the number of rural areas donot exceed 20 :"))
		averagesendtime1=int(input("enter the averagesendtime(ms) :"))
		averagesendtime2=int(input("enter the second averagesendtime(ms):"))
		averagesendtime3=round((averagesendtime1+averagesendtime2)/2)
		for z in range(1,21):
			positionx=random.randint(17,21) 
			positiony=random.randint(28,36) 
			
			if z>numberofrural:
				area='metropolitan'
			else:
				area='rural'
			dota={"bsid":z,"area_type":area,"xloction":(positionx),"ylocation":(positiony),"min_height":(z+30),"max_height":(z+40)}
			h.append(dota)
		
		for x in range(1,1000):
			y=random.randint(22,24)
			k=random.randint(24,27)
			loc={"sensornumber":x,"slocx":y,"slocy":k}
			j.append(loc)	

		data={"basestations":h,"simulation":{"basestation_configuration":{"min_nrbs":1,"max_nrbs":20,"max_distance":12,"min_distance":1,"min_antenna_gain":0,"max_antenna_gain":6}},"sensor_configuration":{"min_number_sensors":3,"max_number_sensors":1000,"min_transmit_power":0,"max_transmit_power":20,"min_antenna_gain":0,"max_antenna_gain":3,"min_bw":125,"max_bw":250}}
		z=data.pop("sensor_configuration")
		z.update({"sensor_placement":{"sensor_x_y":j}})
		z.update({"Frequencyalocation":{"frequency_EUstandard":[868.1,868.3,868.5,867.1,867.3,867.5,867.7,867.9]},"averagesendtime":{"selectedtime":[averagesendtime1,averagesendtime2,averagesendtime3]}})
		with open('parameters__settings__of__notfixedsensor_configuration.json', 'w') as ps:
			json.dump(z,ps)
		with open('parameters__settings__of__notfixedbasestion.json','w') as ps:
			json.dump(data,ps)	


run=int(input("enter the number of runs :"))

   

for i in range(run):
	exec(open("./completelorawansimnew.py").read())


