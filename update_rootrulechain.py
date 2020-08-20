import glob
import requests
import json

URL = 'http://127.0.0.1:8080/api/rulechain'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


def check_authorization():
	url = "http://127.0.0.1:8080/api/auth/login"
	data = {"username":"tenant@thingsboard.org", "password":"tenant"}
	res = requests.post(url, data=json.dumps(data), headers=headers)
	auth_token = res.json()['token']
	headers['X-Authorization'] = 'Bearer '+auth_token


def get_rulechain_ids(limit):
	url = 'http://127.0.0.1:8080/api/ruleChains?limit='+limit
	res = requests.get(url, headers=headers)
	rulechains = []
	rulechain_ids = []
	if res.status_code == 200:
		rulechains = res.json()['data']

	for rulechain in rulechains:
		rulechain_id = rulechain['id']['id']
		rulechain_ids.append(rulechain_id)

	return rulechain_ids


def get_rootrulechain_metadata(root_id):
	url = 'http://127.0.0.1:8080/api/ruleChain/' + root_id + '/metadata'
	res = requests.get(url, headers=headers)

	return res.json()


def make_new_rootrulechain_metadata(root_metadata, rulechain_ids):
	print('*' * 50)
	rulechain_connections = root_metadata['ruleChainConnections']
	id_count = 8
	layoutX = 50
	layoutY = 610
	if rulechain_connections != None:
		last = rulechain_connections[-1]
		last_id = last['additionalInfo']['ruleChainNodeId']
		last_num = last_id[-1]
		last_num = int(last_num)
		id_count = last_num+1
		last_layoutY = last['additionalInfo']['layoutY']
		layoutY = last_layoutY+60
	else:
		root_metadata['ruleChainConnections'] = []

	nodeId = 'rule-chain-node-' + str(id_count)
	next_addi_metadata = {'layoutX':layoutX, 'layoutY':layoutY, 'ruleChainNodeId':nodeId}

	for id in rulechain_ids[1:]:
		if next_addi_metadata['layoutX'] > 2200:
			next_addi_metadata['layoutX'] = 50
			next_addi_metadata['layoutY'] += 60
		temp_X = next_addi_metadata['layoutX']
		temp_Y = next_addi_metadata['layoutY']
		temp_addi_metadata = {'layoutX':temp_X, 'layoutY':temp_Y, 'ruleChainNodeId':'rule-chain-node-'+str(id_count)}
		new_metadata = {'fromIndex':0, 'targetRuleChainId':{'entityType':'RULE_CHAIN','id':id}, 'additionalInfo':temp_addi_metadata, 'type':'Success'}
		root_metadata['ruleChainConnections'].append(new_metadata)

		id_count = id_count + 1
		next_addi_metadata['ruleChainNodeId'] = 'rule-chain-node-' + str(id_count)
		next_addi_metadata['layoutX'] += 220
#	print(root_metadata['ruleChainConnections'])
	print('Create new RootRuleChain Metadata')
	print('*' * 50)
	return root_metadata


def post_rootrulechain_metadata(root_metadata):
	print('*' * 50)
	meta_url = 'http://127.0.0.1:8080/api/ruleChain/metadata'
	meta_res = requests.post(meta_url, data=json.dumps(root_metadata), headers=headers)
	if meta_res.status_code == 200:
		print('Root RULE METADATA POST SUCCESS')
	else:
		print(meta_res.status.code + 'Root RULE METADATA POST FAILD')
	print('*' * 50)

def main():
	check_authorization()

	rulechain_ids = get_rulechain_ids('100')
	root_metadata = get_rootrulechain_metadata(rulechain_ids[0])
	new_rootrulechain_metadata = make_new_rootrulechain_metadata(root_metadata, rulechain_ids)
	post_rootrulechain_metadata(new_rootrulechain_metadata)


if __name__ == "__main__":
	main()
