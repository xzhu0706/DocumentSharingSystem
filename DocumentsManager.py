# This module contains the functions needed to manage a document by interacting with database

import pandas as pd
import time
import numpy as np
import AccountsManager
import InvitationsManager
import EditingCommands

pd.set_option('display.expand_frame_repr', False)

path_to_documents_db = "database/Documents.csv"
path_to_document_versions_db = "database/DocumentVersions.csv"
path_to_contributors_db = "database/contributors.csv"
path_to_user_infos_db = "database/UserInfos.csv"
path_to_locker_db = "database/Locker.csv"
path_to_warning_list_db = "database/WarningList.csv"

#
# different users should have their own page populated by his/her picture and 3 most recent documents.
# For a brand-new user, the 3 most popular (most read and/or updated) files in the system are shown

def get_all_docs():
    '''This function returns a dataframe of all docs in the db sorted by most recently updated'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    return sort_by_most_recent(docs_db)


def get_own_docs(userid):
    '''This function returns a dataframe of docs owned by user given the user id, docs are sorted by most recent'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    own_docs = docs_db.loc[docs_db['owner_id'] == userid]
    own_docs.sort_values(['modified_at'], ascending=False, inplace=True)
    return own_docs


def get_docs_for_gu():
    '''This function returns a sorted dataframe of docs that a guest user can view'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    public_docs = docs_db.loc[docs_db['scope'] == 'Public']
    restricted_docs = docs_db.loc[docs_db['scope'] == 'Restricted']
    can_view_docs = public_docs.append(restricted_docs)
    return sort_by_most_read_most_recent(can_view_docs).head(3)


def get_docs_for_ou(userid):
    '''This function returns the dataframe of docs that a user own or can edit or can view for the user home page'''
    own_docs = get_own_docs(userid)
    shared_docs = get_shared_docs_for_ou(userid)
    docs = own_docs.append(shared_docs)
    if len(docs) < 3:
        docs = docs.append(get_docs_for_gu())  # if less than 3 docs available, call get docs for gu
        docs.drop_duplicates(inplace=True)  # prevent duplicates of doc
    return docs.head(3)


def get_shared_docs_for_ou(userid):
    '''This function returns the dataframe of docs that are shared to user'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    contributors_db = pd.read_csv(path_to_contributors_db)
    shared_docs = contributors_db.loc[contributors_db['contributor_id'] == userid]
    if not shared_docs.empty:
        shared_docs_list = shared_docs['doc_id'].values.tolist()
        shared_docs_df = pd.DataFrame()
        for docid in shared_docs_list:
            if shared_docs_df.empty:
                shared_docs_df = docs_db.loc[docid].to_frame().transpose()
            else:
                shared_docs_df = shared_docs_df.append(docs_db.loc[docid].to_frame().transpose())
        return sort_by_most_recent(shared_docs_df)
    return shared_docs


def sort_by_most_read_most_recent(docs_df):
    '''This function returns a sorted dataframe by most read and most recent'''
    return docs_df.sort_values(['views_count', 'modified_at'], ascending=False)


def sort_by_most_recent(docs_df):
    '''This function returns a sorted dataframe by most recently updated'''
    return docs_df.sort_values('modified_at', ascending=False)


def sort_by_most_read(docs_df):
    '''This function returns a sorted dataframe by mostly read'''
    return docs_df.sort_values('views_count', ascending=False)


def get_scope(docid):
    '''This function returns the scope of the doc'''
    return get_doc_info(docid)['scope']


def set_scope(docid, scope):
    '''This function changes the current scope of doc to a new scope'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    scopes = ['Public', 'Restricted', 'Shared', 'Private']
    if scope in scopes:
        docs_db.loc[docid, 'scope'] = scope
        docs_db.to_csv(path_to_documents_db)


# Scopes:
# public (can be seen by everyone),
# restricted (can only be viewed as read-only by GU's and edited by OU's),
# shared (viewed/edited by OU's who are invited),
# private
def is_viewer(docid):
    '''This function returns boolean value of whether an OU/SU can view a doc'''
    scope = get_scope(docid)
    if scope == 'Public' or scope == 'Restricted':
        return True


def is_contributor(userid, docid, is_su):
    '''This function returns boolean value of whether user is a contributor of doc'''
    contributors_db = pd.read_csv(path_to_contributors_db)
    if get_scope(docid) == 'Restricted':
        return True
    if is_su:
        if get_scope(docid) == 'Private':
            return False
        return True
    contributors_df = contributors_db.loc[contributors_db['doc_id'] == docid]
    if not contributors_df.empty:
        contributors = contributors_df['contributor_id'].tolist()
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


def unlock_doc(userid, docid, is_su):
    '''This function returns the boolean value of whether user unlock doc successfully'''
    locker_db = pd.read_csv(path_to_locker_db, index_col=0)
    try:
        if locker_db.loc[docid]['locker_id'] == userid or is_owner(userid, docid) or is_su:
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


def delete_doc(docid):
    '''This function deletes the row of given docid from documents db and all its old versions from doc verions db'''
    # delete from locker db if it was locked
    if get_doc_info(docid)['is_locked'] == True:
        locker_db = pd.read_csv(path_to_locker_db, index_col=0)
        locker_db.drop(docid, inplace=True)
        locker_db.to_csv(path_to_locker_db)
    # delete from contributors db and invitations db if scope was Shared
    if get_scope(docid) == 'Shared':
        remove_all_contributor(docid)
        InvitationsManager.remove_invitations(docid)
    # delete from warning list if necessary
    warning_list = pd.read_csv(path_to_warning_list_db)
    on_warning_list = warning_list.loc[warning_list['doc_id'] == docid]
    if not on_warning_list.empty:
        index = on_warning_list.index[0]
        warning_list.drop(index=index, inplace=True)
        warning_list.to_csv(path_to_warning_list_db, index=False)
    # delete from doc versions db
    docs_versions_db = pd.read_csv(path_to_document_versions_db, index_col=0)
    filtered_docs_versions_db = docs_versions_db.loc[docs_versions_db['doc_id'] != docid]
    filtered_docs_versions_db.to_csv(path_to_document_versions_db)
    # delete from docs db
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    docs_db.drop(docid, inplace=True)
    docs_db.to_csv(path_to_documents_db)
    # TODO: maybe delete from complaints db


def create_new_doc(userid, scope, title):
    '''This function add new row to documents database and return new_doc_id'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    new_docid = len(docs_db) + 1
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
    df = pd.DataFrame({
        'seq_id': [old_version['current_seq_id']],
        'doc_id': [based_on_seq_id.split('-')[0]],
        'based_on_seq_id': [based_on_seq_id],
        'editing_commands': [EditingCommands.cal_editing_commands(old_version['content'], based_on_content['content'])],  # TODO: need function to calculate the commands
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
    '''This function returns the dataframe that contains old version(s) of document,
        if no old version found then returns an empty dataframe'''
    versions_db = pd.read_csv(path_to_document_versions_db, index_col=0)
    versions = versions_db[versions_db['doc_id'] == docid]
    versions.sort_index(ascending=False, inplace=True)
    return versions


def inc_views_count(docid):
    '''This function increases the views count of the given docid by 1'''
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    docs_db.loc[docid, 'views_count'] += 1
    docs_db.to_csv(path_to_documents_db)


def add_contributor(userid, docid):
    '''This function adds the user to the contributors list of the doc'''
    df = pd.DataFrame({
        'doc_id': [docid],
        'contributor_id': [userid]
    })
    with open(path_to_contributors_db, 'a') as contributors_db:
        df.to_csv(contributors_db, index=False, header=False)


def remove_contributor(userid, docid):
    '''This function removes the user to the contributors list of the doc'''
    contributors_db = pd.read_csv(path_to_contributors_db)
    contributors_df = contributors_db.loc[contributors_db['doc_id'] == docid]
    contributor = contributors_df.loc[contributors_df['contributor_id'] == userid]
    if not contributor.empty:
        index = contributor.index[0]
        contributors_db.drop(index=index, inplace=True)
        contributors_db.to_csv(path_to_contributors_db, index=False)


def remove_all_contributor(docid):
    '''This function removes all contributors of the given doc'''
    contributors_db = pd.read_csv(path_to_contributors_db)
    contributors_df = contributors_db.loc[contributors_db['doc_id'] == docid]
    if not contributors_df.empty:
        index_list = contributors_df.index.tolist()
        print(index_list)
        for index in index_list:
            contributors_db.drop(index=index, inplace=True)
        contributors_db.to_csv(path_to_contributors_db, index=False)


def get_contributors(docid):
    '''This function returns a list of contributors' id of the given docid'''
    contributors_db = pd.read_csv(path_to_contributors_db)
    contributors_df = contributors_db.loc[contributors_db['doc_id'] == docid]
    return contributors_df['contributor_id'].tolist()


def get_old_version_info(seq_id):
    '''This function returns the series of version info '''
    docs_versions_db = pd.read_csv(path_to_document_versions_db, index_col=0)
    return docs_versions_db.loc[seq_id]


def is_current_version(seq_id):
    '''This function returns the boolean value of whether the seq_id is current version of the doc'''
    try:
        versions_db = pd.read_csv(path_to_document_versions_db, index_col=0)
        version = versions_db.loc[seq_id]
        return False
    except KeyError or IndexError:
        return True


def retrieve_old_version(seq_id):
    '''This function returns the content of given seq_id'''
    doc_versions_db = pd.read_csv(path_to_document_versions_db, index_col=0)
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    old_version = doc_versions_db.loc[seq_id]
    based_on_seq_id = old_version['based_on_seq_id']
    edit_commands_sequence = old_version['editing_commands']
    try:
        while True:  # keep looking for based_on_seq_id in the versions db
            ver = doc_versions_db.loc[based_on_seq_id]
            edit_commands_sequence = ver['editing_commands'] + ';' + edit_commands_sequence
            based_on_seq_id = ver['based_on_seq_id']
    except KeyError:  # when catch an error means we reach the current version, read current content from docs db
        curr_ver = docs_db.loc[int(based_on_seq_id.split('-')[0])]
        based_on_content = curr_ver['content']

    print('commands are', edit_commands_sequence)
    print('based on content is', based_on_content)
    new_content_list = EditingCommands.editing_commands_to_content(edit_commands_sequence, based_on_content)
    print('new content is', new_content_list)
    new_content = ''
    for word in new_content_list:
        if word != '*':
            new_content += word + '\n'
    return new_content


def main():
    ## Testing code here
    docid = 47
    userid = 3
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    doc_versions_db = pd.read_csv(path_to_document_versions_db, index_col=0)
    # send_invitation(2, 16)
    #accept_invitation(4, 16)




if __name__ == "__main__":
    main()
