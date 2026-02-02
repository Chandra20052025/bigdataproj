from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum
import json

class SparkAnalytics:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("Company Analytics") \
            .master("local[*]") \
            .getOrCreate()
        self.spark.sparkContext.setLogLevel("ERROR")
    
    def load_all_data(self):
        """Load all department data"""
        try:
            self.sales_df = self.spark.read.csv("data/sales.csv", header=True, inferSchema=True)
            self.hr_df = self.spark.read.csv("data/hr.csv", header=True, inferSchema=True)
            self.finance_df = self.spark.read.csv("data/finance.csv", header=True, inferSchema=True)
            self.production_df = self.spark.read.json("data/production.json")
            
            # Clean data
            self.sales_df = self.sales_df.dropna()
            self.hr_df = self.hr_df.dropna()
            self.finance_df = self.finance_df.dropna()
            self.production_df = self.production_df.dropna()
            
            print("✓ Data loaded successfully")
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    def calculate_profit_loss(self):
        """Calculate overall profit/loss"""
        total_revenue = self.sales_df.agg(spark_sum("amount")).collect()[0][0] or 0
        hr_cost = self.hr_df.agg(spark_sum("salary")).collect()[0][0] or 0
        finance_cost = self.finance_df.agg(spark_sum("amount")).collect()[0][0] or 0
        production_cost = self.production_df.agg(spark_sum("cost")).collect()[0][0] or 0
        
        total_cost = hr_cost + finance_cost + production_cost
        profit_loss = total_revenue - total_cost
        
        return {
            'total_income': float(total_revenue),
            'total_expenses': float(total_cost),
            'profit_loss': float(profit_loss),
            'status': 'Profit' if profit_loss > 0 else 'Loss'
        }
    
    def get_department_breakdown(self):
        """Get department-wise breakdown"""
        sales_revenue = self.sales_df.agg(spark_sum("amount")).collect()[0][0] or 0
        hr_cost = self.hr_df.agg(spark_sum("salary")).collect()[0][0] or 0
        finance_cost = self.finance_df.agg(spark_sum("amount")).collect()[0][0] or 0
        production_cost = self.production_df.agg(spark_sum("cost")).collect()[0][0] or 0
        
        return {
            'Sales': {
                'income': float(sales_revenue),
                'expenses': 0,
                'net': float(sales_revenue)
            },
            'HR': {
                'income': 0,
                'expenses': float(hr_cost),
                'net': float(-hr_cost)
            },
            'Finance': {
                'income': 0,
                'expenses': float(finance_cost),
                'net': float(-finance_cost)
            },
            'Production': {
                'income': 0,
                'expenses': float(production_cost),
                'net': float(-production_cost)
            }
        }
    
    def get_monthly_trend(self):
        """Get monthly trend - mock data for now"""
        return {
            '2025-10': {'income': 50000, 'expenses': 35000, 'profit_loss': 15000},
            '2025-11': {'income': 52000, 'expenses': 34000, 'profit_loss': 18000},
            '2025-12': {'income': 53000, 'expenses': 34000, 'profit_loss': 19000}
        }
    
    def get_detailed_stats(self):
        """Get detailed statistics"""
        return {
            'sales_count': self.sales_df.count(),
            'hr_employees': self.hr_df.count(),
            'finance_transactions': self.finance_df.count(),
            'production_items': self.production_df.count(),
            'avg_sale_amount': float(self.sales_df.agg({'amount': 'avg'}).collect()[0][0] or 0),
            'avg_salary': float(self.hr_df.agg({'salary': 'avg'}).collect()[0][0] or 0)
        }
    
    def stop(self):
        """Stop Spark session"""
        self.spark.stop()

if __name__ == "__main__":
    print("Starting Spark Analytics...")
    analytics = SparkAnalytics()
    analytics.load_all_data()
    
    print("\n=== Profit/Loss Summary ===")
    print(json.dumps(analytics.calculate_profit_loss(), indent=2))
    
    print("\n=== Department Breakdown ===")
    print(json.dumps(analytics.get_department_breakdown(), indent=2))
    
    print("\n=== Detailed Stats ===")
    print(json.dumps(analytics.get_detailed_stats(), indent=2))
    
    analytics.stop()
    print("\nSpark session stopped.")