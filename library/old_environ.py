"""
Owner: Noctsol
Contributors: N/A
Date Created: 20210824

Summary:
    Wrapper class around python-dotenv. I didn't like alot of things....
    - It loaded on all your custom variables from your file ON TOP OF ALSO the global environment variables on your operating system.
    - It felt very hacky having all these unnessary environment variable unrelated to your project
    - Getting environment variable required the use of dotenv and os.getenv(). Why not just put this functionality into one class?
        - There should have been a Get() function like in here

"""


from dotenv import dotenv_values


class Environment():
    '''Example
    import environment

    env_path = "C:/Users/you/environment.env"
    ev = environment.Environment(env_path)
    ev.load()
    ev.get("somevar)
    '''
    def __init__(self, env_file_path):
        self.env_file_path = env_file_path
        self.environment_variable = None

    # Loads up environment variables
    def load(self):
        '''Loads up environment variables'''

        # Loading up default environment variables from current environment
        self.environment_variable = dotenv_values(self.env_file_path)

        return True

    # Fetches a value from environment environment variables - set to error out if key does not exist
    def get(self, env_key_str):
        '''Loads up environment variables'''

        # Throw exception if you forget to set the environment - I don't want to make this automatic - should be explicit
        if self.environment_variable is None:
            raise EnvVarNotSet()

        # Tries to get value - throws error if it doesn't exist
        try:
            value = self.environment_variable[env_key_str]
        except KeyError as error:
            raise EnvVarNotExistError(env_key_str) from error

        # Check if value is null or empty
        if not value:
            raise EnvVarEmptyError(env_key_str)

        return value


class EnvVarNotSet(Exception):
    '''Exception for when we didn't load'''

    def __init__(self):
        self.message = "Environment not set - please call Environment.load_env()"
        super().__init__(self.message)

class EnvVarNotExistError(Exception):
    '''Exception for when we call a nonexistent item'''

    def __init__(self, env_key):
        self.message = f"Environment variable key '{env_key}' not found"
        super().__init__(self.message)

class EnvVarEmptyError(Exception):
    '''Exception for when a environment var is empty or null'''

    def __init__(self, env_key):
        self.message = f"Environment variable key '{env_key}' has an empty or null value"
        super().__init__(self.message)
