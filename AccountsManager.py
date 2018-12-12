# This module contains the functions needed to manage accounts by interacting with database

import pandas as pd

path_to_documents_db = "database/Documents.csv"
path_to_user_infos_db = "database/UserInfos.csv"
path_to_warning_list_db = "database/WarningList.csv"
path_to_accts_applications_db = "database/PendingApplications.csv"


def get_all_users():
    '''This function returns a dataframe of all users in the db'''
    user_infos_db = pd.read_csv(path_to_user_infos_db, index_col=0)
    return user_infos_db


def get_all_users_id_name():
    '''This function returns a dictionary of all users with id being key and username being values'''
    user_infos_db = pd.read_csv(path_to_user_infos_db, index_col=0)
    user_infos_dict = {}
    for id, user_info in user_infos_db.iterrows():
        user_infos_dict[id] = user_info['username']
    return user_infos_dict


def get_all_super_users():
    '''This function returns a list of all super users' userid'''
    user_infos_db = pd.read_csv(path_to_user_infos_db, index_col=0)
    super_users = user_infos_db.loc[user_infos_db['usertype'] == 'SuperUser']
    return super_users.index.tolist()


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


def is_warned(userid):
    '''This function checks if the user is on warning list, if yes return the bad doc info dictionary'''
    ## assuming no more than one doc contains taboo words per user
    warning_list = pd.read_csv(path_to_warning_list_db)
    docs_db = pd.read_csv(path_to_documents_db, index_col=0)
    user_on_list = warning_list[warning_list['user_id'] == userid]
    if not user_on_list.empty:
        bad_docid = user_on_list.get('doc_id').values[0]
        bad_doc_title = docs_db.loc[bad_docid]['title']
        return {
            'bad_docid': bad_docid,
            'bad_doc_title': bad_doc_title
        }

def add_warning(userid, docid):
    '''This function adds the user and the bad doc to warning list'''
    df = pd.DataFrame({
        'user_id': [userid],
        'doc_id': [docid]
    })
    with open(path_to_warning_list_db, 'a') as warning_list_db:
        df.to_csv(warning_list_db, index=False, header=False)


def remove_warning(userid):
    '''This function deletes the warning from database'''
    warning_list = pd.read_csv("database/WarningList.csv")
    index = warning_list.loc[warning_list['user_id'] == userid].index[0]
    warning_list.drop(index=index, inplace=True)
    warning_list.to_csv("database/WarningList.csv", index=False)


def is_pending(username):
    '''This function returns the boolean value of whether the given username exists in pending applications db'''
    accts_applications = pd.read_csv(path_to_accts_applications_db, index_col=0)
    try:
        accts_applications.loc[username]
        return True
    except KeyError:
        return False


def username_exists(username):
    '''This function returns the boolean value of whether the given username exists in user info db'''
    user_infos_db = pd.read_csv(path_to_user_infos_db)
    user = user_infos_db.loc[user_infos_db['username'] == username]
    if user.empty:
        return False
    return True


def validate_user(username, password):
    '''This function validates the given username and password by matching with record in userinfo db
        and returns a dictionary of user info containing user id and user type if validates successfully'''
    user_infos_db = pd.read_csv(path_to_user_infos_db)
    user = user_infos_db.loc[user_infos_db['username'] == username]
    if user.get('password').values[0] == password:
        userinfo = {
            'userid': user.get('id').values[0],
            'usertype': user.get('usertype').values[0]
        }
        return userinfo


def add_user(userinfo):
    '''This function adds a new user to db given the userinfo dictionary'''
    user_infos_db = pd.read_csv(path_to_user_infos_db, index_col=0)
    id = user_infos_db.tail(1).index.values[0] + 1
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


def add_pending_user(userinfo):
    '''This function adds a new account application to pending applications db given the dictionary of user info'''
    df = pd.DataFrame({
        'username': [userinfo['username']],
        'password': [userinfo['password']],
        'technical_interest': [userinfo['technical_interest']]
    })
    with open(path_to_accts_applications_db, 'a') as accts_applications_db:
        df.to_csv(accts_applications_db, index=False, header=False)


def remove_pending_user(username):
    '''This function removes a pending user from db given the username'''
    accts_applications_db = pd.read_csv(path_to_accts_applications_db, index_col=0)
    accts_applications_db.drop(username, inplace=True)
    accts_applications_db.to_csv(path_to_accts_applications_db)


def main():
    ## Testing code here
    userid = 2
    user_infos_db = pd.read_csv(path_to_user_infos_db, index_col=0)

    a = user_infos_db.tail(1).index.values[0]
    print(a)

    # add_user({
    #     'usertype': 'OrdinaryUser',
    #     'username': 'alpaca',
    #     'password': 'llama',
    #     'technical_interest': 'software engineering'
    # })

    # remove_pending_user('fdf')
    get_all_super_users()

if __name__ == "__main__":
    main()