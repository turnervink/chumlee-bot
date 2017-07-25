from resources.firebaseinfo import db

def is_registered(id):
    dbusername = db.child("users").child(id).get()
    if dbusername.val() is None:
        print("returning false")
        return False
    else:
        print("returning true")
        return True

def deposit(id, amt):
    currentbalance = db.child("users").child(id).child("balance").get()
    newbalance = currentbalance.val() + amt
    db.child("users").child(id).child("balance").set(newbalance)

def withdraw(id, amt):
    currentbalance = db.child("users").child(id).child("balance").get()
    newbalance = currentbalance.val() - amt
    db.child("users").child(id).child("balance").set(newbalance)

def set_deal_status(id, bool):
    db.child("users").child(id).child("isInDeal").set(bool)

def is_in_deal(id):
    print("Deal: " + str(db.child("users").child(id).child("isInDeal").get().val()))
    return db.child("users").child(id).child("isInDeal").get().val()

def update_last_deal_time(id):
    db.child("users").child(id).child("lastDealTime").set(int(time.time()))

def last_deal_time(id):
    return db.child("users").child(id).child("lastDealTime").get().val()
