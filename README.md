# twitthon

## Prerequis
Installation des libs nécessaires

    pip install -r requirements.txt
    
Change tokens in file <twitter_credentials.txt> (get twitter tokens from https://developer.twitter.com/en/apps)

    vi twitter_credentials.txt
    
## Usage


    twitthon.py "<candidate>"
    
    
## Trick
Change "twitterCredential" and hide the changes to git:
     
    git update-index --assume-unchanged <twitterCredentials.txt>
    
To track the changes again:

    git update-index --no-assume-unchanged <file>