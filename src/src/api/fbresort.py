import pyrebase
import api.dfsapi
from api.match import Match
import api.iassorter

from collections import defaultdict

def resort_matches(program:str):
    fblocked = get_locked_instructors(program)

    if fblocked != None:
        locked = get_locked_matches(fblocked)
        return locked

def get_locked_instructors(program:str):
    db = api.dfsapi.get_db()
    keys = db.child(program).child("matches").shallow().get()
    recentdb = max(keys.val())

    instructors = db.child(program).child("matches").child(recentdb).child("Locked").get()

    return instructors.val()

def get_locked_matches(fblocked:dict):
    locked = defaultdict(list)

    for school in fblocked:
        locked_num = len(fblocked[school])
        for teacher, info in fblocked[school].items():
            instructors = int(info['Instructors']) - locked_num

            locked[school].append(Match(
                info['TeacherName'], 
                info['SchoolName'], 
                info['Region'], 
                info['PreviousMentor'], 
                info['Car'],
                info['Languages'],
                info['MultipleDays'],
                info['Schedule'],
                instructors,
                info['Locked']
            ))
    return locked