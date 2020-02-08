import pymongo
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from datetime import datetime

from histogram import *
import source_text

# import tweepy
#
# # Authenticate to Twitter
# auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
# auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")
#
# # Creating Tweepy API object
# tweet = tweepy.API(auth)

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/TweetGen')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

# generators = db.generators
favorites = db.favorites

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
        new_tweet = request.form.get('random_sentence_lol')
        # tweet_sentence(new_tweet)
        fav_tweet = {
            'tweet': request.form.get('new_tweet'),
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
        new_tweet = request.form.get('random_sentence_lol')
        # tweet_sentence(new_tweet)
        fav_tweet = {
            'tweet': new_tweet,
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
        new_tweet = request.form.get('random_sentence_lol')
        # tweet_sentence(new_tweet)
        fav_tweet = {
            'tweet': new_tweet,
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


# Create a tweet
def tweet_sentence(random_sentence_lol):
    tweet.update_status(random_sentence_lol)


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


