import random
import pandas as pd
from faker import Faker

from config import RAW_DATA_DIR
from utils.helpers import generate_subscription_id

fake = Faker()

# ------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------

users = pd.read_csv(RAW_DATA_DIR / "users.csv")

plans = pd.read_csv(RAW_DATA_DIR / "subscription_plans.csv")

# ------------------------------------------------------
# BUSINESS DATA
# ------------------------------------------------------

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "UPI",
    "Net Banking",
    "Wallet"
]

BILLING_CYCLES = [
    "Monthly",
    "Annual"
]

PAYMENT_STATUS = [
    "Paid",
    "Pending",
    "Failed"
]

# ------------------------------------------------------

records = []

for _, user in users.iterrows():

    age = user["age"]

    # ----------------------------------------------
    # REALISTIC PLAN ASSIGNMENT
    # ----------------------------------------------

    if age <= 25:

        weights = [60,25,10,5]

    elif age <= 40:

        weights = [15,25,40,20]

    else:

        weights = [5,15,35,45]

    chosen_plan = plans.sample(
        n=1,
        weights=weights
    ).iloc[0]

    start = fake.date_between(
        start_date="-5y",
        end_date="-30d"
    )

    billing = random.choices(
        BILLING_CYCLES,
        weights=[85,15]
    )[0]

    if billing == "Monthly":

        renewal = fake.date_between(
            start_date="today",
            end_date="+30d"
        )

    else:

        renewal = fake.date_between(
            start_date="today",
            end_date="+365d"
        )

    payment_status = random.choices(
        PAYMENT_STATUS,
        weights=[96,3,1]
    )[0]

    status = "Active"

    if payment_status == "Failed":
        status = "Paused"

    records.append({

        "subscription_id": generate_subscription_id(),

        "user_id": user["user_id"],

        "plan_id": chosen_plan["plan_id"],

        "plan_name": chosen_plan["plan_name"],

        "monthly_price": chosen_plan["monthly_price"],

        "billing_cycle": billing,

        "payment_method": random.choice(PAYMENT_METHODS),

        "payment_status": payment_status,

        "auto_renew": random.choice(["Yes","No"]),

        "subscription_status": status,

        "start_date": start,

        "renewal_date": renewal

    })

df = pd.DataFrame(records)

output = RAW_DATA_DIR / "subscriptions.csv"

df.to_csv(output,index=False)

print("="*60)
print("SUBSCRIPTIONS GENERATED")
print(df.head())
print("="*60)
print(f"Rows : {len(df)}")
print(f"Saved : {output}")