from faker import Faker

class User:

    MISSING_FIELDS = "Email, password and name are required fields"
    ALREADY_EXISTS = "User already exists"
    NO_AUTHORIZATION = "You should be authorised"
    EMAIL_EXISTS = "User with such email already exists"
    INVALID_CREDENTIALS = "email or password are incorrect"
    SUCCESSFULLY_REMOVED = "User successfully removed"

    @staticmethod
    def valid_user():
        fake = Faker()

        name = fake.first_name()
        email = fake.email()
        password = fake.password()

        return {
            "name": name,
            "email": email,
            "password": password
        }
    
    
