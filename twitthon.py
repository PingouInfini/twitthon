import sys
import common.twitthon_authentication
import common.twitthon_acquisition

def usage():
    print("Usage:")
    print("python {} <username>".format(sys.argv[0]))

def get_accounts_from_user(user):
    api = common.twitthon_authentication.get_api()
    results = api.search_users(q=user)

    accounts = []
    for result in results:
        accounts.append(result._json['screen_name'])

    print("Compte(s) trouvé(s) pour '"+str(user)+"' : "+str(accounts))
    return accounts

def get_user_tweet(user,
                   limit=500,
                   outputtweet = "timeline/json",
                   outputmedia = "timeline/media"):

    api = common.twitthon_authentication.get_api()
    common.twitthon_acquisition.get_user_tweet(api, user, limit, outputtweet, outputmedia)

def get_tweet_from_keywords(keywords,
                            limit = 500,
                            outputtweet = "keywords/json",
                            outputmedia = "keywords/media"):

    api = common.twitthon_authentication.get_api()
    common.twitthon_acquisition.get_tweet_from_keywords(api, keywords, limit, outputtweet, outputmedia)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    user = sys.argv[1]

    accounts = get_accounts_from_user(user)
    # TODO: boucler sur les comptes twitter

    if len(accounts) > 0:
        # Get the first account, then get tweets
        user = accounts[0]
        get_user_tweet(user)
        get_tweet_from_keywords(user)