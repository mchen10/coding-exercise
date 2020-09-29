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

class Item:
  def __init__(self, itemId, item_price):
    self.itemId = itemId
    self.item_price = item_price

from collections import defaultdict    

class RewardsSystem:
  REWARDS_RATIO_BELOW = 18 #what for?
  REWARDS_CUTOFF = 250
  ERROR_LOG = [] #(7) missing list of error logs

  def __init__(self):
    self.rewards_points = defaultdict(int)
    self.items_purchased = defaultdict(int)

  def process_log(self, log):
    amount_spent = defaultdict(int)

    for log_entry in log:
      customer_id = log_entry[0]
      customer_reward_points_used = log_entry[1] #(1) naming: customer reward points 
      customer_items_purchased = log_entry[2] #customer purchased items

      if customer_items_purchased == None:
      	self.ERROR_LOG.append(log_entry)
      	continue

      if customer_reward_points_used == None:
      	customer_reward_points_used = 0 # (10) if no reward points -> 0

      # if not customer_id: # if customer_id == None ??? move to relevan section only(2.1)
	  total_spent = 0
	  for item in customer_items_purchased:
	    total_spent += item.item_price # (3) iterate all items and add, ignore id, assuming list contains duplicates and not counts
	    #self.items_purchased[item.itemId] = self.items_purchased.get(item.itemId, 0) + 1 #item.item_price # (9) Should be + 1 
	    #(14)  user helper method instead
	    update_items_purchased(self, item)
	      # Update items sold
	      # for purchase in items_purchased: # (8) No need extra for loop
	        #self.items_purchased[purchase.itemId] = self.items_purchased.get(purchase.itemId, 0) + purchase.item_price

	      # items_purchased = len(items_purchased) == 0 (4) just check if None
	      # if items_purchased: (5) check before 
	      #   raise ValueError('Items purchased were not recorded.') (6) should add to error log not raise

      # else: #(11) remove else need to continue logic
      if cusomter_id != None: # (2.2)

        # Subtract rewards points used from customer
        self.rewards_points[customer_id] -= customer_reward_points_used

        # total_spent = 0 (12.0) extra
        # for item in items_purchased:
        #   total_spent += item.itemId * item.item_price
      
        amount_spent[customer_id] = amount_spent.get(customer_id, 0) + total_spent

        # Update items sold
        # for purchase in items_purchased: (12.1) extra as well
        #   self.items_purchased[purchase.itemId] = self.items_purchased.get(purchase.itemId, 0) + purchase.item_price

        print(self.reward_points)

    # At end of day, award reward points back to customers based on how much they spent (13) can modularize this 
    update_rewards(self, amount_spent)
    # for customer_id in amount_spent:
    #   # Calculate rewards points received
    #   rewards_points = amount_spent[customer_id] // RewardsSystem.REWARDS_RATIO_BELOW
    #   if amount_spent > RewardsSystem.REWARDS_CUTOFF:
    #     rewards_points =  amount_spent[customer_id] // 17 

    #   # Update customer rewards points
    #   self.rewards_points[customer_id] += rewards_points

  # (15) rewrite method, bad naming from get_items_purchased to update_items_purchased, bad logic
  def update_items_purchased(self, item_id):
  	self.items_purchased[item.itemId] = self.items_purchased.get(item.itemId, 0) + 1
    # return self.items_purchased[item_id]

  def update_rewards(self, amount_spent):
  	for customer_id in amount_spent:
      # Calculate rewards points received
      rewards_points = amount_spent[customer_id] // RewardsSystem.REWARDS_RATIO_BELOW
      if amount_spent > RewardsSystem.REWARDS_CUTOFF:
        rewards_points =  amount_spent[customer_id] // 17 

      # Update customer rewards points
      self.rewards_points[customer_id] += rewards_points
