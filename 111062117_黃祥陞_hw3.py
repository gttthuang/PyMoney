import sys

def initialize_categories():
    """Return the predefined multi-level list of categories and subcategories."""
    return [
        'expense',
        ['food', ['meal', 'snack', 'drink']],
        ['transportation', ['bus', 'railway']],
        'income',
        ['salary'],
        ['bonus']
    ]

def view_categories(categories, indent=0):
    """Recursively print categories with indentation."""
    for cat in categories:
        if isinstance(cat, str):
            print('  ' * indent + f'- {cat}')
        elif isinstance(cat, list):
            view_categories(cat, indent + 1)

def is_category_valid(category, categories):
    """Recursively check if category is in categories."""
    for cat in categories:
        if isinstance(cat, str):
            if cat == category:
                return True
        elif isinstance(cat, list):
            if is_category_valid(category, cat):
                return True
    return False

def find_subcategories(target, categories):
    """Return a flat list of target and all its subcategories."""
    result = []
    found = False
    for i, cat in enumerate(categories):
        if isinstance(cat, str):
            if cat == target:
                found = True
                result.append(cat)
        elif isinstance(cat, list):
            if found:
                # The next list after a found string is its subcategories
                result += flatten_categories(cat)
                found = False
            else:
                result += find_subcategories(target, cat)
    return result

def flatten_categories(categories):
    """Flatten a nested category list into a flat list of strings."""
    result = []
    for cat in categories:
        if isinstance(cat, str):
            result.append(cat)
        elif isinstance(cat, list):
            result += flatten_categories(cat)
    return result

def initialize(data_file):
    """Load money and records from file, or prompt for money if file not found/empty."""
    records = []
    money = 0
    try:
        with open(data_file, 'r') as f:
            first_line = f.readline().strip()
            if not first_line:
                try:
                    money = int(input("How much money do you have? "))
                except ValueError:
                    sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                return money, records
            try:
                money = int(first_line)
            except ValueError:
                sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                return money, records
            for line in f:
                if line := line.strip():
                    # category, description, amount
                    parts = line.split(',')
                    if len(parts) == 3:
                        records.append(tuple(part.strip() for part in parts))
            print("Welcome back!")
    except FileNotFoundError:
        try:
            money = int(input("How much money do you have? "))
        except ValueError:
            sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
    return money, records

def add(money, records, categories):
    """Add new records with category, description, and amount."""
    print("Add some expense or income records with category, description, and amount (separate by spaces):")
    print("cat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...")
    items = input()
    for item in items.split(","):
        item = item.strip()
        try:
            category, description, amount = item.split()
            try:
                amount_value = int(amount)
            except ValueError:
                sys.stderr.write("Invalid value for money.\nFail to add a record.\n")
                continue
        except ValueError:
            sys.stderr.write("The format of a record should be like this: cat desc amt.\nFail to add a record.\n")
            continue
        if not is_category_valid(category, categories):
            sys.stderr.write("The specified category is not in the category list.\nYou can check the category list by command \"view categories\".\nFail to add a record.\n")
            continue
        money += amount_value
        records.append((category, description, amount))
        print(f"{category} {description} {amount}")
    return money, records

def view(money, records):
    """Display all records with category, description, and amount."""
    print("Here's your expense and income records:")
    print(f"{'Category':<15}{'Description':<20}{'Amount':<7}")
    print("="*40)
    for record in records:
        category, description, amount = record
        print(f"{category:<15}{description:<20}{amount:<7}")
    print("="*40)
    print("Now you have", money, "dollars.")

def delete(money, records):
    """Delete a record by specifying category, description, and amount."""
    record = input("Which record do you want to delete? (category description amount)\n")
    try:
        category, description, amount = record.split()
        try:
            amount_value = int(amount)
        except ValueError:
            sys.stderr.write("Invalid format. Fail to delete a record.\n")
            return money, records
    except ValueError:
        sys.stderr.write("Invalid format. Fail to delete a record.\n")
        return money, records
    if (category, description, amount) in records:
        records.remove((category, description, amount))
        money -= amount_value
    else:
        sys.stderr.write(f"There's no record with {record}. Fail to delete a record.\n")
    return money, records

def save(data_file, money, records):
    """Save money and records to file."""
    with open(data_file, 'w') as f:
        f.write(f"{money}\n")
        for record in records:
            f.write(f"{record[0]}, {record[1]}, {record[2]}\n")

def find(records, categories):
    """Find and display records under a category and its subcategories."""
    category = input("Which category do you want to find? ")
    subcats = find_subcategories(category, categories)
    if not subcats:
        print(f"No such category: {category}")
        return
    filtered = list(filter(lambda r: r[0] in subcats, records))
    print(f"Here's your expense and income records under category \"{category}\":")
    print(f"{'Category':<15}{'Description':<20}{'Amount':<7}")
    print("="*40)
    total = 0
    for record in filtered:
        category, description, amount = record
        print(f"{category:<15}{description:<20}{amount:<7}")
        total += int(amount)
    print("="*40)
    print(f"The total amount above is {total}.")

def main():
    """Main loop for the pymoney application."""
    data_file = "record.txt"
    categories = initialize_categories()
    money, records = initialize(data_file)
    while True:
        try:
            prompt = input("What do you want to do (add / view / delete / view categories / find / exit)? ")
            if prompt == "add":
                money, records = add(money, records, categories)
            elif prompt == "view":
                view(money, records)
            elif prompt == "delete":
                money, records = delete(money, records)
            elif prompt == "view categories":
                view_categories(categories)
            elif prompt == "find":
                find(records, categories)
            elif prompt == "exit":
                save(data_file, money, records)
                break
            else:
                sys.stderr.write("Invalid command. Try again.\n")
        except EOFError:
            break

if __name__ == "__main__":
    main()
