import requests

# Alert System
# h = requests.post("http://127.0.0.1:8000/alert/", data={'latitude':'12','longitude':'12','radius':'30'})
# print(h.text)

# Get A Particular Object
# h = requests.post("http://127.0.0.1:8000/get_object/", data={'reference_id':'31b7d08ef1cf11eb9f4e683e261a1863'})
# print(h.text)

# Get All Objects
# h = requests.post("http://127.0.0.1:8000/get_all_object/")
# with open('text.json', 'w', encoding='utf-8') as f:
#     f.write(h.text)
#     f.close()
# print(h.text)