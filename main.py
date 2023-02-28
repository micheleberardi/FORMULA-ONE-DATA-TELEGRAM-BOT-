from telethon import TelegramClient, events, Button
from aiohttp import ClientSession
from datetime import datetime
from utils import JsonFile
import asyncio
import sys
import re

TEMP_IMAGE_DRIVER = "monza.png"
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


# Button.text("🗓 Schedule", resize=True)],

# BUTTOM HOME PAGEW

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    welcome_msg = "Hi here is some help: \n\n 🔔 My information: Version: 1.00 August 21 Latest addition: BETA-VERSION \n\n (by Michele Berardi 🐗) \n\n" \
                  "💬 I already have a lot of capabilities: \n\n" \
                  "🏆Standings - Show driver standings for the current season and past seasons \n " \
                  "🏁 Results - Show results for the current season. \n " \
                  "🏟️ Circuit - Show info about circuit.\n " \
                  "👱🏼 Driver - Show info about driver.\n " \
                  "🏎️ Constructor - Show info about constructor.\n " \
                  "🗓 Schedule - Get schedule \n" \
                  "💰F1 car cost  \n" \
                  "📋 Telemetry  \n" \
                  "📻 Team Radio  \n"
    await event.respond(welcome_msg,
                        buttons=[
                            [Button.text("🏆 Standings", resize=True), Button.text("🏁 Result", resize=True),
                             Button.text("🏟️ Circuit", resize=True)],
                            [Button.text("👱🏼 Driver", resize=True), Button.text("🏎️ Constructor", resize=True),
                             Button.text("🗓 Schedule", resize=True)],
                            [Button.text("💰 F1 car cost", resize=True), Button.text("📋 Telemetry", resize=True),
                             Button.text("📻 Team Radio", resize=True)],

                        ]
                        )


@client.on(events.NewMessage(pattern="🏆 Standings"))
async def standing(event):
    print(event)
    await event.respond("Get standings from:",
                        buttons=[
                            [Button.inline("👱🏼 Driver (current)", data="standing"),
                             Button.inline("🏎 Constructor (current)", data="constructor_standing")],
                            [Button.inline("👱🏼 Driver (by year)", data="driver_by_year"),
                             Button.inline("🏎 Constructor (by year)", data="constructor_by_year")],
                        ]
                        )


@client.on(events.NewMessage(pattern="👱🏼 Driver (by year)"))
async def standing_info_select_year(event):
    print(event)
    await event.respond("Get standings from:",
                        buttons=[
                            [Button.inline("📅 2022", data="2022"), Button.inline("📅 2023", data="2023")],
                            [Button.inline("📅 2021", data="2021"), Button.inline("📅 2020", data="2020")],
                            [Button.inline("📅 2019", data="2019"), Button.inline("📅 2018", data="2018")],
                            [Button.inline("📅 2017", data="2017"), Button.inline("📅 2016", data="2016")],
                            [Button.inline("📅 2015", data="2015"), Button.inline("📅 2014", data="2014")],
                        ]
                        )


# @client.on(events.NewMessage(pattern="🏁 Result"))
async def result_session(event: events.CallbackQuery.Event, circuitId_result: int):
    # async def result_session(event):
    await event.respond("Get standings from:",
                        buttons=[
                            [Button.inline("🏁 FP1", data="FP1-" + str(circuitId_result)),
                             Button.inline("🏁 FP2", data="FP2-" + str(circuitId_result))],
                            [Button.inline("🏁 FP3", data="FP3-" + str(circuitId_result)),
                             Button.inline("🏁 Qualifying", data="Q-" + str(circuitId_result))],
                            [Button.inline("🏁 Speed Race", data="S-" + str(circuitId_result)),
                             Button.inline("🏁 RACE", data="R-" + str(circuitId_result))],
                        ]
                        )


@client.on(events.NewMessage(pattern="🏎 Constructor (by year)"))
async def standing_constructor_select_by_year(event):
    print(event)
    await event.respond("Get standings from:",
                        buttons=[
                            [Button.inline("📅 2023", data="constructorId2023")],
                            [Button.inline("📅 2022", data="constructorId2022")],
                            [Button.inline("📅 2021", data="constructorId2021"),
                             Button.inline("📅 2020", data="constructorId2020")],
                            [Button.inline("📅 2019", data="constructorId2019"),
                             Button.inline("📅 2018", data="constructorId2018")],
                            [Button.inline("📅 2017", data="constructorId2017"),
                             Button.inline("📅 2016", data="constructorId2016")],
                            [Button.inline("📅 2015", data="constructorId2015"),
                             Button.inline("📅 2014", data="constructorId2014")],
                        ]
                        )


@client.on(events.NewMessage(pattern="🏎️ Constructor"))
async def constructoronly(event):
    async with cSession.get(f"{Config['api_url']}/constructorresults?year=2023&token={Config['api_token']}") as res:
        json = await res.json()

        countries = {(circuit_['name'], circuit_['constructorId']) for circuit_ in json}
        print(countries)

        buttons = [
            Button.inline(name, f"constructor {constructorId}") for name, constructorId in countries
        ]

        await event.respond("🏎️ Constructor information:", buttons=list(chunks(buttons, 2)))


@client.on(events.NewMessage(pattern="🏟️ Circuit"))
async def circuit(event):
    async with cSession.get(f"{Config['api_url']}/circuits?year=2023&token={Config['api_token']}") as res:
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


@client.on(events.NewMessage(pattern="💰 F1 car cost"))
async def driver(event):
    welcome = "💡 F1 CAR COST: \n\n" \
              "🏎️ Engine: $18.32 million \n" \
              "🏎️ Chasis: $707,000 \n" \
              "🏎️ Gearbox: $354,000 \n" \
              "🏎️ Hydraulics: $170,000 \n" \
              "🏎️ Rear wing: $85,000-$150,000 \n" \
              "🏎️ Front wing/nose cone: $141,500 \n" \
              "🏎️ Floor and bargeboards: $141,000 \n" \
              "🏎️ Brake discs and pads: $78,000 \n" \
              "🏎️ Small components: $51,000 \n" \
              "🏎️ Steering wheel: $50,000 \n" \
              "🏎️ Fuel tank: $31,000 \n" \
              "🏎️ Halo: $17,000 \n" \
              "🏎️ Tires: $3,000 per set \n\n" \
              "💰 TOTAL: $20.62 million \n\n" \
              "*Those costs are simply for the parts themselves, not the development or manpower involved in making the car a reality. Obviously, different cars will have different costs, so the money Mercedes puts into their car wouldn’t be the same as Williams. This is just a basic idea of expenses. Also, those numbers are relative to the previous set of regulations that were in place until 2022. The cars racing in F1 this season may be slightly different. It is crazy to think about how the steering wheel on an F1 car, which includes two dozen critical inputs, costs considerably more than the entire car most people drive to work every day. Just don’t think Formula 1 constructors don’t have to think of cost just like the average Joe who has to pay for servicing every year. Cost caps in the sport have made the minor expenses in building a car all the more important.\n\n💰 The current F1 budget cap is $140 million."
    await event.respond(welcome)


@client.on(events.NewMessage(pattern="🏎 Constructor (current)"))
async def standing_constructor_by_year(event):
    print(event)
    async with cSession.get(f"{Config['api_url']}/constructorresults?year=2022&token={Config['api_token']}") as res:
        json = await res.json(content_type=None)

        # drivers = {(f"{driver_['forename']} {driver_['surname']}", driver_['driverId']) for driver_ in json}
        drivers = [(driver['pos'], f"{driver['name']} {driver['points']} ({driver['nationality']}) {driver['url']}") for
                   driver in json]

        buttons = [
            Button.inline(driver_, f"driver {driver_id}") for driver_, driver_id in drivers
        ]

        await event.respond("Get information about the following Driver:", buttons=list(chunks(buttons, 2)))


@client.on(events.NewMessage(pattern="🏁 Result"))
async def circuit(event):
    # async with cSession.get(f"{Config['api_url']}/results?year=2022&token={Config['api_token']}") as res:
    async with cSession.get(f"{Config['api_url']}/newschedule?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        countries = {(circuit_['Country'], circuit_['RoundNumber']) for circuit_ in json}

        buttons = [
            Button.inline(country, f"circuitId_result {circuit_id}") for country, circuit_id, in countries
        ]
        await event.respond("Get information about the result:", buttons=list(chunks(buttons, 2)))


@client.on(events.NewMessage(pattern="🗓 Schedule"))
async def schedule(event):
    print(event)
    await event.respond("Get Schedule from:",
                        buttons=[
                            [Button.inline("📅 FULL CALENDAR 2023", data="schedule-2023")],
                            [Button.inline("📅 NEXT Bahrain Grand Prix", data="schedule-next-01")],
                        ]
                        )


@client.on(events.NewMessage(pattern="📅 FULL CALENDAR 2023"))
async def schedule_year(event):
    print(event)
    async with cSession.get(f"{Config['api_url']}/races?year=2023&token={Config['api_token']}") as res:
        json = await res.json()

        countries = {(circuit_['Country'], circuit_['RoundNumber']) for circuit_ in json}

        buttons = [
            Button.inline(country, f"schedule {RoundNumber}") for country, RoundNumber in countries
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

        message = f"🏟️ Circuit information for {wanted_circuit['country']}:\n\n"
        message += f"📇 Name: {wanted_circuit['name']}\n"
        message += f"🌎 Location: {wanted_circuit['country']}, {wanted_circuit['location']}\n"
        # message += f"📅 Info: {wanted_circuit['url']}\n"
        # message += f"📏 Length: None\n"
        # message += f"📐 Turns: None\n"
        # message += f"🏟️ Capacity: None\n"
        # await client.send_message(event.chat_id, message, file=TEMP_IMAGE_CIRCUIT, force_document=False, buttons=[Button.url(f"{wanted_circuit['name']} Wiki", wanted_circuit['url'])])
        await client.send_message(event.chat_id, message, force_document=False,
                                  buttons=[Button.url(f"{wanted_circuit['name']} Wiki", wanted_circuit['url'])])
        await event.delete()


async def standing_info(event: events.CallbackQuery.Event):
    print(event.data)
    async with cSession.get(f"{Config['api_url']}/driverstandings?year=2023&token={Config['api_token']}") as res:
        json = await res.json()

        drivers = [(driver['pos'], f"{driver['forename']} {driver['surname']} ({driver['points']})") for driver in json]

        drivers = sorted(drivers, key=lambda x: x[0])

        messages = [f"{data[0]}. {data[1]}" for data in drivers]

        await client.send_message(event.chat_id, "🏆 The 2023 Formula 1 driver standings:\n\n" + "\n".join(messages))
        await event.delete()


async def standing_info_by_year(event: events.CallbackQuery.Event, data: int):
    async with cSession.get(f"{Config['api_url']}/driverstandings?year={data}&token={Config['api_token']}") as res:
        json = await res.json()

        drivers = [(driver['pos'], f"{driver['forename']} {driver['surname']} ({driver['points']})") for driver in json]

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

        await client.send_message(event.chat_id,
                                  "🏆 The 2023 Formula 1 constructor standings:\n\n" + "\n".join(messages))
        await event.delete()


async def standing_constructor_by_year(event: events.CallbackQuery.Event, data: int):
    print(data)
    async with cSession.get(f"{Config['api_url']}/constructorstandings?year={data}&token={Config['api_token']}") as res:
        json = await res.json()

        drivers = [(driver['position'], f"{driver['constructorRef']} {driver['points']} ({driver['nationality']}) ") for driver in
                   json]

        print(drivers)
        drivers = sorted(drivers, key=lambda x: x[0])

        messages = [f"{data[0]}. {data[1]}" for data in drivers]

        await client.send_message(event.chat_id,
                                  f"🏆 The {data} Formula 1 constructor  standings:\n\n" + "\n".join(messages))
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
        message += f"🌎 Nationality: {wanted_driver['nationality']}\n"
        message += f"🗓 Age/DOB: {((now - dob).days) // 365}, {dob.strftime(DOB_OUT_FORMAT)}\n"
        message += f"🔢 Number: {wanted_driver['number']}\n"
        message += f"🌎 nationality:{wanted_driver['nationality']}\n"
        # message += f"🏎️ Team: None\n\n"
        # message += f"🏁 Races: None\n"
        # message += f"🏆 Championships: None\n"
        # message += f"🏅 Wins: None\n"
        # message += f"🏅 Podiums: None\n"
        # message += f"🏅 Poles: None\n"

        # await client.send_message(event.chat_id, message, file=TEMP_IMAGE_DRIVER, force_document=False, buttons=[Button.url(f"{wanted_driver['forename']} {wanted_driver['surname']} Wiki", wanted_driver['url'])])
        await client.send_message(event.chat_id, message, force_document=False, buttons=[
            Button.url(f"{wanted_driver['forename']} {wanted_driver['surname']} Wiki", wanted_driver['url'])])
        await event.delete()


async def constructorRef(event: events.CallbackQuery.Event, circuit_id: int):
    async with cSession.get(f"{Config['api_url']}/constructorresults?year=2022&token={Config['api_token']}") as res:
        json = await res.json()

        wanted_circuit = None
        for circuit in json:
            if circuit['constructorId'] == circuit_id:
                wanted_circuit = circuit

        message = f"🏎️ Constructor information for {wanted_circuit['name']}:\n\n"
        message += f"🌐 Nationality:: {wanted_circuit['nationality']}\n"
        # message += f" Location: {wanted_circuit['country']}, {wanted_circuit['location']}\n"
        message += f"📍 URL : {wanted_circuit['url']}\n"
        # message += f"📏 Length: None\n"
        # message += f"📐 Turns: None\n"
        # message += f"🏟️ Capacity: None\n"
        # await client.send_message(event.chat_id, message, file=TEMP_IMAGE_CIRCUIT, force_document=False, buttons=[Button.url(f"{wanted_circuit['name']} Wiki", wanted_circuit['url'])])
        await client.send_message(event.chat_id, message, force_document=False,
                                  buttons=[Button.url(f"{wanted_circuit['name']} Wiki", wanted_circuit['url'])])
        await event.delete()


async def result_info(event: events.CallbackQuery.Event, circuit_id: int):
    print(circuit_id)
    async with cSession.get(
            f"{Config['api_url']}/newdrivers?year=2022&roundnumber={circuit_id}&token={Config['api_token']}") as res:
        json = await res.json()
        print(json)
        if json[0]['id'] == "NO DATA":
            await client.send_message(event.chat_id,
                                      "❌ No data for this session! If this session only finished recently, please try again in a few minutes")
            await event.delete()
        else:
            data = 2022
            drivers = [(driver['Position'],
                        f"{driver['flag']}{driver['FirstName']} {driver['LastName']} Time  ({driver['Time']}) Point  ({driver['Points']}) GridPosition ({driver['GridPosition']})")
                       for driver in json if driver['RoundNumber'] == circuit_id and driver['Position'] != None]

            drivers = sorted(drivers, key=lambda x: x[0])

            messages = [f"{data[0]}. {data[1]}" for data in drivers]

            await client.send_message(event.chat_id,
                                      f"🏆 The {data} Formula 1 driver result:\n\n" + "\n".join(messages))
            await event.delete()
        # await client.send_message(event.chat_id, message, file=TEMP_IMAGE_DRIVER, force_document=False, buttons=[Button.url(f"{wanted_driver['forename']} {wanted_driver['surname']} Wiki", wanted_driver['url'])])
        # await client.send_message(event.chat_id, message_dict, force_document=False)
        # await event.delete()


async def schedule_final(event: events.CallbackQuery.Event, RoundNumber: int):
    print(RoundNumber)
    async with cSession.get(f"{Config['api_url']}/races?year=2023&token={Config['api_token']}") as res:
        json = await res.json()
        for driver in json:
            if int(driver['RoundNumber']) == RoundNumber:
                wanted_driver = driver
        message = f"🏆 The {wanted_driver['OfficialEventName']}\n\n"
        message += f"⏱️ Full Schedules \n\n"
        message += f"🚦 Event Name : {wanted_driver['EventName']}\n"
        message += f"🚦 Event Date : {wanted_driver['EventDate']} {'UTC'}\n"
        message += f"🚦 Event Format : {wanted_driver['EventFormat']}\n"
        message += f"🚦 Session1 : {wanted_driver['Session1']} {wanted_driver['Session1Date']} {'UTC'}\n"
        message += f"🚦 Session2 : {wanted_driver['Session2']} {wanted_driver['Session2Date']} {'UTC'}\n"
        message += f"🚦 Session3 : {wanted_driver['Session3']} {wanted_driver['Session3Date']} {'UTC'}\n"
        message += f"🚦 Session4 : {wanted_driver['Session4']} {wanted_driver['Session4Date']} {'UTC'}\n"
        message += f"🚦 Session5 : {wanted_driver['Session5']} {wanted_driver['Session5Date']} {'UTC'}\n"

        await client.send_message(event.chat_id, message, force_document=True, buttons=[
            Button.url(f"INFO {wanted_driver['OfficialEventName']}  ", wanted_driver['url'])])
        await client.send_message(event.chat_id, message, force_document=True, buttons=allbuttons)
        await event.delete()


async def schedule_next(event: events.CallbackQuery.Event, RoundNumber: int):
    print(RoundNumber)
    async with cSession.get(f"{Config['api_url']}/races?year=2022&token={Config['api_token']}") as res:
        json = await res.json()
        data = 2022
        for driver in json:
            if int(driver['RoundNumber']) == RoundNumber:
                wanted_driver = driver
        message = f"🏆 The {wanted_driver['OfficialEventName']}\n\n"
        message += f"⏱️ Full Schedules \n\n"
        message += f"🚦 EVENT NAME : {wanted_driver['EventName']}\n"
        message += f"🚦 EVENT DATE : {wanted_driver['EventDate']} {'UTC'}\n"
        message += f"🚦 EVENT FORMAT : {wanted_driver['EventFormat']}\n"
        message += f"🚦 Session1 : {wanted_driver['Session1']} {wanted_driver['Session1Date']} {'UTC'}\n"
        message += f"🚦 Session2 : {wanted_driver['Session2']} {wanted_driver['Session2Date']} {'UTC'}\n"
        message += f"🚦 Session3 : {wanted_driver['Session3']} {wanted_driver['Session3Date']} {'UTC'}\n"
        message += f"🚦 Session4 : {wanted_driver['Session4']} {wanted_driver['Session4Date']} {'UTC'}\n"
        message += f"🚦 Session5 : {wanted_driver['Session5']} {wanted_driver['Session5Date']} {'UTC'}\n\n"
        message += f"Get up to speed with everything you need to know about the 2022 Singapore Grand Prix, which takes place over 61 laps of the 5.063-kilometre Marina Bay Street Circuit on Sunday, October 2\n\n"

        message += f"RESULT AND INFO CLICK BUTTON BELOW\n"
        # await client.send_message(event.chat_id, message, file=TEMP_IMAGE_DRIVER, force_document=False, buttons=[Button.url(f"INFO {wanted_driver['OfficialEventName']}  ", wanted_driver['url'])])
        allbuttons = [Button.inline(wanted_driver['OfficialEventName'], f"circuitId_result {RoundNumber}")], [
            Button.url(f"INFO {wanted_driver['OfficialEventName']}  ", wanted_driver['url'])]

        # await client.send_message(event.chat_id, message, force_document=True, buttons=[Button.url(f"INFO {wanted_driver['OfficialEventName']}  ", wanted_driver['url'])])
        await client.send_message(event.chat_id, message, force_document=True, buttons=allbuttons)
        # await client.send_message(event.chat_id, message, file=TEMP_IMAGE_CIRCUIT, force_document=False, buttons=[Button.url(f"{wanted_circuit['name']} Wiki", wanted_circuit['url'])])

        await event.delete()


@client.on(events.NewMessage(pattern="📋 Telemetry"))
async def circuit(event):
    await event.respond("TELEMETRY DUTCH GP 2022:",
                        buttons=[
                            [Button.inline("TELEMETRY VER-RUS", data="telemetry-1")],
                            [Button.inline("TELEMETRY VER-LEC", data="telemetry-2")],
                            [Button.inline("STRATEGY", data="telemetry-3")],
                            [Button.inline("VER-SPEED-IN-TRACK", data="telemetry-4")]

                        ]
                        )

    # async with cSession.get(f"{Config['api_url']}/results?year=2022&token={Config['api_token']}") as res:
    # async with cSession.get(f"{Config['api_url']}/livecomment?token={Config['api_token']}") as res:
    #    json = await res.json()
    #    list_live = []
    #    for j in json:
    #        print(j)
    #        time = j.get('time')
    #        content = j.get('content')
    #        content = re.sub(r"http\S+", "", content)
    #        content = str(content)
    #        list_live.append(f"🕐{time} \n🏎️{content}")

    #   msg = f"📋 Live Feed\n\n"
    #   msg += "\n\n".join(list_live)

    #  await event.respond(msg)


async def telemetry(event: events.CallbackQuery.Event, telemetry: int):
    print(telemetry)
    if int(telemetry) == 1:
        message = ""
        # message += f"🏎️ Verstappen-Russell\n\n"
        await client.send_message(event.chat_id, message, file="telemetry_1.png", force_document=False)
    elif int(telemetry) == 2:
        message = ""
        # message += f"🏎️ Verstappen-Russell\n\n"
        await client.send_message(event.chat_id, message, file="telemetry_2.png", force_document=False)
    elif int(telemetry) == 3:
        message = ""
        message += f"🏎️ Race Strategy Dutch GP \n 🛞 SOFT RED \n 🛞 MEDIUM YELLOW \n 🛞 HARD WHITE \n 🛞 INTERMEDIATE GREEN \n 🛞 WET BLU"
        await client.send_message(event.chat_id, message, file="telemetry_3.png", force_document=False)
    elif int(telemetry) == 4:
        message = ""
        # message += f"🏎️ Race Strategy Dutch GP \n 🛞 SOFT RED \n 🛞 MEDIUM YELLOW \n 🛞 HARD WHITE \n 🛞 INTERMEDIATE GREEN \n 🛞 WET BLU"
        await client.send_message(event.chat_id, message, file="telemetry_4.png", force_document=False)


@client.on(events.NewMessage(pattern="📻 Team Radio"))
async def teamradio(event):
    print(event)
    await event.respond("Get standings from:",
                        buttons=[
                            [Button.inline("📅 TEAM RADIO LAST GP", data="team-radio-13")],

                        ]
                        )


async def teamradio_final(event: events.CallbackQuery.Event):
    async with cSession.get(f"{Config['api_url']}/team_radio?token={Config['api_token']}") as res:
        json = await res.json()

        message = f"📅 Team Radio\n\n"
        drivers = [[Button.url(f"TEAM RADIO {driver['driver']}  ", driver['full_url'])] for driver in json]

        await client.send_message(event.chat_id, message, buttons=drivers, force_document=False)
        await event.delete()


async def result_race_final(event: events.CallbackQuery.Event, circuit_id: str):
    session_race = circuit_id.split("-")[0]
    round = circuit_id.split("-")[-1]
    year = 2022
    async with cSession.get(
            f"{Config['api_url']}/results?token={Config['api_token']}&year={year}&round={round}") as res:
        json = await res.json(content_type=None)
        print(json)
        try:
            if json[0]['id'] == 0:
                await client.send_message(event.chat_id,
                                      "❌ No data for this session! If this session only finished recently, please try again in a few minutes")
                await event.delete()
            else:

                data = 2022

                drivers = [(session_race['position'], f" {session_race['flag']} Time({session_race['lapTime']}) 🏎({session_race['points']})") for session_race in json]

                # drivers = sorted(drivers, key=lambda x: x[1])

                messages = [f"{data[0]} {data[1]}" for data in drivers]

                await client.send_message(event.chat_id, f"🏆 The Race result:\n\n" + "\n".join(messages))
                await event.delete()
        except:
            await client.send_message(event.chat_id,
                                      "❌ No data for this session! If this session only finished recently, please try again in a few minutes")
            await event.delete()


async def result_session_final(event: events.CallbackQuery.Event, circuit_id: str):
    session_race = circuit_id.split("-")[0]
    event_race = circuit_id.split("-")[-1]
    year = 2022
    print(
        f"{Config['api_url']}/faster_session?token={Config['api_token']}&year={year}&event_race={event_race}&session_race={session_race}")
    async with cSession.get(
            f"{Config['api_url']}/faster_session?token={Config['api_token']}&year={year}&event_race={event_race}&session_race={session_race}") as res:
        json = await res.json(content_type=None)
        if json[0]['id'] == "NO DATA":
            await client.send_message(event.chat_id,
                                      "❌ No data for this session! If this session only finished recently, please try again in a few minutes")
            await event.delete()
        else:

            data = 2022
            drivers = [(session_race['flag'],
                        #f" 🕑Time({session_race['lapTime']}) 🛞Tires({session_race['compound']}) 🏎️({session_race['team']})")
                        f" Time({session_race['lapTime']}) 🏎️({session_race['team']})")
                       for session_race in json]

            # drivers = sorted(drivers, key=lambda x: x[1])

            messages = [f"{data[0]} {data[1]}" for data in drivers]

            await client.send_message(event.chat_id, f"🏆 The {session_race} result:\n\n" + "\n".join(messages))
            await event.delete()


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
        case ["2023"]:
            await standing_info_by_year(event, int(data[0]))
        case ["2022"]:
            await standing_info_by_year(event, int(data[0]))
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
            await result_session(event, int(circuit_id))

        case ["schedule-2023"]:
            await schedule_year(event)

        case ["schedule", RoundNumber]:
            await schedule_final(event, int(RoundNumber))

        case ["schedule-next-16"]:
            RoundNumber = 16
            await schedule_next(event, int(RoundNumber))
        case ["schedule-next-17"]:
            RoundNumber = 17
            await schedule_next(event, int(RoundNumber))

        case ["schedule-next-18"]:
            RoundNumber = 18
            await schedule_next(event, int(RoundNumber))

        case ["schedule-next-19"]:
            RoundNumber = 19
            await schedule_next(event, int(RoundNumber))

        case ["team-radio-13"]:
            await teamradio_final(event)

        #####

        case ["constructor_standing"]:
            await standing_constructor_info(event)

        case ["constructor_by_year"]:
            await standing_constructor_select_by_year(event)

        case ["constructorId2023"]:
            data = 2023
            await standing_constructor_by_year(event, int(data))
        case ["constructorId2022"]:
            data = 2022
            await standing_constructor_by_year(event, int(data))
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
            await standing_constructor_by_year(event, int(data))
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
            await constructorRef(event, int(circuit_id))

        #####
        case ["FP1-1"]:
            data = "FP1-1"
            await result_session_final(event, data)
        case ["FP2-1"]:
            data = "FP2-1"
            await result_session_final(event, data)
        case ["FP3-1"]:
            data = "FP3-1"
            await result_session_final(event, data)
        case ["Q-1"]:
            data = "Q-1"
            await result_session_final(event, data)
        case ["S-1"]:
            data = "S-1"
            await result_session_final(event, data)
        case ["R-1"]:
            data = "R-1"
            await result_race_final(event, data)

        case ["FP1-2"]:
            data = "FP1-2"
            await result_session_final(event, data)
        case ["FP2-2"]:
            data = "FP2-2"
            await result_session_final(event, data)
        case ["FP3-2"]:
            data = "FP3-2"
            await result_session_final(event, data)
        case ["Q-2"]:
            data = "Q-2"
            await result_session_final(event, data)
        case ["S-2"]:
            data = "S-2"
            await result_session_final(event, data)
        case ["R-2"]:
            data = "R-2"
            await result_race_final(event, data)

        case ["FP1-3"]:
            data = "FP1-3"
            await result_session_final(event, data)
        case ["FP2-3"]:
            data = "FP2-3"
            await result_session_final(event, data)
        case ["FP3-3"]:
            data = "FP3-3"
            await result_session_final(event, data)
        case ["Q-3"]:
            data = "Q-3"
            await result_session_final(event, data)
        case ["S-3"]:
            data = "S-3"
            await result_session_final(event, data)
        case ["R-3"]:
            data = "R-3"
            await result_race_final(event, data)

        case ["FP1-4"]:
            data = "FP1-4"
            await result_session_final(event, data)
        case ["FP2-4"]:
            data = "FP2-4"
            await result_session_final(event, data)
        case ["FP3-4"]:
            data = "FP3-4"
            await result_session_final(event, data)
        case ["Q-4"]:
            data = "Q-4"
            await result_session_final(event, data)
        case ["S-4"]:
            data = "S-4"
            await result_session_final(event, data)
        case ["R-4"]:
            data = "R-4"
            await result_race_final(event, data)

        case ["FP1-5"]:
            data = "FP1-5"
            await result_session_final(event, data)
        case ["FP2-5"]:
            data = "FP2-5"
            await result_session_final(event, data)
        case ["FP3-5"]:
            data = "FP3-5"
            await result_session_final(event, data)
        case ["Q-5"]:
            data = "Q-5"
            await result_session_final(event, data)
        case ["S-5"]:
            data = "S-5"
            await result_session_final(event, data)
        case ["R-5"]:
            data = "R-5"
            await result_race_final(event, data)

        case ["FP1-6"]:
            data = "FP1-6"
            await result_session_final(event, data)
        case ["FP2-6"]:
            data = "FP2-6"
            await result_session_final(event, data)
        case ["FP3-6"]:
            data = "FP3-6"
            await result_session_final(event, data)
        case ["Q-6"]:
            data = "Q-6"
            await result_session_final(event, data)
        case ["S-6"]:
            data = "S-6"
            await result_session_final(event, data)
        case ["R-6"]:
            data = "R-6"
            await result_race_final(event, data)

        case ["FP1-7"]:
            data = "FP1-7"
            await result_session_final(event, data)
        case ["FP2-7"]:
            data = "FP2-7"
            await result_session_final(event, data)
        case ["FP3-7"]:
            data = "FP3-7"
            await result_session_final(event, data)
        case ["Q-7"]:
            data = "Q-7"
            await result_session_final(event, data)
        case ["S-7"]:
            data = "S-7"
            await result_session_final(event, data)
        case ["R-7"]:
            data = "R-7"
            await result_race_final(event, data)

        case ["FP1-8"]:
            data = "FP1-8"
            await result_session_final(event, data)
        case ["FP2-8"]:
            data = "FP2-8"
            await result_session_final(event, data)
        case ["FP3-8"]:
            data = "FP3-8"
            await result_session_final(event, data)
        case ["Q-8"]:
            data = "Q-8"
            await result_session_final(event, data)
        case ["S-8"]:
            data = "S-8"
            await result_session_final(event, data)
        case ["R-8"]:
            data = "R-8"
            await result_race_final(event, data)

        case ["FP1-9"]:
            data = "FP1-9"
            await result_session_final(event, data)
        case ["FP2-9"]:
            data = "FP2-9"
            await result_session_final(event, data)
        case ["FP3-9"]:
            data = "FP3-9"
            await result_session_final(event, data)
        case ["Q-9"]:
            data = "Q-9"
            await result_session_final(event, data)
        case ["S-9"]:
            data = "S-9"
            await result_session_final(event, data)
        case ["R-9"]:
            data = "R-9"
            await result_race_final(event, data)

        case ["FP1-10"]:
            data = "FP1-10"
            await result_session_final(event, data)
        case ["FP2-10"]:
            data = "FP2-10"
            await result_session_final(event, data)
        case ["FP3-10"]:
            data = "FP3-10"
            await result_session_final(event, data)
        case ["Q-10"]:
            data = "Q-10"
            await result_session_final(event, data)
        case ["S-10"]:
            data = "S-10"
            await result_session_final(event, data)
        case ["R-10"]:
            data = "R-10"
            await result_race_final(event, data)

        case ["FP1-11"]:
            data = "FP1-11"
            await result_session_final(event, data)
        case ["FP2-11"]:
            data = "FP2-11"
            await result_session_final(event, data)
        case ["FP3-11"]:
            data = "FP3-11"
            await result_session_final(event, data)
        case ["Q-11"]:
            data = "Q-11"
            await result_session_final(event, data)
        case ["S-11"]:
            data = "S-11"
            await result_session_final(event, data)
        case ["R-11"]:
            data = "R-11"
            await result_race_final(event, data)

        case ["FP1-12"]:
            data = "FP1-12"
            await result_session_final(event, data)
        case ["FP2-12"]:
            data = "FP2-12"
            await result_session_final(event, data)
        case ["FP3-12"]:
            data = "FP3-12"
            await result_session_final(event, data)
        case ["Q-12"]:
            data = "Q-12"
            await result_session_final(event, data)
        case ["S-12"]:
            data = "S-12"
            await result_session_final(event, data)
        case ["R-12"]:
            data = "R-12"
            await result_race_final(event, data)

        case ["FP1-13"]:
            data = "FP1-13"
            await result_session_final(event, data)
        case ["FP2-13"]:
            data = "FP2-13"
            await result_session_final(event, data)
        case ["FP3-13"]:
            data = "FP3-13"
            await result_session_final(event, data)
        case ["Q-13"]:
            data = "Q-13"
            await result_session_final(event, data)
        case ["S-13"]:
            data = "S-13"
            await result_session_final(event, data)
        case ["R-13"]:
            data = "R-13"
            await result_race_final(event, data)

        case ["FP1-14"]:
            data = "FP1-14"
            await result_session_final(event, data)
        case ["FP2-14"]:
            data = "FP2-14"
            await result_session_final(event, data)
        case ["FP3-14"]:
            data = "FP3-14"
            await result_session_final(event, data)
        case ["Q-14"]:
            data = "Q-14"
            await result_session_final(event, data)
        case ["S-14"]:
            data = "S-14"
            await result_session_final(event, data)
        case ["R-14"]:
            data = "R-14"
            await result_race_final(event, data)

        case ["FP1-15"]:
            data = "FP1-15"
            await result_session_final(event, data)
        case ["FP2-15"]:
            data = "FP2-15"
            await result_session_final(event, data)
        case ["FP3-15"]:
            data = "FP3-15"
            await result_session_final(event, data)
        case ["Q-15"]:
            data = "Q-15"
            await result_session_final(event, data)
        case ["S-15"]:
            data = "S-15"
            await result_session_final(event, data)
        case ["R-15"]:
            data = "R-15"
            await result_race_final(event, data)
        case ["FP1-16"]:
            data = "FP1-16"
            await result_session_final(event, data)
        case ["FP2-16"]:
            data = "FP2-16"
            await result_session_final(event, data)
        case ["FP3-16"]:
            data = "FP3-16"
            await result_session_final(event, data)
        case ["Q-16"]:
            data = "Q-16"
            await result_session_final(event, data)
        case ["S-16"]:
            data = "S-16"
            await result_session_final(event, data)
        case ["R-16"]:
            data = "R-16"
            await result_race_final(event, data)

        case ["FP1-17"]:
            data = "FP1-17"
            await result_session_final(event, data)
        case ["FP2-17"]:
            data = "FP2-17"
            await result_session_final(event, data)
        case ["FP3-17"]:
            data = "FP3-17"
            await result_session_final(event, data)
        case ["Q-17"]:
            data = "Q-17"
            await result_session_final(event, data)
        case ["S-17"]:
            data = "S-17"
            await result_session_final(event, data)
        case ["R-17"]:
            data = "R-17"
            await result_race_final(event, data)

        case ["FP1-18"]:
            data = "FP1-18"
            await result_session_final(event, data)
        case ["FP2-18"]:
            data = "FP2-18"
            await result_session_final(event, data)
        case ["FP3-18"]:
            data = "FP3-18"
            await result_session_final(event, data)
        case ["Q-18"]:
            data = "Q-18"
            await result_session_final(event, data)
        case ["S-18"]:
            data = "S-18"
            await result_session_final(event, data)
        case ["R-18"]:
            data = "R-18"
            await result_race_final(event, data)

        case ["FP1-19"]:
            data = "FP1-19"
            await result_session_final(event, data)
        case ["FP2-19"]:
            data = "FP2-19"
            await result_session_final(event, data)
        case ["FP3-19"]:
            data = "FP3-19"
            await result_session_final(event, data)
        case ["Q-19"]:
            data = "Q-19"
            await result_session_final(event, data)
        case ["S-19"]:
            data = "S-19"
            await result_session_final(event, data)
        case ["R-19"]:
            data = "R-19"
            await result_race_final(event, data)

        case ["FP1-20"]:
            data = "FP1-20"
            await result_session_final(event, data)
        case ["FP2-20"]:
            data = "FP2-20"
            await result_session_final(event, data)
        case ["FP3-20"]:
            data = "FP3-20"
            await result_session_final(event, data)
        case ["Q-20"]:
            data = "Q-20"
            await result_session_final(event, data)
        case ["S-20"]:
            data = "S-20"
            await result_session_final(event, data)
        case ["R-20"]:
            data = "R-20"
            await result_race_final(event, data)

        case ["FP1-21"]:
            data = "FP1-21"
            await result_session_final(event, data)
        case ["FP2-21"]:
            data = "FP2-21"
            await result_session_final(event, data)
        case ["FP3-21"]:
            data = "FP3-21"
            await result_session_final(event, data)
        case ["Q-21"]:
            data = "Q-21"
            await result_session_final(event, data)
        case ["S-21"]:
            data = "S-21"
            await result_session_final(event, data)
        case ["R-21"]:
            data = "R-21"
            await result_race_final(event, data)

        case ["FP1-22"]:
            data = "FP1-22"
            await result_session_final(event, data)
        case ["FP2-22"]:
            data = "FP2-22"
            await result_session_final(event, data)
        case ["FP3-22"]:
            data = "FP3-22"
            await result_session_final(event, data)
        case ["Q-22"]:
            data = "Q-22"
            await result_session_final(event, data)
        case ["S-22"]:
            data = "S-22"
            await result_session_final(event, data)
        case ["R-22"]:
            data = "R-22"
            await result_race_final(event, data)

        case ["telemetry-1"]:
            data = "1"
            await telemetry(event, data)
        case ["telemetry-2"]:
            data = "2"
            await telemetry(event, data)
        case ["telemetry-3"]:
            data = "3"
            await telemetry(event, data)
        case ["telemetry-4"]:
            data = "4"
            await telemetry(event, data)


async def main():
    global cSession

    cSession = ClientSession()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
client.run_until_disconnected()
