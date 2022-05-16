from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId


app = Flask(__name__)

app.secret_key = 'myawesomesecretkey'

app.config['MONGO_URI'] = 'mongodb://database/pythonmongodb'

mongo = PyMongo(app)


@app.route('/songs/createSong', methods=['POST'])
def create_song():
    # Receiving Data
    song_name = request.json['song_name']
    song_path = request.json['song_path']
    song_lyric = request.json['song_lyric']
    artist = request.json['artist']

    if song_name and song_path and song_lyric and artist:
        id = mongo.db.songs.insert(
            {'song_name': song_name, 'song_path': song_path, 'song_lyric': song_lyric, 'artists': artist})
        response = jsonify({
            '_id': str(id),
            'song_name': song_name,
            'song_path': song_path,
            'song_lyric': song_lyric,
            'artist': artist
        })
        response.status_code = 201
        return response
    else:
        return not_found()


'''@app.route('/songs', methods=['GET'])
def get_songs():
    songs = mongo.db.songs.find()
    response = json_util.dumps(songs)
    return Response(response, mimetype="application/json")'''


@app.route('/songs/getSongById/<id>', methods=['GET'])
def get_song(id):
    print(id)
    song = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(song)
    return Response(response, mimetype="application/json")


@app.route('/songs/deleteSongById/<id>', methods=['DELETE'])
def delete_song(id):
    mongo.db.songs.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Song' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/songs/updateSongById/<_id>', methods=['PUT'])
def update_song(_id):
    song_name = request.json['song_name']
    song_path = request.json['song_path']
    song_lyric = request.json['song_lyric']
    artist = request.json['artist']
    if song_name and song_path and song_lyric and artist and _id:
        mongo.db.songs.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'song_name': song_name, 'song_path': song_path, 'song_lyric': song_lyric, 'artist': artist}})
        response = jsonify({'message': 'Song' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True, port=3002)

