import sys

class Record:
    """Represent a record."""
    def __init__(self, category, description, amount):
        self._category = category
        self._description = description
        self._amount = int(amount)

    @property
    def category(self):
        return self._category

    @property
    def description(self):
        return self._description

    @property
    def amount(self):
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the current amount of money."""
    def __init__(self):
        self._records = []
        self._initial_money = 0
        try:
            with open('record.txt', 'r') as f:
                first_line = f.readline().strip()
                if not first_line:
                    try:
                        self._initial_money = int(input("How much money do you have? "))
                    except ValueError:
                        sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                        self._initial_money = 0
                else:
                    try:
                        self._initial_money = int(first_line)
                    except ValueError:
                        sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                        self._initial_money = 0
                for line in f:
                    if line.strip():
                        cat, desc, amt = [x.strip() for x in line.strip().split(',')]
                        self._records.append(Record(cat, desc, amt))
        except FileNotFoundError:
            try:
                self._initial_money = int(input("How much money do you have? "))
            except ValueError:
                sys.stderr.write("Invalid value for money. Set to 0 by default.\n")
                self._initial_money = 0

    def add(self, items, categories):
        """Add records from a string input, checking category validity."""
        for item in items.split(","):
            item = item.strip()
            try:
                category, description, amount = item.split()
                try:
                    amount_value = int(amount)
                except ValueError:
                    sys.stderr.write("Invalid value for money.\nFail to add a record.\n")
                    continue
                if not categories.is_category_valid(category):
                    sys.stderr.write("The specified category is not in the category list.\nYou can check the category list by command \"view categories\".\nFail to add a record.\n")
                    continue
                record = Record(category, description, amount_value)
                self._records.append(record)
                self._initial_money += amount_value
                print(f"{category} {description} {amount}")
            except ValueError:
                sys.stderr.write("The format of a record should be like this: cat desc amt.\nFail to add a record.\n")

    def view(self):
        """Print all records and the balance."""
        print("Here's your expense and income records:")
        print(f"{'Category':<15}{'Description':<20}{'Amount':<7}")
        print("="*40)
        for r in self._records:
            print(f"{r.category:<15}{r.description:<20}{r.amount:<7}")
        print("="*40)
        print(f"Now you have {self._initial_money} dollars.")

    def delete(self, record_str):
        """Delete a record by string."""
        try:
            category, description, amount = record_str.split()
            try:
                amount_value = int(amount)
            except ValueError:
                sys.stderr.write("Invalid format. Fail to delete a record.\n")
                return
            for r in self._records:
                if r.category == category and r.description == description and r.amount == amount_value:
                    self._records.remove(r)
                    self._initial_money -= amount_value
                    return
            sys.stderr.write(f"There's no record with {record_str}. Fail to delete a record.\n")
        except ValueError:
            sys.stderr.write("Invalid format. Fail to delete a record.\n")

    def find(self, target_categories):
        """Print records whose category is in the given list, and the total."""
        if not target_categories:
            print("No such category.")
            return
        filtered = [r for r in self._records if r.category in target_categories]
        print(f"Here's your expense and income records under category \"{target_categories[0]}\":")
        print(f"{'Category':<15}{'Description':<20}{'Amount':<7}")
        print("="*40)
        total = 0
        for r in filtered:
            print(f"{r.category:<15}{r.description:<20}{r.amount:<7}")
            total += r.amount
        print("="*40)
        print(f"The total amount above is {total}.")

    def save(self):
        """Write the current money and all records to 'record.txt'."""
        with open('record.txt', 'w') as f:
            f.write(f"{self._initial_money}\n")
            for r in self._records:
                f.write(f"{r.category}, {r.description}, {r.amount}\n")

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = [
            'expense',
            ['food', ['meal', 'snack', 'drink']],
            ['transportation', ['bus', 'railway']],
            'income',
            ['salary'],
            ['bonus']
        ]

    def view(self, categories=None, indent=0):
        """Recursively print categories with indentation."""
        if categories is None:
            categories = self._categories
        for cat in categories:
            if isinstance(cat, str):
                print('  ' * indent + f'- {cat}')
            elif isinstance(cat, list):
                self.view(cat, indent + 1)

    def is_category_valid(self, category, categories=None):
        """Recursively check if category is in categories."""
        if categories is None:
            categories = self._categories
        for cat in categories:
            if isinstance(cat, str):
                if cat == category:
                    return True
            elif isinstance(cat, list):
                if self.is_category_valid(category, cat):
                    return True
        return False

    def find_subcategories(self, target, categories=None):
        """Return a flat list of target and all its subcategories."""
        if categories is None:
            categories = self._categories
        result = []
        found = False
        for i, cat in enumerate(categories):
            if isinstance(cat, str):
                if cat == target:
                    found = True
                    result.append(cat)
            elif isinstance(cat, list):
                if found:
                    result += self._flatten(cat)
                    found = False
                else:
                    result += self.find_subcategories(target, cat)
        return result

    def _flatten(self, categories):
        """Flatten a nested category list into a flat list of strings."""
        result = []
        for cat in categories:
            if isinstance(cat, str):
                result.append(cat)
            elif isinstance(cat, list):
                result += self._flatten(cat)
        return result

# Main program
categories = Categories()
records = Records()

while True:
    command = input("What do you want to do (add / view / delete / view categories / find / exit)? ")
    if command == 'add':
        items = input("Add some expense or income records with category, description, and amount (separate by spaces):\ncat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...\n")
        records.add(items, categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        delete_record = input("Which record do you want to delete? (category description amount)\n")
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input("Which category do you want to find? ")
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write("Invalid command. Try again.\n")
