import math
import configparser
import os

class RealEstateCalculator:

    incomes        = {}
    expenses       = {}
    initial_costs  = {}

    config = None

    def __init__(self):
        os.chdir(os.path.dirname(__file__))
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    # Getter for incomes
    def getIncomes(self):
        return self.incomes

    # Getter for expenses
    def getExpenses(self):
        return self.expenses

    # Getter for initial_costs
    def getInitialCosts(self):
        return self.initial_costs

    # Setter for incomes
    def setIncomes(self, incomes):
        self.incomes = incomes

    # Setter for expenses
    def setExpenses(self, expenses):
        self.expenses = expenses

    # Setter for initial_costs
    def setInitialCosts(self, initial_costs):
        self.initial_costs = initial_costs

    # Add income
    def addIncome(self, name, amount):
        if name not in self.incomes:
            self.incomes[name] = amount

    # Add expense
    def addExpense(self, name, amount):
        if name not in self.expenses:
            self.expenses[name] = amount

    # Add inital cost
    def addInitialCost(self, name, amount):
        if name not in self.initial_costs:
            self.initial_costs[name] = amount

    # Change income
    def changeIncome(self, name, amount):
        if name in self.incomes:
            self.incomes[name] = amount

    # Change expense
    def changeExpense(self, name, amount):
        if name in self.expenses:
            self.expenses[name] = amount

    # Change inial cost
    def changeInitialCost(self, name, amount):
        if name in self.initial_costs:
            self.initial_costs[name] = amount

    # Remove income
    def deleteIncome(self, name):
        if name in self.incomes:
            del self.incomes[name]

    # Remove expense
    def deleteExpense(self, name):
        if name in self.expenses:
            del self.expenses[name]

    # Remove initial cost
    def deleteInitialCosts(self, name):
        if name in self.initial_costs:
            del self.initial_costs[name]

    # Get Gross Income
    def getMonthlyIncome(self):
        return sum(self.incomes.values())

    # Get Total Expenses
    def getMonthlyExpenses(self):
        return sum(self.expenses.values())

    # Get Monthly Cashflow
    def getMonthlyCashFlow(self):
        return self.getMonthlyIncome() - self.getMonthlyExpenses()

    def getAnnualCashFlow(self):
        return self.getMonthlyCashFlow() * 12
    
    # Get Total Investment
    def getTotalInvestment(self):
        return sum(self.initial_costs.values())

    # Calculate ROI
    def getROI(self):
        return self.getAnnualCashFlow() / self.getTotalInvestment()
    
    # Add Purchase Price
    # Method that takes a House Price and adds the mortgage and adds all associated expenses
    def addHousePrice(self, price):
        self.expenses['tax']                = price * float(self.config.get('calculations', 'tax')) / 12
        self.initial_costs['rehab budget']  = price * float(self.config.get('calculations', 'rehab'))
        self.initial_costs['closing costs'] = price * float(self.config.get('calculations', 'closing costs'))


    # Print Report 
    def printReport(self):
        self.__printTop()
        self.__printMiddle()
        self.__printBottom()

    def __printTop(self):
        self.__printLineRow()
        self.__printHeadingRow("Gross Income", "Cash Flow")

        left_side = [(name, amount) for name, amount in self.incomes.items()]
        right_side = [("Income", self.getMonthlyIncome()), ("Expenses", self.getMonthlyExpenses())]
        row = 0

        while(row < len(left_side) or row < len(right_side)):
            if row < len(left_side):
                self.__printItemsRow(left_side[row][0], left_side[row][1], True)
            else:
                self.__printItemsRow("", "", True)

            if row < len(right_side):
                self.__printItemsRow(right_side[row][0], right_side[row][1], False)
            else:
                self.__printItemsRow("", "", False)

            row += 1
    
    def __printMiddle(self):
        print("|" + "-"*47 + "|" + "-"*47 + "|")
        self.__printItemsRow("Total Monthly Income", self.getMonthlyIncome(), True)
        self.__printItemsRow("Total Monthly Cashflow", self.getMonthlyCashFlow(), False)
        self.__printLineRow()
        self.__printHeadingRow("Expenses", "Cash on Cash ROI")

    def __printBottom(self):
        left_side = [(name, amount) for name, amount in self.expenses.items()]
        right_side = [(name, amount) for name, amount in self.initial_costs.items()] + [("", ""), ("Total Investment", self.getTotalInvestment()), ("Annual Cashflow", self.getAnnualCashFlow())]
        row = 0

        while(row < len(left_side) or row < len(right_side)):
            if row < len(left_side):
                self.__printItemsRow(left_side[row][0], left_side[row][1], True)
            else:
                self.__printItemsRow("", "", True)

            if row < len(right_side):
                self.__printItemsRow(right_side[row][0], right_side[row][1], False)
            else:
                self.__printItemsRow("", "", False)

            row += 1
        
        print("|" + "-"*47 + "|" + "-"*47 + "|")
        self.__printItemsRow("Total Monthly Expenses", self.getMonthlyExpenses(), True)
        name = "Cash on Cash ROI"
        print(f'{name:<30} = {self.getROI():>14.2%}|')
        self.__printLineRow()

    def __printLineRow(self):
        print("+" + "-"*47 + "+" + "-"*47 + "+")

    def __printHeadingRow(self, left_heading, right_heading):
        print(f'|{left_heading:^47}|{right_heading:^47}|')

    def __printItemsRow(self, name, amount, left):
        if name == amount == "":
            if left: 
                print('|', end='')
            print(" "*47 + "|", end = '' if left else '\n')
        else:
            formatted_name = name[:25] + "..." if len(name) > 30 else name
            formatted_amount = '' if amount == '' else f'${amount:,.2f}'
            if left: 
                print('|', end='')
            print(f'{formatted_name.capitalize():<30} = {formatted_amount:>14}|', end = '' if left else '\n')


if __name__ == '__main__':
    test = RealEstateCalculator()
    incomes = {'rental income' : 2000, 'laundry' : 0, 'storage' : 0, 'misc' : 0}
    expenses = {'utilities': 0, 'HOA':0, 'lawn': 0, 'repairs' : 100,
                'capital Expenses': 100, 'morgage' : 860, 'insurance' : 100,
                'property managment' : 200, 'vacancy': 100}
    initials = {'down payment': 40000, "misc others": 0}
    test.setExpenses(expenses)
    test.setIncomes(incomes)
    test.setInitialCosts(initials)
    test.addHousePrice(200000)
    test.printReport()