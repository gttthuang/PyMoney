import sys

def initialize(data_file):
    records = []
    money = 0
    
    try:
        with open(data_file, 'r') as f:
            # Check if file is empty
            first_line = f.readline().strip()
            if not first_line:  # Handle empty file
                try:
                    money = int(input("How much money do you have? "))
                except ValueError:
                    sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                return money, records

            # Process the first line (money)
            try:
                money = int(first_line)
            except ValueError:
                sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                return money, records

            for line in f:
                if line := line.strip():
                    records.append(line)
            print("Welcome back!")
    except FileNotFoundError:
        try:
            money = int(input("How much money do you have? "))
        except ValueError:
            sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
    
    return money, records

def add(money, records):
    print("Add some expense or income records with description and amount:")
    print("desc1 amt1, desc2 amt2, desc3 amt3, ...")
    items = input()
    
    for item in items.split(","):
        item = item.strip()

        # Check if the format is valid
        try:
            description, amount = item.split()
            try:
                amount_value = int(amount)  # Validate amount is a number
            except ValueError:
                sys.stderr.write("Invalid value for money.\n")
                sys.stderr.write("Fail to add a record.\n")
                continue
        except ValueError:
            sys.stderr.write("The format of a record should be like this: breakfast -50.\n")
            sys.stderr.write("Fail to add a record.\n")
            continue
            
        money += amount_value
        records.append(f"{description} {amount}")
        print(f"{description} {amount}")
    
    return money, records

def view(money, records):
    print("Here's your expense and income records:")
    print(f"{'Description':<20}{'Amount':<10}")
    print("===================================")
    for record in records:
        description, amount = record.split()
        print(f"{description:<20}{amount:<10}")
    print("===================================")
    print("Now you have", money, "dollars.")

def delete(money, records):
    record = input("Which record do you want to delete?\n")
    
    # Check if the format is valid
    try:
        description, amount = record.split()
        try:
            amount_value = int(amount)
        except ValueError:
            sys.stderr.write("Invalid format. Fail to delete a record.\n")
            return money, records
    except ValueError:
        sys.stderr.write("Invalid format. Fail to delete a record.\n")
        return money, records
    
    if record in records:
        records.remove(record)
        money -= amount_value
    else:
        sys.stderr.write(f"There's no record with {record}. Fail to delete a record.\n")
    
    return money, records

def save(data_file, money, records):
    with open(data_file, 'w') as f:
        f.write(f"{money}\n")
        for record in records:
            f.write(f"{record}\n")

def main():
    data_file = "record.txt"
    money, records = initialize(data_file)
    
    while True:
        try:
            prompt = input("What do you want to do (add / view / delete / exit)?")
            if prompt == "add":
                money, records = add(money, records)
            elif prompt == "view":
                view(money, records)
            elif prompt == "delete":
                money, records = delete(money, records)
            elif prompt == "exit":
                save(data_file, money, records)
                break
            else:
                sys.stderr.write("Invalid command. Try again.\n")
        except EOFError:
            break

if __name__ == "__main__":
    main()
