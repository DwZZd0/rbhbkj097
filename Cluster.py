import asyncio
import re
import telethon
from telethon import TelegramClient, events, errors
import aiosqlite 
from datetime import datetime, timedelta
from telethon.tl.functions.channels import GetParticipantsRequest as GetParticipants
from telethon.tl.types import ChannelParticipantsSearch
import sys
from telethon.tl.types import InputPeerChannel
from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from colorama import init, Fore, Back, Style
init()

async def api():
    while True:
        try:
            game = await aiosqlite.connect('TEST99.db')
            cur = await game.cursor()
            await cur.execute('''CREATE TABLE IF NOT EXISTS api (api_id TEXT, api_hash TEXT)''')
            await cur.execute('SELECT api_id, api_hash FROM api')  # Fetch both values in one query
            row = await cur.fetchone()
            
            if not row:
                api_id = str(input("Введите значение API ID: "))
                api_hash = input("Введите значение API Hash: ")
                
                try:
                    if len(api_id) == 8 and len(api_hash) == 32 and api_hash.isalnum():
                        ins = """
                            INSERT INTO api (api_id, api_hash)
                            VALUES (?, ?);
                        """
                        await cur.execute(ins, (api_id, api_hash))
                        await game.commit()
                        print("API ID и API Hash валидны. Значения сохранены.")
                        return api_id, api_hash
                        
                    else:
                        print("Неверные значения API ID или API Hash. Пожалуйста, проверьте введенные данные.")
                except ValueError:
                    print("Введите корректные значения API ID и API Hash.")
            else:
                return row[0], row[1]  # Return the values from the fetched row
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            await cur.close()
            await game.close()

upt = None  

async def open_database():
    game = await aiosqlite.connect('TEST99.db')
    cur = await game.cursor()
    await cur.execute('''CREATE TABLE IF NOT EXISTS dov (user_id INTEGER PRIMARY KEY, username TEXT)''')
    await cur.execute('''CREATE TABLE IF NOT EXISTS stat (autoins TEXT)''')
    await cur.execute('CREATE TABLE IF NOT EXISTS dovpref (user_id INTEGER PRIMARY KEY, pref TEXT)')
    await cur.execute('''
        CREATE TABLE IF NOT EXISTS zlst (
            user INTEGER PRIMARY KEY,
            res INTEGER,
            data TEXT
        )
    ''')
    return game, cur

async def close_database(game):
    await game.close()

async def get_user_data(cur, user_id):
    await cur.execute(f'SELECT * FROM dov WHERE user_id={user_id}')
    dov_users = await cur.fetchone()
    await cur.execute('SELECT pref FROM dovpref')
    pref_value = await cur.fetchone()
    pref_value = str(pref_value[0]) 
    return dov_users, pref_value
    
    
    
async def msgwait(cls, client):
    try:
        if cls == 'ла':
            sendmsg = await client.send_message(6333102398, 'Биолаб')
            for _ in range(10):
                    await asyncio.sleep(0.3)
                    msg = (await client.get_messages(6333102398, limit=1))[0].text
                    if msg:
                        break
                    else:
                        print("Нет ответа от бота на 'ла'")
            
        if cls == 'ежа':
            sendmsg = await client.send_message(6333102398, 'Биоежа')
            for _ in range(10):
                    await asyncio.sleep(0.3)
                    msg = (await client.get_messages(6333102398, limit=1))[0].text
                    if msg:
                        break
                    else:
                        print("Нет ответа от бота на 'ежа'")
            
        if cls == 'дос':
           sendmsg = await client.send_message(6333102398, 'Биолаб')
           for _ in range(10):
                   await asyncio.sleep(0.3)
                   msg = (await client.get_messages(6333102398, limit=1))[0].text
                   if msg:
                       break
                   else:
                        print("Нет ответа от бота на 'дос'")
           
        if cls == 'хи':
           sendmsg = await client.send_message(6333102398, 'Хил')
           for _ in range(10):
                   await asyncio.sleep(0.3)
                   msg = (await client.get_messages(6333102398, limit=1))
                   if msg:
                       msg = msg[0].text
                       break
                   else:
                        print("Нет ответа от бота на 'хи'")
        return msg
    except Exception as e:
        print(f"Ошибка в msgwait: {e}")
    
async def la(event, user_id, client):
    try:
        sender = event.sender_id
        if sender == user_id:
            editmsg = await event.edit("Ожидание")
            sms = ''
            cls = 'ла'
            msg = await msgwait(cls, client)     
            msg = msg.splitlines()
            for i in msg:
                if "🧪 Патогенов:" in i:
                    s = i.replace("🧪 Патогенов:", "")
                    s = s.split('(')[0].strip()
                    sms += f"🧪 `{s}`\n"
                    
                if "☣️ Био-опыт:" in i:
                    s = i.replace("☣️ Био-опыт: ", "")
                    sms += f"💸 `{s}`\n"
                    
                if "🧬 Био-ресурс:" in i:
                    s = i.replace("🧬 Био-ресурс: ", "")
                    sms += f"💶 `{s}`\n"
                    
                if "🥴 У вас горячка" in i:
                    s = i.split('`')[1].strip() and i.split('ещё')[1].strip()
                    sms += f"💉 {s}\n"
                    
            await client.send_read_acknowledge(6333102398)
            await editmsg.edit(sms, parse_mode='markdown')
            
    except Exception as e:
        print(f"Ошибка в ла: {e}")
        

async def dovla(event, user_id, cur, client):
    try:
        sender = event.sender_id
        dov_users, pref_value = await get_user_data(cur, sender)
        if (dov_users and dov_users[0] == sender):
            editmsg = await event.reply("Ожидание")
            sendmsg = await client.send_message(6333102398, 'Биолаб')
            sms = ''
            cls = 'ла'
            msg = await msgwait(cls, client)     
            msg = msg.splitlines()
            for i in msg:
                if "🧪 Патогенов:" in i:
                    s = i.replace("🧪 Патогенов:", "")
                    s = s.split('(')[0].strip()
                    sms += f"🧪 `{s}`\n"
                    
                if "☣️ Био-опыт:" in i:
                    s = i.replace("☣️ Био-опыт: ", "")
                    sms += f"💸 `{s}`\n"
                    
                if "🧬 Био-ресурс:" in i:
                    s = i.replace("🧬 Био-ресурс: ", "")
                    sms += f"💶 `{s}`\n"
                    
                if "🥴 У вас горячка" in i:
                    s = i.split('`')[1].strip() and i.split('ещё')[1].strip()
                    sms += f"💉 {s}\n"
                    
            await client.send_read_acknowledge(6333102398)
            await editmsg.edit(sms, parse_mode='markdown')
            
    except Exception as e:
        print(f"Ошибка в ла: {e}")        
                
                                
async def ub(event, user_id, client):
    try:
        sender = event.sender_id
        if sender == user_id:
            me = await client.get_me()
            now = datetime.now()
            uptime_delta = now - upt
            hours, remainder = divmod(uptime_delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            ping_message = (
                f"**💠Cluster:**\n    Stable2.5\n"
                f"**🚸Владелец:**\n    [{me.first_name}](tg://openmessage?user_id={me.id})\n\n"
                f"**🕯️Аптайм:**\n    {hours}ч {minutes}м {seconds}с"
            )

            await event.edit(ping_message, parse_mode='markdown')
            
        else:
            pass

    except Exception as e:
        print(f"Ошибка в ping: {e}")
        
async def dovub(event, cur, client):
    try:
        sender = event.sender_id        
        dov_users, pref_value = await get_user_data(cur, sender)
        print(f"{dov_users} and {dov_users[0]}")
        if (dov_users and dov_users[0]) == sender:
            me = await client.get_me()
            now = datetime.now()
            uptime_delta = now - upt
            hours, remainder = divmod(uptime_delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            ping_message = (
                "<pre>"
                "<code>"
                "{\n"
                f"   <b>\"💠 Cluster\":</b> \"Stable2.5\",\n"
                f"   <b>\"🚸 Владелец\":</b> \"{me.first_name}\",\n"
                "}"
                "</code>"
                "</pre>"
                "<pre>"
                "<code>"
                "{\n"
                f"   <b>\"🕯️ Аптайм\" : \"{hours}ч {minutes}м {seconds}с\"</b>\n"
                "}"
                "</code>"
                "</pre>"
            )

            await event.reply(ping_message, parse_mode='html')

        else:
            print("eblan")

    except Exception as e:
        print(f"Ошибка в ping: {e}")        
        

async def doh(event, user_id, client):
    try:
        sender = event.sender_id
            
        if sender == user_id:
            editmsg = await event.edit("Ожидаем")
            cls = 'ежа'
            msg = await msgwait(cls, client)     
            msg = msg.splitlines()
            sms = ""

            for i in msg:
                if "🤒 Итого" in i:
                    s = i.replace('🤒 Итого ', '')
                    s = ''.join(c for c in s if c.isdigit())
                    sms += f"📕 `{s}`\n"
                if '🧬 Общая прибыль:' in i:
                    s = i.replace('🧬 Общая прибыль: ', '')
                    s = ''.join(c for c in s if c.isdigit())
                    sms += f"💶 `{s}`\n"
                    sint = int(s)
                    min = round(sint/1440, 1)
                    sms += f"⏳ `{min}`\n"
                    

            await client.send_read_acknowledge(6333102398)
           

            await editmsg.edit(sms, parse_mode='markdown')
        else:
            pass

    except Exception as e:
        print(f"Ошибка в bioeagle: {e}")


async def dos(event, user_id, cur, client):
    try:
        sender = event.sender_id
        if sender == user_id:
            
            editmsg = await event.edit("Ожидаем")
            cls = 'дос'
            msg = await msgwait(cls, client)     
            msg = msg.splitlines()
            sms = ""
            for i in msg:
                if "🧪 Патогенов:" in i:
                    s = i.replace('🧪 Патогенов: ', '')
                    sms += f"🧪 {s}\n"
                    sms = sms.split('(')[0].strip()
                    sms += "\n"
                if "👨🏻‍🔬 Разработка:" in i:
                    s = i.replace('👨🏻‍🔬 Разработка: ', '')
                    sms += f"👨🏻‍🔬 {s}\n"
                    sms = sms.split('(')[0].strip()
                    sms += "\n"
                if "🦠 Заразность:" in i:
                    s = i.replace('🦠 Заразность: ', '')
                    sms += f"🦠 {s}\n"
                    sms = sms.split('(')[0].strip()
                    sms += "\n"
                if "🛡 Иммунитет:" in i:
                    s = i.replace('🛡 Иммунитет: ', '')
                    sms += f"🛡 {s}\n"
                    sms = sms.split('(')[0].strip()
                    sms += "\n"
                if "☠️ Летальность:" in i:
                    s = i.replace('☠️ Летальность: ', '')
                    sms += f"☠️ {s}\n"
                    sms = sms.split('(')[0].strip()
                    sms += "\n"
                if "🕵️‍♂️ Безопасность:" in i:
                    s = i.replace('🕵️‍♂️ Безопасность: ', '')
                    sms += f"🕵️‍♂️ {s}\n"
                    sms = sms.split('(')[0].strip()
                    sms += "\n"
                if "☣️ Био-опыт:" in i:
                    s = i.replace('☣️ Био-опыт: ', '')
                    sms += f"☣️ {s}\n"
                    sms = sms.split('(')[0].strip()
                    sms += "\n"
                if "🧬 Био-ресурс:" in i:
                    s = i.replace('🧬 Био-ресурс: ', '')
                    sms += f"🧬 {s}\n"
                    sms = sms.split('(')[0].strip()
                    sms += "\n"
                if "😷 Спецопераций:" in i:
                    s = i.replace('😷 Спецопераций: ', '')
                    sms += f"😷 {s}\n"
                    sms = sms.split('(')[0].strip()
                    sms += "\n"
                if "🥽 Предотвращены:" in i:
                    s = i.replace('🥽 Предотвращены: ', '')
                    sms += f"🥽 {s}"
                    sms = sms.split('(')[0].strip()
                    
               
            await client.send_read_acknowledge(6333102398)   
            
            
            await editmsg.edit(sms, parse_mode='html')
        else:
            pass

    except Exception as e:
        print(f"Ошибка в dos: {e}")
    
async def help(event, user_id, cur, game):
    sender = event.sender_id
    await cur.execute('SELECT user_id FROM dov')
    dov_users = await cur.fetchall()   

    if sender == user_id:
        sms = ""
        if dov_users:
            dov_list = '\n'.join([f'<code>@{user[0]}</code>' for user in dov_users])
            sms += f'    📗 Довы :    \n\n{dov_list}\n'
            await event.edit(sms, parse_mode='html')
        else:
            sms += f'  📗 Нет пользователей с доверенностью.\n'
            await event.edit(sms, parse_mode='html')
    else:
        print("daun")
    
async def dov(event, cur, game, user_id):
    try:
        sender = event.sender_id
        if sender == user_id:
            reply = await event.get_reply_message()
            if not reply:
                neotv = f"<b>Требуется ответ на сообщение</b>"
                await event.edit(neotv, parse_mode='html')
            else:
                user = reply.sender
                userid = user.id
                if userid == user_id:
                    await event.reply(f"Калека ебаная нахуя овнеру в доверку")
                    return
                username = user.username or f"user{userid}"
                await cur.execute(f'SELECT user_id FROM dov WHERE user_id={userid}')
                dov = await cur.fetchone()
                if dov:
                    await cur.execute('DELETE FROM dov WHERE user_id = ?', (userid,))
                    await game.commit()
                    name = f"{user.first_name}"
                    dovdob = f"🚬 <b>{name}</b> удален из доверки\n"
                    await event.edit(dovdob, parse_mode='html')
                else:
                    await cur.execute('INSERT INTO dov (user_id, username) VALUES (?, ?)', (userid, username))
                    await game.commit()
                    name = f"{user.first_name}"
                    dovdob = f"🚬 <b>{name}</b> добавлен в доверку\n"
                    await event.edit(dovdob, parse_mode='html')
        else:
            pass
    except Exception as e:
        print(f"Ошибка в dov: {e}")
        
async def pref(event, user_id, cur, game):
    try:
        sender = event.sender_id
        if sender == user_id:
            command_parts = event.text.split(' ', 1)

            if len(command_parts) > 1:
                pref_value = command_parts[1].strip()

                await cur.execute('DELETE FROM dovpref WHERE user_id = ?', (user_id,))
                await game.commit()

                await cur.execute('INSERT INTO dovpref (user_id, pref) VALUES (?, ?)', (user_id, pref_value))
                await game.commit()

                success_message = f"**Установлен префикс: `{pref_value}`**"
                await event.respond(success_message, parse_mode='markdown')
            else:
                error_message = "Не удалось извлечь значение префикса из команды."
                await event.respond(error_message)
        else:
            print('daun')
    except Exception as e:
        error_message = f"Ошибка при добавлении значения pref: {e}"
        print(error_message)


async def cmd(event, user_id, cur, game):    
    try:
        await cur.execute('SELECT pref FROM dovpref')
        dovpref = await cur.fetchone()
        dovpref_value = dovpref[0] if dovpref else ''
        sender = event.sender_id
        if sender == user_id:
            sms = (
                f"**[CLUSTER 2.5]**(tg://openmessage?user_id=6307195353)\n\n📓**Датабаза:**\n    `Преф` - установить префикс для доверок\n    `Дов` - +/- дов по реплаю\n    `Довы` - просмотр доверенных пользователей\n    `Жд` - добавить запись в зарлист (жд @ ресы)\n    `Автоинс` - вкл/выкл автодобавление жертв в зарлист (это не сохранение при заражении!!)\n    `Стат` - посмотреть текущий статус доп настроек\n\n😈**Заражение:**\n    &`Еб` - заражение по реплаю\n    &`Еб` х - заражение по юзу/айди или одного из списка\n    &`Еб` х-х - заражение по диапазону в списке\n\n📕**Зарлист:**\n    &`З` - чек по реплаю\n    &`З` х - чек по айди/юзу\n    &`Зз` - чек биотопа\n    &`Зар` х - чек зарлиста\n\n🧑‍🦽**Прочее:**\n    &`Ла` - краткая лаба\n    `Дос` - полная лаба\n    &`Хи` - купить вакцину\n    `Ежа` - ежедневная премия\n    &`Пинг` - скорость отклика тг\n    &`Юб` - краткая справка\n    `Хелп` - текущая страница\n\n**&** - __команды доступные к использованию доверенным пользователям с префиксом__"
            )
            
            await event.edit(sms, parse_mode = 'markdown')
    except Exception as e:
        print(f"Ошибка в cmd: {e}")
    
async def farm(event, cur, game, user_id):
    try:
        sender = event.sender_id        
        if sender == user_id:
            while True:
                await event.respond('Биоферма')
                await asyncio.sleep(3610*4)
    except Exception as e:
        print(f"Ошибка в farm: {e}")


async def vac(event, cur, user_id, client):
    try:
        sender = event.sender_id
            
        if sender == user_id:
            
            editmsg = await event.edit("Ожидаем")
            cls = 'хи'
            msg = await msgwait(cls, client)     
            msg = msg.splitlines()
            sms = ""
            for i in msg:
                if "🤓Вы успешно исцелились!" and "Потрачено" in i:
                    sms += f"⚕️Исцелен\n"
                if "😃 У вас нету горячки!" in i:
                    s = "💊 Горячка отсутствует"
                    sms += f"{s}"
                    

            await client.send_read_acknowledge(6333102398)
            
            

            await editmsg.edit(sms, parse_mode='markdown')
            
        else:
            pass

    except Exception as e:
        print(f"Ошибка в heal: {e}")    
        
        
async def dovvac(event, user_id, cur, client):
    try:
        sender = event.sender_id        
        dov_users, pref_value = await get_user_data(cur, sender)
        if (dov_users and dov_users[0] == sender):
            
            sms = ""
            editmsg = await event.reply("Ожидаем")
            cls = 'хи'
            msg = await msgwait(cls, client)     
            msg = msg.splitlines()
            for i in msg:
                if "🤓Вы успешно исцелились!" and "Потрачено" in i:
                    sms += f"⚕️Исцелен"
                if "У вас нету горячки!" in i:
                    sms += f"💊 Горячка отсутствует"
                    

            await client.send_read_acknowledge(6333102398)
            
            
            await editmsg.edit(sms, parse_mode='markdown')
            
        else:
            pass

    except Exception as e:
        print(f"Ошибка в heal: {e}")            


async def zins(event, user_id, cur, game, client):
    try:
        sender = event.sender_id
        if sender == user_id:
            command_parts = event.text.split(' ', 1)
            if len(command_parts) > 1:
                insert = command_parts[1].strip()
                user_id_match = re.search(r'(?<=@)[a-z0-9_]+', insert, re.I)
                t_me_match = re.search(r'(?<=t\.me/)[a-z0-9_]+', insert, re.I)
                open_message_match = re.search(r'(?<=tg://openmessage\?user_id=)[0-9]+', event.text)
        
                if user_id_match:
                    user = user_id_match.group(0)
                elif t_me_match:
                    user = t_me_match.group(0)
                elif open_message_match:
                    user = open_message_match.group(0)
                else:
                    user = None
                    return
                
                st = '0'
                res, data = await zlstd(user, cur, st, client, game)
                res = str(res)
                
                if not (res and data) == None:
                        zmsg1 = f"🚸 `@{user}`\n💸 `{res.replace(' ', '')}`\n🖋️ `️{data}`"
                        await event.edit(zmsg1, parse_mode='markdown')
                else:
                        st = '0'
                        res, data = await zlstd(user, cur, st, client, game)
                        res = str(res)
                        
                        if not (res and data) == None:
                                zmsg1 = f"🚸 `@{user}`\n💸 `{res.replace(' ', '')}`\n🖋️ `️{data}`"
                                await event.edit(zmsg1, parse_mode='markdown')
                        else:
                                zars = (
                                                f"🚸 `@{user}`\n"
                                                f"💤 Не найден в зарлисте"
                                            )
                                await event.edit(zars, parse_mode='markdown')
                
        else:
            pass
    except Exception as e:
        error_message = f"Ошибка: {e}"
        print(error_message)


async def dovzins(event, user_id, cur, game, client):
    try:
        sender = event.sender_id
        dov_users, pref_value = await get_user_data(cur, sender)
        if (dov_users and dov_users[0] == sender):
            command_parts = event.text.split(' ', 1)
            if len(command_parts) > 1:
                insert = command_parts[1].strip()
                user_id_match = re.search(r'(?<=@)[a-z0-9_]+', insert, re.I)
                t_me_match = re.search(r'(?<=t\.me/)[a-z0-9_]+', insert, re.I)
                open_message_match = re.search(r'(?<=tg://openmessage\?user_id=)[0-9]+', event.text)
        
                if user_id_match:
                    user = user_id_match.group(0)
                elif t_me_match:
                    user = t_me_match.group(0)
                elif open_message_match:
                    user = open_message_match.group(0)
                else:
                    user = None
                    return
                
                st = '0'
                res, data = await zlstd(user, cur, st, client, game)
                res = str(res)
                
                if not (res and data) == None:
                        zmsg1 = f"🚸 `@{user}`\n💸 `{res.replace(' ', '')}`\n🖋️ `️{data}`"
                        await event.reply(zmsg1, parse_mode='markdown')
                else:
                        st = '0'
                        res, data = await zlstd(user, cur, st, client, game)
                        res = str(res)
                        if user and res is not None and data is not None:
                            if not (res and data) == None:
                                zmsg1 = f"🚸 `@{user}`\n💸 `{res.replace(' ', '')}`\n🖋️ `️{data}`"
                                await event.reply(zmsg1, parse_mode='markdown')
                            else:
                                zars = (
                                                f"🚸 `@{user}`\n"
                                                f"💤 Не найден в зарлисте"
                                            )
                                await event.reply(zars, parse_mode='markdown')
                
                    
                    
                
        else:
            print('zdaun')
    except Exception as e:
        error_message = f"Ошибка: {e}"
        print(error_message)


        
async def zlstd(user, cur, st, client, game):
    try:
        await cur.execute(f"SELECT res, data FROM zlst WHERE user = '{user}'")  
        row = await cur.fetchone()
        if row and len(row) == 2:
            res, data = row
            return res, data
        else:
            await cur.execute(f"SELECT res, data FROM zlst WHERE user = '{user}'")  
            row = await cur.fetchone()
            if row and len(row) == 2:
                res, data = row
                return res, data
            else:
                is_stat = int(1)
                is_stat_result = await stat(is_stat, cur)
                if is_stat_result == "Off":
                    return None, None
                elif st == "1":
                    return None, None
                else:
                    msg = await client.send_message(6333102398, f'.чек @{user}')
                    for _ in range(10):  # Повторите попытку получения autozar 10 раз
                        await asyncio.sleep(0.2)
                        autozar = (await client.get_messages(6333102398, limit=1))[0]
                        if autozar:
                            break

                    if autozar:
                        autozar_text = autozar.text
                        pattern = r'Жертва `@(.*?)` приносит вам (\d+) ☣️ до (\d{2}\.\d{2}\.\d{4})'
                        await client.send_read_acknowledge(6333102398)
                        match = re.search(pattern, autozar_text)
                        if match:
                            user = match.group(1)
                            res = match.group(2)
                            data = match.group(3)
                            await cur.execute(f"INSERT INTO zlst (user, res, data) VALUES (?, ?, ?)", (user, res, data))
                            await game.commit()
                            return res, data
                        else:                            
                            return None, None
                    else:
                        return None, None

    except Exception as e:
        print(f"Ошибка в зарлисте: {e}")
        return None, None
        
        
        
    
async def autozar(event, client, user_id, cur, game):
    try:
        sender = event.sender_id
        if sender == 6333102398:
            user_id = str(user_id)
            print('autozar started')
            match = re.search(fr'😎 \[.*?\]\(tg://openmessage\?user_id={re.escape(user_id)}\) подверг заражению \[.*?\]\(tg://openmessage\?user_id=(\d+)\)', event.text)
            match2 = re.search(fr'☣️ Жертва приносит __([\d ]+) био-ресурса__', event.text)
            match3 = re.search(fr'☠️ Заражение на __(\d+) дней__', event.text)

            if match and match2 and match3:
                user = match.group(1)
                print(f'{user}')
                st = "1"
                res, data = await zlstd(user, cur, st, client, game)
                res2 = res
                data = data
                if res2 == None:
                    res2 = int(0)
                await asyncio.sleep(1)
                print(res2)
                res = int(match2.group(1).replace(' ', ''))  
                print(f'{res2} -> {res}')
                zartime = int(match3.group(1))
                print(f'{zartime}')
                current_date = datetime.now()
                expiration_date = current_date + timedelta(days=zartime)
                data = expiration_date.strftime('%d.%m.%Y')

                try:
                    # Сначала вставляем или обновляем запись
                    insert_query = """
                        INSERT OR REPLACE INTO zlst (user, res, data)
                        VALUES (?, ?, ?);
                    """
                    await cur.execute(insert_query, (user, res, data))
                    
                    # Затем обновляем значения, если запись уже существует
                    update_query = """
                        UPDATE zlst SET res = ?, data = ? WHERE user = ?;
                    """
                    await cur.execute(update_query, (res, data, user))
                    await game.commit()
                    
                   
                    res_change = int(res) - int(res2)
                    zars = (
                        f"🚸 `@{user}` сохранен\n"
                        f"💸 ~~{res2}~~ -> **{res}** // {'+' if res_change >= 0 else ''}{res_change}\n"
                        f"🖋️ `{data}`"
                    )

                    await event.reply(zars, parse_mode='markdown')

                except Exception as e:
                    print(f"Ошибка в автозар: {e}")
                    pass

            else:
                print('No match found')
    except Exception as e:
        print(f"Ошибка в autozar: {e}")





async def z(client, event, user_id, cur, game):
    try:
        if event.is_reply:  
            sender = event.sender_id
            if sender == user_id:
                user_id = str(user_id)
                msg = await event.get_reply_message()
                msg = msg.text.lower()
                print(f"{msg}")
                match = None
                
                if "👨🏻‍🔬 была" in msg or "👺 попытка заразить" in msg:
                    match = re.search(r"организатор: \[.*?\]\(tg://openmessage\?user_id=(\d+)\)", msg)
                    match = match.group(1)
                    
                elif "😎" in msg and "подверг заражению" in msg:
                    match = re.search(r"заражению \[.*?\]\(tg://openmessage\?user_id=(\d+)\)", msg)
                    match = match.group(1)
                else:
                    
                        pizda = re.findall(r'((t\.me/[a-z0-9_]+)|(tg://(openmessage\?user_id=[a-z0-9_]+)|(tguser\?id=[a-z0-9_]+))|(@[a-z0-9_]+))', msg, re.I)
                        if pizda:
                            match = pizda[0][0]
                            user_id_match = re.search(r'(?<=@)[a-z0-9_]+', match, re.I)
                            t_me_match = re.search(r'(?<=t\.me/)[a-z0-9_]+', match, re.I)
                            open_message_match = re.search(r'(?<=tg://openmessage\?user_id=)[0-9]+', match)
                    
                            if user_id_match:
                                match = user_id_match.group(0)
                            elif t_me_match:
                                match = t_me_match.group(0)
                            elif open_message_match:
                                match = open_message_match.group(0)
                            else:
                                match = None
                                return
                            
                        else:
                            if event.is_reply:
                                reply = await event.get_reply_message()
                                match = reply.sender_id
                                    
                
                if match:
                        user = match
                        print(f"{user}")
                        st = '0'
                        res, data = await zlstd(user, cur, st, client, game)
                        print(f"{res} {data}")
                        if not (res and data) == None:
                            
                            zars = (
                                f"🚸 `@{user}`\n"
                                f"💸 `{res}`\n" 
                                f"🖋️ `{data}`"
                            )
                            await event.edit(zars, parse_mode='markdown')
                        else:
                            st = '0'
                            res, data = await zlstd(user, cur, st, client, game)
                            print(f"nananana2")
                            if not (res and data) == None:
                                
                                zars = (
                                    f"🚸 `@{user}`\n"
                                    f"💸 `{res}`\n" 
                                    f"🖋️ `{data}`"
                                )
                                await event.edit(zars, parse_mode='markdown')
                            else:
                               zars = (
                                    f"🚸 `@{user}`\n"
                                    f"💤 Не найден в зарлисте"
                                )
                               await event.edit(zars, parse_mode='markdown')
                        
                else:
                        print("eshe huinya")
    except Exception as e:
        print(f"Ошибка в з: {e}")
                        


async def dovz(client, event, user_id, cur, game):
    try:
        if event.is_reply:  
            sender = event.sender_id
            dov_users, pref_value = await get_user_data(cur, sender)
            print(f"{dov_users} and {dov_users[0]}")
            if (dov_users and dov_users[0]) == sender:
                user_id = str(user_id)
                msg = await event.get_reply_message()
                msg = msg.text.lower()
                print(f"{msg}")
                match = None
                
                if "👨🏻‍🔬 была" in msg or "👺 попытка заразить" in msg:
                    match = re.search(r"организатор: \[.*?\]\(tg://openmessage\?user_id=(\d+)\)", msg)
                    match = match.group(1)
                    
                elif "😎" in msg and "подверг заражению" in msg:
                    match = re.search(r"заражению \[.*?\]\(tg://openmessage\?user_id=(\d+)\)", msg)
                    match = match.group(1)
                else:
                    pizda = re.findall(r'((t\.me/[a-z0-9_]+)|(tg://(openmessage\?user_id=[a-z0-9_]+)|(tguser\?id=[a-z0-9_]+))|(@[a-z0-9_]+))', msg, re.I)
                    if pizda:
                            match = pizda[0][0]
                            user_id_match = re.search(r'(?<=@)[a-z0-9_]+', match, re.I)
                            t_me_match = re.search(r'(?<=t\.me/)[a-z0-9_]+', match, re.I)
                            open_message_match = re.search(r'(?<=tg://openmessage\?user_id=)[0-9]+', match)
                    
                            if user_id_match:
                                match = user_id_match.group(0)
                            elif t_me_match:
                                match = t_me_match.group(0)
                            elif open_message_match:
                                match = open_message_match.group(0)
                            else:
                                match = None
                                return
                            
                    else:
                            if event.is_reply:
                                reply = await event.get_reply_message()
                                match = reply.sender_id
                                    
                
                if match:
                        user = match
                        print(f"{user}")
                        st = '0'
                        res, data = await zlstd(user, cur, st, client, game)
                        print(f"{res} {data}")
                        if not (res and data) == None:
                            
                            zars = (
                                f"🚸 `@{user}`\n"
                                f"💸 `{res}`\n" 
                                f"🖋️ `{data}`"
                            )
                            await event.reply(zars, parse_mode='markdown')
                        else:
                            st = '0'
                            res, data = await zlstd(user, cur, st, client, game)
                            print(f"nananana2")
                            if not (res and data) == None:
                                
                                zars = (
                                    f"🚸 `@{user}`\n"
                                    f"💸 `{res}`\n" 
                                    f"🖋️ `{data}`"
                                )
                                await event.reply(zars, parse_mode='markdown')
                            else:
                               zars = (
                                    f"🚸 `@{user}`\n"
                                    f"💤 Не найден в зарлисте"
                                )
                               await event.reply(zars, parse_mode='markdown')
                        
                else:
                        print("eshe huinya")
    except Exception as e:
        print(f"Ошибка в довз: {e}")



async def eb(client, event, user_id, cur, game):
    try:
        if event.is_reply:  
            sender = event.sender_id
            if sender == user_id:
                user_id = str(user_id)
                msg = await event.get_reply_message()
                msg = msg.text.lower()
                print(f"{msg}")
                match = None
                
                if "👨🏻‍🔬 была" in msg or "👺 попытка заразить" in msg:
                    match = re.search(r"организатор: \[.*?\]\(tg://openmessage\?user_id=(\d+)\)", msg)
                    match = match.group(1)
                    
                elif "😎" in msg and "подверг заражению" in msg:
                    match = re.search(r"заражению \[.*?\]\(tg://openmessage\?user_id=(\d+)\)", msg)
                    match = match.group(1)
                else:
                    pizda = re.findall(r'((t\.me/[a-z0-9_]+)|(tg://(openmessage\?user_id=[a-z0-9_]+)|(tguser\?id=[a-z0-9_]+))|(@[a-z0-9_]+))', msg, re.I)
                    if pizda:
                            match = pizda[0][0]
                            user_id_match = re.search(r'(?<=@)[a-z0-9_]+', match, re.I)
                            t_me_match = re.search(r'(?<=t\.me/)[a-z0-9_]+', match, re.I)
                            open_message_match = re.search(r'(?<=tg://openmessage\?user_id=)[0-9]+', match)
                    
                            if user_id_match:
                                match = user_id_match.group(0)
                            elif t_me_match:
                                match = t_me_match.group(0)
                            elif open_message_match:
                                match = open_message_match.group(0)
                            else:
                                match = None
                                return
                            
                    else:
                            if event.is_reply:
                                reply = await event.get_reply_message()
                                match = reply.sender_id
                
                if match:
                        user = match
                        print(f"{user}")
                        
                        
                        await client.send_message(event.chat_id, f"биоеб {user}", parse_mode='markdown')
                else:
                        print("eshe huinya")
    except Exception as e:
        print(f"Ошибка в еб: {e}")
        

async def doveb(client, event, user_id, cur, game):
    try:
        if event.is_reply:  
            sender = event.sender_id
            dov_users, pref_value = await get_user_data(cur, sender)
            print(f"{dov_users} and {dov_users[0]}")
            if (dov_users and dov_users[0]) == sender:
                user_id = str(user_id)
                msg = await event.get_reply_message()
                msg = msg.text.lower()
                print(f"{msg}")
                match = None
                
                if "👨🏻‍🔬 была" in msg or "👺 попытка заразить" in msg:
                    match = re.search(r"организатор: \[.*?\]\(tg://openmessage\?user_id=(\d+)\)", msg)
                    match = match.group(1)
                    
                elif "😎" in msg and "подверг заражению" in msg:
                    match = re.search(r"заражению \[.*?\]\(tg://openmessage\?user_id=(\d+)\)", msg)
                    match = match.group(1)
                else:
                    pizda = re.findall(r'((t\.me/[a-z0-9_]+)|(tg://(openmessage\?user_id=[a-z0-9_]+)|(tguser\?id=[a-z0-9_]+))|(@[a-z0-9_]+))', msg, re.I)
                    if pizda:
                            match = pizda[0][0]
                            user_id_match = re.search(r'(?<=@)[a-z0-9_]+', match, re.I)
                            t_me_match = re.search(r'(?<=t\.me/)[a-z0-9_]+', match, re.I)
                            open_message_match = re.search(r'(?<=tg://openmessage\?user_id=)[0-9]+', match)
                    
                            if user_id_match:
                                match = user_id_match.group(0)
                            elif t_me_match:
                                match = t_me_match.group(0)
                            elif open_message_match:
                                match = open_message_match.group(0)
                            else:
                                match = None
                                return
                            
                    else:
                            if event.is_reply:
                                reply = await event.get_reply_message()
                                match = reply.sender_id
                
                if match:
                        user = match
                        print(f"{user}")
                        
                        await client.send_message(event.chat_id, f"биоеб {user}", parse_mode='markdown')
                else:
                        print("eshe huinya")
    except Exception as e:
        print(f"Ошибка в довеб: {e}")

        
async def rawtext(client, event, user_id):
    try:        
        if event.is_reply:  
            sender = event.sender_id
            if sender == user_id:
                replied_message = await event.get_reply_message()
                sender_id = replied_message.sender_id
                sender = await client.get_entity(sender_id)
                await event.edit(f"Вы ответили на сообщение от {sender.username}:\n ```{replied_message.text}```")
            else:
                pass
    except Exception as e:
        print(f"Ошибка в rawtext: {e}")        
        
        
       

async def get_zarlist_page(cur, page_number, page_size=30):
    try:
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size

        await cur.execute("SELECT user, res, data FROM zlst")
        rows = await cur.fetchall()

        if start_index >= len(rows):
            pass

        total_pages = (len(rows) + page_size - 1) // page_size
        page_rows = rows[start_index:end_index]
        zar_list = []

        for index, row in enumerate(page_rows, start=start_index + 1):
            user, res, data = row
            zar_list.append(f"{index}. [{user}](tg://openmessage?user_id={user}) <§> **{res}** <§> __{data}__\n")

        return total_pages, "".join(zar_list)

    except Exception as e:
        print(f"Ошибка в get_zarlist_page: {e}")
        pass


async def zarlist(user_id, event, cur, client):
    try:
        sender = event.sender_id
        if sender == user_id: 
           if 'зар' in event.text.lower():
                page_number = event.text.split()
                page_number = int(page_number[1]) if len(page_number) > 1 and page_number[1].isdigit() else 1

                total_pages, result = await get_zarlist_page(cur, page_number)
                if result:
                    await cur.execute("SELECT COUNT(*) FROM zlst")
                    user_count = await cur.fetchone()
                    user_count = user_count[0] if user_count else 0

                    sms = f"**📕 Зарлист, страница:** {page_number}/{total_pages}\n" + result + f"**👥 Всего сохранено: {user_count}**"
                    await event.edit(sms, parse_mode='markdown')
                else:
                    print("Страница не найдена.")
    except Exception as e:
        print(f"Ошибка в process_zarlist_command: {e}")
        pass


async def dovzarlist(user_id, event, cur):
    try:
        sender = event.sender_id
        dov_users, pref_value = await get_user_data(cur, sender)
        if (dov_users and dov_users[0] == sender):
           if 'зар' in event.text.lower():
                page_number = event.text.split()
                page_number = int(page_number[1]) if len(page_number) > 1 and page_number[1].isdigit() else 1
                total_pages, result = await get_zarlist_page(cur, page_number)
                if result:
                    await cur.execute("SELECT COUNT(*) FROM zlst")
                    user_count = await cur.fetchone()
                    user_count = user_count[0] if user_count else 0
                    sms = f"**📕 Зарлист, страница:** {page_number}/{total_pages}\n" + result + f"**👥 Всего сохранено: {user_count}**"
                    await event.reply(sms, parse_mode='markdown')
                else:
                    print("Страница не найдена.")
    except Exception as e:
        print(f"Ошибка в process_zarlist_command: {e}")
        pass


async def ebins(event, user_id, cur, game, client):
    try:
        sender = event.sender_id
        if sender == user_id:
            command_parts = event.text.split(' ', 1)
            if len(command_parts) > 1:
                insert = command_parts[1].strip()
                user_id_match = re.search(r'(?<=@)[a-z0-9_]+', insert, re.I)
                t_me_match = re.search(r'(?<=t\.me/)[a-z0-9_]+', insert, re.I)
                open_message_match = re.search(r'(?<=tg://openmessage\?user_id=)[0-9]+', event.text)
        
                if user_id_match:
                    user = user_id_match.group(0)
                elif t_me_match:
                    user = t_me_match.group(0)
                elif open_message_match:
                    user = open_message_match.group(0)
                else:
                    user = None
                    return
                
                await client.send_message(event.chat_id, f"биоеб {user}")
        else:
            pass
    except Exception as e:
        error_message = f"Ошибка: {e}"
        print(error_message)        
        
        
 
async def dovebins(event, user_id, cur, game, client):
    try:
        sender = event.sender_id
        dov_users, pref_value = await get_user_data(cur, sender)
        print(f"{dov_users} and {dov_users[0]}")
        if (dov_users and dov_users[0]) == sender:
            command_parts = event.text.split(' ', 1)
            if len(command_parts) > 1:
                insert = command_parts[1].strip()
                user_id_match = re.search(r'(?<=@)[a-z0-9_]+', insert, re.I)
                t_me_match = re.search(r'(?<=t\.me/)[a-z0-9_]+', insert, re.I)
                open_message_match = re.search(r'(?<=tg://openmessage\?user_id=)[0-9]+', event.text)
        
                if user_id_match:
                    user = user_id_match.group(0)
                elif t_me_match:
                    user = t_me_match.group(0)
                elif open_message_match:
                    user = open_message_match.group(0)
                else:
                    user = None
                    return
                
                await client.send_message(event.chat_id, f"биоеб {user}")
        else:
            pass
    except Exception as e:
        error_message = f"Ошибка: {e}"
        print(error_message)               
        
        
        
async def zhdob(event, user_id, cur, game, client):
        try:
            sender = event.sender_id
            if sender == user_id:
                match = re.match(r'^жд (\S+) (\d+)$', event.text)
                if match:
                    user = match.group(1)
                    res = match.group(2)
                    data = ' '
                    print(f"{user} {res} {data}")
                    if user:
                        user_id_match = re.search(r'(?<=@)[a-z0-9_]+', user, re.I)
                        t_me_match = re.search(r'(?<=t\.me/)[a-z0-9_]+', user, re.I)
                        open_message_match = re.search(r'(?<=tg://openmessage\?user_id=)[0-9]+', user)
                
                        if user_id_match:
                            user = user_id_match.group(0)
                        elif t_me_match:
                            user = t_me_match.group(0)
                        elif open_message_match:
                            user = open_message_match.group(0)
                        else:
                            print("dalbaeb")
                            return
                           
                    print(f"{res}")
                    try:
                        # Сначала вставляем или обновляем запись
                        insert_query = """
                            INSERT OR REPLACE INTO zlst (user, res, data)
                            VALUES (?, ?, ?);
                        """
                        await cur.execute(insert_query, (user, res, data))
                        
                        # Затем обновляем значения, если запись уже существует
                        update_query = """
                            UPDATE zlst SET res = ?, data = ? WHERE user = ?;
                        """
                        await cur.execute(update_query, (res, data, user))
                        await game.commit()
                        zars = (
                            f"🚸 `@{user}` сохранен\n"
                            f"💸 `{res}`\n"
                            f"🖋️ `{data}`"
                        )
    
                        await event.reply(zars, parse_mode='markdown')
                    except aiosqlite.IntegrityError:
                        print(f"Пользователь {user} уже существует в базе данных.")
                        pass
                else:
                    print("superdalbaeb")
                    pass
        except Exception as e:
                print(f"Ошибка в жд: {e}")
                        
                        
                        
                        

async def zz(event, user_id, cur, game, client):           
    try:
        sender = event.sender_id
        if sender == user_id:
            msg = await event.get_reply_message()
            msg = msg.text.lower()
            
            if not msg or not msg.startswith("биотоп чмоней"):
                await event.edit("Паскуда, это для биотопа", parse_mode='markdown')
                return
                
            else:
                await event.edit("Ожидание")
                result = re.findall(r'\[.*?\]\(tg://openmessage\?user_id=[a-z0-9_]+\) \| [\d,]+k', msg)
                user_list = []
                for match in result:
                    user_match = re.search(r'\[.*?\]\(tg://openmessage\?user_id=([a-z0-9_]+)\) \| ([\d,]+k)', match)
                    if user_match:
                        user, res_from_msg = user_match.group(1), user_match.group(2)
                        if 'k' in res_from_msg.lower():
                            res_from_msg = round(float(res_from_msg[:-1].replace(',', '.')) * 100)
                        else:
                            res_from_msg = round(float(res_from_msg.replace(',', '.')))

                        st = '0'
                        res, data = await zlstd(user, cur, st, client, game)

                        if res is not None and data is not None:
                            res_diff = res_from_msg - int(res)

                            if res_diff > 0:
                                user_list.append(f"🚸 `@{user}` <§> 💸 {int(res):,} <§> 👁️‍🗨️**+{int(res_diff):,}**")
                        else:
                            user_list.append(f"🚸 `@{user}` <§> 🆕")

                await event.edit(f"{'🫣**Дрочилово через 3... 2... 1...**' if user_list else '🧑‍🦽**Хуйня, бт сдох**'}" + "\n\n" + ('\n'.join([f"{index + 1}. {line}" for index, line in enumerate(user_list)])), parse_mode="markdown")
        else:
            pass
    except Exception as e:
        print(f"Ошибка в зз: {e}")
        
        
        
async def dovzz(event, user_id, cur, game, client):           
    try:
        sender = event.sender_id
        dov_users, pref_value = await get_user_data(cur, sender)
        if (dov_users and dov_users[0] == sender):
            msg = await event.get_reply_message()
            msg = msg.text.lower()
            
            if not msg or not msg.startswith("биотоп чмоней"):
                await event.edit("Паскуда, это для биотопа", parse_mode='markdown')
                return
                
            else:
                pizda = await event.reply("Ожидание")
                result = re.findall(r'\[.*?\]\(tg://openmessage\?user_id=[a-z0-9_]+\) \| [\d,]+k', msg)
                user_list = []
                for match in result:
                    user_match = re.search(r'\[.*?\]\(tg://openmessage\?user_id=([a-z0-9_]+)\) \| ([\d,]+k)', match)
                    if user_match:
                        user, res_from_msg = user_match.group(1), user_match.group(2)
                        if 'k' in res_from_msg.lower():
                            res_from_msg = round(float(res_from_msg[:-1].replace(',', '.')) * 100)
                        else:
                            res_from_msg = round(float(res_from_msg.replace(',', '.')))

                        st = '0'
                        res, data = await zlstd(user, cur, st, client, game)

                        if res is not None and data is not None:
                            res_diff = res_from_msg - int(res)

                            if res_diff > 0:
                                user_list.append(f"🚸 `@{user}` <§> 💸 {int(res):,} <§> 👁️‍🗨️**+{int(res_diff):,}**")
                        else:
                            user_list.append(f"🚸 `@{user}` <§> 🆕")

                await pizda.edit(f"{'🫣**Дрочилово через 3... 2... 1...**' if user_list else '🧑‍🦽**Хуйня, бт сдох**'}" + "\n\n" + ('\n'.join([f"{index + 1}. {line}" for index, line in enumerate(user_list)])), parse_mode="markdown")
        else:
            pass
    except Exception as e:
        print(f"Ошибка в зз: {e}")
                
                    
async def ping(event, user_id, client):
    try:
        sender = event.sender_id
        if sender == user_id:
            time1 = datetime.now()
            me = await client.get_me()
            time2 = datetime.now()
            time = (time2 - time1).microseconds / 1000
            time = round(time, 2)
            await event.edit(f"<b>Пинг: {time}мс</b>", parse_mode='html')
        else:
            pass
    except Exception as e:
        print(f"Ошибка в пинг: {e}")
        
        
async def dovping(event, cur, user_id, client):
    try:
        sender = event.sender_id
        dov_users, pref_value = await get_user_data(cur, sender)
        if (dov_users and dov_users[0] == sender):
            time1 = datetime.now()
            me = await client.get_me()
            time2 = datetime.now()
            time = (time2 - time1).microseconds / 1000
            time = round(time, 2)
            await event.reply(f"<b>Пинг: {time}мс</b>", parse_mode='html')
        else:
            pass
    except Exception as e:
        print(f"Ошибка в пинг: {e}")        
        
                        
                        
async def ebsp(client, event, user_id, cur, game):
    try:
        if event.is_reply:
            sender = event.sender_id
            if sender == user_id:
                user_id = str(user_id)
                sms = event.message
                sms = sms.text.lower()
                msg = await event.get_reply_message()
                msg_text = msg.text.lower()
                print(f"{msg_text}")
                
                
                if sms.startswith('еб '):
                    # Получаем номер из команды 'з'
                    selected_number = int(sms.split(' ')[1])
                    
                    # Разбиваем сообщение на строки
                    lines = msg_text.split('\n')
                    
                    # Ищем строку, начинающуюся с номера, который указан в команде 'з'
                    for line in lines:
                        if line.startswith(f"{selected_number}. "):
                            # Извлекаем айди из строки и отправляем 'биоеб {айди}' в чат
                            match = re.search(r'@([a-z0-9_]+)', line, re.I)
                            if match:
                                bio_id = match.group(1)
                                await client.send_message(event.chat_id, f"биоеб {bio_id}", parse_mode='markdown')
                                return
                            else:
                                print("Неверный формат строки.")
                                return
                else:
                    print("Команда 'з' не найдена в сообщении.")
    except Exception as e:
        print(f"Ошибка в еб: {e}")
        
        
async def dovebsp(client, event, user_id, cur, game):
    try:
        if event.is_reply:
            sender = event.sender_id
            dov_users, pref_value = await get_user_data(cur, sender)
            if (dov_users and dov_users[0] == sender):
                user_id = str(user_id)
                sms = event.message
                sms = sms.text.lower()
                msg = await event.get_reply_message()
                msg_text = msg.text.lower()
                print(f"{msg_text}")
                
                
                if sms.startswith(pref_value + 'еб '):
                    # Получаем номер из команды 'з'
                    selected_number = int(sms.split(' ')[1])
                    
                    # Разбиваем сообщение на строки
                    lines = msg_text.split('\n')
                    
                    # Ищем строку, начинающуюся с номера, который указан в команде 'з'
                    for line in lines:
                        if line.startswith(f"{selected_number}. "):
                            # Извлекаем айди из строки и отправляем 'биоеб {айди}' в чат
                            match = re.search(r'@([a-z0-9_]+)', line, re.I)
                            if match:
                                bio_id = match.group(1)
                                await client.send_message(event.chat_id, f"биоеб {bio_id}", parse_mode='markdown')
                                return
                            else:
                                print("Неверный формат строки.")
                                return
                else:
                    print("Команда 'з' не найдена в сообщении.")
    except Exception as e:
        print(f"Ошибка в еб: {e}")        
        
        
        
from telethon.tl import functions        
        
from telethon import errors

async def is_user_in_group(client, group_id, user_id):
    try:
        # Проверяем наличие пользователя в группе
        participants = await client.get_participants(group_id)

        user_ids = [participant.id for participant in participants]

        return user_id in user_ids
    except errors.FloodWaitError as e:
        print(f"Error checking user in group: {e}")
        sys.exit()
    except errors.ChatAdminRequiredError as e:
        print(f"Error checking user in group: {e}")
        sys.exit()
    except errors.UserNotParticipantError as e:
        print("Пользователь не является участником группы. Скрипт завершается.")
        sys.exit()
    except Exception as e:
        print(f"Error checking user in group: {e}")
        sys.exit()

async def check_license(client, user_id):
    group_id = -1002058510134  # Замените на ваш ID группы
    user_id_to_check = user_id
    is_user_present = await is_user_in_group(client, group_id, user_id_to_check)

    if not is_user_present:
        print("Пользователь отсутствует в группе. Скрипт завершается.")
        sys.exit()
    else:
        pass
        
        
async def editstat(event, user_id, cur, game, client):
    try:
        sender = event.sender_id
        if sender == user_id:
            msg = event.text.lower()
            if msg == "автоинс":
                await cur.execute("SELECT autoins FROM stat")
                stat = await cur.fetchone()
                if stat is not None:
                    stat = stat[0]
                print(f"{stat}")
                if stat is None:
                    autoins = "Off"
                    await cur.execute("INSERT INTO stat (autoins) VALUES (?)", (autoins,))
                    await game.commit()
                    await cur.execute("SELECT autoins FROM stat")
                    stat = await cur.fetchone()

                if stat == "Off":
                    autoins = "On"
                    await cur.execute("UPDATE stat SET autoins = ?", (autoins,))
                    await game.commit()
                    await event.edit("Автоинсерт жертв включен")
                else:
                    autoins = "Off"
                    await cur.execute("UPDATE stat SET autoins = ?", (autoins,))
                    await game.commit()
                    await event.edit("Автоинсерт жертв выключен")

        else:
            pass
    except Exception as e:
        print(f"Ошибка в статмоде: {e}")
            
async def stat(is_stat, cur):
    try:
        if is_stat == int(1):
            await cur.execute("SELECT autoins FROM stat")
            stat = await cur.fetchone()
            if stat == None:
                stat = "Off"
            else:
                stat = stat[0]
            return stat
    except Exception as e:
        print(f"Ошибка в обработке стат: {e}")
    
    
    
async def statch(event, user_id, cur, client):
    try:
        sender = event.sender_id
        if sender == user_id:
            is_stat = int(1)
            autoins = await stat(is_stat, cur)
            sms = (
            "<b>⚙️Лист доп настроек:</b>\n\n"
            f"Автоинсерт жертв: {autoins}"
            )
            await event.edit(sms, parse_mode = 'html')
    except Exception as e:
        print(f"Ошибка в стат чек: {e}")
    
   

async def ebspdp(client, event, user_id, cur, game):
    try:
        if event.is_reply:
            sender = event.sender_id
            if sender == user_id:
                user_id = str(user_id)
                sms = event.message
                sms = sms.text.lower()
                msg = await event.get_reply_message()
                msg_text = msg.text.lower()
                

                if sms.startswith('еб '):
                   
                    if '-' in sms:
                        start, end = map(int, sms.split(' ')[1].split('-'))
                        selected_numbers = range(start, end + 1)
                    else:
                        selected_numbers = [int(sms.split(' ')[1])]

                    
                    lines = msg_text.split('\n')

                    
                    found_bio_ids = []

                    for selected_number in selected_numbers:
                        
                        for line in lines:
                            if line.startswith(f"{selected_number}. "):
                                
                                match = re.search(r'@([a-z0-9_]+)', line, re.I)
                                if match:
                                    bio_id = match.group(1)
                                    found_bio_ids.append(bio_id)
                                    break  

                    if found_bio_ids:
                        
                        for bio_id in found_bio_ids:
                            await client.send_message(event.chat_id, f"биоеб {bio_id}", parse_mode='markdown')
                            await asyncio.sleep(1.1)

                else:
                    print("Команда 'еб' не найдена в сообщении.")

    except Exception as e:
        print(f"Ошибка в еб: {e}")
    
    
    
    
async def dovebspdp(client, event, user_id, cur, game):
    try:
        if event.is_reply:
            sender = event.sender_id
            dov_users, pref_value = await get_user_data(cur, sender)
            if (dov_users and dov_users[0] == sender):
                user_id = str(user_id)
                sms = event.message
                sms = sms.text.lower()
                msg = await event.get_reply_message()
                msg_text = msg.text.lower()
                

                if sms.startswith(f'{pref_value}еб '):
                   
                    if '-' in sms:
                        start, end = map(int, sms.split(' ')[1].split('-'))
                        selected_numbers = range(start, end + 1)
                    else:
                        selected_numbers = [int(sms.split(' ')[1])]

                    
                    lines = msg_text.split('\n')

                    
                    found_bio_ids = []

                    for selected_number in selected_numbers:
                        
                        for line in lines:
                            if line.startswith(f"{selected_number}. "):
                                
                                match = re.search(r'@([a-z0-9_]+)', line, re.I)
                                if match:
                                    bio_id = match.group(1)
                                    found_bio_ids.append(bio_id)
                                    break  

                    if found_bio_ids:
                        
                        for bio_id in found_bio_ids:
                            await client.send_message(event.chat_id, f"биоеб {bio_id}", parse_mode='markdown')
                            await asyncio.sleep(1.1)

                else:
                    print("Команда 'еб' не найдена в сообщении.")

    except Exception as e:
        print(f"Ошибка в еб: {e}")    
    
    
processed_messages = set()

async def main():
    
    global upt
    api_id, api_hash = await api()
    
    client = TelegramClient('byzantium', api_id, api_hash)
    await client.start()
    user_id = (await client.get_me()).id
    data = datetime.now().strftime("%Y-%m-%d")
    data2 = datetime.now().strftime("%H:%M:%S")
    print(f'''.
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣶⡖⠚⠉⠀⠀    
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣶⣿⠿⠛⠉⠁⠀⠀⠀⠀⠀    
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣶⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀    
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⡿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⠏⠀⠀⠀⠀⣀⣀⣀⣤⣤⣤⣤⣤⡤⠀    
    ⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⡟⠋⠁⣀⣴⣶⣿⣿⡟⠛⠛⠻⣿⣿⣿⣷⣀⣀    
    ⠀⠀⠀⠀⠀⢀⣴⣿⣿⡿⠛⠉{Fore.RED}⣰⣶⣿⣿⣿⣿⣿⣷{Style.RESET_ALL}⠀⠀⠀⠀⠀⠉⣿⣿⡏⠁
    ⠀⠀⠀⢀⣴⡿⢛⡿⠋{Fore.RED}⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇{Style.RESET_ALL}⠀⠀⠀⠀⠀⢻⣿⠃⠀    
    ⠀⠀⣴⡿⠏⠠⠈{Fore.RED}⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁{Style.RESET_ALL}⠀⠀⠀⠀⠀⠀⠀⢸⡿⠀    
    ⢀⣸⠏⠀⠀{Fore.RED}⣠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁{Style.RESET_ALL}⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀    
    ⠊⠀⠀⠀{Fore.RED}⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡴⠃{Style.RESET_ALL}⠀⠀⠀⠀⠀⢀⠘⠀⠀⠀    
    ⠀⠀⠀⠀{Fore.RED}⡿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁{Style.RESET_ALL}⠀⠀⠀⠀⠀⠀⣾⠶⠟⠀⠀    
    ⠀⠀⠀⠀⠀{Fore.RED}⢿⠛⠈⠛⠿⣿⣿⣿⣿⠿⠛⠁{Style.RESET_ALL}⠀⠀⠀⠀⠀⢀⣤⣾⠟⠀⠀⠀⠀    
    ⠀⠀⠀⠀⠀{Fore.RED}⠈{Style.RESET_ALL}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⠟⠁⠀⠀⠀⠀⠀    
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠤⠤⣀⣀⣀⡀⠤⠤⢌⠿⠉⠁⠀⠀⠀⠀⠀⠀
    
    ▄▀▀▄ ▒█▀▀█ ▒█▀▀▀ ░█▀▀█ ▒█░▄▀ ▒█▀▀▀█ 
    ▀▄▄█ ▒█▄▄█ ▒█▀▀▀ ▒█▄▄█ ▒█▀▄░ ░▀▀▀▄▄ 
    ░▄▄▀ ▒█░░░ ▒█▄▄▄ ▒█░▒█ ▒█░▒█ ▒█▄▄▄█
    
    
    {Fore.RED}CLIENT STARTED{Style.RESET_ALL}
    {user_id}        
    {data}        
    {data2}
    {api_id}                                      
    {api_hash}     
    ''')

    message = await client.send_message('me', '<pre><code>{\n    \"Сделал\" : \"@wi7chblades\" \n    \"Список команд\" : \"хелп\"\n}</code></pre>\n<b>Отдельное спасибо:</b>\n    @nefris\n    @ZachemTiEtoChitaeshHaker', parse_mode='html')
    upt = datetime.now()
    game, cur = await open_database() 
    
    await check_license(client, user_id)
    try:
        @client.on(events.NewMessage())
        async def trg(event):
            try:
                sender = event.sender_id
                user_id = (await client.get_me()).id
                user_id1 = str(user_id)
                text_lower = event.text.lower()

                if (sender == user_id) or (sender == 6333102398):
                    
                    
                    if text_lower == ('стат').lower():
                        await statch(event, user_id, cur, client)
                    if text_lower == ('автоинс').lower():
                        await editstat(event, user_id, cur, game, client)
                    if text_lower == ('ла').lower():
                        await la(event, user_id, client)
                    if text_lower == ('хи').lower():
                        await vac(event, cur, user_id, client)
                    if text_lower == ('дос').lower():
                        await dos(event, user_id, cur, client)
                    if text_lower == ('ежа').lower():
                        await doh(event, user_id, client)
                    if text_lower == ('фарм').lower():
                        await farm(event, cur, game, user_id)
                                         
                    if text_lower == ('юб').lower():
                        await ub(event, user_id, client)                    
                    if re.match(r'^\преф (.+)$', text_lower):
                        await pref(event, user_id, cur, game)
                    if text_lower == (r'хелп').lower():
                        await cmd(event, user_id, cur, client)   
                    if text_lower == ('дов').lower():
                        await dov(event, cur, game, user_id)
                    if text_lower == (r'довы').lower():
                        await help(event, user_id, cur, client)
                    if text_lower == ('рав').lower():
                        await rawtext(client, event, user_id)
                    if text_lower == ('пинг').lower():
                        await ping(event, user_id, client)
                                             
                    if re.match(r'^\з (.+)$', text_lower):
                        await zins(event, user_id, cur, game, client)   
                    if text_lower == ('з').lower():
                        await z(client, event, user_id, cur, game)
                    if re.match(r'^\зар$', text_lower):
                        await zarlist(user_id, event, cur, client)
                    if re.match(r'^\зар (\d+)$', text_lower):
                        await zarlist(user_id, event, cur, client)
                    if re.match(r'^жд (\S+) (\d+)$', text_lower):
                        await zhdob(event, user_id, cur, game, client)
                    if text_lower == ('зз').lower():
                        await zz(event, user_id, cur, game, client)
                        
                    if text_lower == ('еб').lower():
                        await eb(client, event, user_id, cur, game)
                    if re.match(r'^еб (\d+)', text_lower):
                        await ebsp(client, event, user_id, cur, game)
                    if re.search(r'^еб (\d+)-(\d+)$', text_lower):
                        await ebspdp(client, event, user_id, cur, game)
                    if re.match(r'^\еб (.+)$', text_lower):
                        await ebins(event, user_id, cur, game, client)
                                                                        
                    if re.match(fr'😎 \[.*?\]\(tg://openmessage\?user_id={re.escape(user_id1)}\) подверг заражению', event.text):
                        await autozar(event, client, user_id, cur, game)
                        
                    else:
                        pass
                    
                    
            except Exception as e:
                print(f"Unexpected error: {e}")
                
        @client.on(events.NewMessage())
        async def trgdov(event):
            try:
                sender = event.sender_id
                user_id = (await client.get_me()).id
                text_lower = event.text.lower()
                await cur.execute('SELECT pref FROM dovpref')
                pref_value = await cur.fetchone()
                pref_value = str(pref_value[0]) if pref_value and pref_value[0] else 'двззд'
                if text_lower.startswith(pref_value.lower()):
                                  
                    if text_lower == (pref_value + 'ла').lower():
                        await dovla(event, user_id, cur, client)                    
                    if text_lower == (pref_value + 'хи').lower():
                        await dovvac(event, user_id, cur, client)
                                        
                    if text_lower == (pref_value + 'еб').lower():
                        await doveb(client, event, user_id, cur, game)
                    if re.search(f'{re.escape(pref_value)}еб (\d+)$', text_lower):
                        await dovebsp(client, event, user_id, cur, game)
                    if re.search(f'{re.escape(pref_value)}еб (\d+)-(\d+)$', text_lower):
                        await dovebspdp(client, event, user_id, cur, game)
                    if re.search(f'{re.escape(pref_value)}еб (.+)$', text_lower):
                        await dovebins(event, user_id, cur, game, client)
                    
                                        
                                                                                
                    if text_lower == (pref_value + 'з').lower():
                        await dovz(client, event, user_id, cur, game)
                    if re.search(f'{re.escape(pref_value)}зз', text_lower):
                        await dovzz(event, user_id, cur, game, client)
                    if re.search(f'{re.escape(pref_value)}з (.+)$', text_lower):
                        await dovzins(event, user_id, cur, game, client)
                    if re.search(f'{re.escape(pref_value)}зар$', text_lower):
                        await dovzarlist(user_id, event, cur)
                    elif re.search(f'{re.escape(pref_value)}зар (\d+)$', text_lower):
                        await dovzarlist(user_id, event, cur)
                                          
                                                                                      
                    if text_lower == (pref_value + 'юб').lower():
                        await dovub(event, cur, client)
                    if text_lower == (pref_value + 'пинг').lower():
                        await dovping(event, cur, user_id, client)
                else:
                    pass
            
            except Exception as e2:
                print(f"Dovtrg error: {e2}")
            
            except errors.MessageNotModifiedError:
                pass
            
                
        await client.run_until_disconnected()
    finally:
        await close_database(game)

if __name__ == "__main__":
    asyncio.run(main())