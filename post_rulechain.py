import glob
import requests
import json

URL = 'http://127.0.0.1:8080/api/rulechain'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


def get_rulechain_list():
	path = './rulechains/*'
	file_list = glob.glob(path)
	json_file_list = [file for file in file_list if file.endswith(".json")]
	return json_file_list


def check_authorization():
	url = "http://127.0.0.1:8080/api/auth/login"
	data = {"username":"tenant@thingsboard.org", "password":"tenant"}
	res = requests.post(url, data=json.dumps(data), headers=headers)
	auth_token = res.json()['token']
	headers['X-Authorization'] = 'Bearer '+auth_token


def post_rulechain(rulechain_file):
	print('*' * 50)
	print('FILE : ' + rulechain_file)
	rule_object = {}
	rule_metadata = {}
	id_object = {}

	with open(rulechain_file) as json_file:
		json_data = json.load(json_file)
		rule_object = json_data['ruleChain']
		rule_metadata = json_data['metadata']

	rule_node = rule_metadata['nodes']

	url = 'http://127.0.0.1:8080/api/ruleChain'
	data = rule_object
	res = requests.post(url, data=json.dumps(data), headers=headers)
	if res.status_code == 200:
		id_object = res.json()['id']
		print('RULE CHAIN POST SUCCESS')
	else:
		print(res.status_code + ', RULE CHAIN POST FAILD')

	if len(rule_node) != 0:
		rule_metadata['ruleChainId'] = id_object
		meta_url = 'http://127.0.0.1:8080/api/ruleChain/metadata'
		meta_res = requests.post(meta_url, data=json.dumps(rule_metadata), headers=headers)
		if meta_res.status_code == 200:
			print('RULE METADATA POST SUCCESS')
		else:
			print(meta_res.status.code + 'RULE METADATA POST FAILD')
	print('*' * 50)

def main():
	rulechain_filelist = get_rulechain_list()
	check_authorization()

	for rule_file in rulechain_filelist:
		post_rulechain(rule_file)


if __name__ == "__main__":
	main()
