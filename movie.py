from flask import Flask, request, render_template
import pickle
import requests

app = Flask(__name__)

# Load the pickled similarity model and movie list
similarity = pickle.load(open('model/similarity.pkl', 'rb'))
movies_list = pickle.load(open('model/movies_list.pkl', 'rb'))

# TMDb API key
TMDB_API_KEY = '0167a498988cfd618c0f07a5c87d927f'  # Replace with your TMDb API key

# Function to fetch the poster path
def fetch_poster(movie_name):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}'
    response = requests.get(url).json()
    results = response.get('results', [])
    if results:
        poster_path = results[0].get('poster_path')
        return poster_path
    return None


movie_titles = movies_list['title'].values


@app.route('/')
def home():
    return render_template('home.html', movies=movie_titles)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/bolly')
def bolly():
    return render_template('bolly.html')

@app.route('/holly')
def holly():
    return render_template('holly.html')

@app.route('/cartoon')
def cartoon():
    return render_template('cartoon.html')

@app.route('/user_profiles')
def user_profiles():
    return render_template('user_profiles.html')

@app.route('/social_sharing')
def social_sharing():
    return render_template('social_sharing.html')

@app.route('/thank')
def thank():
    return render_template('thank.html')

@app.route('/me')
def me():
    return render_template('me.html')

@app.route('/submit', methods=['POST'])
def submit():
    
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    
    with open('contact_submissions.txt', 'a') as file:
        file.write(f'Name: {name}\n')
        file.write(f'Email: {email}\n')
        file.write(f'Message: {message}\n')
        file.write('-' * 40 + '\n')  # Add a separator line for readability
    
    return 'Thank you for your submission!'

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    bot_response = get_bot_response(user_message)
    return render_template('index.html', user_message=user_message, bot_response=bot_response)

def get_bot_response(message):
    message = message.lower()
    if 'recommend' in message:
        return 'I can suggest some great movies for you. What genre do you like?'
    elif 'hello' in message or 'hi' in message or 'hey' in message:
        return 'Hello! How can I assist you today?'
    elif 'thank you' in message or 'thankyou' in message:
        return 'You’re welcome!'
    elif 'movie' in message or 'what is your work?' in message:
        return 'I can provide information on movies. What would you like to know?'
    elif 'education' in message or 'student' in message:
        return 'Some movies related to education are: 1. Like Stars on Earth · 2. The Hunt · 3. 3 Idiots · 4. Whiplash · 5. A Beautiful Mind · 6. 127 Hours'
    elif 'romantic' in message or 'love' in message:
        return 'Some suggested romantic movies are: 1. The Crow · 2. It Ends with Us · 3. The Fall Guy · 4. Wicked · 5. Anyone But You · 6. Hit Man · 7. Queer · 8. Poor Things.'
    elif 'science' in message or 'fiction' in message:
        return 'Some suggested science fiction movies are: 1. Deadpool & Wolverine · 2. Alien: Romulus · 3. Uglies · 4. Venom: The Last Dance · 5. Furiosa: A Mad Max Saga · 6. Borderlands.'
    elif 'best' in message:
        return 'Some of the best movies are: 1. The Shawshank Redemption · 2. The Godfather · 3. The Dark Knight · 4. The Godfather Part II · 5. 12 Angry Men'
    elif 'who are you?' in message:
        return 'I am a movie chatbot created by Nisha ❤'
    elif 'best bollywood' in message or 'bollywood movies' in message:
        return 'Some of the best Bollywood movies are: 1. Mission Raniganj: The Great Bharat Rescue · 2. Kho Gaye Hum Kahan · 3. 12th Fail · 4. Gumraah · 5. Bhakshak · 6. Khufiya · 7. Murder Mubarak · 8. Article 370'
    elif 'disney' in message or 'snow white' in message:
        return 'Some popular Disney movies are: 1. Tangled · 2. The Princess and the Frog · 3. Beauty and the Beast · 4. Monsters, Inc. · 5. Aladdin'
    else:
        return 'I am not sure how to respond to that. Can you please ask something else?'


@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie']
    index = movies_list[movies_list['title'] == movie_name].index[0]

    
    distances = similarity[index]

    
    recommended_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
    recommended_movie_details = []
    for i in recommended_movies:
        movie_title = movies_list.iloc[i[0]].title
        poster_path = fetch_poster(movie_title)
        recommended_movie_details.append({'title': movie_title, 'poster_path': poster_path})

    return render_template('output.html', movies_and_posters=recommended_movie_details, selected_movie=movie_name)



if __name__ == '__main__':
    app.run(debug=True)
