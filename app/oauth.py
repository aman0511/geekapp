
from rauth import OAuth1Service, OAuth2Service
from flask import url_for, request, redirect, session
from config import OAUTH_CREDENTIALS


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.consumer_id = OAUTH_CREDENTIALS[provider_name]['id']
        self.consumer_secret = OAUTH_CREDENTIALS[provider_name]['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}
        )
        me = oauth_session.get('me').json()
        me = {
                'email': me['email'],
                'name': me['name'],
                'image': "//graph.facebook.com/"+me['id']+"/picture?type=large",
                'id': me['id']
            }
        return me


class TwitterSignIn(OAuthSignIn):
    def __init__(self):
        super(TwitterSignIn, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

    def authorize(self):
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )
        me = oauth_session.get('account/verify_credentials.json').json()
        social_id = 'twitter$' + str(me.get('id'))
        username = me.get('screen_name')
        me = {
                'email': 'none@gmail.com',
                'name': str(me.get('screen_name')),
                'image': "",
                'id': str(me.get('id'))
            }
        return me   # Twitter does not provide email


class LinkedinSignIn(OAuthSignIn):
    """docstring for Link"""
    def __init__(self):
        super(LinkedinSignIn, self).__init__('linkedin')
        self.service = OAuth1Service(
            name='linkedin',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.linkedin.com/uas/oauth/requestToken',
            authorize_url='https://api.linkedin.com/uas/oauth/authorize',
            access_token_url='https://api.linkedin.com/uas/oauth/accessToken',
            base_url='http://api.linkedin.com/v1/'
        )

    def authorize(self):
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url(),
                    'scope': "r_fullprofile r_emailaddress r_network"}
        )
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']},
            header_auth=True
        )
        me = oauth_session.get('people/~:(id,first-name,last-name,headline,maiden-name,formatted-name,picture-url,email-address)',
                               params={'type': 'SHAR', 'format': 'json'},
                               header_auth=True).json()
        me = {
                'email': me['emailAddress'],
                'name': me['formattedName'],
                'image': me['pictureUrl'],
                'id': me['id']
            }
        return me
