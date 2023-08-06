dd-ansible-syspass
==================
[![coverage report](https://git.digdeo.fr/digdeo-system/dd-ansible-syspass/badges/master/coverage.svg)](https://git.digdeo.fr/digdeo-system/dd-ansible-syspass/commits/master) [![pipeline status](https://git.digdeo.fr/digdeo-system/dd-ansible-syspass/badges/master/pipeline.svg)](https://git.digdeo.fr/digdeo-system/dd-ansible-syspass/commits/master)

**DISCLAIMER:**<br>
This module has been heavily inspired by https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/lookup/password.py for password generation and term handling and thus is under GPL.

    lookup: syspass
    author: Gousseaud Gaëtan <gousseaud.gaetan.pro@gmail.com>, Pierre-Henry Muller <pierre-henry.muller@digdeo.fr>
    short_description: get syspass user password and syspass API client
    description:
    - This lookup returns the contents from Syspass database, a user's password more specificly. Other functions are also implemented for further use.
    ansible_version: ansible 2.6.2 with mitogen
    python_version: 2.7.9
    syspass_version: 3.0 Beta (300.18082701)

params:
------
- **term**: the account name (required and must be unique)
- **login**: login given to created account
- **category**: category given to created account
- **customer**: client given to created account
- **state**: like in Ansible absent to remove the password, present in default to create (Optional)
- **pass_length**: generated password length (Optional)
- **chars**: type of chars used in generated (Optional)
- **url**: url given to created account (Optional)
- **notes**: notes given to created account (Optional)
- **private**: is this password private for users who have access or public for all users in acl (default false)
- **privategroup**: is private only for users in same group (default false)
- **expirationDate**: expiration date given to created account (Optional) and not tested (no entry in webui)

notes:
-----
- Account is only created if exact name has no match.
- A different field passed to an already existing account wont modify it.
- Utility of tokenPass: https://github.com/nuxsmin/sysPass/issues/994#issuecomment-409050974
- Rudimentary list of API accesses (Deprecated): https://github.com/nuxsmin/sysPass/blob/d0056d74a8a2845fb3841b02f4af5eac3e4975ed/lib/SP/Services/Api/ApiService.php#L175
- Usage of ansible vars: https://github.com/ansible/ansible/issues/33738#issuecomment-350819222
    
        syspass function list:
          SyspassClient:
            Account:
              -AccountSearch
              -AccountViewpass
              -AccountCreate
              -AccountDelete
              -AccountView
            Category:
              -CategorySearch
              -CategoryCreate
              -CategoryDelete
            Client:
              -ClientSearch
              -ClientCreate
              -ClientDelete
            Tag:
              -TagCreate
              -TagSearch
              -TagDelete
            UserGroup:
              - UserGroupCreate
              - UserGroupSearch
              - UserGroupDelete
            Others:
              -Backup

### IN HOST VARS ###

    syspass_API_URL: http://syspass-server.net/api.php
    syspass_API_KEY: 'API_KEY' #Found in Users & Accesses -> API AUTHORIZATION -> User token
    syspass_API_ACC_TOKPWD: Password for API_KEY for Account create / view / delete password account permission in API
    syspass_default_length: number of chars in password

### IN PLAYBOOK ###

NOTE: Default values are handled 

##### USAGE 1 #####

    - name: Minimum declaration to get / create password
      local_action: debug msg="{{ lookup('syspass', 'Server 1 test account', login=test, category='MySQL', customer='Customer 1') }}"
    
    - name: All details for password declaration
      local_action: debug msg="{{ lookup('syspass', 'Server 1 test account', login=test, category='MySQL', customer='Customer 1', 
        url='https://exemp.le', notes='Additionnal infos', private=True, privategroupe=True) }}"
    
    - name: Minimum declaration to delete password
      local_action: debug msg="{{ lookup('syspass', 'Server 1 test account', state=absent) }}"

