#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from itertools import izip

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM standings")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    # If you are deleting players, you need to remove them
    # from the standings table as well so there aren't any
    # orphan standings for players that no longer exist.
    cur.execute("DELETE FROM standings")
    cur.execute("DELETE FROM players")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT count(*) from players")
    count = cur.fetchall()
    db.close()
    return count[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT into players VALUES (%s)", (name,))
    cur.execute("SELECT lastval()")
    player_id = cur.fetchall()[0]
    cur.execute("INSERT into standings VALUES (%s)", (player_id,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT id, name, wins, losses from standings, players where player_id = id")
    standings = [(str(row[0]), str(row[1]), row[2], (row[2]+row[3])) for row in cur.fetchall()]
    db.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cur = db.cursor()
    cur.execute("UPDATE standings SET wins = wins + 1 WHERE player_id = %s ", (winner,))
    cur.execute("UPDATE standings SET losses = losses + 1 WHERE player_id = %s ", (loser,))
    db.commit()
    db.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    matches = []
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT player_id, name FROM standings, players where id = player_id ORDER BY wins")
    players = cur.fetchall()
    db.close()
    for player1, player2 in pairwise(players):
        matches.append((str(player1[0]), player1[1], str(player2[0]), player2[1]))
    return matches

# From http://stackoverflow.com/a/5389547
def pairwise(iterable):
    """Allows iterating throw the iterable by twos, makes the swiss pairings much easier"""
    item = iter(iterable)
    return izip(item, item)



