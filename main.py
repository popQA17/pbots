text = """
======================================================                                             
,-.----.                                              
\    /  \                          ___                
|   :    \   ,---,               ,--.'|_              
|   |  .\ :,---.'|      ,---.    |  | :,'             
.   :  |: ||   | :     '   ,'\   :  : ' :  .--.--.    
|   |   \ ::   : :    /   /   |.;__,'  /  /  /    '   
|   : .   /:     |,-..   ; ,. :|  |   |  |  :  /`./   
;   | |`-' |   : '  |'   | |: ::__,'| :  |  :  ;_     
|   | ;    |   |  / :'   | .; :  '  : |__ \  \    `.  
:   ' |    '   : |: ||   :    |  |  | '.'| `----.   \ 
:   : :    |   | '/ : \   \  /   ;  :    ;/  /`--'  / 
|   | :    |   :    |  `----'    |  ,   /'--'.     /  
`---'.|    /    \  /              ---`-'   `--'---'   
  `---`    `-'----'       
======================================================                            

"""
print(text)
import os
import time
time.sleep(0.5)
from config import token, client_secret, client_id, redirect_uri, mongodb_uri
print("[Pbots] Config file read")
time.sleep(0.5)
from flask import Flask, redirect, url_for, render_template, request
from flask_discord import DiscordOAuth2Session, requires_authorization
import pymongo, dns
import logging
from pymongo import MongoClient
from flask_turbolinks import turbolinks
from flask_socketio import SocketIO, emit
print("[Pbots] All imports completed")
client = MongoClient(mongodb_uri)
data = client.botdata2
bots = data["bots"]
time.sleep(0.5)
print("[Pbots] Databases loaded")
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
app.secret_key = b"%\xe0'\x01\xdeH\x8e\x85m|\xb3\xffCN\xc9g"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

<<<<<<< HEAD
app.config["DISCORD_CLIENT_ID"] = client_id
app.config["DISCORD_CLIENT_SECRET"] = client_secret
app.config["DISCORD_BOT_TOKEN"] = token
=======
app.config["DISCORD_CLIENT_ID"] = 10000000
app.config["DISCORD_CLIENT_SECRET"] = ""
app.config["DISCORD_BOT_TOKEN"] = ""
app.config["DISCORD_REDIRECT_URI"] = "https://localhost/callback"
>>>>>>> origin/master

app.config["DISCORD_REDIRECT_URI"] = redirect_uri
time.sleep(0.5)
print("{Pbots] Flask-discord configured.")
socketio = SocketIO(app)
turbolinks(app)
discord = DiscordOAuth2Session(app)
HYPERLINK = '<a href="{}">{}</a>'


def welcome_user(user):
    dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
    )


@app.route("/")
def index():
    return render_template('index.html', bots = bots, discord=discord)
@app.route('/unfeature/<int:botid>')
def unfeature(botid):
  user = discord.fetch_user()
  userapi = discord.bot_request(f"/guilds/875172026195783751/members/{user.id}")
  roles = userapi['roles']
  counter = 0
  for role in roles:
    role= int(role)
    if role == 875172026577453101 or role == 875172026577453100 or role == 878658001202991155 or role == 878658328765558897:
      counter += 1
  if counter == 0:
    return redirect(url_for('index'))
  myquery = { "botid": str(botid) }
  bot = bots.find_one({'botid': str(botid)})
  newvalues = { "$set": { "featured": "false" } }
  bots.update_one(myquery, newvalues)
  dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": bot['ownerid']})
  message = {
      "content": "Signed, Pbots.",
      "tts": False,
      "embeds": [{
      "title": f"Your bot "+ bot['bot']+" has been sadly removed from the Feature list.",
      "description": f"**Reviewer:**\n {user.name}\n\n **Bot:**\n" + bot['bot']
    }]
  }
  discord.bot_request(f"/channels/{dm_channel['id']}/messages", "POST", json=message)
  return redirect(url_for('admin'))
@app.route('/feature/<int:botid>')
def feature(botid):
  user = discord.fetch_user()
  userapi = discord.bot_request(f"/guilds/875172026195783751/members/{user.id}")
  roles = userapi['roles']
  counter = 0
  for role in roles:
    role= int(role)
    if role == 875172026577453101 or role == 875172026577453100 or role == 878658001202991155 or role == 878658328765558897:
      counter += 1
  if counter == 0:
    return redirect(url_for('index'))
  myquery = { "botid": str(botid) }
  bot = bots.find_one({'botid': str(botid)})
  newvalues = { "$set": { "featured": "yes" } }
  bots.update_one(myquery, newvalues)
  dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": bot['ownerid']})
  message = {
      "content": "Signed, Pbots.",
      "tts": False,
      "embeds": [{
      "title": f"Your bot "+ bot['bot']+" is featured on Pbots!",
      "description": f"**Reviewer:**\n {user.name}\n\n **Bot:**\n" + bot['bot']
    }]
  }
  discord.bot_request(f"/channels/{dm_channel['id']}/messages", "POST", json=message)
  return redirect(url_for('admin'))
@app.route('/approve/<int:botid>')
def approve(botid):
  user = discord.fetch_user()
  userapi = discord.bot_request(f"/guilds/875172026195783751/members/{user.id}")
  roles = userapi['roles']
  counter = 0
  for role in roles:
    role = int(role)
    if role == 875172026577453101 or role == 875172026577453100 or role == 878658001202991155 or role == 878658328765558897:
      counter += 1
  if counter == 0:
    return redirect(url_for('index'))
  myquery = { "botid": str(botid) }
  result = bots.find_one({'botid': str(botid)})
  newvalues = { "$set": { "status": "approved" } }
  bots.update_one(myquery, newvalues)
  dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": result['ownerid']})
  message = {
      "content": "Signed, Pbots.",
      "tts": False,
      "embeds": [{
      "title": f"Your bot "+ result['bot']+" was approved!",
      "description": f"**Reviewer:**\n {user.name}\n\n **Bot:**\n" + result['bot']
      }]
  }
  discord.bot_request(f"/channels/{dm_channel['id']}/messages", "POST", json=message)
  return redirect(url_for('admin'))

@app.route('/deny/<int:botid>', methods=['POST', 'GET'])
def deny(botid):
  user = discord.fetch_user()
  userapi = discord.bot_request(f"/guilds/875172026195783751/members/{user.id}")
  roles = userapi['roles']
  counter = 0
  for role in roles:
    if role == "875172026577453101" or role == "875172026577453100" or role == "878658001202991155" or role == "878658328765558897":
      counter += 1
  if counter == 0:
    return redirect(url_for('index'))
  if request.method == "POST":
    reason = request.form['reason']
    bot = bots.find_one({'botid': str(botid)})
    dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": bot['ownerid']})
    message = {
      "content": "Signed, Pbots.",
      "tts": False,
      "embeds": [{
      "title": f"Your bot"+  bot['bot']+" was denied.",
      "description": f"**Reviewer:**\n {user.name}\n\n **Bot:**\n"+bot['bot']+f"\n\n **Reason:**\n{reason} "
      }]
    }
    discord.bot_request(f"/channels/"+dm_channel['id']+f"/messages", "POST", json=message)
    bots.delete_one({"botid": bot['botid']})
    return redirect(url_for('admin'))
  return render_template('deny.html', discord=discord, user=user, bots=bots)
@app.route('/adelete/<int:botid>', methods=['POST', 'GET'])
def adelete(botid):
  user = discord.fetch_user()
  userapi = discord.bot_request(f"/guilds/875172026195783751/members/{user.id}")
  roles = userapi['roles']
  counter = 0
  for role in roles:
    if role == "875172026577453101" or role == "875172026577453100" or role == "878658001202991155" or role == "878658328765558897":
      counter += 1
  if counter == 0:
    return redirect(url_for('index'))
  if request.method == "POST":
    reason = request.form['reason']
    bot = bots.find_one({'botid': str(botid)})
    dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": bot['ownerid']})
    message = {
      "content": "Signed, Pbots.",
      "tts": False,
      "embeds": [{
      "title": f"Your bot"+  bot['bot']+" was deleted from Pbots.",
      "description": f"**Reviewer:**\n {user.name}\n\n **Bot:**\n"+bot['bot']+f"\n\n **Reason:**\n{reason} "
      }]
    }
    discord.bot_request(f"/channels/"+dm_channel['id']+f"/messages", "POST", json=message)
    bots.delete_one({"botid": bot['botid']})
    return redirect(url_for('admin'))
  return render_template('adelete.html', discord=discord, user=user, bots=bots)
@app.route("/login/")
def login():
    return discord.create_session(scope=["identify", "guilds"])
@app.route("/callback/")
def callback():
    data = discord.callback()
    user = discord.fetch_user()

    return redirect(url_for("index"))
@app.route('/me')
def me():
  if not discord.authorized:
    return redirect(url_for('index'))
  user = discord.fetch_user()
  userapi = discord.bot_request(f"/guilds/875172026195783751/members/{user.id}")
  roles = userapi['roles']
  counter = 0
  for role in roles:
    role=int(role)
    if role == 875172026577453101 or role == 875172026577453100 or role == 878658001202991155 or role == 878658328765558897:
      counter += 1
  if counter == 0:
    admin = False
  else:
    admin = True
  botuser = bots.find({'ownerid': str(user.id)})
  return render_template('me.html', admin=admin, discord=discord, bots=botuser, user=user)
@app.route('/me/config')
def meconfig():
  if not discord.authorized:
    return redirect(url_for('index'))
  user = discord.fetch_user()
  userapi = discord.bot_request(f"/guilds/875172026195783751/members/{user.id}")
  roles = userapi['roles']
  counter = 0
  for role in roles:
    role = int(role)
    if role == 875172026577453101 or role == 875172026577453100 or role == 878658001202991155 or role == 878658328765558897:
      counter += 1
  if counter == 0:
    admin = False
  else:
    admin = True
  botuser = bots.find({'owner': str(user.id)})
  return render_template('meconfig.html', admin=admin, discord=discord, bots=botuser, user=user)
@app.route('/admin')
def admin():
  if not discord.authorized:
    return redirect(url_for('index'))
  user = discord.fetch_user()
  userapi = discord.bot_request(f"/guilds/875172026195783751/members/{user.id}")
  roles = userapi['roles']
  counter = 0
  for role in roles:
    if role == 875172026577453101 or role == 875172026577453100 or role == 878658001202991155 or role == 878658328765558897:
      counter += 1
  if counter == 0:
    admin = False
  else:
    admin = True
  return render_template('admin.html', admin=admin, discord=discord, bots=bots, user=user)

@app.route('/add-bot/')
def addbot():
  if discord.authorized:
    return render_template('addbot.html', discord=discord)
  else:
    return redirect(url_for('index'))
  
@app.route('/lookup/<int:userid>/')
def lookupuser(userid):
  if discord.authorized:
    result = discord.bot_request(f"/users/{userid}", "GET")
    print(result)
    if result == None:
      return redirect(url_for('lookupuser'))
    try:
      bot = result["bot"]
    except:
      bot = "False"
    return render_template('looked.html', discord=discord, name=result["username"], bot=bot, avatar=result['avatar'], full=result)
@app.route("/logout/")
def logout():
    discord.revoke()
    return redirect(url_for(".index"))
@app.route('/bot/<int:botid>/edit')
def edit(botid):
  user = discord.fetch_user()
  bot = bots.find_one({"botid": str(botid)})
  if bot is None:
    return redirect(url_for('index'))
  userapi = discord.bot_request(f"/guilds/875172026195783751/members/{user.id}")
  roles = userapi['roles']
  counter = 0
  for role in roles:
    role= int(role)
    if role == 875172026577453101 or role == 875172026577453100 or role == 878658001202991155 or role == 878658328765558897:
      counter += 1
    if bot['ownerid'] == str(user.id):
      counter += 1
  if counter == 0:
    return redirect(url_for('index'))
  return render_template('edit.html', discord=discord, bot=bot)
@socketio.on('deletebot')
def delete(data):
  bots.delete_one({'bot': data['bot']})
  return emit('success', {'message': "Your bot has been deleted."})
@socketio.on('submitbot')
def submit(data):
    user = discord.fetch_user()
    userid = data["id"] 
    result = discord.bot_request(f"/users/{userid}", "GET")
    try:
      bot = result['bot']
    except:
      return emit('error', {'error': "The user you submited does not exist, or isn't a bot."})
    if bots.find_one({"botid": str(userid)}) is not None:
            return emit('error', {'error': "That bot already exists in our system."})
    
    payload = {
      "ownerid": str(user.id),
      "owner": user.name,
      "owneravatar": user.avatar_url,
      "ownerdiscriminator": user.discriminator,
      "status": "unapproved",
      "shortdesc": data["shortdesc"],
      "prefix": data["prefix"],
      "longdesc": data["longdesc"],
      "bot": result['username'],
      'botid': userid,
      "botdiscriminator": result['discriminator'],
      'botavatar': f"https://cdn.discordapp.com/avatars/{userid}/" + result['avatar'],
      "votes": 0,
      "featured": "false",
      "invite": data["invite"],
      "website": data["website"],
      "banner": data["banner"]
    }
    bots.insert_one(payload)
    return emit('submitted')
@socketio.on('editbot')
def edit(data):
    user = discord.fetch_user()
    userid = data["id"] 
    bot = bots.find_one({'botid': str(data['id'])})
    payload = {
      "shortdesc": data["shortdesc"],
      "prefix": data["prefix"],
      "longdesc": data["longdesc"],
      "invite": data["invite"],
      "website": data["website"],
      'votes': bot['votes'],
      "banner": data["banner"]
    }
    newvalues = { "$set": payload}
    bots.update_one({"botid": userid}, newvalues)
    return emit('submitted')

@app.route('/bot/<int:botid>')
def botpage(botid):
  bot = bots.find_one({"botid": str(botid)})
  if bot is None:
    return redirect(url_for("index"))
  user = discord.fetch_user()
  bot = bots.find_one({"botid": str(botid)})
  if bot is None:
    return redirect(url_for('index'))
  userapi = discord.bot_request(f"/guilds/875172026195783751/members/{user.id}")
  roles = userapi['roles']
  counter = 0
  for role in roles:
    role= int(role)
    if role == 875172026577453101 or role == 875172026577453100 or role == 878658001202991155 or role == 878658328765558897:
      counter += 1
    if bot['ownerid'] == str(user.id):
      counter += 1
  if counter == 0:
    staff = False
  else:
    staff = True
  return render_template("botpage.html", staff=staff, discord=discord, bots=bots, bot=bot)
if __name__ == "__main__":
<<<<<<< HEAD
    print('[Pbots] Website is now running')
    socketio.run(app, host='0.0.0.0', port=8080)
=======
    app.run(host="0.0.0.0")
>>>>>>> origin/master
