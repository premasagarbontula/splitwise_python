class Expense:
    def __init__(self, amount, description, payer, participants, weights=None):
        self.amount = amount
        self.description = description
        self.payer = payer  # The person who paid the expense
        self.participants = participants
        # If no weights are provided, assume equal share for all participants
        self.weights = weights if weights else {person: 1 / len(participants) for person in participants}
        self.shares = self.calculateShares()

    def calculateShares(self):
        total_weight = sum(self.weights.values())
        # Calculate each participant's share based on their weight
        shares = {person: (self.amount * self.weights[person]) / total_weight for person in self.participants}
        return shares

class Person:
    def __init__(self, name):
        self.name = name
        self.balance = 0  # Balance shows how much a person owes (+ve) or is owed (-ve)
        self.amount_spent = 0  # Tracks how much the person has paid

    def addSpent(self, amount):
        self.amount_spent += amount
        # print(self.amount_spent)

    def updateBalance(self, value):
        self.balance = self.balance + value

class Trip:
    def __init__(self):
        self.people = {}  # Holds people as key-value pairs, where key = name, value = Person object
        self.expenses = []

    def addPerson(self, name):
        if name not in self.people:
            self.people[name] = Person(name)

    def addExpense(self, amount, description, payer, participants, weights=None):
        # Ensure all participants (including the payer) are added to the trip (if not already added)
        for participant in participants:
            self.addPerson(participant)
        self.addPerson(payer)  # Make sure the payer is also added

        # Create an Expense object and calculate shares
        expense = Expense(amount, description, payer, participants, weights)
        self.expenses.append(expense)
        
        shares = expense.shares
        if payer not in participants:
            # self.people[participant].addSpent(amount)
            self.people[payer].updateBalance(amount)
        # Update each person's spent and balance
        for participant in participants:
            share = shares[participant]
            if participant == payer:
                # The payer pays the full amount and their balance increases by the full amount
                # self.people[participant].addSpent(amount)
                self.people[participant].updateBalance(amount-share)
            else:
                # Non-payers only pay their respective share
                # self.people[participant].addSpent(share)
                self.people[participant].updateBalance(-share)

    def calculateBalances(self):
        # Calculate the total amount spent and the average amount spent by each person
        total_spent = sum(person.amount_spent for person in self.people.values())
        avg_spent = total_spent / len(self.people)

        # Adjust each person's balance based on the average spent
        for person in self.people.values():
            person.updateBalance(avg_spent - person.amount_spent)

    def getTransactionSummary(self):
        # self.calculateBalances()
        
        owes = []
        gets = []
        
        # Classify people into those who owe money and those who are owed money
        for person in self.people.values():
            
            if person.balance < 0:
                owes.append((person.name, -person.balance))  # If balance is negative, they owe money
            elif person.balance > 0:
                gets.append((person.name, person.balance))  # If balance is positive, they are owed money

        # # Sort people by the amount they owe or are owed (descending order)
        # owes.sort(key=lambda x: x[1], reverse=True)
        # gets.sort(key=lambda x: x[1], reverse=True)

        # Prepare the transaction summary for display
        summary = []
        for person, amount in owes:
            summary.append(f"{person} owes {amount:.2f}")
        for person, amount in gets:
            summary.append(f"{person} gets {amount:.2f}")
        
        return "\n".join(summary)

    def get_individual_transactions(self):
        """Generate the detailed transactions between individuals."""
        transactions = []
        balances = {person.name: person.balance for person in self.people.values()}
        print(balances)
        # Separate people who owe money from those who are owed money
        owes = {name: -balance for name, balance in balances.items() if balance < 0}  # Who owes
        gets = {name: balance for name, balance in balances.items() if balance > 0}  # Who gets
        print(owes)
        print(gets)
        # Now match who owes with who gets, and calculate exact transactions
        for owe_person, owe_amount in owes.items():
            for get_person, get_amount in list(gets.items()):
                

                # Calculate the transfer amount between the debtor and the creditor
                transfer_amount = min(owe_amount, get_amount)
                transactions.append(f"{owe_person} needs to pay {get_person} an amount of {transfer_amount:.2f}")

                owes[owe_person] -= transfer_amount
                gets[get_person] -= transfer_amount
                if owes[owe_person] == 0:
                    break  # No further payments needed from this person
                # If the person no longer owes anything or needs any more money, remove them from the dictionary
                # if owes[owe_person] == 0:
                #     del owes[owe_person]
                # if gets[get_person] == 0:
                #     del gets[get_person]

        return "\n".join(transactions)


# Test the solution with the provided sample input
trip = Trip()

# Add the expenses as described
# trip.addExpense(100, "Snacks", "A", ["A", "B", "C", "D"], weights={"A": 0.25, "B": 0.25, "C": 0.25, "D": 0.25})  # A paid 100 for A, B, C, D
# trip.addExpense(500, "Taxi", "B", ["C", "D"], weights={"C": 0.5, "D": 0.5})  # B paid 500 for C, D
# trip.addExpense(300, "Bus", "D", ["A", "B"], weights={"A": 0.5, "B": 0.5})  # D paid 300 for A, B
trip.addExpense(300, "Snacks", "A", ["A", "B", "C"])
trip.addExpense(600, "Snacks", "B", ["C", "D", "E"])
trip.addExpense(200, "Snacks", "C", ["A", "F"])
trip.addExpense(500, "Snacks", "D", ["B", "E"])
trip.addExpense(600, "Snacks", "E", ["C", "F"])
trip.addExpense(900, "Snacks", "F", ["A", "B", "C"])

# Print the transaction summary (who owes and who gets how much)
print("Transaction Summary:")
print(trip.getTransactionSummary())

# Print detailed person-to-person transactions
print("\nDetailed person-to-person transactions:")
print(trip.get_individual_transactions())