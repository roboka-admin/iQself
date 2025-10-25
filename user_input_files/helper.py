import aiohttp , aiofiles , json , random , psutil , os
from flask import Flask , request

app = Flask(__name__)

token = '2102899812:AAHzlZ9G1ikEB_Z4eBYf-Xn7EzB030onc9E'
admins = [1725955696,2113629872]

async def get(file):
	async with aiofiles.open(file,'r') as r:
		return json.loads(await r.read())

async def put(file,data):
	async with aiofiles.open(file,'w') as w:
		await w.write(json.dumps(data))

async def font(text):
	text = text.lower()
	return text.translate(text.maketrans("qwertyuiopasdfghjklzxcvbnm","ǫᴡᴇʀᴛʏᴜɪᴏᴘᴀsᴅғɢʜᴊᴋʟᴢxᴄᴠʙɴᴍ"))

async def kill(path,filename):
	for process in psutil.process_iter():
		try:
			cmdline = process.cmdline()
			pid = process.pid
			if os.path.basename(cmdline[1]) == filename:
				return os.system(f"kill -9 {pid} && {path} && python3 {filename}")
		except:
			continue
	return os.system(f"{path} && python3 {filename}")

class Updates:
	def __init__(self,args):
		for key,value in args.items():
			if isinstance(key,(list,tuple)):
				setattr(self,key,[Updates(x) if isinstance(x,dict) else x for x in value])
			else:
				setattr(self,key,Updates(value) if isinstance(value,dict) else value)

	def __getattr__(self,name):
		return self

	def __str__(self):
		return 'None'

class Bot:
	def __init__(self,token):
		self.token = token

	async def bot(self,method,datas = []):
		async with aiohttp.ClientSession() as session:
			async with session.post('https://api.telegram.org/bot' + str(self.token) + '/' + str(method),data = datas) as result:
				return await self.format(await result.json())

	def __getattr__(self,action):
		async def function(**kwargs):
			return await self.bot(action,kwargs)
		return function

	async def format(self,dictionary):
		return Updates(dictionary)

@app.route('/helper',methods = ['POST','GET'])
async def helper():
	telegram = Bot(token)
	update = request.get_json(force = True)
	if 'message' in update.keys():
		message_text = update['message']['text']
		message_type = update['message']['chat']['type']
		message_from_id = update['message']['from']['id']
		message_first_name = update['message']['from']['first_name']
		if message_text.startswith('/start') and message_from_id in admins:
			if message_type == 'private':
				await telegram.SendMessage(
				chat_id = message_from_id,
				text = message_first_name,
				parse_mode = 'HTML'
				)
	if 'inline_query' in update.keys():
		inline_text = update['inline_query']['query']
		inline_id = update['inline_query']['id']
		inline_from_id = update['inline_query']['from']['id']
		inline_first_name = update['inline_query']['from']['first_name']
		if inline_text.startswith('panel') and inline_from_id in admins:
			await telegram.AnswerInlineQuery(
			inline_query_id = inline_id,
			cache_time = 0,
			is_personal = True,
			results = json.dumps([{
			'type':'article',
			'id':random.randint(111,999),
			'title':'❦ پنل مدیریت سلف پایتون ❦',
			'thumb_url':'https://t.me/Mafia_nit/156',
			'input_message_content':{
			'message_text':'✰ ᴛʜᴇ ᴘᴀɴᴇʟ ʜᴀs ʙᴇᴇɴ ᴏᴘᴇɴᴇᴅ ғᴏʀ ʏᴏᴜ . . . !',
			'parse_mode':'HTML'
			},
			'reply_markup':{'inline_keyboard':[
			[{'text':'✰ ʟᴏᴄᴋ ᴍᴏᴅᴇs ✰','callback_data':'lockmode-null'},{'text':'✰ ʟᴏᴄᴋ ᴀᴄᴛɪᴏɴs ✰','callback_data':'lockaction-null'}],
			[{'text':'✰ ɪɴғᴏ ✰','callback_data':'info'}],
			[{'text':'✰ ᴄʀᴀsʜ ʟɪsᴛ ✰','callback_data':'list-crash'},{'text':'✰ ᴇɴᴇᴍʏ ʟɪsᴛ ✰','callback_data':'list-enemy'}],
			[{'text':'✰ ʜᴇʟᴘ ✰','callback_data':'help'},{'text':'✰ sᴛᴀᴛᴜs ✰','callback_data':'stats'}],
			[{'text':'✰ ᴇxɪᴛ ✰','callback_data':'exit'},{'text':'✰ ʀᴇsᴛᴀʀᴛ ✰','callback_data':'restart'}],
			]}
			}])
			)

		elif inline_text.startswith('xo') and inline_from_id in admins:
			await telegram.AnswerInlineQuery(
			inline_query_id = inline_id,
			cache_time = 0,
			is_personal = True,
			results = json.dumps([{
			'type':'article',
			'id':random.randint(111,999),
			'title':'❦ بازی دوز پایتون ❦',
			'thumb_url':'https://t.me/Mafia_nit/332',
			'input_message_content':{
			'message_text':'✰ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ sᴛᴀʀᴛ ʙᴜᴛᴛᴏɴ ᴛᴏ sᴛᴀʀᴛ ᴛʜᴇ ɢᴀᴍᴇ . . . !',
			'parse_mode':'HTML'
			},
			'reply_markup':{'inline_keyboard':[
			[{'text':'✰ sᴛᴀʀᴛ ✰','callback_data':'doz-0-0-0-0~0~0~0|0~0~0~0|0~0~0~0|0~0~0~0'}],
			]}
			}])
			)

	elif 'callback_query' in update.keys():
		callback_id = update['callback_query']['id']
		callback_data = update['callback_query']['data']
		callback_message_id = update['callback_query']['inline_message_id']
		callback_from_id = update['callback_query']['from']['id']
		callback_first_name = update['callback_query']['from']['first_name']
		if callback_data.startswith('fake') and callback_from_id in admins:
			await telegram.AnswerCallbackQuery(
			callback_query_id = callback_id,
			text = 'ᴛʜɪs ʙᴜᴛᴛᴏɴ ɪs ғᴏʀ ᴅɪsᴘʟᴀʏɪɴɢ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴏɴʟʏ . . . !',
			show_alert = True
			)

		elif callback_data.startswith('back') and callback_from_id in admins:
			await telegram.AnswerCallbackQuery(
			callback_query_id = callback_id,
			text = 'ᴡᴀɪᴛ . . . !'
			)
			await telegram.EditMessageText(
			text = '➣ ʏᴏᴜ ᴀʀᴇ ʙᴀᴄᴋ ᴛᴏ ᴛʜᴇ ᴍᴀɪɴ ᴍᴇɴᴜ',
			inline_message_id = callback_message_id,
			parse_mode = 'HTML',
			reply_markup = json.dumps({'inline_keyboard':[
			[{'text':'✰ ʟᴏᴄᴋ ᴍᴏᴅᴇs ✰','callback_data':'lockmode-null'},{'text':'✰ ʟᴏᴄᴋ ᴀᴄᴛɪᴏɴs ✰','callback_data':'lockaction-null'}],
			[{'text':'✰ ɪɴғᴏ ✰','callback_data':'info'}],
			[{'text':'✰ ᴄʀᴀsʜ ʟɪsᴛ ✰','callback_data':'list-crash'},{'text':'✰ ᴇɴᴇᴍʏ ʟɪsᴛ ✰','callback_data':'list-enemy'}],
			[{'text':'✰ ʜᴇʟᴘ ✰','callback_data':'help'},{'text':'✰ sᴛᴀᴛᴜs ✰','callback_data':'stats'}],
			[{'text':'✰ ᴇxɪᴛ ✰','callback_data':'exit'},{'text':'✰ ʀᴇsᴛᴀʀᴛ ✰','callback_data':'restart'}],
			]})
			)

		elif callback_data.startswith('info') and callback_from_id in admins:
			await telegram.AnswerCallbackQuery(
			callback_query_id = callback_id,
			text = 'ᴡᴀɪᴛ . . . !'
			)
			await telegram.EditMessageText(
			text = 'ɴɪᴄᴋɴᴀᴍᴇ : ❍➯꯭𝆺𝅥𝅮 ꯭‌ᴛ‌ᴀ‌꯭ᴋ‌꯭+ᴘ‌꯭꯭ᴇ꯭‌s꯭‌꯭ᴀ‌꯭ʀ‌꯭ـٜ۪ٜ۪ٜ۪ٜ۪ٜ۪ٜ۪ٜ۪ٜ۪ٜ۪ٜ۪ٜ۪ٜ۪◌‌✾꯭ᵇᶤ꯭↛꯭ᑋᵉ꯭ˢ ꯭℡꯭꯭ |\nᴜsᴇʀɴᴀᴍᴇ : @AsirRam\nᴘʜᴏɴᴇ : +68279337\nʙɪᴏɢʀᴀᴘʜʏ : 🥀••𝓖𝓸𝓲𝓷𝓰 𝓪𝓷𝓭 𝓫𝓮𝓲𝓷𝓰 𝓲𝓼 𝓫𝓮𝓽𝓽𝓮𝓻 𝓽𝓱𝓪𝓷 𝓼𝓽𝓪𝔂𝓲𝓷𝓰 𝓪𝓷𝓭 𝓫𝓮𝓬𝓸𝓶𝓲𝓷𝓰 𝔀𝓸𝓻𝓽𝓱𝓵𝓮𝓼𝓼!\nᴠᴇʀsɪᴏɴ : 0.2',
			inline_message_id = callback_message_id,
			parse_mode = 'HTML',
			reply_markup = json.dumps({'inline_keyboard':[
			[{'text':'➣ ʙᴀᴄᴋ ➢','callback_data':'back'}]
			]})
			)
		
		elif callback_data.startswith('help') and callback_from_id in admins:
			await telegram.AnswerCallbackQuery(
			callback_query_id = callback_id,
			text = 'ᴡᴀɪᴛ . . . !'
			)
			await telegram.EditMessageText(
			text = 'ʜᴇʟᴘ ᴛᴇxᴛ ɪs ɴᴏᴛ sᴇᴛ . . . !',
			inline_message_id = callback_message_id,
			parse_mode = 'HTML',
			reply_markup = json.dumps({'inline_keyboard':[
			[{'text':'➣ ʙᴀᴄᴋ ➢','callback_data':'back'}]
			]})
			)

		elif callback_data.startswith('stats') and callback_from_id in admins:
			memoryUse = psutil.Process(os.getpid()).memory_info()[0] / 1073741824
			memoryPercent = psutil.virtual_memory()[2]
			cpuPercent = psutil.cpu_percent(3)
			await telegram.AnswerCallbackQuery(
			callback_query_id = callback_id,
			text = f'• ᴍᴇᴍᴏʀʏ ᴜsᴇᴅ : {memoryUse}\n• ᴍᴇᴍᴏʀʏ : {memoryPercent} %\n• ᴄᴘᴜ : {cpuPercent} %',
			show_alert = True
			)

		elif callback_data.startswith('exit') and callback_from_id in admins:
			await telegram.AnswerCallbackQuery(
			callback_query_id = callback_id,
			text = 'ᴡᴀɪᴛ . . . !'
			)
			await telegram.EditMessageText(
			text = '✄ ʏᴏᴜ ʜᴀᴠᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴇxɪᴛᴇᴅ ᴛʜᴇ ᴘᴀɴᴇʟ',
			inline_message_id = callback_message_id,
			parse_mode = 'HTML',
			)

		elif callback_data.startswith('restart') and callback_from_id in admins:
			await telegram.AnswerCallbackQuery(
			callback_query_id = callback_id,
			text = 'ᴡᴀɪᴛ . . . !'
			)
			await kill('source /home/bot/virtualenv/py/3.9/bin/activate && cd /home/bot/py/public','file.py')
			await telegram.EditMessageText(
			text = '✄ ᴛʜᴇ ʀᴇsᴛᴀʀᴛ ᴡᴀs sᴜᴄᴄᴇssғᴜʟ',
			inline_message_id = callback_message_id,
			parse_mode = 'HTML',
			)

		elif callback_data.startswith('lockmode-') and callback_from_id in admins:
			mode = callback_data.split('-')[1]
			if not mode == 'null':
				js = await get("data.json")
				js[mode] = str('off' if js[mode] == 'on' else 'on')
				await put("data.json",js)
			await telegram.AnswerCallbackQuery(
			callback_query_id = callback_id,
			text = 'ᴡᴀɪᴛ . . . !'
			)
			js = await get("data.json")
			keyboard = [[{'text':'✅' if js[text] == 'on' else '❌','callback_data':'lockmode-' + text},{'text':'✰ ' + await font(text) + ' ✰','callback_data':'fake'}] for text in ['hashtag','bold','italic','delete','code','underline','reverse','part','mention','spoiler']]
			keyboard.append([{'text':'➣ ʙᴀᴄᴋ ➢','callback_data':'back'}])
			await telegram.EditMessageText(
			text = '✎﹏﹏﹏ ᴏғғ / ᴏɴ ᴍᴏᴅᴇs ᴘᴀɴᴇʟ',
			inline_message_id = callback_message_id,
			parse_mode = 'HTML',
			reply_markup = json.dumps({'inline_keyboard':keyboard})
			)

		elif callback_data.startswith('lockaction-') and callback_from_id in admins:
			mode = callback_data.split('-')[1]
			if not mode == 'null':
				js = await get("data.json")
				js[mode] = str('off' if js[mode] == 'on' else 'on')
				await put("data.json",js)
			await telegram.AnswerCallbackQuery(
			callback_query_id = callback_id,
			text = 'ᴡᴀɪᴛ . . . !'
			)
			js = await get("data.json")
			keyboard = [[{'text':'✅' if js[text] == 'on' else '❌','callback_data':'lockaction-' + text},{'text':'✰ ' + await font(text) + ' ✰','callback_data':'fake'}] for text in ['typing','game','voice','video','sticker']]
			keyboard.append([{'text':'➣ ʙᴀᴄᴋ ➢','callback_data':'back'}])
			await telegram.EditMessageText(
			text = '✎﹏﹏﹏ ᴏғғ / ᴏɴ ᴀᴄᴛɪᴏɴs ᴘᴀɴᴇʟ',
			inline_message_id = callback_message_id,
			parse_mode = 'HTML',
			reply_markup = json.dumps({'inline_keyboard':keyboard})
			)

		elif callback_data.startswith('list-') and callback_from_id in admins:
			type = callback_data.split('-')[1]
			await telegram.AnswerCallbackQuery(
			callback_query_id = callback_id,
			text = 'ᴡᴀɪᴛ . . . !'
			)
			mylist = await font(type) + " ʟɪsᴛ :\n"
			js = await get("data.json")
			if js[type]:
				for i in js[type]:
					mylist += f"\n• <a href ='tg://user?id={i}'>{i}</a>"
			else:
				mylist += f"\nᴛʜᴇ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ !"
			await telegram.EditMessageText(
			text = mylist,
			inline_message_id = callback_message_id,
			parse_mode = 'HTML',
			reply_markup = json.dumps({'inline_keyboard':[
			[{'text':'➣ ʙᴀᴄᴋ ➢','callback_data':'back'}]
			]})
			)

		elif callback_data.startswith('doz-'):
			exp = callback_data.split('-')
			rows = exp[1]
			columns = exp[2]
			id = exp[3]
			zero_one = exp[4]
			if int(callback_from_id) == int(id):
				await telegram.AnswerCallbackQuery(
				callback_query_id = callback_id,
				text = 'ɪᴛ ɪs ɴᴏᴛ ʏᴏᴜʀ ᴛᴜʀɴ . . . !',
				show_alert = True
				)
			else:
				open = [x.split('~') for x in zero_one.split('|')]
				if int(id):
					if open[int(rows)][int(columns)] == '0':
						open[int(rows)][int(columns)] = 'X' if callback_from_id in admins else 'O'
					else:
						await telegram.AnswerCallbackQuery(
						callback_query_id = callback_id,
						text = 'ʏᴏᴜ ᴄᴀɴ ɴᴏᴛ sᴇʟᴇᴄᴛ ᴛʜɪs ʙᴜᴛᴛᴏɴ . . . !',
						show_alert = True
						)
						return {'error':'exit'}
				await telegram.AnswerCallbackQuery(
				callback_query_id = callback_id,
				text = 'ᴡᴀɪᴛ . . . !'
				)
				close = '|'.join(['~'.join(x) for x in open])
				keyboard = [[{'text':open[row][column] if open[row][column] != '0' else ' ','callback_data':f'doz-{row}-{column}-{callback_from_id}-{close}'} for column in range (4)] for row in range(4)]
				await telegram.EditMessageText(
				text = '▌│█║▌║▌║ ᴛɪᴄ-ᴛᴀᴄ-ᴛᴏᴇ / xᴏ ║▌║▌║█│▌',
				inline_message_id = callback_message_id,
				parse_mode = 'HTML',
				reply_markup = json.dumps({'inline_keyboard':keyboard})
				)
	return update

if __name__ == '__main__':
	app.run(port = 80)