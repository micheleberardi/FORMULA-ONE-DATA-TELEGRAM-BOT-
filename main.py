from telethon import TelegramClient, events, Button
from aiohttp import ClientSession
from datetime import datetime
from utils import JsonFile
import asyncio
import sys

TEMP_IMAGE_DRIVER = "driver_temp.jpg"
TEMP_IMAGE_CIRCUIT = "circuit_temp.jpg"
DOB_IN_FORMAT = "%Y-%m-%d"
DOB_OUT_FORMAT = "%d %B %Y"

DEFAULT_CONFIG = {
    "api_id": "",
    "api_hash": "",
    "bot_token": "",
    "api_url": "",
    "api_token": ""
}

Config = JsonFile("Config.json", DEFAULT_CONFIG)
print(Config)
client = TelegramClient('bot', int(Config['api_id']), Config['api_hash']).start(bot_token=Config['bot_token'])
cSession: ClientSession = None

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond("Start message", 
            buttons=[
                [Button.text("🏆 Standings", resize=True),Button.text("🏁 Result", resize=True),Button.text("🗓 Schedule", resize=True)],
                [Button.text("👱🏼 Driver", resize=True),Button.text("🏎️ Constructor", resize=True),Button.text("🏟️ Circuit", resize=True)],


            ]
        )

@client.on(events.NewMessage(pattern="🏆 Standings"))
async def standing(event):
    print(event)
    await event.respond("Get standings from:", 
            buttons=[
                [Button.inline("👱🏼 Driver (current)", data="standing"), Button.inline("🏎 Constructor (current)", data="constructor_standing")],
                [Button.inline("👱🏼 Driver (by year)", data="driver_by_year"), Button.inline("🏎 Constructor (by year)", data="constructor_by_year")],
            ]
        )



@client.on(events.NewMessage(pattern="👱🏼 Driver (by year)"))
async def standing_info_select_year(event):
    print(event)
    await event.respond("Get standings from:",
            buttons=[
                [Button.inline("📅 2021", data="2021"), Button.inline("📅 2020", data="2020")],
                [Button.inline("📅 2019", data="2019"), Button.inline("📅 2018", data="2018")],
                [Button.inline("📅 2017", data="2017"), Button.inline("📅 2016", data="2016")],
                [Button.inline("📅 2015", data="2015"), Button.inline("📅 2014", data="2014")],
            ]
        )

@client.on(events.NewMessage(pattern="🏎 Constructor (by year)"))
async def standing_constructor_select_by_year(event):
    print(event)
    await event.respond("Get standings from:",
            buttons=[
                [Button.inline("📅 2021", data="constructorId2021"), Button.inline("📅 2020", data="constructorId2020")],
                [Button.inline("📅 2019", data="constructorId2019"), Button.inline("📅 2018", data="constructorId2018")],
                [Button.inline("📅 2017", data="constructorId2017"), Button.inline("📅 2016", data="constructorId2016")],
                [Button.inline("📅 2015", data="constructorId2015"), Button.inline("📅 2014", data="constructorId2014")],
            ]
        )

@client.on(events.NewMessage(pattern="🏎️ Constructor"))
async def constructoronly(event):
    async with cSession.get(f"{Config['api_url']}/constructorresults?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        countries = {(circuit_['name'], circuit_['constructorId']) for circuit_ in json}
        print(countries)

        buttons = [
            Button.inline(name, f"constructor {constructorId}") for name, constructorId in countries
        ]

        await event.respond("🏎️ Constructor information:", buttons=list(chunks(buttons, 2)))

@client.on(events.NewMessage(pattern="🏟️ Circuit"))
async def circuit(event):
    async with cSession.get(f"{Config['api_url']}/circuits?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        countries = {(circuit_['country'], circuit_['circuitId']) for circuit_ in json}

        buttons = [
            Button.inline(country, f"circuit {circuit_id}") for country, circuit_id in countries
        ]

        await event.respond("Get information about the following circuit:", buttons=list(chunks(buttons, 2)))

@client.on(events.NewMessage(pattern="👱🏼 Driver"))
async def driver(event):
    print(event)
    async with cSession.get(f"{Config['api_url']}/driversinfo?year=2022&token={Config['api_token']}") as res:
        json = await res.json(content_type=None)

        drivers = {(f"{driver_['forename']} {driver_['surname']}", driver_['driverId']) for driver_ in json}

        buttons = [
            Button.inline(driver_, f"driver {driver_id}") for driver_, driver_id in drivers
        ]

        await event.respond("Get information about the following Driver:", buttons=list(chunks(buttons, 2)))

@client.on(events.NewMessage(pattern="🏎 Constructor (current)"))
async def standing_constructor_by_year(event):
    print(event)
    async with cSession.get(f"{Config['api_url']}/constructorresults?year=2022&token={Config['api_token']}") as res:
        json = await res.json(content_type=None)

        #drivers = {(f"{driver_['forename']} {driver_['surname']}", driver_['driverId']) for driver_ in json}
        drivers = [(driver['pos'], f"{driver['name']} {driver['points']} ({driver['nationality']}) {driver['url']}") for driver in json]

        buttons = [
            Button.inline(driver_, f"driver {driver_id}") for driver_, driver_id in drivers
        ]

        await event.respond("Get information about the following Driver:", buttons=list(chunks(buttons, 2)))

@client.on(events.NewMessage(pattern="🏁 Result"))
async def circuit(event):
    async with cSession.get(f"{Config['api_url']}/results?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        countries = {(circuit_['name'], circuit_['circuitId']) for circuit_ in json}

        buttons = [
            Button.inline(country, f"circuitId_result {circuit_id}") for country, circuit_id in countries
        ]

        await event.respond("Get information about the following circuit:", buttons=list(chunks(buttons, 2)))

@client.on(events.NewMessage(pattern="🗓 Schedule"))
async def schedule(event):
    print(event)
    async with cSession.get(f"{Config['api_url']}/results?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        countries = {(circuit_['name'], circuit_['circuitId']) for circuit_ in json}

        buttons = [
            Button.inline(country, f"schedule {circuit_id}") for country, circuit_id in countries
        ]

        await event.respond("Get schedule from:", buttons=list(chunks(buttons, 2)))

#####

async def circuit_info(event: events.CallbackQuery.Event, circuit_id: int):
    async with cSession.get(f"{Config['api_url']}/circuits?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        wanted_circuit = None
        for circuit in json:
            if circuit['circuitId'] == circuit_id:
                wanted_circuit = circuit

        message  = f"🏟️ Circuit information for {wanted_circuit['country']}:\n\n"
        message += f"📇 Name: {wanted_circuit['name']}\n"
        message += f" Location: {wanted_circuit['country']}, {wanted_circuit['location']}\n"
        #message += f"📅 Info: {wanted_circuit['url']}\n"
        #message += f"📏 Length: None\n"
        #message += f"📐 Turns: None\n"
        #message += f"🏟️ Capacity: None\n"
        #await client.send_message(event.chat_id, message, file=TEMP_IMAGE_CIRCUIT, force_document=False, buttons=[Button.url(f"{wanted_circuit['name']} Wiki", wanted_circuit['url'])])
        await client.send_message(event.chat_id, message, force_document=False, buttons=[Button.url(f"{wanted_circuit['name']} Wiki", wanted_circuit['url'])])
        await event.delete()

async def standing_info(event: events.CallbackQuery.Event):
    print(event.data)
    async with cSession.get(f"{Config['api_url']}/driverstandings?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        drivers = [(driver['pos'], f"{driver['forename']} {driver['surname']} ({driver['points']})") for driver in json]

        drivers = sorted(drivers, key=lambda x: x[0])

        messages = [f"{data[0]}. {data[1]}" for data in drivers]

        await client.send_message(event.chat_id, "🏆 The 2021 Formula 1 driver standings:\n\n" + "\n".join(messages))
        await event.delete()

async def standing_info_by_year(event: events.CallbackQuery.Event, data: int):
    print(type(data))
    async with cSession.get(f"{Config['api_url']}/driverstandings?year={data}&token={Config['api_token']}") as res:
        json = await res.json()

        drivers = [(driver['pos'], f"{driver['forename']} {driver['surname']} ({driver['points']})") for driver in json]

        print(drivers)
        drivers = sorted(drivers, key=lambda x: x[0])

        messages = [f"{data[0]}. {data[1]}" for data in drivers]

        await client.send_message(event.chat_id, f"🏆 The {data} Formula 1 driver standings:\n\n" + "\n".join(messages))
        await event.delete()

async def standing_constructor_info(event: events.CallbackQuery.Event):
    print(event.data)
    async with cSession.get(f"{Config['api_url']}/constructorresults?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        drivers = [(driver['pos'], f"{driver['name']} {driver['points']} ({driver['nationality']})") for driver in json]

        drivers = sorted(drivers, key=lambda x: x[0])

        messages = [f"{data[0]}. {data[1]}" for data in drivers]

        await client.send_message(event.chat_id, "🏆 The 2021 Formula 1 constructor standings:\n\n" + "\n".join(messages))
        await event.delete()


async def standing_constructor_by_year(event: events.CallbackQuery.Event, data: int):
    print(data)
    async with cSession.get(f"{Config['api_url']}/constructorresults?year={data}&token={Config['api_token']}") as res:
        json = await res.json()

        drivers = [(driver['pos'], f"{driver['name']} {driver['points']} ({driver['nationality']}) ") for driver in json]

        print(drivers)
        drivers = sorted(drivers, key=lambda x: x[0])

        messages = [f"{data[0]}. {data[1]}" for data in drivers]

        await client.send_message(event.chat_id, f"🏆 The {data} Formula 1 constructor  standings:\n\n" + "\n".join(messages))
        await event.delete()

async def driver_info(event: events.CallbackQuery.Event, driver_id: int):
    async with cSession.get(f"{Config['api_url']}/driversinfo?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        wanted_driver = None
        for driver in json:
            if driver['driverId'] == driver_id:
                wanted_driver = driver

        now = datetime.now()
        dob = datetime.strptime(wanted_driver['dob'], DOB_IN_FORMAT)

        message = f"👱🏼 Driver information for {wanted_driver['code']}:\n\n"
        message += f"📇 Name: {wanted_driver['forename']} {wanted_driver['surname']}\n"
        message += f"Nationality: {wanted_driver['nationality']}\n"
        message += f"🗓 Age/DOB: {((now - dob).days) // 365}, {dob.strftime(DOB_OUT_FORMAT)}\n"
        message += f"🔢 Number: {wanted_driver['number']}\n"
        message += f"🏎️ Team: None\n\n"
        message += f"🏁 Races: None\n"
        message += f"🏆 Championships: None\n"
        message += f"🏅 Wins: None\n"
        message += f"🏅 Podiums: None\n"
        message += f"🏅 Poles: None\n"

        #await client.send_message(event.chat_id, message, file=TEMP_IMAGE_DRIVER, force_document=False, buttons=[Button.url(f"{wanted_driver['forename']} {wanted_driver['surname']} Wiki", wanted_driver['url'])])
        await client.send_message(event.chat_id, message, force_document=False, buttons=[Button.url(f"{wanted_driver['forename']} {wanted_driver['surname']} Wiki", wanted_driver['url'])])
        await event.delete()


async def constructorRef(event: events.CallbackQuery.Event, circuit_id: int):
    async with cSession.get(f"{Config['api_url']}/constructorresults?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        wanted_circuit = None
        for circuit in json:
            if circuit['constructorId'] == circuit_id:
                wanted_circuit = circuit

        message  = f"🏎️ Constructor information for {wanted_circuit['name']}:\n\n"
        message += f"🇨🇭 Nationality:: {wanted_circuit['nationality']}\n"
        #message += f" Location: {wanted_circuit['country']}, {wanted_circuit['location']}\n"
        message += f"📍 URL : {wanted_circuit['url']}\n"
        #message += f"📏 Length: None\n"
        #message += f"📐 Turns: None\n"
        #message += f"🏟️ Capacity: None\n"
        #await client.send_message(event.chat_id, message, file=TEMP_IMAGE_CIRCUIT, force_document=False, buttons=[Button.url(f"{wanted_circuit['name']} Wiki", wanted_circuit['url'])])
        await client.send_message(event.chat_id, message, force_document=False, buttons=[Button.url(f"{wanted_circuit['name']} Wiki", wanted_circuit['url'])])
        await event.delete()


async def result_info(event: events.CallbackQuery.Event, circuit_id: int):
    #print(circuit_id)
    async with cSession.get(f"{Config['api_url']}/results?year=2022&token={Config['api_token']}") as res:
        json = await res.json()
        data = 2022
        drivers = [(driver['position'], f"{driver['forename']} {driver['surname']} Time : ({driver['time']}) Point : ({driver['points']})") for driver in json if driver['circuitId'] == circuit_id and driver['position'] != None]
        drivers = sorted(drivers, key=lambda x: x[0])
        messages = [f"{data[0]}. {data[1]}" for data in drivers]
        await client.send_message(event.chat_id,f"🏆 The {data} Formula 1 driver standings:\n\n" + "\n".join(messages))
        await event.delete()
        #await client.send_message(event.chat_id, message, file=TEMP_IMAGE_DRIVER, force_document=False, buttons=[Button.url(f"{wanted_driver['forename']} {wanted_driver['surname']} Wiki", wanted_driver['url'])])
        #await client.send_message(event.chat_id, message_dict, force_document=False)
        #await event.delete()


async def schedule(event: events.CallbackQuery.Event, circuit_id: int):
    print(circuit_id)
    async with cSession.get(f"{Config['api_url']}/results?year=2022&token={Config['api_token']}") as res:
        json = await res.json()
        data = 2022
        fp2_date = "0"
        for driver in json:
            if driver['circuitId'] == circuit_id:
                wanted_driver = driver
        message = f"🏆 The {wanted_driver['name']} Grand Prix full schedules:\n\n"
        message += f"🚦 FP1 : {wanted_driver['fp1_date']}\n"
        message += f"🚦 FP2 : {wanted_driver['fp2_date']}\n"
        #message += f"🚦 info : {wanted_driver['url']}\n"
        await client.send_message(event.chat_id, message, force_document=True, buttons=[
            Button.url(f"INFO {wanted_driver['name']}  ", wanted_driver['url'])])
        await event.delete()



        #drivers = [(f"🚦 Practice 1: {driver['fp1_date']} \n🚦 Practice 2: {driver['fp2_date']}\n🚦 Practice 2: ({driver['fp3_date']}) \n🚦 Practice 3: ({driver['quali_date']})") for driver in json if driver['circuitId'] == circuit_id ]
        #drivers = sorted(drivers, key=lambda x: x[0])
        #messages = [f"{data[0]}. {data[1]}" for data in drivers]
        #await client.send_message(event.chat_id,f"🏆 The {data}  Grand Prix full schedules:\n\n" + "\n".join(messages))
        #await event.delete()

@client.on(events.CallbackQuery())
async def button_handler(event):
    data = event.data.decode("utf-8").split(" ")
    print("data:", data)
    print(type(data))
    print(event)
    match data:
        case ["standing"]:
            await standing_info(event)

        case ["driver", driver_id]:
            await driver_info(event, int(driver_id))

        case ["circuit", circuit_id]:
            await circuit_info(event, int(circuit_id))

        case ["2021"]:
            await standing_info_by_year(event, int(data[0]))
        case ["2020"]:
            await standing_info_by_year(event, int(data[0]))
        case ["2019"]:
            await standing_info_by_year(event, int(data[0]))
        case ["2018"]:
            await standing_info_by_year(event, int(data[0]))
        case ["2017"]:
            await standing_info_by_year(event, int(data[0]))
        case ["2016"]:
            await standing_info_by_year(event, int(data[0]))
        case ["2015"]:
            await standing_info_by_year(event, int(data[0]))
        case ["2014"]:
            await standing_info_by_year(event, int(data[0]))
        case ['driver_by_year']:
            await standing_info_select_year(event)
        ######
        case ["circuitId_result", circuit_id]:
            await result_info(event, int(circuit_id))

        case ["schedule", circuit_id]:
            await schedule(event, int(circuit_id))

        #####

        case ["constructor_standing"]:
            await standing_constructor_info(event)

        case["constructor_by_year"]:
            await standing_constructor_select_by_year(event)

        case ["constructorId2021"]:
            data = 2021
            await standing_constructor_by_year(event, int(data))
        case ["constructorId2020"]:
            data = 2020
            await standing_constructor_by_year(event, int(data))
        case ["constructorId2019"]:
            data = 2019
            await standing_constructor_by_year(event, int(data))
        case ["constructorId2018"]:
            data = 2018
            await standing_constructor_by_year(event, int(data))
        case ["constructorId2017"]:
            data = 2017
            await standing_constructor_by_year(event,int(data))
        case ["constructorId2016"]:

            await standing_constructor_by_year(event, int(data))
        case ["constructorId2015"]:
            data = 2015
            await standing_constructor_by_year(event, int(data))
        case ["constructorId2014"]:
            data = 2014
            await standing_constructor_by_year(event, int(data))

        ###
        case ["constructor", circuit_id]:
            print("cazzo")
            await constructorRef(event, int(circuit_id))


async def main():
    global cSession

    cSession = ClientSession()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
client.run_until_disconnected()
