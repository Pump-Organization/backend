class MockModel:
    def to_json(self):
        return self.__dict__
    
    def to_quickview(self):
        return self.__dict__

class MockUser(MockModel):
    def __init__(self, name, email, username, profile_pic) :
        self.name = name
        self.email = email
        self.username = username
        self.profile_pic = profile_pic

class MockFriendship(MockModel):
    def __init__(self, friendship_id, sender_id, recipient_id, status):
        self.friendship_id = friendship_id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.status = status
