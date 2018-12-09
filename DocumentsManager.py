# This module contains the functions needed to manage a document by interacting with database

import pandas as pd
import time
import numpy as np
import AccountsManager

pd.set_option('display.expand_frame_repr', False)

path_to_documents_db = "database/Documents.csv"
path_to_document_versions_db = "database/DocumentVersions.csv"
path_to_invitations_db = "database/Invitations.csv"
path_to_complaints_db = "database/Complaints.csv"
path_to_contributors_db = "database/contributors.csv"
path_to_taboo_words_db = "database/TabooWords.csv"
path_to_user_infos_db = "database/UserInfos.csv"
path_to_warning_list_db = "database/WarningList.csv"
path_to_locker_db = "database/Locker.csv"

# TODO: load three docs for each user
# different users should have their own page populated by his/her picture and 3 most recent documents.
# For a brand-new user, the 3 most popular (most read and/or updated) files in the system are shown

def get_own_docs(userid):
    '''This function returns a dataframe of 3 docs owned by user given the user id, docs are sorted by most recent'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    own_docs = docs_db.loc[docs_db['owner_id'] == userid]
    own_docs.sort_values(['modified_at'], ascending=False, inplace=True)
    return own_docs.head(3)

# def get_sorted_docs():
#     '''This function returns a dataframe of docs that is sorted by most read and most recent'''
#     docs_db = pd.read_csv(path_to_documents_db, index_col=0)
#     docs_db.sort_values(['views_count', 'modified_at'], ascending=False, inplace=True)
#     return docs_db

# Scopes:
# public (can be seen by everyone),
# restricted (can only be viewed as read-only by GU's and edited by OU's),
# shared (viewed/edited by OU's who are invited),
# private

def get_docs_for_gu():
    '''This function returns a sorted dataframe of 3 docs that a guest user can view'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    public_docs = docs_db.loc[docs_db['scope'] == 'Public']
    restricted_docs = docs_db.loc[docs_db['scope'] == 'Restricted']
    can_view_docs = public_docs.append(restricted_docs)
    return sort_by_most_read_most_recent(can_view_docs).head(3)


def get_docs_for_ou(userid):
    '''This function '''
    #TODO
    own_docs = get_own_docs(userid)

    # if len(own_docs) < 3:
    #     docs = own_docs.append(get_docs_for_gu())
    # return docs.head(3)


def get_shared_docs_for_ou(userid):
    '''This function '''
    #TODO
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)


def sort_by_most_read_most_recent(docs_df):
    '''This function returns a sorted dataframe by most read and most recent'''
    return docs_df.sort_values(['views_count', 'modified_at'], ascending=False)


def sort_by_most_recent(docs_df):
    '''This function returns a sorted dataframe by most recently updated'''
    return docs_df.sort_values('modified_at', ascending=False)


def sort_by_most_read(docs_df):
    '''This function returns a sorted dataframe by mostly read'''
    return docs_df.sort_values('views_count', ascending=False)


# def can_view(uesrid, docid):
    # userid = 0 stands for a guest user
    # TODO

# def can_edit(userid, docid):
#     # TODO


def is_contributor(userid, docid):
    '''This function returns boolean value of whether user is a contributor of doc'''
    contributors_db = pd.read_csv(path_to_contributors_db, index_col=0)
    contributors = contributors_db.loc[contributors_db['doc_id'] == docid]['contributors_id'].values.tolist()
    if userid in contributors:
        return True
    return False


def is_owner(userid, docid):
    '''This function returns boolean value of whether user is the owner of doc'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    owner = docs_db.loc[docid]['owner_id']
    if userid == owner:
        return True
    return False


def is_locker(userid, docid):
    '''This function returns boolean value of whether use is the locker of doc'''
    locker_db = pd.read_csv(path_to_locker_db, index_col=0)
    try:
        if locker_db.loc[docid]['locker_id'] == userid:
            return True
        else:
            return False
    except KeyError:
        return False


def get_locker(docid):
    '''This function returns a dictionary that contains the user id and user name of the locker of doc'''
    locker_db = pd.read_csv(path_to_locker_db, index_col=0)
    userid = locker_db.loc[docid]['locker_id']
    locker = {
        'id': userid,
        'name': AccountsManager.get_user_info(userid)['username']
    }
    return locker


def lock_doc(userid, docid):
    '''This function returns boolean value of whether user lock doc successfully'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    # check if document is locked already
    if docs_db.loc[docid]['is_locked']:
        return False
    else:
        docs_db.loc[docid, 'is_locked'] = True
        # Update database
        df = pd.DataFrame({
            'doc_id': [docid],
            'locker_id': [userid]
        })
        docs_db.to_csv(path_to_documents_db)
        with open(path_to_locker_db, 'a') as locker_db:
            df.to_csv(locker_db, index=False, header=False)
        return True


def unlock_doc(userid, docid):
    '''This function returns the boolean value of whether user unlock doc successfully'''
    locker_db = pd.read_csv(path_to_locker_db, index_col=0)
    try:
        if locker_db.loc[docid]['locker_id'] == userid or is_owner(userid, docid):
            doc_db = pd.read_csv(path_to_documents_db, index_col=0)
            doc_db.loc[docid, 'is_locked'] = False
            doc_db.to_csv(path_to_documents_db)
            locker_db.drop(docid, inplace=True)
            locker_db.to_csv(path_to_locker_db)
            return True
        else:
            return False
    except KeyError:
        return False


def create_new_doc(userid, scope, title):
    '''This function add new row to documents database and return new_doc_id'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    new_docid = docs_db.tail(1).index.values[0] + 1
    # Add new doc to db (doc_id and owner_id)
    # initial seq_id is just a dash '-' (meaning no content in it)
    # initial content is just a blank space
    df = pd.DataFrame(
        {
            'doc_id': [new_docid],
            'owner_id': [userid],
            'current_seq_id': ['-'],
            'scope': [scope],
            'is_locked': [False],
            'views_count': [0],
            'modified_by': [userid],
            'modified_at': [create_time_object()],
            'title': [title],
            'content': [' ']
        })
    with open(path_to_documents_db, 'a') as docs_db:
        df.to_csv(docs_db, index=False, header=False)
    return new_docid


def create_time_object():
    '''This function returns a datetime64 object of current time'''
    t = int(time.time())
    return pd.Timestamp(np.datetime64(t, 's') - np.timedelta64(5, 'h'))


# def time_to_str(time_obj):
#     return pd.Timestamp(time_obj)


def update_doc(userid, docid, updated_content):
    '''This function updates the info of given document in the database'''
    # unique sequence id: doc_id + '-' + nth version(current_version + 1)
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    old_seq_id = docs_db.loc[docid]['current_seq_id']
    if old_seq_id == '-':
        new_seq_id = '{}-{}'.format(docid, 1)
    else:
        version = int(old_seq_id.split('-')[1]) + 1
        new_seq_id = '{}-{}'.format(docid, version)
        store_old_version(docs_db.loc[docid], new_seq_id, updated_content)
    docs_db.loc[docid, 'current_seq_id'] = new_seq_id
    docs_db.loc[docid, 'modified_by'] = userid
    docs_db.loc[docid, 'modified_at'] = create_time_object()
    docs_db.loc[docid, 'title'] = updated_content['title']
    docs_db.loc[docid, 'content'] = updated_content['content']
    docs_db.to_csv(path_to_documents_db)


def store_old_version(old_version, based_on_seq_id, based_on_content):
    # TODO: NOT FINISHED!!!!!!!!!!!!
    df = pd.DataFrame({
        'seq_id': [old_version['current_seq_id']],
        'doc_id': [based_on_seq_id.split('-')[0]],
        'based_on_seq_id': [based_on_seq_id],
        'editing_commands': ['TODO'],  # TODO: need function to calculate the commands
        'modified_by': [old_version['modified_by']],
        'modified_at': [old_version['modified_at']]
    })
    with open(path_to_document_versions_db, 'a') as versions_db:
        df.to_csv(versions_db, index=False, header=False)



def get_doc_info(docid):
    '''This function returns a dataframe of document information from Document.csv'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    doc_info = docs_db.loc[docid]
    return doc_info


def get_doc_old_versions(docid):
    '''This function returns the row(s) of old versions of document'''
    versions_db = pd.read_csv(path_to_document_versions_db)
    versions = versions_db[versions_db['doc_id'] == docid]
    # TODO: need to check with example, might contain error
    return versions


def add_warning(userid, docid):
    '''This function adds the user and the bad doc to warning list'''
    df = pd.DataFrame({
        'user_id': [userid],
        'doc_id': [docid]
    })
    with open(path_to_warning_list_db, 'a') as warning_list_db:
        df.to_csv(warning_list_db, index=False, header=False)


def inc_views_count(docid):
    '''Thid function increases the views count of the given docid by 1'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    docs_db.loc[docid, 'views_count'] += 1
    docs_db.to_csv(path_to_documents_db)


def main():
    ## Testing code here
    docid = 41
    userid = 1
    # docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    # print(get_doc_info(docid)['title'])
    # df = get_docs_for_gu()
    # print(df)
    # for docid, row in df.iterrows():
    #     print(docid,
    #           row['title'],
    #           row['owner_id'],
    #           row['scope'],
    #           row['views_count'],
    #           row['modified_at'])
    inc_views_count(docid)



if __name__ == "__main__":
    main()
