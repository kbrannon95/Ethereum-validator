import pandas as pd
import numpy as np
import requests

def get_val_earnings(eth_api_key, validator_ids):

	#initialize dictionary to store validator id and earnings
	validator_earnings = {}

	#loop through each validator and fetch earnings to date
	for val_id in validator_ids:

		#create request string
		request_string = 'https://beaconcha.in/api/v1/validator/' + val_id + '?apikey=' + eth_api_key

		#make API call
		r = requests.get(request_string)

		#extract data from request
		val_data = r.json()

		#calculate the lifetime earnings in ETH
		val_earn = val_data['data']['balance']/1000000000 - 32

		#append earnings
		validator_earnings[val_id] = val_earn

	return validator_earnings

def get_pool_operator_earnings (earnings_to_date, fee_percentage = 0.1):

	#sum the earnings of each validator and multiply by the stake pool operator fee
	pool_earnings = sum(earnings_to_date.values()) * fee_percentage
	return pool_earnings

def get_staker_balance(stakers_list, ownership_dict, val_earnings):

	#initialize empty dictionary for ETH balances of stakers
	eth_balance = {}

	#for each staker in stakers_list, search ownership_dict to find the stakers initial contribution for each active validator
	for staker in stakers_list:

		#initialize total ETH to zero
		total_eth = 0

		#for each validator check and see if staker has invested ETH, if so increase total_eth by ETH amount
		for validator in ownership_dict:

			#check if staker is investor in validator
			if staker in ownership_dict[validator]:

				#retrieve amount of ETH initially staked
				initial_stake = ownership_dict[validator][staker]

				#convert stake to percentage
				stake_percentage = initial_stake/32

						#calculate earnings in ETH
				earnings_share = stake_percentage * val_earnings[validator] * 0.9

				#calculate total ETH balance
				val_balance = earnings_share + initial_stake

				#add ETH balance from this validator to running total
				total_eth = total_eth + val_balance

		#store ETH balance for each staker in dictionary
		eth_balance[staker] = total_eth

	return eth_balance

def get_usd_balance(eth_balance):

	#request binance API for current price of ETH/USD
	price_request_string = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
	r = requests.get(price_request_string)
	data = r.json()
	eth_price = float(data['price'])

	#multiply staker ETH holdings by current price
	usd_balance = {}
	for staker in eth_balance:
		usd = eth_balance[staker] * eth_price
		usd_balance[staker] = usd
	return usd_balance
