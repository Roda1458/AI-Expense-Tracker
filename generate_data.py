import pandas as pd
import random
from datetime import datetime, timedelta

categories = ["Food", "Travel", "Entertainment", "Utilities", "Shopping", "Health", "Education", "Other"]
descriptions = {
    "Food": ["Dominos", "Swiggy", "Zomato", "Subway", "Starbucks", "Grocery", "Bakery"],
    "Travel": ["Uber", "Ola", "Bus Ticket", "Train", "Flight Booking", "Petrol"],
    "Entertainment": ["Netflix", "Movie", "Spotify", "Concert", "Gaming"],
    "Utilities": ["Rent", "Electricity Bill", "Water Bill", "Internet", "Mobile Recharge"],
    "Shopping": ["Amazon", "Flipkart", "Myntra", "Mall Purchase", "Local Store"],
    "Health": ["Pharmacy", "Doctor Visit", "Gym", "Health Checkup"],
    "Education": ["Books", "Online Course", "Tuition Fee", "Exam Fee"],
    "Other": ["Gift", "Charity", "Miscellaneous"]
}

def generate_data(n=300, start_date="2024-01-01", end_date="2024-12-31"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    data = []

    for _ in range(n):
        category = random.choice(categories)
        desc = random.choice(descriptions[category])
        amount = random.randint(100, 10000)
        date = start + timedelta(days=random.randint(0, (end - start).days))
        if random.random() < 0.15:  # leave 15% categories empty for AI prediction
            category = None
        data.append([date.strftime("%Y-%m-%d"), desc, category, amount])

    df = pd.DataFrame(data, columns=["Date", "Description", "Category", "Amount"])
    df.to_csv("sample_expenses.csv", index=False)
    print("✅ Generated sample_expenses.csv with", len(df), "rows")

generate_data()
