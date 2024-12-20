class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total_balance = sum(item["amount"] for item in self.ledger)
        return total_balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = self.name.center(30, "*")
        items = ""
        for item in self.ledger:
            amount = f"{item['amount']:.2f}"
            items += f"{item['description'][:23].ljust(23)}{amount.rjust(7)}\n"
        total = f"Total: {self.get_balance():.2f}"
        return f"{title}\n{items}{total}"

def create_spend_chart(categories):
    spend_data = {category.name: 0 for category in categories}
    
    for category in categories:
        total_withdrawn = sum(-item["amount"] for item in category.ledger if item["amount"] < 0)
        spend_data[category.name] = total_withdrawn
        
    total_spent = sum(spend_data.values())
    spend_percentages = {name: (amount / total_spent * 100) // 10 * 10 for name, amount in spend_data.items()}
    
    chart = "Percentage spent by category\n"
    for percentage in range(100, -1, -10):
        line = f"{percentage:3}|"
        for name in spend_data:
            line += " o " if spend_percentages[name] >= percentage else "   "
        chart += line + " \n"

    chart += "    " + "-" * (3 * len(categories) + 1) + "\n"

    max_length = max(len(name) for name in spend_data)
    for i in range(max_length):
        name_str = "     "
        for name in spend_data:
            name_str += name[i] + "  " if i < len(name) else "   "
        chart += name_str + "\n"

    return chart.rstrip("\n")  # Remove trailing newline for exact match