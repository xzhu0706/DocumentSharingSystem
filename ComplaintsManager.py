# This module contains the functions needed to manage complaints by interacting with database

import pandas as pd

path_to_complaints_db = "database/Complaints.csv"


def get_complaints_received(userid):
    complaints_db = pd.read_csv(path_to_complaints_db, index_col=0)
    complaints_received = complaints_db.loc[complaints_db['receiver_id'] == userid]
    return complaints_received

def get_unprocessed_complaints(userid):
    complaints_received = get_complaints_received(userid)
    unprocessed = complaints_received.loc[complaints_received['processed'] == False]
    return unprocessed

def add_complaint(userid, complaint_info):
    new_id = len(pd.read_csv(path_to_complaints_db)) + 1
    df = pd.DataFrame({
        'complaint_id': [new_id],
        'complainer_id': [userid],
        'receiver_id': [complaint_info['receiver_id']],
        'complaint_type': [complaint_info['complaint_type']],
        'complainee_id': [complaint_info['complainee_id']],
        'seq_id': [complaint_info['seq_id']],
        'content': [complaint_info['content']],
        'processed': [False]
    })
    with open(path_to_complaints_db, 'a') as complaints_db:
        df.to_csv(complaints_db, index=False, header=False)


def mark_as_processed(complaint_id):
    complaints_db = pd.read_csv(path_to_complaints_db, index_col=0)
    complaints_db.loc[complaint_id, 'processed'] = True
    complaints_db.to_csv(path_to_complaints_db)


def remove_complaint(complaint_id):
    complaints_db = pd.read_csv(path_to_complaints_db, index_col=0)
    complaints_db.drop(complaint_id, inplace=True)
    complaints_db.to_csv(path_to_complaints_db)


def main():
    ## Testing code here
    userid = 2
    docid = 16
    complaints_db = pd.read_csv(path_to_complaints_db, index_col=0)
    get_unprocessed_complaints(1)




if __name__ == "__main__":
    main()