
# Document Sharing System

This is  a document sharing system such that group members can collaborate on the same documents without causing inconsistencies. There are three types of users in this system: Super User (SU), Ordinary User (OU) and Guest (GU).

## Specifications
**Super User(SU)** can:
- [x] update membership.
- [x] maintain a list of taboo words.
- [x] unlock any locked document.
- [x] process complaints about OU's.
- [x] have all privileges reserved for OU's inside any group.

**Ordinary User(OU)** can:
- [x] create new document(s), the creator of a document is the owner of the document and can invite other OU's to update it, and decide if the document is open to the public (can be seen by everyone), restricted (can only be viewed as read-only by GU's and edited by OU's), shared (viewed/edited by OU's who are invited) and private.
- [x] accept or deny the invitation(s) placed by other OU's for their documents.
- [x] lock a shared document for updating, only one OU can lock a document successfully, the system should indicate which OU is updating the document.
- [x] update a successfully locked document, and then assign a unique version sequence number and remember who and when makes the updates.
- [x] unlock a shared document locked by him/herself.
- [x] file complaints to the owner of a document about other OU's updates or to the SU about the owner of the documents.
- [x] deal with complaints filed by other OU's as the owner of a document (remove some OU's who were invited before).
- [x] search own file(s) based on (partial) keyword.
- [x] search information about other OU's based on name and/or interests.
- [x] have all privileges for GU's.

**Guest User (GU)** can:
- [x] read open document(s), retrieve old version(s) of open document(s) and complains about those documents.
- [x] send suggestions to SU about taboo words.
- [x] apply to be an OU that is to be confirmed or rejected by SU, this is done by Sign Up.

**General Features:**
- [x] Any word(s) belonging to the taboo list (maintained by SU) are replaced by **UNK** by the system.
- [x] Any user who uses taboo words are warned automatically, s/he should update the document next time s/he log in the system as the first job.
- [x] For a brand-new user, the 3 most popular (most read and/or updated) files in the system are shown as a selection of the document.
- [x] Only the editing command(s) are saved for older versions with three possible actions: add, delete and update.

**Creative Features:**
- [x] speech recognition is incorporated as a user can update a document by speech.
- [x] a user who is not in warning list can download a document, which saves the documents contents as a text file in **Downloads** of your computer.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


### Prerequisites

* [Python3](https://www.python.org/downloads/)

### Installing

After successfully installing python we might need to install modules to successfully run this software: pandas, speech recognition, pyaudio, numpy,  A step by step series of examples on the installation guide are as follows:

```
pip3 install numpy
```

```
pip3 install pandas
```

```
pip3 install pyaudio
```
```
pip3 install SpeechRecognition
```

## Built With

* [Tkinter] - The python3 API used
* [csv]- Database Management
* [draw.io] - To draw use-cases


## Authors

* **Xin Zhao**
* **Xiaohong Zhu**
* **Phurpa Sherpa**
* **Baivab Pokhrel**


See also the list of [contributors](https://github.com/xzhu0706/DocumentSharingSystem/contributors) who participated in this project.
