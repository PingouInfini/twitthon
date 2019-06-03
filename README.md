# twitthon

consomme file kafka TOPIC_IN, en extrait id bio, nom et prenom, recupere des tweets (variable LIMIT)
et les medias des tweets pour les envoyer dans trois files kafka distinctes (TOPICTWEET_OUT, TOPICTWEET_OUTDEUX et TOPICMEDIA_OUT)

## Prerequis
Installation des libs nécessaires

    pip install -r requirements.txt
    
Change tokens in file <twitter_credentials.txt> (get twitter tokens from https://developer.twitter.com/en/apps)

    vi twitter_credentials.txt
    
## Usage


    twitthon.py
    
    
    
## Trick
Change "twitterCredential" and hide the changes to git:
     
    git update-index --assume-unchanged <twitterCredentials.txt>
    
To track the changes again:

    git update-index --no-assume-unchanged <file>