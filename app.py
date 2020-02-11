from flask import Flask, render_template, request, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import pymongo
import tweepy
import os

from secret import api_key, api_secret, access_token, access_token_secret
from histogram import *
import source_text

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
# Creating Tweepy API object
tweet = tweepy.API(auth)

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/TweetGen')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
favorites = db.favorites
# generators = db.generators


# Create a tweet
def tweet_sentence(random_sentence_lol):
    try:
        just_tweeted = tweet.update_status(random_sentence_lol)
        return just_tweeted.id_str
    except:
        return "ERR"


def tweet_it():
    """ Function for test purposes. """
    for faved_tweet in favorites.find():
        if "tweeted" not in faved_tweet:
            new_id = tweet_sentence(faved_tweet['tweet'])
            if new_id == 'ERR':
                faved_tweet["tweeted"] = False
            else:
                faved_tweet["status_id"] = new_id
                faved_tweet["tweeted"] = True
            print(new_id)
            favorites.update_one(
                {'_id': faved_tweet["_id"]},
                {'$set': faved_tweet})
            break
        else:
            print('already tweeted')


auto_tweet = BackgroundScheduler(daemon=True)
one_min = datetime.now() + timedelta(minutes=1)
auto_tweet.add_job(tweet_it, 'interval', hours=24, next_run_time=one_min)
auto_tweet.start()


# def url_for_tweets():
#     continue_search = False
#     for faved_tweet in favorites.find():
#         if "status_id" not in faved_tweet:
#             continue_search = True
#     if continue_search:
#         for status_o in tweepy.Cursor(tweet.user_timeline, screen_name='@nicc_bot', tweet_mode="extended").items():
#             status = status_o._json
#             for faved_tweet in favorites.find():
#                 if "status_id" not in faved_tweet:
#                     if faved_tweet['tweet'] == status["full_text"]:
#                         faved_tweet["status_id"] = status["id_str"]
#                         favorites.update_one(
#                             {'_id': faved_tweet["_id"]},
#                             {'$set': faved_tweet})
#                         print(f"***Found id for: {status['full_text']}***")
#     else:
#         print("all tweets found have ID")
#     print('done')

# hobo johnson histogram
cuco_hist = Histogram(source_text.cuco)
cuco_gen = {
    'url': 'cuco',
    'name': "Cuco",
    'description': "Generates Cuco bars!"
}

# hobo johnson histogram
hobo_hist = Histogram(source_text.hobo_johnson)
hobo_gen = {
    'url': 'hobo_johnson',
    'name': "Hobo Johnson",
    'description': "Generates Hobo Johnson bars!"
}

# reddit trip report histogram
trip_hist = Histogram(source_text.reddit_trip_reports)
trip_gen = {
    'url': 'trip_report',
    'name': "Trip Report",
    'description': "Generates trip reports :)"
}
gens = [cuco_gen, hobo_gen, trip_gen]


@app.route('/', methods=['POST', 'GET'])
def show_all():
    ''' show all histograms '''
    return render_template('index.html', generators=gens, title='Tweet Generator')


@app.route('/generator/cuco', methods=['POST', 'GET'])
def cuco_music():
    if request.form.get('intent') == 'TWEET':
        fav_tweet = {
            'tweet': cuco_gen['rand_sentence'],
            'time': datetime.now().strftime('%-d %b %Y, %-I:%M %p'),
            'name': cuco_gen['name'],
            'gen_url': cuco_gen['url']
        }
        favorites.insert_one(fav_tweet)
        cuco_gen['intent'] = 'TWEET'
    else:
        cuco_gen['rand_sentence'] = random_sentence(cuco_hist.markov_chain)
        cuco_gen['intent'] = 'REFRESH'
    return render_template('show_generator.html', generator=cuco_gen, title=cuco_gen['name'])


@app.route('/generator/trip_report', methods=['POST', 'GET'])
def trip_report():
    if request.form.get('intent') == 'TWEET':
        fav_tweet = {
            'tweet': trip_gen['rand_sentence'],
            'time': datetime.now().strftime('%-d %b %Y, %-I:%M %p'),
            'name': trip_gen['name'],
            'gen_url': trip_gen['url']
        }
        favorites.insert_one(fav_tweet)
        trip_gen['intent'] = 'TWEET'
    else:
        trip_gen['rand_sentence'] = random_sentence(trip_hist.markov_chain)
        trip_gen['intent'] = 'REFRESH'
    return render_template('show_generator.html', generator=trip_gen, title=trip_gen['name'])


@app.route('/generator/hobo_johnson', methods=['POST', 'GET'])
def hobo_johnson():
    if request.form.get('intent') == 'TWEET':
        fav_tweet = {
            'tweet': hobo_gen['rand_sentence'],
            'time': datetime.now().strftime('%-d %b %Y, %-I:%M %p'),
            'name': hobo_gen['name'],
            'gen_url': hobo_gen['url']
        }
        favorites.insert_one(fav_tweet)
        hobo_gen['intent'] = 'TWEET'
    else:
        hobo_gen['rand_sentence'] = random_sentence(hobo_hist.markov_chain)
        hobo_gen['intent'] = 'REFRESH'
    return render_template('show_generator.html', generator=hobo_gen, title=hobo_gen['name'])


@app.route('/favs')
def favorite():
    return render_template('favs.html', tweets=favorites.find().sort("time",pymongo.DESCENDING), title="Favorites!")


@app.route('/favs/<tweet_id>/delete', methods=['POST'])
def delete_fav(tweet_id):
    favorites.delete_one({'_id': ObjectId(tweet_id)})
    return redirect(url_for('favorite'))


# @app.route('/generator', methods=['POST', 'GET'])
# def histogram_saved():
#     generator = Histogram(request.form.get('source_text'))
#     new_generator = {
#         'name': request.form.get('name'),
#         'description': request.form.get('desc'),
#         'word_list': generator.word_list,
#         'types': generator.total_types,
#         'tokens': generator.total_tokens
#     }
#     generator_id = generators.insert_one(new_generator).inserted_id
#     return redirect(url_for('show_generator', generator_id=generator_id))
#
#
# @app.route('/generator/<generator_id>')
# def show_generator(generator_id):
#     generator = generators.find_one({'_id': ObjectId(generator_id)})
#     # generator['random_words'] = bulk_sample(generator['histogram'], generator['tokens'], 10)
#     generator['random_sentence'] = random_sentence(markov(generator['word_list']))
#     return render_template('show_generator.html', generator=generator, title=generator['name'])
#
#
# @app.route('/generator/<generator_id>/edit')
# def edit_generator(generator_id):
#     generator = generators.find_one({'_id': ObjectId(generator_id)})
#     return render_template('edit_form.html', generator=generator, title='Edit Generator')
#
#
# @app.route('/generator/<generator_id>', methods=['POST'])
# def update_generator(generator_id):
#     text = request.form.get('source_text')
#     name = request.form.get('name')
#     desc = request.form.get('desc')
#
#     generator = Histogram(str(text))
#     updated_generator = {
#         'name': name,
#         'description': desc,
#         'word_list': generator.word_list,
#         'types': generator.total_types,
#         'tokens': generator.total_tokens
#     }
#     generators.update_one(
#         {'_id': ObjectId(generator_id)},
#         {'$set': updated_generator})
#     return redirect(url_for('show_generator', generator_id=generator_id))
#
#
# @app.route('/generator/<generator_id>/delete', methods=['POST'])
# def remove_generator(generator_id):
#     generators.delete_one({'_id': ObjectId(generator_id)})
#     return redirect(url_for('show_all'))
#
#
# @app.route('/create')
# def create_histogram():
#     ''' form to create a generator '''
#     return render_template('sourcetext_form.html', generator={})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


