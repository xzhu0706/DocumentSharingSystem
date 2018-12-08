# This module contains the functions needed to manage accounts by interacting with database

import pandas as pd
import DocumentsManager

path_to_documents_db = "database/Documents.csv"
path_to_document_versions_db = "database/DocumentVersions.csv"
path_to_invitations_db = "database/Invitations.csv"
path_to_complaints_db = "database/Complaints.csv"
path_to_contributors_db = "database/contributors.csv"
path_to_taboo_words_db = "database/TabooWords.csv"
path_to_user_infos_db = "database/UserInfos.csv"
path_to_warning_list_db = "database/WarningList.csv"
path_to_locker_db = "database/Locker.csv"

def get_user_info(userid):
    '''This function returns a dictionary of user info given the user id'''
    user_infos_db = pd.read_csv(path_to_user_infos_db, index_col=0)
    user_info = user_infos_db.loc[userid]
    return user_info

def get_username(userid):
    '''This function returns the username of the given user id'''
    return get_user_info(userid)['username']

def get_technical_interest(userid):
    '''This function returns the technical interest of the given user id'''
    return get_user_info(userid)['technical_interest']

def add_user(userinfo):
    '''This function adds a new user to db given the userinfo dictionary'''
    id = len(pd.read_csv(path_to_user_infos_db, index_col=0)) + 1
    df = pd.DataFrame({
        'id': id,
        'usertype': [userinfo['usertype']],
        'username': [userinfo['username']],
        'password': [userinfo['password']],
        'technical_interest': [userinfo['technical_interest']]
    })
    with open(path_to_user_infos_db, 'a') as user_infos_db:
        df.to_csv(user_infos_db, index=False, header=False)

def remove_user(userid):
    '''This function deletes a user from db given the user id'''
    user_infos_db = pd.read_csv(path_to_user_infos_db, index_col=0)
    user_infos_db.drop(userid, inplace=True)
    user_infos_db.to_csv(path_to_user_infos_db)


def main():
    ## Testing code here
    userid = 2
    user_infos_db = pd.read_csv(path_to_user_infos_db, index_col=0)
    # a = user_infos_db.loc[user_infos_db['id'] == userid]
    # print(a['password'])
    # print(user_infos_db.loc[userid]['username'])
    print(get_username(userid))



if __name__ == "__main__":
    main()