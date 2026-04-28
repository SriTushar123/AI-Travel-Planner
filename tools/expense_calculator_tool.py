from langchain.tools import tool
from utils.expenses_calculator import ExpensesCalculation

class ExpenseCalculator():

    def __init__(self):
        self.expense_calculator = ExpensesCalculation()
        self.calculator_tools_list =self._setup_tools()
    

    def _setup_tools(self):
        """Setup all the tools for the calculator tool"""

        # @tool
        # def estimate_total_hotel_cost(no_of_nights,cost_per_night):
        #     """This takes number of nights and cost per night and returns the product of the same which is the 
        #     total expense of the hotel"""

        #     return self.expense_calculator.multiply(no_of_nights,cost_per_night)
        
        @tool
        def trip_budget_calculator(expenses:list):

            """This method takes all the expenses of the trip and returns the sum of all the expenses"""

            return self.expense_calculator.calc_total_sum(expenses)
        
        @tool
        def calculate_daily_budget(no_of_days,total_expense):

            """This method takes no of days and total expense as the input and divides total expense by number of 
            days thus giving daily budget of the trip"""

            return self.expense_calculator.calc_daily_budget(total_expense,no_of_days)

        return [trip_budget_calculator,calculate_daily_budget]


if (__name__=="__main__"):
    obj = ExpenseCalculator()
    print(obj.calculator_tools_list)