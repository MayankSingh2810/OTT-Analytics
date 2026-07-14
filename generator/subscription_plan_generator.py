import pandas as pd

from config import RAW_DATA_DIR

plans = [

    {
        "plan_id":"PLAN001",
        "plan_name":"Mobile",
        "monthly_price":149,
        "video_quality":"480p",
        "screens":1,
        "ads":"Yes",
        "download":"No"
    },

    {
        "plan_id":"PLAN002",
        "plan_name":"Basic",
        "monthly_price":249,
        "video_quality":"720p",
        "screens":1,
        "ads":"No",
        "download":"Yes"
    },

    {
        "plan_id":"PLAN003",
        "plan_name":"Standard",
        "monthly_price":499,
        "video_quality":"1080p",
        "screens":2,
        "ads":"No",
        "download":"Yes"
    },

    {
        "plan_id":"PLAN004",
        "plan_name":"Premium",
        "monthly_price":799,
        "video_quality":"4K",
        "screens":4,
        "ads":"No",
        "download":"Yes"
    }

]

df = pd.DataFrame(plans)

output = RAW_DATA_DIR / "subscription_plans.csv"

df.to_csv(output,index=False)

print("="*60)
print("SUBSCRIPTION PLANS GENERATED")
print(df)
print("="*60)