#this is basic variable assignment in Python
employee_name = "John Doe"
employee_id = 12345
is_active = True

print(employee_name, employee_id, is_active)

#List & dictionary
employeeList=["John","JAne", "Dom","Doe"]  #list
Hr_data={"John":"HR", "Jane":"Finance", "Dom":"IT", "Doe":"Admin"} #dictionary
print(employeeList[0])
print(Hr_data["Jane"])


#Loops
employees =[{"name":"John","active":True},
          {"name":"Man","active":False}]
for emp in employees:
   if emp["active"]:
      print(emp["name"] ,"is active")