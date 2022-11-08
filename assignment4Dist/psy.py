#!/usr/bin/python3
import psycopg2
import json
import sys
from types import *

def runPsy(conn, curs, jsonFile):
    

    with open(jsonFile) as f:
        for line in f:
            temp = (json.loads(line))

           

            if temp.get("newcustomer"):
                new_cust = temp.get("newcustomer")
                sq1 = """ INSERT INTO customers VALUES('%s','%s','%s',(SELECT airlineid FROM airlines WHERE name = '%s'));
                 """%(new_cust.get("customerid"),new_cust.get("name"),new_cust.get("birthdate"),new_cust.get("frequentflieron"))
                
                try:
                     curs.execute(sq1)
                except (Exception,psycopg2.DatabaseError):
                    print("Error424")
            elif temp.get("flewon"):
                newflew = temp.get("flewon")
                for i in temp.get("flewon").get("customers"):
                    if len(i) > 1:
                        tempCUST = """INSERT INTO customers values('%s','%s','%s','%s');
                                      """%(i.get("customerid"),i.get("name"),i.get("birthdate"),i.get("frequentflieron"))

                        try:
                            curs.execute(tempCUST)
                        except (Exception,psycopg2.DatabaseError):
                            print("Error424")


                        sq2 = """ INSERT INTO flewon values('%s','%s','%s');
                                 """%(newflew.get("flightid"),i.get("customerid"),newflew.get("flightdate"))

                        try:
                            curs.execute(sq2)
                        except (Exception,psycopg2.DatabaseError):
                            print("Error424")
                    else:
                        flewon_2 = """INSERT INTO flewon values('%s','%s','%s');
                                     """%(newflew.get("flightid"),i.get("customerid"),newflew.get("flightdate"))
                        try:
                            curs.execute(flewon_2)
                        except (Exception,psycopg2.DatabaseError):
                            print("Error424")
                            

                            
        conn.commit()
