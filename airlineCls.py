import mysql.connector as mysql

db = mysql.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="airplaneDb"
)

cursor = db.cursor(buffered=True)


class Reservation:
    def __init__(self):
        status = True
        while (status):
            try:
                self.passenger_id = int(input("Put your id "))
                if len(str(self.passenger_id)) == 8:
                    status = False
            except Exception as e:
                print(e)

        self.passenger_fname = str(input("Your name "))
        self.passenger_lname = str(input("Your last name "))
        self.expenses = 0

        self.airplane_seats = {"Business Class": 15,
                               "First Class": 10,
                               "Economy": 12}

        self.airplane_prices = {"Business Class": 1000,
                                "First Class": 1500,
                                "Economy": 2000}

        self.hotel_room = {"Penthouse": 1,
                           "Queen Bedroom": 8,
                           "King Bedroom": 12
                           }

        self.hotel_prices = {"Penthouse": 500,
                             "Queen Bedroom": 250,
                             "King Bedroom": 150}

    def airplane_cost(self):
        status = True
        while (status):

            try:
                self.airplane_input = input("Choose: Business Class:1000,First Class:1500, Economy:2000 ")

                for seat, quantity in self.airplane_seats.items():
                    if seat == self.airplane_input:
                        cursor.execute(
                            "SELECT count(airplane_seat) FROM AirplaneTable WHERE airplane_seat='%s'" % seat)
                        if quantity > cursor.fetchone()[0]:
                            status = False
                            break
                        else:
                            status = True
                            print("not enough room")
                            break
                for seat,value in self.airplane_prices.items():
                    if seat==self.airplane_input:
                        self.expenses+=value
                    break


            except Exception as e:
                print(e)





    def hotel_cost(self):

        status = True

        while (status):

            try:
                self.hotel_choice_input = input("Do you want to check in a hotel? ")

                if self.hotel_choice_input == "yes" or self.hotel_choice_input == "Yes":

                    self.hotel_room_input = input("Choose: Penthouse:500, Queen Bedroom:250,King Bedroom:150 ")
                    for room, value in self.hotel_room.items():
                        if self.hotel_room_input == room:
                            cursor.execute("SELECT count(hotel_room) FROM HotelTable WHERE hotel_room='%s'" % room)
                            if value > cursor.fetchone()[0]:
                                self.expenses += value
                                status=False
                                break
                elif self.hotel_choice_input == "No" or self.hotel_choice_input == "no":
                    self.hotel_room_input = ""
                    print("Okay have a nice day")
                    status = False
                    break
                else:
                    status = True
                    print("Sorry,not enough room")



            except Exception as e:
                print(e)

    def check_expenses(self):
        print("Your cost is", self.expenses)


c = Reservation()
c.airplane_cost()
c.hotel_cost()
c.check_expenses()

# cursor.execute("CREATE TABLE  AirplaneTable (name VARCHAR(50),lastname VARCHAR(50),airplane_seat VARCHAR(50), id int)")
# cursor.execute("CREATE TABLE  HotelTable (name VARCHAR(50),lastname VARCHAR(50),hotel_room VARCHAR(50), id int)")

sql = "INSERT INTO AirplaneTable (name,lastname,airplane_seat,id) VALUES (%s,%s,%s,%s)"
sql1 = "INSERT INTO HotelTable (name,lastname,hotel_room,id) VALUES (%s,%s,%s,%s)"
val = (c.passenger_fname, c.passenger_lname, c.airplane_input, c.passenger_id)

val2 = (c.passenger_fname, c.passenger_lname, c.passenger_id)
val1 = (c.passenger_fname, c.passenger_lname, c.hotel_room_input, c.passenger_id)
cursor.execute(sql, val)

if c.hotel_choice_input == "yes" or c.hotel_choice_input == "Yes":
    cursor.execute(sql1, val1)

db.commit()
