import json

import discord
import requests

client = discord.Client()

parameters = {
    'category': 'finance',
    'goal': 1200,
    'backers': 10,
    'currency': 'dollar'
}
data = {

    "Inputs": {

        "input1":
        {
            "ColumnNames": ["category", "currency", "goal", "state", "backers"],
            "Values": [["value", "value", "0", "value", 0], ["value", "value", "0",  "value", 0], ]
        }, },
    "GlobalParameters": {
    }
}
APIKEY = NONE
with open('credAzure.txt', 'r') as f:
    APIKEY = f.read()
if APIKEY == None:
    print('NOAZUREKEY')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


async def send_all(channel):
    if all(i is not None for i in parameters.values()):
        # Replace this with the API key for the web service
        api_key = APIKEY
        headers = {'Content-Type': 'application/json',
                   'Authorization': ('Bearer ' + api_key)}

        vs = data['Inputs']['input1']['Values'][0]
        vs[0] = parameters['category']
        vs[1] = parameters['currency']
        vs[2] = parameters['goal']
        vs[4] = parameters['backers']
        body = str.encode(json.dumps(data))

        res = requests.post(
            'https://uswestcentral.services.azureml.net/workspaces/1d86a9682ebe402d8db66e6fccf79f1b/services/2065969a6da24069bed61170dfa31151/execute?api-version=2.0&details=true', data=body, headers=headers)
        print(res.text)
        a = json.loads(res.text)
        j = json.loads(res.text)['Results']['output1']['value']['Values']
        await channel.send(f'Project will {j[0][5].replace("successful", "succeed").replace("failed", "fail")} ! \n=> {j[0][6]}')
    else:
        await channel.send(f"Cannot predict because some parameters are not set:{parameters.values()}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('<@!657181413820596225>'):
        m = message.content
        m = m.split()
        if m[1] == 'predict':
            await send_all(message.channel)
            return
        m[1] = m[1].replace(':', '')
        print(m[1], m)
        if not m[1] in parameters.keys():
            await message.channel.send(f"Unknown parameters please chose one of these: {parameters.keys()}")
            return
        if m[1] == 'goal' or m[1] == 'backers':
            m[2] = int(m[2])
        parameters[m[1]] = m[2]

        await message.channel.send('ok')

s = None
with open('cred.txt', 'r') as f:
    s = f.read()
if s is None:
    print('no creds exiting')
    exit(0)

client.run(s)
