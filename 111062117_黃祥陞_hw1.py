money = int(input("How much money do you have? "))
description, amount = input("Add an expense or income record with description and amount:\n").split()
money += int(amount)
print(f"Now you have {money} dollars.")