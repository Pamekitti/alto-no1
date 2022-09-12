import requests

response = requests.get('https://www.tmd.go.th/province.php?id=37')
print('yo')
print(response.content)