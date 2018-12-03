## This module contains the functions needed to manage a document and interact with database

import pandas as pd
import time

path_to_documents_db = "database/Documents.csv"
path_to_document_versions_db = "database/DocumentVersions.csv"
path_to_invitations_db = "database/Invitations.csv"
path_to_complaints_db = "database/Complaints.csv"
path_to_contributors_db = "database/contributors.csv"
path_to_taboo_words_db = "database/TabooWords.csv"
path_to_user_infos_db = "database/UserInfos.csv"
path_to_warning_list_db = "database/WarningList.csv"

def load_docs(usertype, userid):
    docs_db = pd.read_csv(path_to_documents_db)
    docs = docs_db['title']
    ## TODO: load three docs for each user
    # different users should have their own page populated by his/her picture and 3 most recent documents.
    # For a brand-new user, the 3 most popular (most read and/or updated) files in the system are shown

    print(docs)

##unique sequence id: doc_id + nth version(current_version + 1) + updater_id + time

def is_contributor(userid, docid):
    contributors_db = pd.read_csv(path_to_contributors_db, index_col=0)
    ## TODO


def is_owner(userid, docid):
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    ## TODO


def lock_doc(userid, docid):
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)

    ## TODO: check if user is owner or is contributor

    ## check if document is locked already
    if docs_db.loc[docid]['is_locked'] == 1:
        return False
    else:
        docs_db.loc[docid, 'is_locked'] = '1'
        docs_db.loc[docid, 'locker_id'] = str(userid)
        ## Update database
        docs_db.to_csv(path_to_documents_db)
        return True

def create_new_doc(userid):
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    new_doc_id = len(docs_db) + 1

    # Add new doc to db (doc_id and owner_id)
    data = [[new_doc_id, userid, '', '', 0, '', 0, '', '']]
    df = pd.DataFrame(data, columns=['doc_id', 'owner_id', 'current_seq_id',
                                     'scope', 'is_locked', 'locker_id',
                                     'views_count', 'title', 'content'])
    with open('database/Documents.csv', 'a') as docs_db:
        df.to_csv(docs_db, index=False, header=False)

def update_doc(userid, doc_info): #doc_info should be a dictionary containing necessary info
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    ## TODO


def get_doc_info(docid):
    '''This function returns the row of document information from Document.csv'''
    docs_db = pd.read_csv(path_to_documents_db)

    doc_info = docs_db.loc[docs_db['doc_id'] == docid]
    return doc_info

def get_doc_old_versions(docid):
    '''This function returns the row(s) of old versions of document'''
    versions_db = pd.read_csv(path_to_document_versions_db)
    versions = versions_db[versions_db['doc_id'] == docid]
    return versions


def main():

    #### Testing code here
    load_docs(1, 1)
    # doc = {
    #     'scope': 'shared',
    #     'is_locked': 0,
    #     'views_count': 0,
    #     'title': 'Hello World',
    #     'content': 'Welcome\nto\nthe\nworld'
    # }
    # create_doc(1, doc)
    #get_doc_info(1)
    #get_doc_old_versions(1)
    #create_new_doc(2)
    lock_doc(1,1)

if __name__ == "__main__":
    main()