import csv
from pymongo import MongoClient
from datetime import datetime
import os

class User:
    def __init__(self, mongo_uri="mongodb+srv://joseph:josephcode@cluster0.1wjst2q.mongodb.net/survey_db?retryWrites=true&w=majority"):
        """Initialize the User class with MongoDB connection"""
        self.client = MongoClient(mongo_uri)
        self.db = self.client['survey_db']
        self.collection = self.db['responses']
        
    def get_all_users(self):
        """Fetch all user data from MongoDB"""
        try:
            return list(self.collection.find({}))
        except Exception as e:
            print(f"Error fetching data from MongoDB: {e}")
            return []
    
    def format_user_data(self, user_data):
        """Format MongoDB document into a flat dictionary for CSV"""
        formatted = {
            'age': user_data.get('age', ''),
            'gender': user_data.get('gender', ''),
            'income': user_data.get('income', ''),
            'timestamp': user_data.get('timestamp', '').strftime('%Y-%m-%d %H:%M:%S') if user_data.get('timestamp') else ''
        }
        
        # Add expense categories
        expenses = user_data.get('expenses', {})
        for category in ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']:
            formatted[category] = expenses.get(category, 0)
            
        return formatted
    
    def export_to_csv(self, filename='user_data.csv'):
        """Export all user data to CSV file"""
        users = self.get_all_users()
        
        if not users:
            print("No data found in MongoDB collection.")
            return False
        
        # Prepare CSV header
        fieldnames = [
            'age', 'gender', 'income', 'timestamp',
            'utilities', 'entertainment', 'school_fees', 
            'shopping', 'healthcare'
        ]
        
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for user in users:
                    writer.writerow(self.format_user_data(user))
            
            print(f"Successfully exported {len(users)} records to {filename}")
            return True
            
        except Exception as e:
            print(f"Error writing to CSV file: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Initialize the User class
    user_manager = User()
    
    # Export data to CSV
    output_filename = f"user_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    if user_manager.export_to_csv(output_filename):
        print(f"Data exported successfully to {os.path.abspath(output_filename)}")
    else:
        print("Export failed")