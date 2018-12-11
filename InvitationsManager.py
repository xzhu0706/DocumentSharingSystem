# This module contains the functions needed to manage invitations by interacting with database

import pandas as pd
import DocumentsManager
import AccountsManager

path_to_documents_db = "database/Documents.csv"
path_to_document_versions_db = "database/DocumentVersions.csv"
path_to_invitations_db = "database/Invitations.csv"
path_to_complaints_db = "database/Complaints.csv"
path_to_contributors_db = "database/contributors.csv"
path_to_taboo_words_db = "database/TabooWords.csv"
path_to_user_infos_db = "database/UserInfos.csv"
path_to_warning_list_db = "database/WarningList.csv"
path_to_locker_db = "database/Locker.csv"
path_to_accts_applications_db = "database/PendingApplications.csv"

def send_invitation(invitee_id, docid):
    '''This function records an invitation in db'''
    df = pd.DataFrame({
        'inviter_id': [DocumentsManager.get_doc_info(docid)['owner_id']],
        'invitee_id': [invitee_id],
        'doc_id': [docid],
        'time': [DocumentsManager.create_time_object()],
        'accepted': [False]
    })
    with open(path_to_invitations_db, 'a') as invitations_db:
        df.to_csv(invitations_db, index=False, header=False)


def get_invitations(userid):
    '''This function returns a dataframe of all the invitations the user received'''
    invitations_db = pd.read_csv(path_to_invitations_db)
    invitations_received = invitations_db.loc[invitations_db['invitee_id'] == userid]
    return invitations_received


def get_invitation_index(invitee_id, docid):
    '''This function returns the index of the invitation in the db'''
    invitations_received = get_invitations(invitee_id)
    invitation = invitations_received.loc[invitations_received['doc_id'] == docid]
    index = invitation.index[0]
    return index


def accept_invitation(invitee_id, docid):
    '''This function removes the invitation from invitations db'''
    invitations_db = pd.read_csv(path_to_invitations_db)
    index = get_invitation_index(invitee_id, docid)
    invitations_db.drop(index=index, inplace=True)
    invitations_db.to_csv(path_to_invitations_db, index=False)
    DocumentsManager.add_contributor(invitee_id, docid)


def reject_invitation(invitee_id, docid):
    '''This function set the invitation to be rejected in invitations db'''
    invitations_db = pd.read_csv(path_to_invitations_db)
    index = get_invitation_index(invitee_id, docid)
    invitations_db.loc[index, 'rejected'] = True
    invitations_db.to_csv(path_to_invitations_db, index=False)


def is_rejected(invitee_id, docid):
    '''This function returns the boolean value of whether the invitation has been rejected by invitee'''
    try:
        invitations_db = pd.read_csv(path_to_invitations_db)
        index = get_invitation_index(invitee_id, docid)
        if invitations_db.loc[index]['rejected'] == True:
            return True
        return False
    except IndexError:
        return False


def is_invited(invitee_id, docid):
    '''This function returns the boolean value of whether the invitation already exists'''
    try:
        get_invitation_index(invitee_id, docid)
        return True
    except IndexError:
        return False


def remove_invitations(docid):
    '''This function removes all invitations of a doc from db,
        should be called when doc is deleted or scope is changed'''
    invitations_db = pd.read_csv(path_to_invitations_db)
    invitations = invitations_db.loc[invitations_db['doc_id'] == docid]
    if not invitations.empty:
        index_list = invitations.index.tolist()
        for index in index_list:
            invitations_db.drop(index=index, inplace=True)
        invitations_db.to_csv(path_to_invitations_db, index=False)


def main():
    ## Testing code here
    docid = 16
    userid = 4





if __name__ == "__main__":
    main()