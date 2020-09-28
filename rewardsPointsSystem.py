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

from collections import defaultdict

# This class represents an item in catalog.
class Item:
  def __init__(self, id, price):
    self.id = id
    self.price = price

# This class represents a log of a transaction.
class Log:
  def __init__(self, customer_id, rewards_points_used, items_purchased):
    self.customer_id = customer_id
    self.rewards_points_used = rewards_points_used
    self.items_purchased = items_purchased     

# This class represents a store's rewards system. 
class RewardsSystem:
  SPENDING_CUTOFF = 250 # The threshold that determines the amount in dollars equivalent to 1 rewards point.
  ABOVE_CUTOFF_ONSTANT = 17 # The amount in dollars equivalent to 1 rewards point if a customer has spent more than SPENDING_CUTOFF for a particular day.
  BELOW_CUTOFF_CONSTANT = 18 # The amount in dollars equivalent to 1 rewards point if a customer has less than or equal to SPENDING_CUTOFF for a particular day.

  def __init__(self):
    self.customer_rewards = defaultdict(int)

  # This function processes all the logs for a particular day.
  # It returns a tuple containing a mapping between Items to their bought frequencies, a mapping between customers to their respective amounts spent and a list of invalid logs for a particular day.
  # 'daily_logs' is a list of Logs documented for a particular day.
  def process_logs(self, daily_logs):
    item_purchased_count = defaultdict(int)
    customer_amount_spent = defaultdict(int)
    error = []

    for log in daily_logs:

      if log.items_purchased is None:
        error.append(log)
        continue

      customer_id = log.customer_id
      rewards_points_used = log.rewards_points_used if (log.rewards_points_used is not None && log.rewards_points_used > 0) else 0
      items_purchased = log.items_purchased

      total_spent = 0
      for item in items_purchased:
        total_spent += item.price
        item_purchased_count[item.id] += 1

      if customer_id is not None:
        reward_points_used = min(reward_points_used, customer_rewards[customer_id])
        total_spent -= reward_points_used;
        customer_amount_spent[customer_id] += total_spent

        self.customer_rewards[customer_id] -= rewards_points_used

    update_customer_rewards(customer_amount_spent)
    return (item_purchased, customer_amount_spent, error)

  # This function updates the rewards system.
  # 'customer_amount_spent' is a mapping between customers to their respective amounts spent for a particular day.
  def update_customer_rewards(self, customer_amount_spent):
    for customer_id in customer_amount_spent:
      rewards_constant = ABOVE_CUTOFF_ONSTANT if customer_amount_spent[customer_id] > SPENDING_CUTOFF else BELOW_CUTOFF_CONSTANT
      rewards_points =  customer_amount_spent[customer_id] // rewards_constant

      self.customer_rewards[customer_id] += rewards_points


