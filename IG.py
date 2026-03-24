import random
import json
import traceback

# Class Structure
class Asset:
    def __init__(self, name, base_value, volatility, cashflow):
        self.name = name
        self.base_value = base_value # base value of the asset
        self.value = base_value # current value of the asset
        self.volatility = volatility #volatility of the asset
        self.cashflow = cashflow # cashflow of the asset
        self.n_owned = 0 # number of assets owned

    @classmethod
    def market(cls, economic_growth): # get the market growth for the asset class
        chance = random.randint(-cls.market_volatility, cls.market_volatility)
        market_growth = round(chance + economic_growth, 2)
        return market_growth
    
    @staticmethod
    def investment_portfolio(): # portfolio of all assets owned
        print()
        print("List of stocks owned:")
        for stock in Stocks.stock_portfolio.values():
            print(stock)
        print()
        print("List of bonds owned:")
        for bond in Bonds.bond_portfolio.values():
            print(bond)
        print()
        print("List of crypto owned:")
        for crypto in Crypto.crypto_portfolio.values():
            print(crypto)
        print()
        print("List of real estate owned:")
        for real_estate in RealEstate.real_estate_portfolio.values():
            print(real_estate)
        print()
        print("List of busninesses owned:")
        for business in Business.business_portfolio.values():
            print(business)
     
    @staticmethod
    def investment_value(): # get the total value of all assets owned
        total_value = 0
        for stock_obj in Stocks.stock_portfolio.values():
            total_value += round(stock_obj.value * stock_obj.n_owned, 2)
        for bond_obj in Bonds.bond_portfolio.values():
            total_value += round(bond_obj.value * bond_obj.n_owned, 2)
        for crypto_obj in Crypto.crypto_portfolio.values():
            total_value += round(crypto_obj.value * crypto_obj.n_owned, 2)
        for real_estate_obj in RealEstate.real_estate_portfolio.values():
            total_value += round(real_estate_obj.equity, 2)
        for business_obj in Business.business_portfolio.values():
            total_value += round(business_obj.value, 2)
        return total_value


    def inflation(self, monthly_inflation, investment_income): # Raise the base value and the cashflow of each asset each month (excluding bonds)
        self.base_value += round(self.base_value * (monthly_inflation / 100), 2)
        if self.name in Stocks.stock_portfolio or \
        self.name in Bonds.bond_portfolio or \
        self.name in Crypto.crypto_portfolio or \
        self.name in RealEstate.real_estate_portfolio or \
        self.name in Business.business_portfolio:
            investment_income -= self.cashflow
            self.cashflow += round(self.cashflow * (monthly_inflation / 100), 2)
            investment_income += self.cashflow
        else:
            self.cashflow += round(self.cashflow * (monthly_inflation / 100), 2)
        return investment_income
    
    def asset_growth(self, market_growth): # get the asset growth for the specific asset
        chance = random.randint(-self.volatility, self.volatility)
        pre_governer = self.value - self.base_value
        governer = abs(pre_governer) / self.base_value
        asset_growth = chance + market_growth

        if self.name.lower() in Bonds.available_bonds:
            bond_governer = 120 - self.months_left
            if governer != 0:
                if pre_governer > 0:
                    if asset_growth > 0:
                        self.value += round(self.value * ((asset_growth / bond_governer) / 100), 2)
                    else:
                        self.value += round(self.value * (asset_growth / 100), 2)
                if pre_governer < 0:
                    if asset_growth < 0:
                        self.value += round(self.value * ((asset_growth / bond_governer) / 100), 2)
                    else:
                        self.value += round(self.value * (asset_growth / 100), 2)
            else:
                self.value += round(self.value * (asset_growth / 100), 2)

        elif governer != 0:
            if pre_governer > 0:
                if asset_growth > 0:
                    self.value += round(self.value * ((asset_growth - (asset_growth * governer)) / 100), 2)
                else:
                    self.value += round(self.value * (asset_growth / 100), 2)
            if pre_governer < 0:
                if asset_growth < 0:
                    self.value += round(self.value * ((asset_growth - (asset_growth * governer)) / 100), 2)
                else:
                    self.value += round(self.value * (asset_growth / 100), 2)
        else:
            self.value += round(self.value * (asset_growth / 100), 2)

    
class Stocks(Asset):
    market_volatility = 25
    available_stocks = {} # list of all stocks available
    stock_portfolio = {} # list of stocks owned

    def __init__(self, name, base_value, volatility, cashflow):
        super().__init__(name, base_value, volatility, cashflow)
        Stocks.available_stocks[name.lower()] = self # add the stock to the list of available stocks

    def __repr__(self): # string representation of the stock
        return f"Name: {self.name}, Value: ${self.value:,.2f}, Dividend: ${self.cashflow:,.2f}/month, Shares Owned: {self.n_owned}"

    def bankrupt(self):
        if self.value < 1:
            print()
            print(f"{self.name} is bankrupt.")
            print("Asset removed from portfolio.")
            print(f"New company has gone public with ticker {self.name}.")
            self.n_owned = 0
            del Stocks.stock_portfolio[self]
            self.reset()
        else:
            return
        
    def reset(self): # reset the value of the asset to the base value
        self.value = round(self.base_value, 2)

    #Save method
    def pack_details(self):
        return {
            "name": self.name,
            "base_value": self.base_value,
            "value": self.value,
            "cashflow": self.cashflow,
            "volatility": self.volatility,
            "n_owned": self.n_owned
        }


    # Load Method
    @classmethod
    def unpack_details(cls, data):
        obj = cls(
            name = data["name"],
            base_value = data["base_value"],
            cashflow = data["cashflow"],
            volatility = data["volatility"],
        )
        obj.value = data["value"]
        obj.n_owned = data["n_owned"]
        return obj

class Bonds(Asset):
    market_volatility = 5
    available_bonds = {} # list of all bonds available
    bond_portfolio = {} # list of bonds owned

    def __init__(self, name, base_value, volatility, cashflow, months_left, total_months):
        super().__init__(name, base_value , volatility, cashflow)
        self.total_months = total_months # total months until maturity
        self.months_left = months_left # current months left until maturity
        self.interest_built = round((self.total_months - self.months_left) * self.cashflow, 2)
        self.og_value = base_value
        Bonds.available_bonds[name.lower()] = self # add the stock to the list of available bonds

    def __repr__(self): # string representation of the bond
        return (f"Name: {self.name}, Value: ${self.value:,.2f}, Principle: ${self.base_value:,.2f}, Interest: ${self.cashflow:,.2f}/month, Months Left: {self.months_left}, Total Months: {self.total_months}, Notes Owned: {self.n_owned}")
    
    @classmethod
    def starting_values(cls): # get the correct value for the bond 
        for bond in cls.available_bonds.values():
            bond.base_value += round((bond.total_months - bond.months_left) * bond.cashflow, 2)
            bond.value = round(bond.base_value, 2)
    
    def monthly_bond_growth(self):
        self.base_value += round(self.cashflow, 2)
        self.interest_built += round(self.cashflow, 2)
        self.months_left -= 1
        return self.base_value, self.interest_built

    def maturity(self, savings):
        if self.months_left == 0:
            if self.name.lower() in Bonds.bond_portfolio:
                print()
                print(f"Bond matured.  Amount received: ${self.base_value * self.n_owned:,.2f}")
                savings += round(self.base_value * self.n_owned, 2)
                self.n_owned = 0
                del Bonds.bond_portfolio[self.name.lower()]
                self.reset()
                return savings
            else:
                self.reset()
                return savings
        else:
            return savings
    
    def bankrupt(self):
        if self.value < .25 * self.base_value:
            print()
            print(f"{self.name} is bankrupt.")
            print("Asset removed from portfolio.")
            self.n_owned = 0
            del Bonds.bond_portfolio[self.name]
            self.reset()
        else:
            return
    
    def reset(self): # reset the value of the asset to the base value
        self.base_value = self.og_value
        self.value = self.base_value
        self.months_left = round(self.total_months, 2)
        print(f"New company has issued a bond under {self.name}.")

    # Save Method
    def pack_details(self):
        return {
            "name": self.name,
            "base_value": self.base_value,
            "value": self.value,
            "cashflow": self.cashflow,
            "volatility": self.volatility,
            "n_owned": self.n_owned,
            "total_months": self.total_months,
            "months_left": self.months_left,
            "interest_built": self.interest_built
        }
    
    # Load Method
    @classmethod
    def unpack_details(cls, data):
        obj = cls(
            name = data["name"],
            base_value = data["base_value"],
            cashflow = data["cashflow"],
            volatility = data["volatility"],
            total_months = data["total_months"],
            months_left = data["months_left"]
        )
        obj.value = data["value"]
        obj.n_owned = data["n_owned"]
        obj.interest_built = data["interest_built"]
        return obj
        
class Crypto(Asset):
    market_volatility = 50
    available_crypto = {} # list of all crypto available
    crypto_portfolio = {} # list of crypto owned

    def __init__(self, name, base_value, volatility, cashflow):
        super().__init__(name, base_value, volatility, cashflow)
        Crypto.available_crypto[name.lower()] = self # add the stock to the list of available crypto

    def __repr__(self): # string representation of the stock
        return f"Name: {self.name}, Value: ${self.value:,.2f}, Cashflow: ${self.cashflow:,.2f}/month, Coins Owned: {self.n_owned}"

    def bankrupt(self):
        if self.value < 1:
            print()
            print(f"{self.name} has been disconinued.")
            if self in Crypto.crypto_portfolio:
                print("Asset removed from portfolio.")
                self.n_owned = 0
                del Crypto.crypto_portfolio[self.name]
            self.reset()
        else:
            return
    
    def reset(self): # reset the value of the asset to the base value
        self.value = round(self.base_value, 2)
        print(f"A new currency has been started under the name {self.name}.")

    #Save method
    def pack_details(self):
        return {
            "name": self.name,
            "base_value": self.base_value,
            "value": self.value,
            "cashflow": self.cashflow,
            "volatility": self.volatility,
            "n_owned": self.n_owned
        }
    
    # Load Method
    @classmethod
    def unpack_details(cls, data):
        obj = cls(
            name = data["name"],
            base_value = data["base_value"],
            cashflow = data["cashflow"],
            volatility = data["volatility"]
        )
        obj.value = data["value"]
        obj.n_owned = data["n_owned"]
        return obj

class RealEstate(Asset):
    market_volatility = 5
    available_realestate = {} # list of all real estate available
    real_estate_portfolio = {} # list of real estate owned


    def __init__(self, name, base_value, volatility, cashflow):
        super().__init__(name, base_value, volatility, cashflow)
        self.down_payment = self.value * .1 # down payment for the real estate -- will probably have to be set in the purchase function
        self.mortgage = self.value - self.down_payment # mortgage for the real estate -- will probably have to be set in the purchase function
        self.mortgage_payment = self.mortgage / 360
        self.mortgage_months_left = 360
        self.equity = self.value - self.mortgage
        RealEstate.available_realestate[name.lower()] = self # add the stock to the list of available real estate

    def __repr__(self): # string representation of the stock
        if self.name.lower() in RealEstate.real_estate_portfolio:
            return (f"Name: {self.name}, Value: ${self.value:,.2f}, Rental Income: ${self.cashflow:,.2f}/month, Property owned?: Yes, Mortgage Payment: ${self.mortgage_payment:,.2f}, \n" 
                    f"Mortgage Balance: ${self.mortgage:,.2f}, Months Left on Mortgage: {self.mortgage_months_left}, Equity: {self.equity:,.2f}")
        else:
            return (f"Name: {self.name}, Value: ${self.value:,.2f}, Rental Income: ${self.cashflow:,.2f}/month, Property owned?: No, Down Payment Required: ${self.down_payment:,.2f}")

    def mortgage_paydown(self, investment_income): # to be run every month
        if self.name.lower() in RealEstate.real_estate_portfolio:
            if self.mortgage_months_left > 0:
                self.mortgage_months_left -= 1
            self.mortgage -= self.mortgage_payment
            self.equity = self.value - self.mortgage
            if self.mortgage <= 0:
                print()
                print (f"Mortgage on {self.name} is paid off! ${self.mortgage_payment:,.2f} is added to rental income.")
                investment_income -= round(self.cashflow, 2)
                self.cashflow += round(self.mortgage_payment, 2) # add the mortgage payment to the cashflow
                investment_income += round(self.cashflow, 2)
            return self.mortgage, self.cashflow, investment_income, self.equity
        return self.mortgage, self.cashflow, investment_income, self.equity

    def bankrupt(self):
        if self.value < self.mortgage * 0.5:
            print()
            print(f"The loan to value on {self.name} is too high. {self.name} been forclosed.")
            print("Asset removed from portfolio.")
            del RealEstate.real_estate_portfolio[self.name]
            self.reset()
        else:
            return
    
    def reset(self): # reset the value of the asset to the base value
        self.value = round(self.base_value, 2)
        print(f"A new property has been offered for sale: {self.name}.")

    #Save method
    def pack_details(self):
        return {
            "name": self.name,
            "base_value": self.base_value,
            "value": self.value,
            "cashflow": self.cashflow,
            "volatility": self.volatility,
            "n_owned": self.n_owned,
            "down_payment": self.down_payment,
            "mortgage": self.mortgage,
            "mortgage_payment": self.mortgage_payment,
            "mortgage_months_left": self.mortgage_months_left
        }
    
        # Load Game Method
    @classmethod
    def unpack_details(cls, data):
        obj = cls(
            name = data["name"],
            base_value = data["base_value"],
            cashflow = data["cashflow"],
            volatility = data["volatility"]
        )
        obj.value = data["value"]
        obj.n_owned = data["n_owned"]
        obj.down_payment = data["down_payment"]
        obj.mortgage = data["mortgage"]
        obj.mortgage_payment = data["mortgage_payment"]
        obj.mortgage_months_left = data["mortgage_months_left"]
        return obj

class Business(Asset):
    market_volatility = 2
    available_businesses = {} # list of all businesses available
    business_portfolio = {} # list of businesses owned

    def __init__(self, name, base_value, volatility, cashflow):
        super().__init__(name, base_value, volatility, cashflow)
        Business.available_businesses[name.lower()] = self # add the stock to the list of available businesses

    def __repr__(self): # string representation of the stock
        if self.name in Business.available_businesses:
            return f"Name: {self.name}, Value: ${self.value:,.2f}, Profit: ${self.cashflow:,.2f}/month, Business owned?: Yes"
        else:
            return f"Name: {self.name}, Value: ${self.value:,.2f}, Profit: ${self.cashflow:,.2f}/month, Business owned?: No"
    
    def cashflow_change(self, investment_income):
        if self.name in Business.business_portfolio:
            investment_income -= round(self.cashflow, 2)
            self.cashflow = round(self.value * .2 / 12, 2)
            investment_income += round(self.cashflow, 2)
            return investment_income
        else:
            self.cashflow = round(self.value * .2 / 12, 2)
            return investment_income
    
    def bankrupt(self):
        liquidate = self.base_value * .01
        if self.value < liquidate:
            print()
            print(f"{self.name} is bankrupt.")
            print("Asset removed from portfolio.")
            del Business.business_portfolio[self.name]
            self.reset()
        else:
            return
    
    def reset(self): # reset the value of the asset to the base value
        self.value = round(self.base_value, 2)
        print(f"A new business has opened under the name: {self.name}.")

    #Save method
    def pack_details(self):
        return {
            "name": self.name,
            "base_value": self.base_value,
            "value": self.value,
            "cashflow": self.cashflow,
            "volatility": self.volatility,
            "n_owned": self.n_owned
        }
    
    # Load Game Method
    @classmethod
    def unpack_details(cls, data):
        obj = cls(
            name = data["name"],
            base_value = data["base_value"],
            cashflow = data["cashflow"],
            volatility = data["volatility"]
        )
        obj.value = data["value"]
        obj.n_owned = data["n_owned"]
        return obj


# Game Variables
# income statement variables
job_income = 2000
investment_income = 0
investment_value = 0
income = round(job_income + investment_income, 2)
expenses = 1500
margin = round(income - expenses, 2)

# balance sheet variables
savings = round(margin * 3, 2) # savings starts at 3 months of margin
monthly_inflation = round(5 / 12, 2) # inflation is 5% per year, so 5/12% per month
investment_value = 0 # investment value starts at 0

month_counter = 1


# Game Functions
# income statement function
def income_statement(income, expenses):
    margin = round(income - expenses, 2)
    print()
    print("Income Statement:")
    print(f"Salary: ${job_income: ,.2f}, Investment Income ${investment_income: ,.2f}, Total Income ${income: ,.2f} , Expenses: ${expenses: ,.2f}, Margin: ${margin: ,.2f}")
    return margin

# balance shteet function
def balance_sheet(savings, investment_value):
    total_assets = round(savings + investment_value, 2)
    print()
    print("Balance Sheet:")
    print(f"Cash: ${savings: ,.2f}, Investments: ${investment_value: ,.2f}, Total Assets: ${total_assets: ,.2f}")
    return total_assets

# monthly actions:
# improve job income
def improve_job_income(job_income):
    chance = random.randint(1, 100)
    if chance <= 75:
        job_income += 0
        print("Employers don't recognize your increased productivity.  Your salary has not impoved.")
    else:
        increase = round(chance, 2)
        job_income += round(increase, 2)
        print(f"Success! Your hard work has been rewarded with a raise of ${increase: ,.2f}/month!")
        print(f"Salary improved to ${job_income: ,.2f}")
    return job_income

# research stocks
def research_stocks():
    print()
    for stock in Stocks.available_stocks.values():
        print(stock)

# purchase stocks
def purchase_stocks(stock_name, n_shares, savings, investment_income, investment_value):
    stock = Stocks.available_stocks[stock_name]
    price = round(stock.value, 2)
    cost = price * n_shares
    cashflow = round(stock.cashflow * n_shares, 2)
    if cost > savings:
        print("Not enough cash.")
        return savings, investment_income, investment_value
    else:
        savings -= round(cost, 2)
        if stock.name in Stocks.stock_portfolio: # if the stock is already in the portfolio, add the number of shares owned
            stock.n_owned += n_shares # add the number of shares owned
        else:
            stock.n_owned += n_shares # add the number of shares owned
            Stocks.stock_portfolio[stock.name.lower()] = stock  # add the stock to the portfolio if not already there
        investment_income += round(cashflow, 2) # add the cashflow to the investment income
        investment_value = Asset.investment_value()
        print(f"Purchased {n_shares} shares of {stock.name} for ${cost: ,.2f}.")
        return savings, investment_income, investment_value
    
# sell stocks
def sell_stocks(stock_name, n_shares, savings, investment_income, investment_value):
    stock = Stocks.available_stocks[stock_name]
    price = round(stock.value, 2)
    cost = round(price * n_shares, 2)
    cashflow = round(stock.cashflow * n_shares, 2)
    if n_shares > stock.n_owned:
        print("Not enough shares owned.")
        return savings, investment_income, investment_value
    else:
        savings += round(cost, 2)
        stock.n_owned -= n_shares
        if stock.n_owned == 0: # if the number of shares owned is 0, remove the stock from the portfolio
            del Stocks.stock_portfolio[stock.name.lower()]
        investment_income -= round(cashflow, 2) # remove the cashflow from the investment income
        investment_value = Asset.investment_value()
        print(f"Sold {n_shares} shares of {stock.name} for ${cost: ,.2f}.")
        return savings, investment_income, investment_value

# research bonds
def research_bonds():
    print()
    for bond in Bonds.available_bonds.values():
        print(bond)

# purchase bonds
def purchase_bonds(bond_name, n_notes, savings, investment_income, investment_value):
    bond = Bonds.available_bonds[bond_name]
    cost = bond.value * n_notes
    cashflow = bond.cashflow * n_notes
    if cost > savings:
        print("Not enough cash.")
        return savings, investment_income, investment_value
    else:
        savings -= cost
        if bond.name in Bonds.bond_portfolio: # if the bond is already in the portfolio, add the number of bonds owned
            bond.n_owned += n_notes # add the number of notes owned
        else:
            bond.n_owned += n_notes # add the number of notes owned
            Bonds.bond_portfolio[bond.name.lower()] = bond # add the bond to the portfolio if not already there
        investment_value = Asset.investment_value()
        print(f"Purchased {n_notes} bonds of {bond.name} for ${cost: ,.2f}.")
        return savings, investment_income, investment_value
    
# sell bonds
def sell_bonds(bond_name, n_notes, savings, investment_income, investment_value):
    bond = Bonds.available_bonds[bond_name]
    cost = bond.value * n_notes
    cashflow = bond.cashflow * n_notes
    if n_notes > bond.n_owned:
        print("Not enough notes owned.")
        return savings, investment_income, investment_value
    else:
        savings += cost
        bond.n_owned -= n_notes
        if bond.n_owned == 0: # if the number of notes owned is 0, remove the bond from the portfolio
            del Bonds.bond_portfolio[bond.name.lower()]
        investment_value = Asset.investment_value()
        print(f"Sold {n_notes} bonds of {bond.name} for ${cost: ,.2f}.")
        return savings, investment_income, investment_value
    
# research crypto
def research_crypto():
    print()
    for crypto in Crypto.available_crypto.values():
        print(crypto)

# purchase crypto
def purchase_crypto(crypto_name, n_cryptos, savings,investment_value):
    crypto = Crypto.available_crypto[crypto_name]
    cost = crypto.value * n_cryptos
    if cost > savings:
        print("Not enough cash.")
        return savings, investment_value
    else:
        savings -= cost
        if crypto.name in Crypto.crypto_portfolio: # if the crypto is already in the portfolio, add the number of cryptos owned
            crypto.n_owned += n_cryptos # add the number of shares owned
        else:
            crypto.n_owned += n_cryptos # add the number of shares owned
            Crypto.crypto_portfolio[crypto.name.lower()] = crypto  # add the crypto to the portfolio if not already there
        investment_value = Asset.investment_value()
        print(f"Purchased {n_cryptos} coins of {crypto.name} for ${cost: ,.2f}.")
        return savings, investment_value
    
# sell crypto
def sell_crypto(crypto_name, n_cryptos, savings, investment_value):
    crypto = Crypto.available_crypto[crypto_name]
    cost = crypto.value * n_cryptos
    if n_cryptos > crypto.n_owned:
        print("Not enough coins owned.")
        return savings, investment_income, investment_value
    else:
        savings += cost
        crypto.n_owned -= n_cryptos
        if crypto.n_owned == 0: # if the number of shares owned is 0, remove the crypto from the portfolio
            del Crypto.crypto_portfolio[crypto.name.lower()]
        investment_value = Asset.investment_value()
        print(f"Sold {n_cryptos} coins of {crypto.name} for ${cost: ,.2f}.")
        return savings, investment_value
    
# research real estate
def research_real_estate():
    print()
    for realestate in RealEstate.available_realestate.values():
        print(realestate)

# purchase real estate
def purchase_real_estate(realestate_name, savings, investment_income, investment_value):
    realestate = RealEstate.available_realestate[realestate_name]
    cost = round(realestate.down_payment, 2)
    if cost > savings:
        print("Not enough cash.")
        return savings, investment_income, investment_value
    else:
        if realestate.name in RealEstate.real_estate_portfolio:
            print("Transaction cancelled.  Property already in portfolio.")
            return savings, investment_income, investment_value
        else:
            savings -= cost
            realestate.n_owned += 1 
            realestate.mortgage = realestate.value - cost
            realestate.mortgage_payment = realestate.mortgage / 360
            RealEstate.real_estate_portfolio[realestate.name.lower()] = realestate # add the real estate to the portfolio            
            investment_income += realestate.cashflow # add the cashflow to the investment income
            investment_value = Asset.investment_value()
            print(f"Purchased {realestate.name} for ${realestate.value: ,.2f} with a downpayment of ${cost: ,.2f}.")
            return savings, investment_income, investment_value
    
# sell real estate
def sell_real_estate(realestate_name, savings, investment_income, investment_value):
    realestate = RealEstate.available_realestate[realestate_name]
    if realestate.name.lower() in RealEstate.real_estate_portfolio:
        savings += realestate.equity
        realestate.n_owned -= 1
        del RealEstate.real_estate_portfolio[realestate.name.lower()]
        investment_income -= realestate.cashflow # remove the cashflow from the investment income
        investment_value = Asset.investment_value()
        print(f"Sold {realestate.name} for ${realestate.value: ,.2f}, adding ${realestate.equity: ,.2f} of equity to your account.")
        return savings, investment_income, investment_value
    else:
        print("You do not own this property.")
        return savings, investment_income, investment_value
    
# research business
def research_business():
    print()
    for business in Business.available_businesses.values():
        print(business)

# purchase business
def purchase_business(business_name, savings, investment_income, investment_value):
    business = Business.available_businesses[business_name]
    cost = business.value
    if cost > savings:
        print("Not enough cash.")
        return savings, investment_income, investment_value
    else:
        if business.name in Business.business_portfolio:
            print("Transaction cancelled.  You already own this business.")
            return savings, investment_income, investment_value
        else:
            savings -= cost
            business.n_owned += 1
            Business.business_portfolio[business.name.lower()] = business # add the business to the portfolio            
            investment_income += business.cashflow # add the cashflow to the investment income
            investment_value = Asset.investment_value()
            print(f"Purchased {business.name} for ${cost: ,.2f}.")
            return savings, investment_income, investment_value

# sell business
def sell_business(business_name, savings, investment_income, investment_value):
    business = Business.available_businesses[business_name]
    cost = business.value
    if business.name in Business.business_portfolio:
        savings += cost
        business.n_owned -= 1
        del Business.business_portfolio[business.name.lower()]
        investment_income -= business.cashflow # remove the cashflow from the investment income
        investment_value = Asset.investment_value()
        print(f"Sold {business.name} for ${cost: ,.2f}.")
        return savings, investment_income, investment_value
    else:
        print("You do not own this business.")
        return savings, investment_income, investment_value

# monthly income and expenses
def income_expenses(income, expenses, margin, savings):
    margin = income - expenses
    print()
    print("One month of income and expenses added to your account:")
    print(f"Income ${income: ,.2f} - Expenses ${expenses: ,.2f} + Current Cash: ${savings: ,.2f} = ${margin + savings: ,.2f}")
    savings += margin
    return savings
    
# General economy fluctuations
def economy():
    chance = random.randint(-10, 10)
    economic_growth = chance + monthly_inflation
    return economic_growth

# Spending habits function
def spending_habits(expenses, income, margin):
    chance = random.randint(1, 100)
    line = (margin * 1.2) / income * 100
    decrease_quadrant = (100 - line) / 4
    increase_quadrant = line / 4
    if chance <= line - increase_quadrant * 3:
        expenses += expenses * .2
        print(f"Expenses increased to ${expenses: ,.2f}")
        return expenses
    elif chance <= line - increase_quadrant * 2:
        expenses += expenses * .1
        print(f"Expenses increased to ${expenses: ,.2f}")
        return expenses
    elif chance <= line - increase_quadrant:
        expenses += expenses * .05
        print(f"Expenses increased to ${expenses: ,.2f}")
        return expenses
    elif chance <= line:
        expenses += expenses * .02
        print(f"Expenses increased to ${expenses: ,.2f}")
        return expenses
    elif chance <= line + decrease_quadrant * 2:
        print(f"Expenses unchanged at ${expenses: ,.2f}")
        return expenses
    elif chance <= line + increase_quadrant * 3:
        expenses -= expenses * .02
        print(f"Expenses decreased to ${expenses: ,.2f}")
        return expenses
    else:
        expenses -= expenses * .05
        print(f"Expenses decreased to {expenses: ,.2f}")
        return expenses

# Save and Load Functions
def save_file(filename, month_counter, savings, job_income, expenses, margin, investment_income, investment_value):
    data = {
        "month_counter": month_counter,
        "savings": savings,
        "job_income": job_income,
        "expenses": expenses,
        "margin": margin,
        "investment_income": investment_income,
        "investment_value": investment_value,
        "stock_obj": {
            name: stock.pack_details()
            for name, stock in Stocks.available_stocks.items()
},
        "bond_obj": {
            name: bond.pack_details()
            for name, bond in Bonds.available_bonds.items()
},                                                                                          
        "crypto_obj": {
            name: crypto.pack_details()
            for name, crypto in Crypto.available_crypto.items()
},
        "real_estate_obj": {
            name: real_estate.pack_details()
            for name, real_estate in RealEstate.available_realestate.items()
},
        "business_obj": {
            name: business.pack_details()
            for name, business in Business.available_businesses.items()
},
    }
    
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Game successfully saved.")
    except Exception as e:
        print(f"Failed to save game: {e}")

def load_file(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        month_counter = data["month_counter"]
        savings = data["savings"]
        job_income = data["job_income"]
        expenses = data["expenses"]
        margin = data["margin"]
        investment_income = data["investment_income"]
        investment_value = data["investment_value"]

        Stocks.available_stocks.clear()
        for name, stock_data in data["stock_obj"].items():
            Stocks.available_stocks[name] = Stocks.unpack_details(stock_data)
            stock = Stocks.available_stocks[name]
            if stock.n_owned > 0:
                Stocks.stock_portfolio[name] = stock
        
        Bonds.available_bonds.clear()
        for name, bond_data in data["bond_obj"].items():
            Bonds.available_bonds[name] = Bonds.unpack_details(bond_data)
            bond = Bonds.available_bonds[name]
            if bond.n_owned > 0:
                Bonds.bond_portfolio[name] = Bonds.unpack_details(bond_data)

        Crypto.available_crypto.clear()
        for name, crypto_data in data["crypto_obj"].items():
            Crypto.available_crypto[name] = Crypto.unpack_details(crypto_data)
            crypto = Crypto.available_crypto[name]
            if crypto.n_owned > 0:
                Crypto.crypto_portfolio[name] = Crypto.unpack_details(crypto_data)

        RealEstate.available_realestate.clear()
        for name, realeastate_data in data["real_estate_obj"].items():
            RealEstate.available_realestate[name] = RealEstate.unpack_details(realeastate_data)
            realestate = RealEstate.available_realestate[name]
            if realestate.n_owned > 0:
                RealEstate.real_estate_portfolio[name] = RealEstate.unpack_details(realeastate_data)

        Business.available_businesses.clear()
        for name, business_data in data["business_obj"].items():
            Business.available_businesses[name] = Business.unpack_details(business_data)
            business = Business.available_businesses[name]
            if business.n_owned > 0:
                Business.business_portfolio[name] = Business.unpack_details(business_data)

        print("Game successfully loaded.")
        return month_counter, savings, expenses, margin, investment_income, investment_value, job_income

    except FileNotFoundError:
        print("Save file not found.")
    except Exception as e:
        print(f"Failed to load game: {e}")

# Player Bankruptcy
def player_bankrupt(job_income, savings, expenses):
    job_income = 2000
    expenses = 1500
    savings = 0
    for obj in Stocks.stock_portfolio: #remove stocks
        obj.n_owned = 0
    Stocks.stock_portfolio.clear()

    for obj in Bonds.bond_portfolio: #remove bonds
        obj.n_owned = 0
    Bonds.bond_portfolio.clear()

    for obj in Crypto.crypto_portfolio: #remove crypto
        obj.n_owned = 0
    Crypto.crypto_portfolio.clear()

    for obj in RealEstate.real_estate_portfolio: #remove real estate
        obj.n_owned = 0
    RealEstate.real_estate_portfolio.clear()

    for obj in Business.business_portfolio: #remove businesses
        obj.n_owned = 0
    Business.business_portfolio.clear()
    print()
    print("The courts have taken all your assets to pay your creditors. \n"
        "In the stress of the process, your job performance lagged and you were let go. \n"
        "You've found a new entry-level job.  You're starting from scratch, but can still make it! \n"
        "Keep going!")
    return job_income, savings, expenses


# Assets
# stocks
stock_a = Stocks("Stock A", 10, 25, 0) # name, base_value, volatility, cashflow
stock_b = Stocks("Stock B", 12, 25, 0)
stock_c = Stocks("Stock C", 15, 25, 0)
stock_d = Stocks("Stock D", 15, 24, 0)
stock_e = Stocks("Stock E", 17, 24, 0)
stock_f = Stocks("Stock F", 18, 24, 0)
stock_g = Stocks("Stock G", 19, 20, 0)
stock_h = Stocks("Stock H", 19, 20, 0)
stock_i = Stocks("Stock I", 20, 20, 0)
stock_j = Stocks("Stock J", 20, 19, 0)
stock_k = Stocks("Stock K", 20, 18, 0)
stock_l = Stocks("Stock L", 25, 17, 0.04)
stock_m = Stocks("Stock M", 25, 16, 0)
stock_n = Stocks("Stock N", 20, 15, 0.03)
stock_o = Stocks("Stock O", 26, 14, 0)
stock_p = Stocks("Stock P", 30, 13, 0.05)
stock_q = Stocks("Stock Q", 35, 12, 0)
stock_r = Stocks("Stock R", 40, 11, 0.07)
stock_s = Stocks("Stock S", 50, 10, 0)
stock_t = Stocks("Stock T", 30, 9, 0.05)
stock_u = Stocks("Stock U", 50, 8, 0)
stock_v = Stocks("Stock V", 120, 7, 0.20)
stock_w = Stocks("Stock W", 150, 6, 0)
stock_x = Stocks("Stock X", 100, 5, 0.67)
stock_y = Stocks("Stock Y", 100, 4, 0)
stock_z = Stocks("Stock Z", 260, 3, 0.43)

# bonds
bond_a = Bonds("Bond A", 100, 1, 0.5, 12, 24) # name, base_value, volatility, cashflow, months_left, total_months
bond_b = Bonds("Bond B", 100, 2, 1, 18, 36)
bond_c = Bonds("Bond C", 100, 2, 0.9, 40, 48)
bond_d = Bonds("Bond D", 100, 3, 1.5, 10, 60)
bond_e = Bonds("Bond E", 100, 1, 0.7, 93, 120)
bond_f = Bonds("Bond F", 150, 1, 0.5, 22, 24)
bond_g = Bonds("Bond G", 150, 2, 1.2, 34, 48)
bond_h = Bonds("Bond H", 150, 1, 0.7, 29, 36)
bond_i = Bonds("Bond I", 150, 1, 1, 10, 60)
bond_j = Bonds("Bond J", 150, 1, 0.3, 8, 120)
bond_k = Bonds("Bond K", 200, 1, 0.5, 4, 24)
bond_l = Bonds("Bond L", 200, 1, 0.8, 27, 36)
bond_m = Bonds("Bond M", 200, 3, 1.9, 27, 48)
bond_n = Bonds("Bond N", 200, 1, 0.4, 19, 60)
bond_o = Bonds("Bond O", 200, 1, 0.5, 56, 120)
bond_p = Bonds("Bond P", 250, 2, 1.1, 21, 24)
bond_q = Bonds("Bond Q", 250, 1, 1.1, 24, 36)
bond_r = Bonds("Bond R", 250, 1, 0.3, 45, 48)
bond_s = Bonds("Bond S", 250, 2, 0.2, 16, 60)
bond_t = Bonds("Bond T", 250, 1, 0.6, 33, 120)
bond_u = Bonds("Bond U", 300, 1, 1.2, 24, 24)
bond_v = Bonds("Bond V", 300, 1, 0.4, 30, 36)
bond_w = Bonds("Bond W", 400, 1, 0.2, 15, 48)
bond_x = Bonds("Bond X", 500, 3, 1.7, 12, 60)
bond_y = Bonds("Bond Y", 500, 1, 1, 7, 36)
bond_z = Bonds("Bond Z", 1000, 1, 2, 82, 120)

# crypto
crypto_a = Crypto("Crypto A", 100, 50, 0) #name, base_value, volatility, cashflow
crypto_b = Crypto("Crypto B", 100, 50, 0)
crypto_c = Crypto("Crypto C", 100, 50, 0)
crypto_d = Crypto("Crypto D", 100, 50, 0)
crypto_e = Crypto("Crypto E", 100, 50, 0)

# real estate
house_a = RealEstate("House A", 100000, 8, 83) #name, base_value, volatility, cashflow
house_b = RealEstate("House B", 110000, 15, 91)
house_c = RealEstate("House C", 125000, 10, 104)
house_d = RealEstate("House D", 125000, 12, 104)
house_e = RealEstate("House E", 130000, 10, 108)
house_f = RealEstate("House F", 135000, 7, 112)
house_g = RealEstate("House G", 135000, 14, 112)
house_h = RealEstate("House H", 140000, 10, 116)
house_i = RealEstate("House I", 145000, 13, 120)
house_j = RealEstate("House J", 150000, 10, 124)
duplex_a = RealEstate("Duplex A", 200000, 7, 166)
duplex_b = RealEstate("Duplex B", 220000, 6, 183)
duplex_c = RealEstate("Duplex C", 250000, 5, 208)
duplex_d = RealEstate("Duplex D", 250000, 9, 208)
duplex_e = RealEstate("Duplex E", 300000, 8, 250)
eight_plex_a = RealEstate("8-Plex A", 800000, 7, 667)
eight_plex_b = RealEstate("8-Plex B", 800000, 6, 667)
eight_plex_c = RealEstate("8-Plex C", 900000, 5, 750)
eight_plex_d = RealEstate("8-Plex D", 1000000, 9, 833)
eight_plex_e = RealEstate("8-Plex E", 1100000, 8, 917)
apartment_complex_a = RealEstate("Apartment Complex A", 2400000, 7, 2000)
apartment_complex_b = RealEstate("Apartment Complex B", 2500000, 6, 2083)
apartment_complex_c = RealEstate("Apartment Complex C", 3000000, 5, 2500)
apartment_complex_d = RealEstate("Apartment Complex D", 5000000, 9, 4167)
apartment_complex_e = RealEstate("Apartment Complex E", 6000000, 8, 5000)
Hotel_a = RealEstate("Hotel A", 50000000, 3, 45000)

# businesses
business_a = Business("Business A", 250000, 5, 4167) # name, base_value, volatility, cashflow
business_b = Business("Business B", 300000, 2, 5000)
business_c = Business("Business C", 500000, 2, 8333)
business_d = Business("Business D", 1000000, 3, 16667)
business_e = Business("Business E", 10000000, 1, 166667)



def main_program():
    try:

        global job_income, investment_income, income, expenses, margin, savings, investment_value, monthly_inflation, month_counter
        one_six = False
        Bonds.starting_values() # get the correct value for each bond

        while True:
            print("New Game or Existing Game?")
            print("1. New Game")
            print("2. Existing Game")
            print("3. Exit Game")
            choice = input("1, 2 or 3:").strip()

            if choice == "1":
                print()
                filename = input("Create a Game Name:").lower().strip()
                save_file(filename, month_counter, savings, job_income, expenses, margin, investment_income, investment_value)
        
            elif choice == "2":
                try:
                    print()
                    filename = input("Enter Game Name:").lower().strip()
                    month_counter, savings, expenses, margin, investment_income, investment_value, job_income = load_file(filename)
                except:
                    continue
            elif choice == "3":
                break

            else:
                print()
                print("Error. Please try again.")
                continue

                
            # Game Loop
            while True:
                income = job_income + investment_income
                margin = income - expenses

                # Monthly Auto-Save
                save_file(filename, month_counter, savings, job_income, expenses, margin, investment_income, investment_value)

                # Menu
                print()
                print(f"Month {month_counter}")
                income_statement(income, expenses)
                balance_sheet(savings, investment_value)
                print()
                print("Choose option 1-9")
                print("Investment actions, (1-6), can only be used once per month:")
                print("1. Improve Salary (Once a month)")
                print("2. Research Stocks (Once a month)")
                print("3. Research Bonds (Once a month)")
                print("4. Research Crypto (Once a month)")
                print("5. Research Real Estate (Once a month)")
                print("6. Research Business (Once a month)")
                print("-------------------------------------------------------")
                print()
                print("7. Check Portfolio/Sell Assets")
                print("8. New Month")
                print("9. Exit Game")

                choice = input("Enter your choice (1-9)").strip()


                if choice == "1":
                    if one_six == False:
                        one_six = True
                        while True:
                            job_income = improve_job_income(job_income)
                            break
                    else:
                        print()
                        print("Can only do one investment action per month.")
                        continue
                
                elif choice == "2":
                    if one_six == False:
                        one_six = True
                        while True:
                            research_stocks()
                            print()
                            print("Enter 'Menu' to exit the research menu.")
                            print("Enter the name of the stock you want to buy:")
                            stock_name = input("Example: 'Stock A'").strip().lower()
                            if stock_name == "menu":
                                break  # Return to monthly actions menu
                            else:
                                if stock_name in Stocks.available_stocks:
                                    print()
                                    print("Enter the number of shares you want to buy:")
                                    try:
                                        n_shares = int(input("Number of shares: "))
                                    except ValueError:
                                        print("Invalid input. Please enter a number.")
                                        continue
                                    savings, investment_income, investment_value = purchase_stocks(stock_name, n_shares, savings, investment_income, investment_value)
                                else:
                                    print("Stock not found. Please try again.")
                    else:
                        print()
                        print("Can only do one investment action per month.")
                        continue

                elif choice == "3":
                    if one_six == False:
                        one_six = True
                        while True:
                            research_bonds()
                            print()
                            print("Enter 'Menu' to exit the research menu.")
                            print("Enter the name of the bond you want to buy:")
                            bond_name = input("Example: 'Bond A'").strip().lower()
                            if bond_name == "menu":
                                break
                            else:
                                if bond_name in Bonds.available_bonds:
                                    print()
                                    print("Enter the number of notes you want to buy:")
                                    try:
                                        n_bonds = int(input("Number of notes: "))
                                    except ValueError:
                                        print("Invalid input. Please enter a number.")
                                        continue
                                    savings, investment_income, investment_value = purchase_bonds(bond_name, n_bonds, savings, investment_income, investment_value)
                                else:
                                    print("Bond not found. Please try again.")
                    else:
                        print()
                        print("Can only do one investment action per month.")
                        continue

                elif choice == "4":
                    if one_six == False:
                        one_six = True
                        while True:
                            research_crypto()
                            print()
                            print("Enter 'Menu' to exit the research menu.")
                            print("Enter the name of the crypto you want to buy:")
                            crypto_name = input("Example: 'Crypto A'").strip().lower()
                            if crypto_name == "menu":
                                break
                            else:
                                if crypto_name in Crypto.available_crypto:
                                    print()
                                    print("Enter the number of coins you want to buy:")
                                    try:
                                        n_cryptos = int(input("Number of coins: "))
                                    except ValueError:
                                        print("Invalid input. Please enter a number.")
                                        continue
                                    savings, investment_value = purchase_crypto(crypto_name, n_cryptos, savings, investment_value)
                                else:
                                    print("Crypto not found. Please try again.")
                    else:
                        print()
                        print("Can only do one investment action per month.")
                        continue

                elif choice == "5":
                    if one_six == False:
                        one_six = True
                        while True:
                            research_real_estate()
                            print()
                            print("Enter 'Menu' to exit the research menu.")
                            print("Enter the name of the real estate you want to buy:")
                            realestate_name = input("Example: 'House A'").strip().lower()
                            if realestate_name == "menu":
                                break
                            else:
                                if realestate_name in RealEstate.available_realestate:
                                    savings, investment_income, investment_value = purchase_real_estate(realestate_name, savings, investment_income, investment_value)
                                else:
                                    print("Real estate not found. Please try again.")
                    else:
                        print()
                        print("Can only do one investment action per month.")
                        continue

                elif choice == "6":
                    if one_six == False:
                        one_six = True
                        while True:
                            research_business()
                            print()
                            print("Enter 'Menu' to exit the research menu.")
                            print("Enter the name of the business you want to buy:")
                            business_name = input("Example: 'Business A'").strip().lower()
                            if business_name == "menu":
                                break
                            else:
                                if business_name in Business.available_businesses:
                                    savings, investment_income, investment_value = purchase_business(business_name, savings, investment_income, investment_value)
                                else:
                                    print("Business not found. Please try again.")
                    else:
                        print()
                        print("Can only do one investment action per month.")
                        continue

                elif choice == "7":
                    while True:
                        print()
                        Asset.investment_portfolio()
                        print()
                        print("Enter 'Menu' to exit the portfolio menu.")
                        print("Enter the name of the asset you want to sell:")
                        asset_name = input("Example: 'Stock A'").strip().lower()
                        if asset_name == "menu":
                            break

                        elif asset_name in Stocks.stock_portfolio: #check if the asset is in the stock portfolio
                            print()
                            print("Enter the number of shares you want to sell:")
                            try:
                                n_shares = int(input("Number of shares: "))
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                                continue
                            savings, investment_income, investment_value = sell_stocks(asset_name, n_shares, savings, investment_income, investment_value)

                        elif asset_name in Bonds.bond_portfolio: #check if the asset is in the bond portfolio
                            print()
                            print("Enter the number of bonds you want to sell:")
                            try:
                                n_notes = int(input("Number of bonds: "))
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                                continue
                            savings, investment_income, investment_value = sell_bonds(asset_name, n_notes, savings, investment_income, investment_value)

                        elif asset_name in Crypto.crypto_portfolio: #check if the asset is in the crypto portfolio
                            print()
                            print("Enter the number of coins you want to sell:")
                            try:
                                n_cryptos = int(input("Number of coins: "))
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                                continue
                            savings, investment_value = sell_crypto(asset_name, n_cryptos, savings, investment_value)

                        elif asset_name in RealEstate.real_estate_portfolio: #check if the asset is in the real estate portfolio
                            print()
                            print("Are you sure you want to sell this property?")
                            confirm = input("Y/N").strip().lower()
                            if confirm == "y":
                                savings, investment_income, investment_value = sell_real_estate(asset_name, savings,investment_income, investment_value)
                            elif confirm == "n":
                                print("Transaction cancelled.")
                                continue
                            else:
                                print("Invalid input. Please try again.")
                                continue

                        elif asset_name in Business.business_portfolio: #check if the asset is in the business portfolio
                            print()
                            print("Are you sure you want to sell this business?")
                            confirm = input("Y/N").strip().lower()
                            if confirm == "y":
                                savings, investment_income, investment_value = sell_business(asset_name, savings, investment_income, investment_value)
                            elif confirm == "n":
                                print("Transaction cancelled.")
                                continue
                            else:
                                print("Invalid input. Please try again.")
                                continue
                            
                        else:
                            print("Asset not found. Please try again.")

                elif choice == "8":
                    while True:
                        print()
                        print("End of month.")
                        savings = round(income_expenses(income, expenses, margin, savings), 2)

                        if savings < 0:
                            print()
                            print("Your accounts are in the red!  Sell assets to appease the bank or declare bankruptcy.")
                            bankruptcy = input("Do you want to declare bankruptcy? (Yes or No)").strip().lower()
                            if bankruptcy == "yes":
                                job_income, savings, expenses = player_bankrupt(job_income, savings, expenses)
                            elif bankruptcy == "no":
                                savings -= margin
                                break

                        print()
                        print("Spending Habits:")
                        expenses = round(spending_habits(expenses, income, margin), 2)

                        print("-------------------------------------------------------")

                        print()
                        print("Previous portfolio values:")
                        Asset.investment_portfolio()       
                        print()            

                        print("-------------------------------------------------------")

                        economic_growth = round(economy(), 2)
                        if economic_growth <0:
                            print(f"The economy has declined by {economic_growth: .0f}%!")
                        else:
                            print(f"The economy has grown by {economic_growth: .0f}%.")


                        print()
                        stock_market_growth = round(Stocks.market(economic_growth), 2)
                        if stock_market_growth < 0:
                            print(f"The stock market is crashing {stock_market_growth: .0f}%!")
                        else:
                            print(f"The stock market has grown by {stock_market_growth: .0f}%.")
                        for value in Stocks.available_stocks.values():
                            stock_obj = value
                            stock_obj.asset_growth(stock_market_growth)

                        print()
                        bond_market_growth = round(Bonds.market(economic_growth), 2)
                        if bond_market_growth < 0:
                            print(f"The bond market is crashing {bond_market_growth: .0f}%!")
                        else:
                            print(f"The bond market has grown by {bond_market_growth: .0f}%.")
                        for value in Bonds.available_bonds.values():
                            bond_obj = value
                            bond_obj.asset_growth(bond_market_growth)

                        print()
                        crypto_market_growth = round(Crypto.market(economic_growth), 2)
                        if crypto_market_growth < 0:
                            print(f"Crypto currencies are crashing {crypto_market_growth: .0f}%!")
                        else:
                            print(f"The cryto market has grown by {crypto_market_growth: .0f}%.")
                        for value in Crypto.available_crypto.values():
                            crypto_obj = value
                            crypto_obj.asset_growth(crypto_market_growth)

                        print()
                        realestate_market_growth = round(RealEstate.market(economic_growth), 2)
                        if realestate_market_growth < 0:
                            print(f"Real Estate is crashing {realestate_market_growth: .0f}%!")
                        else:
                            print(f"The Real Estate market has grown by {realestate_market_growth: .0f}%.")
                        for value in RealEstate.available_realestate.values():
                            realestate_obj = value
                            realestate_obj.asset_growth(realestate_market_growth)
                            realestate_obj.down_payment = round(realestate_obj.value * .1, 2)

                        print()
                        business_market_growth = round(Business.market(economic_growth), 2)
                        if business_market_growth < 0:
                            print(f"Businesses accross the board are declining by {business_market_growth: .0f}%!")
                        else:
                            print(f"General business growth is at {business_market_growth: .0f}%.")
                        for value in Business.available_businesses.values():
                            business_obj = value
                            business_obj.asset_growth(business_market_growth)


                        for value in Stocks.available_stocks.values():
                            stock_obj = value
                            stock_obj.bankrupt()
                            investment_income = stock_obj.inflation(monthly_inflation, investment_income)

                        for value in Bonds.available_bonds.values():
                            bond_obj = value
                            bond_obj.monthly_bond_growth()
                            savings = round(bond_obj.maturity(savings), 2)
                            bond_obj.bankrupt()

                        for value in Crypto.available_crypto.values():
                            crypto_obj = value
                            crypto_obj.bankrupt()
                            investment_income = crypto_obj.inflation(monthly_inflation, investment_income)

                        for value in RealEstate.available_realestate.values():
                            realestate_obj = value
                            realestate_obj.mortgage, realestate_obj.cashflow, investment_income, realestate_obj.equity = realestate_obj.mortgage_paydown(investment_income)
                            realestate_obj.bankrupt()
                            investment_income = realestate_obj.inflation(monthly_inflation, investment_income)

                        for value in Business.available_businesses.values():
                            business_obj = value
                            business_obj.bankrupt()
                            investment_income = business_obj.inflation(monthly_inflation, investment_income)
                            investment_income = business_obj.cashflow_change(investment_income)
                            
                        investment_value = Asset.investment_value()
                        
                        print("-------------------------------------------------------")

                        print()
                        print("New portfolio values:")
                        Asset.investment_portfolio()

                        print("-------------------------------------------------------")

                        if investment_income > expenses:
                            print()
                            print("Your investments pay for all your expenses! \n"
                                  "Congratulations!  You're financially free!")
                            choice = input("'Continue' or 'Exit'?").strip().lower()
                            if choice == "continue":
                                pass
                            elif choice == "exit":
                                quit()
                            else:
                                print("Invalid choice.")
                                continue

                        month_counter += 1

                        one_six = False

                        break

                elif choice == "9":
                    choice = input("Do you wish to exit the game? (Y/N): ").strip().lower()
                    if choice == "Y":
                        quit()
                    else:
                        break
                else:
                    print("Invalid choice. Please try again.")
                    continue
    except Exception as e:
        print("\nAn error occurred:")
        traceback.print_exc()  # Displays full traceback including line numbers
        input("\nPress Enter to exit.")
        
if __name__ == "__main__":
    main_program()

