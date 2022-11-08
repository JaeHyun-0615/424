# EXPLANATION: The given left-join query fails because ...
#
#
queryWilliam = """
select c.customerid, c.name, count(f.*)
from customers c full outer join flewon f on (c.customerid = f.customerid)
where c.name like 'William%'
group by c.customerid, c.name
order by c.customerid;

"""



# NOTE:  This trigger is both INCORRECT and INCOMPLETE. You need to find and fix the bugs, and ensure
# that it will correctly update NumberOfFlightsTaken on both insertions and deletions from "flewon".
queryTrigger = """

CREATE OR REPLACE FUNCTION updateStatusCount() RETURNS trigger AS $updateStatus$
		DECLARE
			old_flight_count integer;
		BEGIN
            IF (TG_OP = 'INSERT') THEN
                IF EXISTS (SELECT customerid FROM NumberOfFlightsTaken WHERE customerid = NEW.customerid) THEN
                    UPDATE NumberOfFlightsTaken
                    SET numflights = numflights + 1
                    WHERE customerid = NEW.customerid;
                ELSE
                    INSERT INTO NumberOfFlightsTaken
                    VALUES(NEW.customerid, (SELECT name from customers where customerid = NEW.customerid), 1);
                END IF;
            ELSE
                SELECT numflights INTO old_flight_count FROM NumberOfFlightsTaken WHERE customerid = OLD.customerid;
                    IF old_flight_count = 1 THEN
                        DELETE FROM NumberOfFlightsTaken WHERE customerid = OLD.customerid;
                    ELSE
                        UPDATE NumberOfFlightsTaken
                        SET numflights = old_flight_count - 1
                        WHERE customerid = OLD.customerid;
                    END IF;
            END IF;
        RETURN NULL;
        
		END;
$updateStatus$ LANGUAGE plpgsql;

CREATE TRIGGER update_num_status AFTER
INSERT OR DELETE ON flewon
FOR EACH ROW EXECUTE PROCEDURE updateStatusCount();
END;

"""


