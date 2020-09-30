from collections import defaultdict 

"""

PROBLEM: Management needs to know how many of each item they are selling each 
day and what each customer’s current reward points balance is.

Design a system that parses the log file and:
1) Calculates the reward points for each customer
2) Generates purchase counts for each item sold during the day

Here are some considerations for the rewards system you want to create:

- For each purchase, a customer can spend a certain amount of reward points for their purchase.
- Some customers come to the store multiple times per day.
- Customers earn 1 reward point for every 18 dollars spent, unless they spend more than $250 per day, in which case they earn 1 reward point for every 17 dollars spent. These reward points are given to the customers at the **end** of each day, not immediately after the purchase.
- For each LogEntry, we want to keep track of:
    - Customer ID
    - Number of reward points used for that purchase
    - List of items purchased and their prices

There can also be malformed logs in which any of the three properties in the LogEntry are 'None'.
If this is the case, please address them in the following ways:
- If there is no customer ID, do not count the rewards points. Instead, only calculate the purchase counts for the items
- If there is no rewards points specified, assume rewards points = 0
- If there is no list of items purchased, then this is an error in the system. Please add this LogEntry to a error log (a list of LogEntry called 'error')

Example- this is written in casual terms, and must be modified to actual data structures
	Items:
		- Banana- $50
		- Apple- $100
	Log Entries:
		- Customer 1 purchased 2 bananas and 1 apple; he used 100 rewards points
		- Customer 2 purchased 1 banana and 1 apple; she used 0 rewards points
		- Customer 1 purchased 1 banana; he used 0 rewards points

"""  

# Class that represents one item and its corresponding price
class Item:
  def __init__(self, itemId, item_price):
    self.itemId = itemId
    self.item_price = item_price 

# Class that represents the details for one log entry
class Log:
  def __init__(self, customer_id, reward_points_used, items_purchased):
    self.customer_id = customer_id
    self.rewards_points_used = rewards_points_used
    self.items_purchased = items_purchased

# Class that represents a reward system for a store
class RewardsSystem:
  REWARDS_RATIO_BELOW = 18
  REWARDS_RATIO_ABOVE = 17
  REWARDS_CUTOFF = 250
  
  # Function that initializes this system
  def __init__(self):
    self.rewards_points = defaultdict(int)
    self.items_purchased = defaultdict(int)
    self.error_logs = defaultdict(int)
  
  # Function that processes logs for one day
  def process_log(self, log):
    # Dictionary of customers and their amounts spent
    amount_spent = defaultdict(int)

    # Parse each log entry
    for log_entry in log:
      customer_id = log_entry.customer_id
      reward_points_used = log_entry.reward_points_used
      items_purchased = log_entry.items_purchased
      total_spent = 0
      rewards_updated = True

      # If not items are purchased, report an error in the system
      if not items_purchased:
        self.error_logs.update(log_entry)
        continue

      # If no rewards points specified, set to 0
      if not reward_points_used:
        reward_points_used = 0

      # If no customer id, do not update rewards for this customer even after calculating amount spent
      if not customer_id:
        rewards_updated = False

      else:
        # Subtract rewards points used from customer
        self.rewards_points[customer_id] -= reward_points_used

      # Updates the total purchases made by one person in a day
      for item in items_purchased:
        total_spent += item.itemId * item.item_price
        amount_spent[customer_id] = amount_spent.get(customer_id, 0) + total_spent

    # Update items purchased in day
    for purchase in items_purchased:
      self.items_purchased[purchase.itemId] = self.items_purchased.get(purchase.itemId, 0) + 1

    self.update_rewards_end_day(amount_spent)
    return

  # Function that gets how many items were purchased of a specific type for that day
  def get_items_purchased(self, item_id):
    return self.items_purchased[item_id]

  # Function that award reward points back to customers based on how much they spent at the end of the day
  def update_rewards_end_day(self, amount_spent):
    for customer_id in amount_spent:
      # Calculate rewards points based on rewards cutoff
      rewards_constant = 0
      if (amount_spent[customer_id] > RewardsSystem.REWARDS_CUTOFF):
        rewards_constant = RewardsSystem.REWARDS_RATIO_ABOVE
      else:
        rewards_constant = RewardsSystem.REWARDS_RATIO_BELOW
      rewards_points = amount_spent[customer_id] // rewards_constant
      # Update customer rewards points
      self.rewards_points[customer_id] += rewards_points
    return

