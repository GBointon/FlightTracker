import requests
import json
import math
from tkinter import *

base = "https://7302htasp6.execute-api.eu-west-1.amazonaws.com/v1/airport/"
base_url = requests.get(base)
base_text = json.loads(base_url.text)
if base_url.status_code!=200:
    output.set("Unable to retreive data! Try again.")
    exit()

airport_ids = []
airport_names = []

for x in base_text: #creating dictionary of airport IDs to names
    airport_names.append(x["name"])
for x in base_text:
    airport_ids.append(x["id"])
names_to_ids = dict(zip(airport_names, airport_ids))
ids_to_names = dict(zip(airport_ids, airport_names))

window = Tk() #setting parameters of UI
window.geometry("320x520")
window.resizable(width=False, height=False)
window.configure(bg="#a8f2f7")
window.title("Travel Cost Calculator")

l1 = Label(window, text = "Departing Airport", bg="#a8f2f7", font=("helvetica 12 bold"))
l1.pack(pady=5)
depart_name = StringVar(window) #dropdown list for airports
depart_name.set("Heathrow Airport")
w = OptionMenu(window, depart_name, *airport_names)
w.pack(pady=5)

l1 = Label(window, text = "Arriving Airport", bg="#a8f2f7", font=("helvetica 12 bold"))
l1.pack(pady=5)
arrive_name = StringVar(window)
arrive_name.set("Heathrow Airport")
y = OptionMenu(window, arrive_name, *airport_names)
y.pack(pady=5)

def ok():
    airportslist1=[]
    airportslist2=[]
    depart=names_to_ids[depart_name.get()]
    arrive=names_to_ids[arrive_name.get()]

    route_url=base+depart+"/to/"+arrive # concatenating url for flight api request
    route_info = requests.get(route_url)
    route=json.loads(route_info.text)
    if route_info.status_code!=200:
        output.set("Unable to retreive data! Try again.")
        exit()
    
    return_route_url=base+arrive+"/to/"+depart # concatenating url for return flight api request
    return_route_info=requests.get(return_route_url)
    return_route=json.loads(return_route_info.text)
    
    arrive_dist=0 #determining journey distance
    for x in route["miles"]:
        arrive_dist+=x
    
    depart_dist=0
    for x in return_route["miles"]:
        depart_dist+=x
    
    for x in route["journey"]: #listing airport name
        airportslist1.append(ids_to_names[x])
    for x in return_route["journey"]:
        airportslist2.append(ids_to_names[x])
    
    travelstr=e.get()
    peoplestr=sp.get()
    
    try:    
        travel=float(travelstr)
        people=int(peoplestr)
        if travel<0 or people<0:
            output.set("You must enter a positive number!")
        return
    except ValueError:
        output.set("You must enter a valid number!")
        return
    car_no = math.ceil(people/4) # calculating cost for each journey
    taxi_cost = 40 * travel * car_no
    car_cost = (20 * travel) + (300 * car_no)
    flight_cost = 10 * arrive_dist * people
    return_flight_cost = 10 * depart_dist * people

    if taxi_cost < car_cost: #if statement for recommendation of car or taxi
        travel_cost = taxi_cost
        rec = "It is cheaper to take a taxi."
    elif taxi_cost > car_cost:
        travel_cost = car_cost
        rec = "It is cheaper to take a car."
    else:
        travel_cost = taxi_cost
        rec = "Either car or taxi will cost the same."
        #string to display all info required
    output.set(rec+"\n\nYour outbound flight goes to: \n"+(str(airportslist1)).replace("'","")[1:-1]+"."
    "\n\nYour return flight goes to: \n"+(str(airportslist2)).replace("'","")[1:-1]+".\n\nThe total"
    " cost of this journey is £"+str("{:.2f}".format((travel_cost+flight_cost+return_flight_cost)/100))+".")

l3 = Label(window, text = "How many miles are \nyou travelling to the airport?", bg="#a8f2f7")
l3.pack(pady=5) #other ui elements
e = Entry(window)
e.insert(0, 0)
e.pack()

l4 = Label(window, text = "How many people are travelling?", bg="#a8f2f7")
l4.pack(pady=5)
sp = Spinbox(window, from_=0, to=100)
sp.pack()

button = Button(window, text="OK", command=ok)
button.pack(pady=8)

output = StringVar()
msg = Message(window, textvariable=output, bg="#a8f2f7")
output.set("")
msg.pack()

window.mainloop()
