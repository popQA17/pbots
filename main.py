import os
from flask import Flask, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization

app = Flask(__name__)

app.secret_key = b"%\xe0'\x01\xdeH\x8e\x85m|\xb3\xffCN\xc9g"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"    # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = 10000000
app.config["DISCORD_CLIENT_SECRET"] = ""
app.config["DISCORD_BOT_TOKEN"] = ""
app.config["DISCORD_REDIRECT_URI"] = "https://localhost/callback"

discord = DiscordOAuth2Session(app)


HYPERLINK = '<a href="{}">{}</a>'


def welcome_user(user):
    dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
    )


@app.route("/")
def index():
    return render_template('index.html', discord=discord)


@app.route("/login/")
def login():
    return discord.create_session()
@app.route("/callback/")
def callback():
    data = discord.callback()
    user = discord.fetch_user()

    return redirect(url_for("index"))


@app.route('/lookup')
def lookup():
  if discord.authorized:
    return render_template('user.html', discord=discord)
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




if __name__ == "__main__":
    app.run(host="0.0.0.0")
