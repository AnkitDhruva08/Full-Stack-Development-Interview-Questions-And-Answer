import os
import razorpay
RAZORPAY_KEY_ID='xxxxxxxxxxxxxxxx'
RAZORPAY_KEY_SECRET='xxxxxxxxxxxxxxxx'

# Initialize Razorpay client
client = razorpay.Client(auth=(
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET
))

# Fetch all plans
plans = client.plan.all()

print("\n📦 Available Razorpay Plans:\n")

for plan in plans['items']:
    plan_id = plan['id']
    name = plan['item']['name']
    period = plan['period']
    amount = plan['item']['amount'] / 100  # convert paise to INR
    print(f"🆔 {plan_id}\n📘 Name: {name}\n⏱️ Period: {period}\n💰 Amount: ₹{amount}\n{'-'*40}")

print("\n✅ Copy these into your .env file accordingly:\n")
for plan in plans['items']:
    name = plan['item']['name'].lower().replace(' ', '_')
    period = plan['period']
    plan_id = plan['id']
    print(f"RAZORPAY_{name.upper()}_{period.upper()}_PLAN_ID={plan_id}")


# run script 
# python coding/Python/unittest/get_pal_id.py


