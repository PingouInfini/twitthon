import src.common.twitthon_acquisition
import src.common.twitthon_authentication

def get_accounts_from_user(user):
    api = src.common.twitthon_authentication.get_api()
    results = api.search_users(q=user)

    accounts = []
    for result in results:
        accounts.append(result._json['screen_name'])

    print("Compte(s) trouve(s) pour '"+str(user)+"' : "+str(accounts))
    return accounts

def get_user_tweet(user,
                   limit=500,
                   outputtweet = "timeline/json",
                   outputmedia = "timeline/media"):

    api = src.common.twitthon_authentication.get_api()
    src.common.twitthon_acquisition.get_user_tweet(api, user, limit, outputtweet, outputmedia)

def get_tweet_from_keywords(keywords,
                            limit = 500,
                            outputtweet = "keywords/json",
                            outputmedia = "keywords/media"):
    api = src.common.twitthon_authentication.get_api()
    src.common.twitthon_acquisition.get_tweet_from_keywords(api, keywords, limit, outputtweet, outputmedia)