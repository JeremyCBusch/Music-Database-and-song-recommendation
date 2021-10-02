from os import name
import sqlite3
import random
from sqlite3.dbapi2 import connect



connection = sqlite3.connect("songs.db")
cursor = connection.cursor()



def get_albums_from_year(year):
    """This function will return a list of albumIDs from an inputted year"""
    values = (year,)
    cursor.execute("SELECT yearReleased, genre, albumID FROM albums WHERE yearReleased is (?)", values)
    print ("{:>20} {:>20}".format("Album Year Released", "Album Genre"))
    albums = []
    for line in cursor.fetchall():
        albums.append(line[2])
        # print ("{:>20} {:>20}".format(line[0], line[1]))
    return albums
    #  print(albums)

def get_tracks_from_albums(albums):
    """expects a list in the parameters and returns the songs from those albums"""
    tracks = []
    for album in albums:
        values = (album,)
        cursor.execute("SELECT trackID FROM tracks WHERE albumID is (?)", values)
        for line in cursor.fetchall():
            tracks.append(line[0])
    return tracks


def get_album_from_genre(genre):
    """This function will return a list of albumIDs that all have the same inputted genre"""
    values = (genre,)
    cursor.execute("SELECT albumID FROM albums WHERE genre is (?)", values)
    albums = []
    for line in cursor.fetchall():
        albums.append(line[0])
    # print()
    return albums


def get_album_year_genre_match(year, genre):
    """generates and returns albumIDs with the same gnere and release year as inputted"""
    values = (genre, year)
    cursor.execute("SELECT albumID FROM albums WHERE genre is (?) AND yearReleased is (?)", values)

    albums = []
    for line in cursor.fetchall():
        albums.append(line[0])
        # print ("{:>20}".format(line[0]))
    return albums
    # print(albums)


def get_tracks_from_same_artist(artistID):
    """returns tracks from the artistID inputted"""
    values = (artistID,)
    cursor.execute("SELECT trackID FROM tracks WHERE artistID is (?)", values)
    # print ("{:>20}".format("TrackID"))
    track_ids = []
    for line in cursor.fetchall():
        track_ids.append(line[0])
    #     print ("{:>20}".format(line[1]))
    return track_ids

def get_tracks_from_album(albumID):
    """returns a list of tracks that are in an albumID that is provided in the parameters"""
    values = (albumID,)
    cursor.execute("SELECT trackID FROM tracks WHERE albumID is (?)", values)
    track_ids = []
    for line in cursor.fetchall():
        track_ids.append(line[0])
        # print ("{:>20}".format(line[1]))
    return track_ids
    # print(track_ids)



def format_track_album_artist(trackID):
    """This will return the format for a song with its proper album and artist"""
    values = (trackID,)
    cursor.execute("SELECT * FROM tracks WHERE trackID is (?)", values)
    track_data = []
    track_data = cursor.fetchall()
    format_list = []
    format_list.append(track_data[0][1])
    values = (track_data[0][2],)
    cursor.execute("SELECT albumName FROM albums WHERE albumID is (?)", values)
    album_data = cursor.fetchall()
    format_list.append(album_data[0][0])
    values = (track_data[0][3],)
    cursor.execute("SELECT artistName FROM artists WHERE artistID is (?)", values)
    artist_data = cursor.fetchall()
    format_list.append(artist_data[0][0])
    return format_list

    

def get_song_from_album(albumID):
    """This function will return track names and IDS from a certain album ID"""
    values = (albumID,)
    cursor.execute("SELECT trackName, trackID FROM tracks WHERE albumID is (?)", values)
    print ("{:>20} {:>20}".format("Track Name", "Track ID"))
    tracks = []
    for line in cursor.fetchall():
        tracks.append(line[1])
        print ("{:>20} {:>20}".format(line[0], line[1]))
    print(tracks)
    

def print_song(song):
    
    print("{:<35}{:<35} {:<35}".format(song[0], song[1], song[2]))


def print_match_songs(songs):
    """expects a list of 5 songs, each songs is a list of 3 pieces of data: track, album, and artist name"""
    print("\nHere are your recomendations:\n")
    print("{:<35}{:<35} {:<35}".format("Track","Album", "Artist"))
    print("{:<35}{:<35} {:<35}".format("-----","-----", "------"))
    for song in songs:
        print_song(format_track_album_artist(song))


def make_recommendation():
    """prints all the tracks from the database and the user can pick a song that he/she likes and the program will try to find 5 songs to reccomend"""
    print("Choose a song that you like and we will make a recomendation based on your choice")
    print("{:<30}{:<30} {:<30}".format("Track","Album", "Artist"))
    cursor.execute("SELECT trackID FROM tracks")
    for track in cursor.fetchall():
        print_song(format_track_album_artist(track[0]))
    user_input = input("\nChoose a song> ")
    values = (user_input,)
    cursor.execute("SELECT * FROM tracks WHERE trackName is (?)", values)
    favorite_song_data = cursor.fetchall()
    trackID = favorite_song_data[0][0]
    albumID = favorite_song_data[0][2]
    artistID = favorite_song_data[0][3]
    values = (albumID,)
    cursor.execute("SELECT yearReleased, genre FROM albums WHERE albumID is (?)", values)
    favorite_song_album_data = cursor.fetchall()
    # print(favorite_song_album_data)
    year_released = favorite_song_album_data[0][0]
    genre = favorite_song_album_data[0][1]


    trackID_recomendations = []
    #getting recomendations from genre and year
    tracks = get_tracks_from_albums(get_album_year_genre_match(year_released, genre))
    if tracks != None:
        for track in tracks:
            if trackID_recomendations.count(track) < 1 and track != trackID:
                trackID_recomendations.append(track)
    # getting recomendations from genre
    tracks = get_tracks_from_albums(get_album_from_genre(genre))
    if tracks != None:
        for track in tracks:
            if trackID_recomendations.count(track) < 1 and track != trackID:
                trackID_recomendations.append(track)
    # getting recomendations from album
    tracks = get_tracks_from_album(albumID)
    if tracks != None:
        for track in tracks:
            if trackID_recomendations.count(track) < 1 and track != trackID:
                trackID_recomendations.append(track)
    # getting recomendations from the artist
    tracks = get_tracks_from_same_artist(artistID)
    if tracks != None:
        # print(tracks)
        for track in tracks:
            if trackID_recomendations.count(track) < 1 and track != trackID:
                trackID_recomendations.append(track)

    # print all the recomenddations
    # print(tracks)
    if len(trackID_recomendations) > 0:
        print_match_songs(trackID_recomendations)
    else:
        print("Sorry you're music taste is too unique")
    # print_song(format_track_album_artist(trackID_recomendations[0][0]))
    # if len(albums) >= 1:
    #     for album in albums:
    #         trackID_recomendations.append(get_song_from_album(album))

    



def get_delete_artist(cursor):
    cursor.execute("SELECT artistName, artistID FROM artists")
    records = cursor.fetchall()
    for record in records:
        print(f"{record[1]} - {record[0]}")
    choice = int(input("\nDelete What> "))
    return records[choice-1][1]

def get_delete_album(cursor):
    cursor.execute("SELECT albumName, albumID FROM albums")
    records = cursor.fetchall()
    for record in records:
        print(f"{record[1]} - {record[0]}")
    choice = int(input("\nDelete What> "))
    return records[choice-1][1]

def get_delete_track(cursor):
    cursor.execute("SELECT trackName, trackID FROM tracks")
    records = cursor.fetchall()
    for record in records:
        print(f"{record[1]} - {record[0]}")
    choice = int(input("\nDelete What> "))
    return records[choice-1][1]

user_input = 0
while user_input != 5:
    print("\n1 - Add\n2 - Delete\n3 - Edit Artist\n4 - Make recommendation\n5 - Quit\n")
    user_input = ''
    user_input = int(input("> "))
    if user_input == 1:
        print("\n1 - Add Artist\n2 - Add Album\n3 - Add Track\n4 - Quit\n")
        user_input = int(input("> "))
        if user_input == 1:
            user_input = str(user_input)
            artist_name = input("Artist name> ")
            values = (artist_name,)
            cursor.execute("INSERT into artists (artistName) values (?)", values)
            connection.commit()
            print("\nSuccessfully Added Artist\n")
        elif user_input == 2:
            # add album
            album_name = input("Album name> ")
            year_released = input("Year released> ")
            genre = input("Genre> ")
            values = (album_name, year_released, genre)
            cursor.execute("INSERT into albums (albumName, yearReleased, genre) values (?,?,?)", values)
            connection.commit()
            print("\nSuccessfully Added Album\n")
        elif user_input == 3:
            # add track
            track_name = input("Track name> ")
            trackAlbum = input("Album ID> ")
            trackArtist = input("Artist ID> ")
            values = (track_name, trackAlbum, trackArtist)
            cursor.execute("INSERT into tracks (trackName, albumID, artistID) values (?,?,?)", values)
            connection.commit()
            print("\nSuccessfully Added Track\n")
        elif user_input == 4:
            pass
        else:
            print("\nInvalid input\n")

    elif user_input == 2:
        # delete stuff
        print("\n1 - Delte Artist\n2 - Delete Album\n3 - Delete Track\n4 - Quit\n")
        user_input = int(input("> "))
        if user_input == 1:
            artistID = int(get_delete_artist(cursor))
            values = (artistID,)
            cursor.execute("DELETE FROM artists WHERE artistID = ?", values)
            connection.commit()
            print("\nSuccessfully Deleted Artist\n")
        elif user_input == 2:
            albumID = int(get_delete_album(cursor))
            values = (albumID,)
            cursor.execute("DELETE FROM albums WHERE albumID = ?", values)
            connection.commit()
            print("\nSuccessfully Deleted Album\n")
        elif user_input == 3:
            trackID = int(get_delete_track(cursor))
            values = (trackID,)
            cursor.execute("DELETE FROM tracks WHERE trackID = ?", values)
            connection.commit()
            print("\nSuccessfully Deleted Track\n")
        elif user_input == 4:
            pass
        else:
            print("\nInvalid input\n")

    elif user_input == 3:
        cursor.execute("SELECT artistName, artistID FROM artists")
        records = cursor.fetchall()
        for record in records:
            print(f"{record[1]} - {record[0]}")
        choice = int(input("\nEdit What> "))
        name = input("New Name of Artist> ")
        values_name = (name, choice)
        values_ID = (choice,)
        cursor.execute("UPDATE artists SET artistName = (?) WHERE artistID is (?)", values_name)
        connection.commit()
    elif user_input == 4:
        make_recommendation() 
    elif user_input == 5:
        pass
    else:
        print("\nInvalid input\n")




