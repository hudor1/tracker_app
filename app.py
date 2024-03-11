"""The program allows the user to:
    - add new expense categories to the database
    - update an expense amount
    - delete an expense category from the database
    - track their spending
    - add income
    - add income categories
    - delete an income category from the database
    - track their income
    - view expense or income categories
    - the program should be able to calculate the user's budget based
      on the income and expenses that they provided
"""

import sqlite3
import atexit
import datetime
from tabulate import tabulate
db = sqlite3.connect('expenses_budget.db')
atexit.register(db.close)
cursor = db.cursor()


def create_expenses_table():
    """Creates an expenses table if it doesn't exist."""
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses(
                    id INTEGER PRIMARY KEY,
                    date DATE,
                    description TEXT COLLATE NOCASE,
                    category TEXT COLLATE NOCASE,
                    amount REAL )
                    ''')


def create_income_table():
    """Creates an income table if it doesn't exist."""
    cursor.execute('''CREATE TABLE IF NOT EXISTS income(
                    id INTEGER PRIMARY KEY,
                    date DATE,
                    description TEXT COLLATE NOCASE,
                    category TEXT COLLATE NOCASE,
                    amount REAL )
                    ''')


def create_category_budget_table():
    """Creates a category_budget table if it doesn't exist."""
    cursor.execute('''CREATE TABLE IF NOT EXISTS category_budget(
                    id INTEGER PRIMARY KEY,
                    date DATE,                       
                    category TEXT COLLATE NOCASE,
                    amount REAL )
                    ''')


def create_financial_goals_table():
    """Creates a financial_goals table if it doesn't exist."""
    cursor.execute('''CREATE TABLE IF NOT EXISTS financial_goals(
                    id INTEGER PRIMARY KEY,
                    date DATE,                       
                    description TEXT COLLATE NOCASE,
                    financial_goal_amt REAL,
                    allotted_amount REAL,
                    req_amount REAL,
                    progress REAL)
                    ''')


def select_category():
    """Creates an enumerated expense category list.

    Raises
    ------
    ValueError
        If the data type entered for selecting a category is not an integer.
    """    
    expense_categories = [
        'Bond/Rent',
        'Rates & taxes',
        'Household',
        'Vehicle/Transport',
        'Children',
        'Insurance',
        'Investments/savings',
        'Retail accounts',
        'Loans',
        'Clothing',
        'Entertainment',
        'Eating out',
        'Other'
    ]    
    while True:        
        try:
            print('Select expense category')
            for i, category_name in enumerate(expense_categories):
                print(f' {i + 1}. {category_name}')
            
            value_range = f'[1 - {len(expense_categories)}]'
            selected_index = int(input(f"Enter a category number{value_range}: " )) - 1

            if selected_index in range(len(expense_categories)):
                category = expense_categories[selected_index]
                return category
            else:
                print("Invalid category option selected!")            
        except ValueError:   
            print("Invalid Entry. Please enter an integer.")            
    

def add_expense(date, category, description, amount):
    """Inserts the expense attributes into the expenses table.

    Parameters
    ----------
    date : str
        the transaction date of the expense.
    category : str
        the category of the expense.
    description : str
        the description of the expense.
    amount : float
        the amount of the expense.
    """                  
    with db:
        cursor.execute('''INSERT OR ABORT INTO expenses(date, category, description, amount)
                        VALUES(?,?,?,?)''',(date, category, description, amount))
    view_expenses()
           

def view_expenses():
    """Displays the expenses in the table."""       
    # Returns the sum total of the expenses.
    expense_total = view_total_expenses()
    cursor.execute('''SELECT id, date, category, description, amount FROM expenses''')
    results = cursor.fetchall()   
    print()
    print('EXPENSES:')
    print()
    # Prints the results and column headings in a table form.
    print(tabulate(results, headers=['ID','DATE', 'CATEGORY', 'DESCRIPTION', 'AMOUNT'], tablefmt='grid'))
    print(f'Total expenses: R{expense_total}')
    print()


def view_expenses_by_category():
    """Displays expenses filtered by category."""        
    # Returns the expense categories menu.
    category = select_category()                
    with db:
        cursor.execute('''SELECT date, description, amount 
                        FROM expenses WHERE category = ?                                   
                        ORDER BY date DESC''',(category,))
        results = cursor.fetchall()
        print()        
        print(f'({len(results)}) item/s for {category}.')
        # Prints the results and column headings in a table form.
        print(tabulate(results, headers=['DATE', 'DESCRIPTION', 'AMOUNT'], tablefmt='grid'))
    # Returns the expenses category total by passing the category as an argument.
    category_total = expense_category_total(category)
    print(f'{category} total = R{category_total}')
            

def update_expense_amount(ID, amount):
    """Updates the expense amount.

    Parameters
    ----------
    ID : int
        the id of the expense item to be updated.
    amount : float
        the new expense amount.
    """
    with db:
        cursor.execute('''SELECT * FROM expenses WHERE id = ?''',(ID,))
        result = cursor.fetchone()
        if result == None:
            print('Invalid id entered.')
        else:
            cursor.execute('''UPDATE expenses SET amount = ? WHERE id = ?''',(amount, ID,))                
            view_expenses()


def remove_expense(ID):
    """Removes the expense item from the table."""       
    with db:
        cursor.execute('''SELECT * FROM expenses WHERE id = ?''',(ID,))
        result = cursor.fetchone()
        if result == None:
            print('Invalid id entered.')
        else:
            cursor.execute('''DELETE FROM expenses WHERE id = ?''',(ID,))            
            view_expenses()
    

def view_total_expenses():
    """Returns the total expenses amount.

    Returns
    -------
    float
        total expenses amount else 0 if the value is null.
    """
    with db:
        cursor.execute('''SELECT SUM(amount) FROM expenses''')
        total, = cursor.fetchone()
        return total if total is not None else 0


def expense_category_total(category):
    """Returns the expenses category total amount.

    Parameters
    ----------
    category : str
        the expenses category to be displayed.
    
    Returns
    -------
    float
        expenses category total amount else 0 if value is null.
    """
    with db:
        cursor.execute('''SELECT SUM(amount) FROM expenses WHERE category = ?''', (category,))
        total, = cursor.fetchone()
        return total if total is not None else 0


def select_income_category():
    """Creates an enumerated income category list.

    Raises
    ------
    ValueError
        If the data type entered for selecting a category is not an integer.
    """
    income_categories = [
        'Salary',
        'Investments',
        'Profit',
        'Interest',
        'Rental income',
        'Other income'
    ]    
    while True:
        try:
            print('Select income category')
            for i, category_name in enumerate(income_categories):
                print(f' {i + 1}. {category_name}')
        
            value_range = f'[1 - {len(income_categories)}]'
            selected_index = int(input(f'Enter a category number{value_range}: ')) - 1

            if selected_index in range(len(income_categories)):
                category = income_categories[selected_index]
                return category
            else:
                print('Invalid category option selected!')
        except ValueError:        
            print('Invalid Entry. Please enter an integer.')


def add_income(date, category, description, amount):
    """Inserts the income attributes into the income table.

    Parameters
    ----------
    date : str
        the income transaction date.
    category : str
        the category of the income. 
    description : str
        the description of the income.
    amount : float
        the income amount.
    """
    with db:
        cursor.execute('''INSERT OR ABORT INTO income(date, category, description, amount)
                        VALUES(?,?,?,?)''',(date, category, description, amount))
        view_income()


def view_income():
    """Displays the income items in the table."""   
    # Returns the total income.
    income_total = view_total_income()
    cursor.execute('''SELECT * FROM income''')
    results = cursor.fetchall()
    print()
    print('INCOME:')
    print()
    # Prints the results and column headings in a table form.
    print(tabulate(results, headers=['ID', 'DATE', 'DESCRIPTION', 'CATEGORY', 'AMOUNT'], tablefmt='grid'))    
    print(f'Total income: R{income_total}')


def view_income_by_category():
    """Displays income items filtered by category."""
    category = select_income_category()
    with db:
        cursor.execute('''SELECT date, description, amount 
                        FROM income WHERE category = ?                                   
                        ORDER BY date DESC''',(category,))
        results = cursor.fetchall()
        print()
        print(f'({len(results)}) item/s for {category}')
        # Prints the results and column headings in a table form.
        print(tabulate(results, headers=['DATE', 'DESCRIPTION', 'AMOUNT'], tablefmt='grid'))                
        # Returns the category total amount by passing the category as an argument.
        category_total = income_category_total(category)
        print(f'{category} total = R{category_total}')


def update_income_amount(ID, amount):
    """Updates the income amount.

    Parameters
    ----------
    ID : int
        the id of the income item.
    amount : float
        the new income amount.
    """
    with db:
        cursor.execute('''SELECT * FROM income WHERE id = ?''',(ID,))
        result = cursor.fetchone()
        if result == None:
            print('Invalid id entered.')
        else:
            cursor.execute('''UPDATE expenses SET amount = ? WHERE id = ?''',(amount, ID,))                
            view_income()


def remove_income():
    """Removes the income item from the income table."""
    with db:
        cursor.execute('''SELECT * FROM income WHERE id = ?''',(ID,))
        result = cursor.fetchone()
        if result == None:
            print('Invalid id entered.')
        else:
            cursor.execute('''DELETE FROM income WHERE id = ?''',(ID,))            
            view_income()


def view_total_income():
    """Displays the income total amount.

    Returns
    -------
    float
        total income else 0 if the value is null.
    """    
    with db:
        cursor.execute('''SELECT SUM(amount) FROM income ''')
        total, = cursor.fetchone()
        return total if total is not None else 0


def income_category_total(category):
    """Returns the income category total amount.

    Parameters
    ----------
    category : str
        the income category items to display.
    
    Returns
    -------
    float
        income category total amount else 0 if value is null.
    """
    with db:
        cursor.execute('''SELECT SUM(amount) FROM income WHERE category = ?''', (category,))
        total, = cursor.fetchone()
        return total if total is not None else 0


def set_budget_for_category(date, category, amount):
    """Sets the budget amount for a selected category.

    Parameters
    ----------
    date : str
        the date for setting the budget.
    category : str
        the category for which the budget is set.
    amount : float
        the category budget amount.
    """             
    with db:
        cursor.execute('''INSERT OR ABORT INTO category_budget(date, category, amount)
                        VALUES(?,?,?)''',(date, category, amount))                
    print(f'{category} budget has been set to R{amount}')          


def get_budget_amount(category):
    """Returns the category budget amount if the amount is not null else returns 0.
    
    Returns
    -------
    float
        budget amount else 0 if the value is null.
    """  
    with db:                    
        cursor.execute('''SELECT SUM(amount) FROM category_budget WHERE category = ?''',(category,))
        budget_amount, = cursor.fetchone()
        return budget_amount if budget_amount is not None else 0


def view_budget_for_category():
    """Displays the expenses category budget amount."""    
    # Returns the category menu, category budget, and total category expenses.
    category = select_category()  
    category_budget = get_budget_amount(category)
    category_expenses = expense_category_total(category)    
    # Calculates the available budget.
    available_budget = category_budget - category_expenses    
    print()
    print(f'CATEGORY: {category}')
    if available_budget < 0:    
        print(f'⚠ You have exceeded your budget for {category} by R{available_budget * (-1)}')    
    # Prints the available funds by subtracting the category expenses from the category budget.
    print(tabulate([[str(category_budget), str(category_expenses), str(available_budget)]], headers=['BUDGET', 'EXPENSES', 'AVAILABLE AMOUNT'], tablefmt='grid'))
                                     
 
def get_available_funds():
    """Returns available funds.
    
    Returns
    -------
    float
        available funds.
    """
    # Returns the total income, total expenses, and total allotted towards financial goals.
    total_income = view_total_income()
    total_expenses = view_total_expenses()
    allotted_total = return_allotted_amount_total()
    # Calculates available funds.
    available_funds = total_income - total_expenses - allotted_total
    return available_funds


def set_financial_goals(date, description, financial_goal_amt, allotted_amount, req_amount, progress):
    """Inserts the financial goals attributes into the financial_goals table.

    Parameters
    ----------
    date : str
        the financial goal due date.
    description : str
        the financial goal description.
    financial_goal_amt : float
        the total amount of the financial goal.
    allotted_amount : float
        the amount allocated towards the financial goal.
    req_amount : float
        the required amount is the difference between financial_goal_amt and allotted_amount
    progress : float
        the goal progress percentage.
    """
    available_funds = get_available_funds()    
    if available_funds <= 0:
        print('Not enough funds to allocate towards goal.')    
    else:
        new_available_funds = available_funds - allotted_amount
        # Calculates the shortfall amount towards the financial goal.
        req_amount = financial_goal_amt - allotted_amount
        # Calculates the progress percentage of the  financial goal.
        progress = (allotted_amount / financial_goal_amt) * 100
        with db:
            cursor.execute('''INSERT INTO financial_goals(date, description, financial_goal_amt, allotted_amount, req_amount, progress)
                           VALUES(?,?,?,?,?,?) ''',(date, description, financial_goal_amt, allotted_amount, req_amount, progress))
        print(f'Available funds = R{new_available_funds}')    
        

def view_financial_goals():
    """Displays the financial goals items."""       
    cursor.execute('''SELECT id, description, financial_goal_amt, allotted_amount, date FROM financial_goals''')
    results = cursor.fetchall()    
    print()
    print('FINANCIAL GOALS:')
    print()
    # Prints the results and column headings in a table form.
    print(tabulate(results, headers=['ID', 'DESCRIPTION', 'GOAL AMOUNT', 'ALLOTTED AMOUNT', 'DUE DATE'], tablefmt='grid'))


def update_allotted_amt(allotted_amount, ID):
    """Updates the amount allocated towards the financial goal.

    Parameters
    ----------
    allotted_amont : float
        the new amount allocated towards the financial goal.
    ID : int
        the id of the financial goal item.
    """
    with db:
        cursor.execute('''SELECT * FROM financial_goals WHERE id = ?''',(ID,))
        result = cursor.fetchone()
        if result == None:
            print('Invalid id entered.')
        else:
            cursor.execute('''SELECT financial_goal_amt FROM financial_goals WHERE id = ?''',(ID,))
            goal_amount, = cursor.fetchone()
            req_amount = goal_amount - allotted_amount
            # Calculates the progress percentage of the financial goals.
            progress = round((allotted_amount / goal_amount) * 100, 2)  
            cursor.execute('''UPDATE financial_goals SET allotted_amount = ?, req_amount = ?, progress = ?
                       WHERE id = ?''',(allotted_amount, req_amount, progress, ID))            
            print('Allotted amount updated!')
            view_financial_goals()


def update_financial_goal_amt(financial_goal_amt, ID):
    """Updates the financial goal amount.

    Parameters
    ----------
    financial_goal_amt : float
        the new financial goal amount.
    ID : int
        the id of the financial goal to be updated.
    """
    with db:
        cursor.execute('''SELECT * FROM financial_goals WHERE id = ?''',(ID,))
        result = cursor.fetchone()
        if result == None:
            print('Invalid id entered.')
        else:
            cursor.execute('''SELECT allotted_amount FROM financial_goals WHERE id = ?''',(ID,))
            allotted_amount, = cursor.fetchone()
            req_amount = financial_goal_amt - allotted_amount
            progress = round((allotted_amount / financial_goal_amt) * 100, 2)
            # Updates the financial goal amount and also updates the required amount as well as the progress percentage.
            cursor.execute('''UPDATE financial_goals SET financial_goal_amt = ?, req_amount = ?, progress = ?
                       WHERE id = ?''',(financial_goal_amt, req_amount, progress, ID))
            print('Financial goal amount updated!')
            view_financial_goals()


def remove_financial_goal(ID):
    """Removes the financial goal.

    Parameters
    ----------
    ID : int
        the id of the financial goal to be removed.
    """
    with db:
        cursor.execute('''SELECT * FROM financial_goals WHERE id = ?''',(ID,))
        result = cursor.fetchone()
        if result == None:
            print('Invalid id entered.')            
        else:
            cursor.execute('''DELETE FROM financial_goals WHERE id = ?''',(ID,))
            print('Financial goal removed!')
            view_financial_goals()             


def view_financial_progress():
    """Displays the financial goals progress."""       
    cursor.execute('''SELECT * FROM financial_goals''')
    results = cursor.fetchall() 
    # Returns the financial progress percentage.
    progress_percent  = return_financial_goals_percentage()
    print()
    print(f'FINANCIAL GOALS PROGRESS: {progress_percent}%')
    # Prints the results and column headings in a table form.
    print(tabulate(results, headers=['ID', 'DUE DATE', 'DESCRIPTION', 'GOAL AMOUNT', 'ALLOTTED AMOUNT', 'REQUIRED AMOUNT', 'PROGRESS %'], tablefmt='grid'))


def return_financial_goals_total():
    """Returns the financial goals total amount.
    
    Returns
    -------
    float
        financial goals total amount else 0 if value is null.
    """
    with db:
        cursor.execute('''SELECT SUM(financial_goal_amt) FROM financial_goals''')
        goals_total, = cursor.fetchone()
        return goals_total if goals_total is not None else 0


def return_allotted_amount_total():
    """"Returns the allotted amount total.
    
    Returns
    -------
    float
        allotted total amount else 0 if value is null.
    """   
    with db:  
        cursor.execute('''SELECT SUM(allotted_amount) FROM financial_goals''')
        amount_total, = cursor.fetchone()
        return amount_total if amount_total is not None else 0 


def return_financial_goals_percentage():
    """Returns the financial goals percentage.
    
    Returns
    -------
    float
        financial goals percentage.

    Raises
    ------
    ZeroDivisionError 
        if division by zero.
    """
    goals_total = return_financial_goals_total()   
    allotted_total = return_allotted_amount_total()
    try:   
        goals_percentage = round((allotted_total / goals_total) * 100, 2)
        return goals_percentage 
    except ZeroDivisionError:
        print('Goal amount is equal to 0. Unable to calculate progress!') 
        

# Creates the tables
create_expenses_table()
create_income_table()
create_category_budget_table()
create_financial_goals_table()

while True:
    menu = ''              
    print('''
=== expense and budget main menu ===
1. Add expense
2. View expenses
3. View expenses by category
4. Add income
5. View income
6. View income by category     
7. Set budget for a category
8. View budget for a category
9. Set financial goals
10. View progress towards financial goals
11. Quit              
''')
    try:
        menu = int(input('Enter your choice: '))            
    except ValueError:
        print('Invalid entry! Please enter an integer.')
    
    if menu == 1:
        while True:
            expense_menu = ''              
            print('''
=== expense menu ===
1. Add expense
2. Update expense
3. Delete expense
0. Exit              
''')
            try:
                expense_menu = int(input('Enter your choice: '))            
            except ValueError:
                print('Invalid entry! Please enter an integer.')
            
            if expense_menu == 1:                                
                category = select_category()                
                date = input('Enter transaction date(YYYY-MM-DD) or press [Enter] to use today\'s date: ')                               
                # If the user does not enter the date, the program will use the current date.
                if len(date) == False:                                                   
                    date = datetime.date.today()               
                description = input('Enter expense description (25 characters max): ')
                # If the user does not enter the description, they will be notified and the program will use "Not specified" as a description.
                if len(description) == False:
                    print('You did not enter the description!')
                    description = 'Not specified'
                else:
                    # The program will slice the description to 25 characters if the user enters more characters.
                    description = description[0:24]            
                try:
                    amount = float(input('Enter expense amount: '))
                except ValueError:
                    print('Invalid input. Please try a number!')                                   
                add_expense(date, category, description, amount)
            
            elif expense_menu == 2:
                try:
                    view_expenses()
                    ID = int(input('Enter item id to update amount: '))
                    amount = float(input('Enter new expense amount: '))
                except ValueError:
                    print('Invalid input. Please try a number!')                    
                update_expense_amount(ID, amount)
           
            elif expense_menu == 3:                
                try:
                    view_expenses()
                    ID = int(input('Enter item id to remove item: '))
                    remove_expense(ID)
                except ValueError:
                    print('Invalid input!')                                        
            elif expense_menu == 0:
                break
            else:
                print('Invalid input. Please try again!')
    
    elif menu == 2:
        view_expenses()
    elif menu == 3:
        view_expenses_by_category()   
    elif menu == 4:
        while True:
            income_menu = ''              
            print('''
=== expense menu ===
1. Add income
2. Update income
3. Delete income
0. Exit              
''')
            try:
                income_menu = int(input('Enter your choice: '))            
            except ValueError:
                print('Invalid entry! Please enter an integer.')
            if income_menu == 1:
                category = select_income_category()
                # If the user does not enter the date, the program will use the current date.
                date = input('Enter transaction date(YYYY-MM-DD) or press [Enter] to use today\'s date: ')
                if len(date) == False:                                                   
                    date = datetime.date.today()
                # If the user does not enter the description, they will be notified and the program will use "Not specified" as a description.
                description = input('Enter income description (25 characters max): ')
                if len(description) == False:
                    print('You did not enter the description!')
                    description = 'Not specified'
                else:
                    # The program will slice the description to 25 characters if the user enters more characters.
                    description = description[0:24] 
                try:
                    amount = float(input('Enter income amount: '))
                except ValueError:
                    print('Invalid input. Please try a number!')
                add_income(date, category, description, amount)
            
            elif income_menu == 2:
                try:
                    view_expenses()
                    ID = int(input('Enter item id to update amount: '))
                    amount = float(input('Enter new income amount: '))
                except ValueError:
                    print('Invalid input. Please try a number!')                    
                update_income_amount(ID, amount)
            elif income_menu == 3:
                try:
                    view_income()
                    ID = int(input('Enter item id to remove item: '))
                    remove_expense(ID)
                except ValueError:
                    print('Invalid input!')
            elif income_menu == 0:
                break

    elif menu == 5:
        view_income()
    elif menu == 6:
        view_income_by_category()    
    elif menu == 7:
        category = select_category()
        date = input('Enter transaction date(YYYY-MM-DD) or press [Enter] to use today\'s date: ')
        # If the user does not enter the date, the program will use the current date.
        if len(date) == False:                               
            date = datetime.date.today()
        try:
            amount = float(input('Enter category budget amount: '))
        except ValueError:
            print('Invalid input. Please try a number!')        
        set_budget_for_category(date, category, amount)
        
    elif menu == 8:
        view_budget_for_category()
    elif menu == 9:
        while True:
            financial_goal_menu = ''              
            print('''
=== financial_goal_menu ===
1. Set financial goal
2. View financial goals
3. Update financial goal amount
4. Update amount allotted to financial goal
5. Delete financial goal
0. Exit              
''')
            try:
                financial_goal_menu = int(input('Enter your choice: '))            
            except ValueError:
                print('Invalid entry! Please enter an integer.')
            
            if financial_goal_menu == 1:
                # Returns the available funds.
                available_funds = get_available_funds()
                print(f'Available funds = R{available_funds}')
                date = input('Enter target date(YYYY-MM-DD) or press [Enter] to use today\'s date: ')
                # If the user does not enter the date, the program will use the current date.
                if len(date) == False:                               
                    date = datetime.date.today()
                description = input('Enter financial goal description (25 characters max): ')
                # If the user does not enter the description, the program will use "Not specified" as a description.
                if len(description) == False:
                    print('You did not enter the description!')
                    description = 'Not specified'
                else:
                    # The program will slice the description to 25 characters if the user enters more characters.
                    description = description[0:24]
                try:
                    financial_goal_amt = float(input('Enter the financial goal amount: '))
                    allotted_amount = float(input('Enter amount to allot towards financial goal: '))
                    req_amount = financial_goal_amt - allotted_amount
                    progress = round((allotted_amount / financial_goal_amt) * 100, 2)
                except ValueError:
                    print('Invalid input. Please try a number!')
                    set_financial_goals()       
                set_financial_goals(date, description, financial_goal_amt, allotted_amount, req_amount, progress)
            
            elif financial_goal_menu == 2:
                view_financial_goals()
            
            elif financial_goal_menu == 3:
                view_financial_goals()
                try:
                    ID = int(input('Enter item id to update financial goal amount: '))
                    financial_goal_amt = float(input('Enter new financial goal amount: '))                    
                except ValueError:
                    print('Invalid input. Please try a number!')
                update_financial_goal_amt(financial_goal_amt, ID)
            
            elif financial_goal_menu == 4:
                view_financial_goals()
                try:
                    ID = int(input('Enter item id to update allocated amount: '))
                    allotted_amount = float(input('Enter the new amount to allot towards financial goal: '))                    
                except ValueError:
                    print('Invalid input. Please try a number!')
                update_allotted_amt(allotted_amount, ID)
            
            elif financial_goal_menu == 5:
                view_financial_goals()
                try:
                    ID = int(input('Enter item id to remove financial goal: '))
                except ValueError:
                    print('Invalid input. Please try a number!')
                remove_financial_goal(ID)
            elif financial_goal_menu == 0:
                break
            else:
                print('Invalid input. Please try again!')    

    elif menu == 10:
        view_financial_progress()
    elif menu == 11:
        print('Good-bye!')
        db.close()
        quit()    
    else:
        print('Invalid input. Please try again!')

