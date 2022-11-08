from peewee import *
from datetime import date
from datetime import datetime
import json


database = PostgresqlDatabase('flightsskewed', **{'host': 'localhost','user': 'vagrant', 'password': 'vagrant'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Airports(BaseModel):
    airportid = CharField(primary_key=True)
    city = CharField(null=True)
    name = CharField(null=True)
    total2011 = IntegerField(null=True)
    total2012 = IntegerField(null=True)

    class Meta:
        table_name = 'airports'

class Airlines(BaseModel):
    airlineid = CharField(primary_key=True)
    hub = ForeignKeyField(column_name='hub', field='airportid', model=Airports, null=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'airlines'

class Customers(BaseModel):
    birthdate = DateField(null=True)
    customerid = CharField(primary_key=True)
    frequentflieron = ForeignKeyField(column_name='frequentflieron', field='airlineid', model=Airlines, null=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'customers'

class Flights(BaseModel):
    airlineid = ForeignKeyField(column_name='airlineid', field='airlineid', model=Airlines, null=True)
    dest = ForeignKeyField(column_name='dest', field='airportid', model=Airports, null=True)
    flightid = CharField(primary_key=True)
    local_arrival_time = TimeField(null=True)
    local_departing_time = TimeField(null=True)
    source = ForeignKeyField(backref='airports_source_set', column_name='source', field='airportid', model=Airports, null=True)

    class Meta:
        table_name = 'flights'

class Flewon(BaseModel):
    customerid = ForeignKeyField(column_name='customerid', field='customerid', model=Customers, null=True)
    flightdate = DateField(null=True)
    flightid = ForeignKeyField(column_name='flightid', field='flightid', model=Flights, null=True)

    class Meta:
        table_name = 'flewon'

class Numberofflightstaken(BaseModel):
    customerid = CharField(null=True)
    customername = CharField(null=True)
    numflights = BigIntegerField(null=True)

    class Meta:
        table_name = 'numberofflightstaken'
        primary_key = False

def runORM(jsonFile):
    with open(jsonFile) as f:
       for line in f:
           temp = (json.loads(line))
 
           if temp.get("newcustomer"):
               new_cust = temp.get("newcustomer")
               sq1 = Customers(name= new_cust.get("name"), customerid=new_cust.get("customerid"), birthdate=new_cust.get("birthdate"), frequentflieron=Airlines.select(Airlines.airlineid).where(Airlines.name == new_cust.get("frequentflieron")))
               sq1.save(force_insert=True)
           elif temp.get("flewon"):
               newflew = temp.get("flewon")
 
               for i in temp.get("flewon").get("customers"):
                   if len(i) > 1:
                       tempCUST = Customers(name = i.get("name"), customerid = i.get("customerid"), birthdate = i.get("birthdate"),frequentflieron = i.get("frequentflieron"))
                       tempCUST.save(force_insert=True)
 
                       sq2 = Flewon(flightid = newflew.get("flightid"),flightdate = newflew.get("flightdate"),customerid = i.get("customerid"))
                       sq2.save(force_insert=True)
                   else:
                       flewon_2 = Flewon(flightid = newflew.get("flightid"),flightdate = newflew.get("flightdate"),customerid = i.get("customerid"))
                       flewon_2.save(force_insert=True)

    Numberofflightstaken.delete().execute()
    
    
    addTEMP = []
    
    for customer in Flewon.select():
        if customer.customerid not in addTEMP:
            holy = Numberofflightstaken(
            customerid = customer.customerid,
            customername = Customers.select(Customers.name).where(Customers.customerid == customer.customerid),
            numflights = Flewon.select(fn.Count(Flewon.customerid)).group_by(Flewon.customerid).where(Flewon.customerid == customer.customerid))
            holy.save(force_insert=True)
            addTEMP.append(customer.customerid)
