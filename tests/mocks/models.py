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

class MockWorkout(MockModel):
    def __init__(self, title, description):
        self.title = title
        self.description = description

class MockAttendee(MockModel):
    def __init__(self, attendee_id, workout_id, user_id, attendee_type="guest", status="pending"):
        self.attendee_id = attendee_id
        self.workout_id = workout_id
        self.user_id = user_id
        self.attendee_type = attendee_type
        self.status = status

class MockProfile(MockModel):
    def __init__(self, name, email, username, profile_pic, num_friends, workout_counts):
        self.name = name
        self.email = email
        self.username = username
        self.profile_pic = profile_pic
        self.num_friends = num_friends
        self.workout_counts = workout_counts
