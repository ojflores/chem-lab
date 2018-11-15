from rest_framework.authentication import TokenAuthentication as OldTokenAuthentication


class TokenAuthentication(OldTokenAuthentication):
    def __init__(self):
        super(TokenAuthentication, self).__init__()
        self.keyword = 'Bearer'
