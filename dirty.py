import pandas as pd
import random

random.seed(42)

first_names = [
    " John", "jane ", "ALICE", "bob", " Charlie ", "dAvE", " Eve", "frank ",
    "GRACE", " hannah", "Isaac ", "JULIA", " kevin", "Liam ", "mia", " Noah",
    "olivia ", "PETER", " quinn", "Ruby "
]

last_names = [
    " Smith", "johnson ", "WILLIAMS", "brown", " Jones ", "Miller", " Davis",
    "garcia ", "RODRIGUEZ", "wilson ", "Martinez", "Anderson ", "TAYLOR"
]

cities = [
    " New York", "los angeles ", "CHICAGO", "houston", " Phoenix ",
    "philadelphia", "SAN ANTONIO ", "san diego", " Dallas ", "austin"
]

departments = [
    " Sales", "engineering ", "HR", "marketing", " Finance ",
    "operations", "IT ", "support", " Legal ", "product"
]

statuses = ["Active", " inactive ", "PENDING", "active ", " Suspended", None]

notes = [
    " good client", "Needs Follow Up ", "VIP", " late payer ",
    "Returned item", None, "duplicate?", "  ", "Prefers email"
]

dirty_numbers = [
    "100", " 250 ", "$300", "N/A", "four hundred", None, "500.00", " 75", "1,200", "??"
]

dirty_dates = [
    "2024-01-15", "01/22/2024", "March 5 2024", "2024/04/18",
    "not a date", None, "13/13/2024", "2024-07-32", " 2024-09-10 ", "02-28-2024"
]

emails = [
    "test@example.com", " USER@MAIL.COM ", "bademail@", "none",
    None, "sample.user@gmail.com", "hello@site", "foo@bar.com "
]

rows = []

for i in range(100):
    first = random.choice(first_names)
    last = random.choice(last_names)
    full_name = f"{first} {last}"

    row = {
        # duplicates + missing
        "customer_id": random.choice([i + 1, i + 1, i, None]),
        "full_name": full_name,
        "email": random.choice(emails),
        "city": random.choice(cities),
        "department": random.choice(departments),
        "status": random.choice(statuses),
        "purchase_amount": random.choice(dirty_numbers),
        "signup_date": random.choice(dirty_dates),
        "notes": random.choice(notes),
        "score": random.choice(["90", "85 ", " seventy", None, "100", "N/A", " 72"])
    }

    rows.append(row)

# Force a few exact duplicate rows
rows[10] = rows[5]
rows[25] = rows[5]
rows[50] = rows[20]
rows[75] = rows[20]

df = pd.DataFrame(rows)
df.to_csv("dirty_test_data.csv", index=False)

print("dirty_test_data.csv created with 100 dirty records.")
