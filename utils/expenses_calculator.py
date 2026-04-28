import json

class ExpensesCalculation():
    def __init__(self):
        pass

    def multiply(self,a:float,b:float):
        """Returns the product of two numbers"""

        return json.dumps({
            "status":"success",
            "data":{
                "first_number":a,
                "second_number":b,
                "product_of_numbers":a*b
            }
        })

    def calc_total_sum(self,x:list):
        """Return the total sum"""

        return json.dumps({
            "status":"success",
            "data":{
                "list of numbers":x,
                "sum_of_numbers":sum(x)
            }
        })
    
    def calc_daily_budget(self, total_budget:float,no_of_days:int):
        
        daily_budget = total_budget/no_of_days if no_of_days!=0 else 0
        return json.dumps({
            "status":"success",
            "data":{
                "total_budget":total_budget,
                "number_of_days":no_of_days,
                "daily_budget":daily_budget
            }
        })

if __name__=="__main__":
    obj = ExpensesCalculation()
    print(obj.calc_total_sum([1,2,3,4,5,6]))