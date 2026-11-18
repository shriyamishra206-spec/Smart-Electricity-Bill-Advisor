#IMPORTING REQUIRED MODULES
import csv
import os
from datetime import datetime

#CSV FILE PATH
folder_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(folder_path, "electricity_bills.csv")

#WELCOME MESSAGE
print("==========================================")
print("           SMART ENERGY ADVISOR")
print("==========================================")
print("Welcome to the Electricity Bill Calculator!")

#MAIN MENU LOOP (runs until the user chooses Exit)
while True:
    print("\n1. Calculate New Electricity Bill")
    print("2. View Previous Electricity Bills")
    print("3. Exit")
    choice = input("\nEnter your choice (1, 2 or 3): ")

    #OPTION 1: CALCULATE NEW ELECTRICITY BILL
    if choice == "1":
        print("\n------ METER READING INPUT ------")
        try:
            previous_reading = float(input("Enter Previous Meter Reading: "))
            current_reading = float(input("Enter Current Meter Reading: "))

            if previous_reading < 0 or current_reading < 0:
                print("\nInvalid Input! Meter readings cannot be negative.")
            elif current_reading < previous_reading:
                print("\nInvalid Input! Current reading cannot be less than previous reading.")
            else:
                units = current_reading - previous_reading
                print("\nUnits Consumed:", units)
                if units <= 100:
                    bill = units * 5
                    status = "Low Consumer"
                elif units <= 300:
                    bill = (100 * 5) + ((units - 100) * 7)
                    status = "Moderate Consumer"
                else:
                    bill = (100 * 5) + (200 * 7) + ((units - 300) * 10)
                    status = "High Consumer"

                #DISPLAYING BILL DETAILS
                print("\n==========================================")
                print("            ELECTRICITY BILL")
                print("==========================================")
                print("Previous Meter Reading:", previous_reading)
                print("Current Meter Reading:", current_reading)
                print("Units Consumed:", units)
                print("First 100 Units: Rs. 5 per unit")
                print("Next 200 Units: Rs. 7 per unit")
                print("Above 300 Units: Rs. 10 per unit")
                print("------------------------------------------")
                print("Total Electricity Bill: Rs.", round(bill, 2))
                print("Consumer Status:", status)
                print("------------------------------------------")

                #ENERGY CONSERVATION ADVICE
                print("\n------ ENERGY CONSERVATION ADVICE ------")
                if status == "Low Consumer":
                    advice = "Great! Maintain your energy-saving habits."
                elif status == "Moderate Consumer":
                    advice = "Switch off unused appliances and use LED bulbs. "
                    advice += f"Cutting {units - 100:.0f} units would make you a Low Consumer and save Rs. {(units - 100) * 7:.2f}."
                else:
                    advice = "Reduce unnecessary AC usage and avoid leaving appliances on standby. "
                    advice += f"Cutting {units - 300:.0f} units would make you a Moderate Consumer and save Rs. {(units - 300) * 10:.2f}."

                #COMPARE WITH LAST SAVED BILL (read before saving the new one)
                last_units = None
                if os.path.isfile(file_path):
                    with open(file_path, "r", newline="") as file:
                        rows = list(csv.reader(file))
                    if len(rows) > 1:
                        last_units = float(rows[-1][3])

                if last_units is not None and last_units > 0:
                    change = ((units - last_units) / last_units) * 100
                    if change > 0:
                        advice += f" Your usage is up {change:.1f}% from your last bill."
                    elif change < 0:
                        advice += f" Your usage is down {abs(change):.1f}% from your last bill. Well done!"
                    else:
                        advice += " Your usage is the same as your last bill."

                print(advice)

                #DATE AND TIME
                date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                print("\nDate and Time:", date_time)

                #SAVING TO CSV
                file_exists = os.path.isfile(file_path)
                with open(file_path, "a", newline="") as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(["Date and Time", "Previous Reading", "Current Reading",
                                         "Units Consumed", "Bill Amount", "Consumer Status", "Energy Advice"])
                    writer.writerow([date_time, previous_reading, current_reading,
                                     units, bill, status, advice])

                print("\nBill successfully saved!")
                print("CSV File Location:", file_path)
                print("==========================================")

        except ValueError:
            print("\nInvalid Input! Please enter numerical values.")

    #OPTION 2: VIEW PREVIOUS ELECTRICITY BILLS
    elif choice == "2":
        print("\n------ PREVIOUS ELECTRICITY BILLS ------")
        if os.path.isfile(file_path):
            with open(file_path, "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    print(" | ".join(row))
        else:
            print("No previous electricity bills found.")

    #OPTION 3: EXIT
    elif choice == "3":
        print("\nThank you for using Smart Energy Advisor!")
        print("==========================================")
        break

    #INVALID MENU CHOICE
    else:
        print("\nInvalid Choice! Please enter 1, 2 or 3.")