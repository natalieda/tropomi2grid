'''   
description:
	Connect to PiCaS server
	Reset tokens that are locked for more time than 'hour' (default=72) in the specified view. The function can be used to release the lock of tokens that were killed when the job hit the queue limit (e.g 72 hours for the long queue).
	Increase the scrubcount and update the database
'''

import sys
import os
import couchdb
import picasconfig
from time import time


def get_db():
    """
    Connect to the database with the credentials set in "picasconfig.py" file.
    It returns a couchdb object (not truly connect) since couchdb is RESTFULL and no
    separate connection is made for authorization and authentication.
    """
    
    server = couchdb.Server(picasconfig.PICAS_HOST_URL)
    username = picasconfig.PICAS_USERNAME
    pwd = picasconfig.PICAS_PASSWORD
    server.resource.credentials = (username, pwd)
    db = server[picasconfig.PICAS_DATABASE]
	return db

def reset_doc_values(doc):
    """
    Reset the values of a token to make it available in the todo list and increase the
    scrub_count to count the amount of fails.
    This function returns the document but does not save the changes in the database.
    """

    doc['lock'] = 0
    doc["done"] = 0
    doc["scrub_count"] += 1
    doc['hostname'] = ''
    doc['exit_code'] = ''

    #uncomment to delete all attachments if present
    """
    if doc.has_key("_attachments"):
        del doc["_attachments"]
    """

    #add here any other application-specific values to reset

def reset_locked_tokens(view_name, hour=72):

    # Create a connection to the server
	db = get_db()

    max_age = time() - (hour * 3600)
    to_update = []
    for row in db.iterview(view_name + "/" + "locked", 100):
        doc = db[row["id"]]
        if (doc["lock"] < max_age):
            reset_doc_values(doc)
            to_update.append(doc)

    db.update(to_update)
    #print(to_update)
    print("Number of reset tokens in locked state: " + str(len(to_update)))


if __name__ == '__main__':
    pass