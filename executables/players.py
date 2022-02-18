import sys
from utils.fut import savePlayers, getPlayers
from utils.util import extract_information

component = 'players'
print(component.upper())

print('####### CHOICE AN OPTION ######')
print('### A. SEND ALL THE DATA    ###')
print('### B. SEND A SPECIFIC PAGE ###')
print('### C. SEND A RANGE         ###')

option = input("Enter your value: ")

initial = 1
if option == 'A':
    totalPages = 908
elif option == 'B':
    totalPages = input("Enter the page number: ")
    initial = totalPages 
elif option == 'C':
    initial = input("Enter initial page number: ")
    totalPages = input("Enter final page number: ")
else:
    print("WRONG OPTION")
    exit()
    
initial = int(initial)
totalPages = int(totalPages)
    
players = []
initial -= 1

try:
    response = getPlayers()
    for i in range(initial,totalPages):
        print(i)
        response = getPlayers(i)
        players.extend(response.json()['items'])
except Exception as e:
    message = f'There was an error getting FUT data: {e}'
    print(message)

    sys.exit()

length_players = len(players)
message = f'{length_players} records obtained'
print(message)

num_items = 10000

num_blocks = length_players // num_items + (length_players % num_items > 0)
message = f'{num_blocks} blocks of {num_items} registers to send'
print(message)

i = 0

while len(players) > 0:
    i += 1
    message = f'Starting sending process number {i} of {num_blocks}'
    print(message)

    block = players[:num_items]

    data = []

    for player in players:
        name = player['commonName'] if player['commonName'] else '{} {}'.format(player['firstName'], player['lastName'])
        if not any(d['name'] == name for d in data):
            data.append({
                'name': player['commonName'] if player['commonName'] else '{} {}'.format(player['firstName'], player['lastName']),
                'position': player['position'],
                'nation': player['nation']['name'],
                'team': player['club']['name']
            })

    message = 'Sending records to the database...'
    print(message)
    resp = savePlayers({'data': data})
    data_response = extract_information(resp)
    if data_response[0] == 200:
        status, success, details = data_response
        message = 'Successful sending'
        if not success:
            message = 'Something went wrong'
            print(message)
            print(details)
    else:
        message = 'There was an error sending the information'
    print(message)

    print('Finished process')
    
    del players[:num_items]
    print('Current record block removed from total')

    mensaje = 'Full load...'
    print(mensaje)
