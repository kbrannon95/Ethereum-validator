from ethfunctions import get_val_earnings, get_pool_operator_earnings, get_staker_balance, get_usd_balance

def main():

	eth_api_key = 'NmVSM2x3S3BUNFNsSnhvOFgxdFN1'
	validator_ids = ['310494', '356165', '356169','410931']
	stakers_list = ['Mr. Lites','Dr. Hutchinson','Matt','Nader','Kairn']
	ownership = {validator_ids[0]:{'Mr. Lites':32},\
		validator_ids[1]:{'Mr. Lites':32},\
		validator_ids[2]:{'Dr. Hutchinson':32},\
		validator_ids[3]:{'Mr. Lites':10,'Matt':14,'Nader':4,'Kairn':4}}

	#calculate current validator earnings to date
	current_validator_earnings = get_val_earnings(eth_api_key, validator_ids)
	print(current_validator_earnings)

	#calculate stake pool operator earnings (10%)
	pool_operator_earnings = get_pool_operator_earnings(current_validator_earnings)
	print(pool_operator_earnings)

	#calculate active balance of all stakers in ETH
	staker_balance_ETH = get_staker_balance(stakers_list, ownership, current_validator_earnings)
	print(staker_balance_ETH)

	#calculate active balance of all stakers in USD
	staker_balance_USD = get_usd_balance(staker_balance_ETH)
	print(staker_balance_USD)

if __name__ == "__main__":
	main()
