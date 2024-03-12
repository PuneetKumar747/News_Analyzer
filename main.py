from flask import Flask, render_template, request,jsonify,url_for,redirect,session
from authlib.integrations.flask_client import OAuth
from bs4 import BeautifulSoup
import nltk as nl
import json
import psycopg2
import requests
import urllib.request
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
nl.download('averaged_perceptron_tagger')
nl.download("stopwords")
nl.download("punkt")
nl.download('universal_tagset')
# Initialize Flask app
app = Flask(__name__, template_folder='templates')

oauth =OAuth(app)
app.config['SECRET_KEY'] = 'Puneet'
app.config['GITHUB_CLIENT_ID'] ="33925839a7b51db0d714"
app.config['GITHUB_CLIENT_SECRET'] = '22b9b8294e3e669fd14166c2c24a2d3391deceb4'
github = oauth.register(name ='github',client_id = app.config['GITHUB_CLIENT_ID'],client_secret=app.config["GITHUB_CLIENT_SECRET"],access_token_url = 'https://github.com/login/oauth/access_token',access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

conn=psycopg2.connect(
    host="dpg-cnmnrf2cn0vc738f4j60-a",database='puneet_kumar',user='puneet_kumar_user',password='jFa3zNVSR8AQcQpLo7HAlQxwFxl1CGAn', port="5432"
)
cur=conn.cursor()

# create News_Summary table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS News_Summary(
        ID SERIAL PRIMARY KEY,
        News_Text TEXT NOT NULL,
        No_of_Sentence INT NOT NULL,
        No_of_Words INT NOT NULL,
        No_of_Pos_Tag JSON NOT NULL,
        Type_of_News TEXT NOT NULL,
        URL TEXT NOT NULL
    )
''')
conn.commit()
admin_password = 'admin4567'
# Function to extract and process content
def extract_and_process_content(url):
    try:
        with urllib.request.urlopen(url) as response:
            html_content= response.read().decode('utf-8')
        soup = BeautifulSoup(html_content, "html.parser")
        
        main_title = soup.find('h1', class_='jsx-ace90f4eca22afc7 Story_strytitle__MYXmR').text

        # Removing specified div elements
        auth_date = soup.find('div', class_='published__on')
        date_text = auth_date.text.strip().split(':')[1]
        for div in soup.find_all('div', class_=['authors__container', 'tab-link']):
            div.decompose()
        for fox in soup.find_all('div', id=['tab-link-wrapper-plugin', '1']):
            fox.decompose()

        main_content = soup.find('div', class_='jsx-ace90f4eca22afc7 Story_description__fq_4S description paywall').text
        clean_text = ''
        for line in nl.sent_tokenize(main_content):
            line.strip()
            clean_text += line

        news_text = main_title + clean_text

        # Summarize the News Text
        parser = PlaintextParser.from_string(news_text,Tokenizer('english'))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document,sentences_count=15)
        News_summary = ''.join([str(sentence)for sentence in summary])

        space_text = ''
        for char in news_text:
            if char == ".":
                space_text += char + " "
            else:
                space_text += char
        no_of_sentence = len(nl.sent_tokenize(space_text))

        count = 0
        for char in news_text:
            if char not in ["/", ",", ".", "?", "(", ")", "'", "``", "''", "\n", '""']:
                count += 1
        no_of_words = count

        pos_word = nl.word_tokenize(news_text)
        pos_tag_dict = {}
        # if len(pos_tag_dict)<6:
        for word,verb in nl.pos_tag(pos_word, tagset="universal"):
            if len(pos_tag_dict)<8:
                if word.isalpha():
                    if verb in pos_tag_dict:
                        pos_tag_dict[verb] += 1
                    else:
                        pos_tag_dict[verb] = 1
                else:
                    pass
            else:
        
                no_of_pos_tag_json = json.dumps(pos_tag_dict)


        dict2 = {
            'Politics': ["Government", "Elections", "Policies", "Legislation", "Political_parties", "presidents",
                        "prime_ministers"],
            'Business': ["Companies", "Stockmarket", "Economy", "Finance", "Business_leaders"],
            'Technology': ['Innovation', 'Gadgets', 'Software', 'Startups', 'Artificial intelligence', 'Facebook',
                        "Instagram", 'Whatsapp', "Twitter"],
            'Health': ["Diseases", "Medical research", "Healthcare system", "Vaccines", "Public health", "Wellness"],
            'Environment': ["Climate change", "Conservation", "Renewable energy", "Pollution", "Natural disasters",
                            "Environmental policies"],
            'Entertainment': ["Celebrities", "Movies", "Music", "Television", "Awards", "Entertainment industry",
                            'Bollywood', 'Hollywood', 'Tollywood'],
            'Sports': ["Teams", "Athletes", "Matches", "Tournaments", "Championships", "Sports events"]
        }

        category = 'Unknown'
        for key, value in dict2.items():
            for word in value:
                if word.lower() in news_text.lower():
                    category = key
                    break
            if category != 'Unknown':
                break
        type_of_news = category

        return news_text,no_of_sentence, no_of_words, no_of_pos_tag_json, type_of_news, News_summary, date_text
    except:
        return "Error in extracting and processing content"

@app.route('/')
def index():
    return render_template('search_form.html')
@app.route("/submit", methods=["POST", "GET"])
def search():
        if request.method == "POST":
            url = request.form["url"]
            try:
                if 'https://www.indiatoday.in/' not in url:
                    error = 'Please provide india today news article URL ONLY'
                    return render_template('search_form.html',error = error)
                news_text,no_of_sentence, no_of_words, no_of_pos_tag_json, type_of_news, News_summary, date_text = extract_and_process_content(url)
        
                # Insert data into the News_Summary table
                cur.execute('''
                    INSERT INTO News_Summary(News_Text, No_of_Sentence, No_of_Words, No_of_Pos_Tag, Type_of_News, URL)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (news_text, no_of_sentence, no_of_words, no_of_pos_tag_json, type_of_news, url))
                conn.commit()

                return render_template("display_table.html", msg_data=[(News_summary, no_of_sentence, no_of_words, no_of_pos_tag_json, type_of_news, date_text)])
            except Exception as e:

                error_message = str(e)
                return render_template('search_form.html',error =error_message)
            
        return render_template('search_form.html')


    
# return render_template("search_form.html",)
@app.route('/history', methods = ['GET'])
def get_history():
    return render_template('admin.html')

@app.route("/history",methods=['POST'])
def post_history():
    # print(request.form["password"])
    # if request.json.get('password') == admin_password:
    if request.form["password"] == admin_password:
        cur.execute('SELECT * FROM News_Summary order by ID DESC ')
        his_data = cur.fetchall()
        return render_template('History.html',his_data=his_data)
    else:
        return jsonify('Unauthorizes access')
# to come on home page
@app.route('/', methods = ['GET'])
def come_back():
    return render_template('search_form.html')
# Github login route
@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)
# Github authorize route
@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    session['github_token'] = token
    resp = github.get('user').json()
    print(f"\n{resp}\n")

    cur.execute("SELECT * FROM News_summary order by ID DESC")
    data = cur.fetchall()

    conn.close()

    return render_template('History.html', his_data= data)
    # Redirect to a template or another route after successful authorization

# Logout route for GitHub
@app.route('/logout/github')
def github_logout():
    session.pop('github_token', None)
    return redirect(url_for('index1'))


if __name__ == "__main__":
    app.run(debug=True)
