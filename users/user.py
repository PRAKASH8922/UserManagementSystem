class User:
    """
    Python equivalent of original reference User.js model helper.
    """
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def get_user_details(self):
        return f"ID: {self.id}, Name: {self.name}, Email: {self.email}"
