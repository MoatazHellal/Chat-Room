import subprocess
import threading

class Room:
    def __init__(self, name, chatroom_keys_path):
        self.key_path = str(chatroom_keys_path) + '\\' + name.replace(' ', '_') + '.pem'
        self.name = name
        self.users = {}
        self.messages = []
        self.user_lock = threading.Lock()
        self.message_lock = threading.Lock()
        self.__generate_key()

    def __generate_key(self):
        print('Generating key for room', self.name)
        result = subprocess.run([
        'openssl', 'genrsa', '-aes256', '-passout', 'pass:' + self.name, '-out', self.key_path, '2048'
        ], capture_output=True)
        if result.returncode != 0:
            print("Error generating key:", result.stderr)
        return result

    def join(self, user):
        self.__add_user(user)
        self.send_message(user.name + " has joined the room.")

    def leave(self, user_name):
        self.__remove_user(user_name)
        self.send_message(user_name, " has left the room.")

    def __add_user(self, user):
        # self.user_lock.acquire()
        self.users[user.name] = user
        user.define_room(self)
        # self.user_lock.release()

    def __remove_user(self, user_name):
        # self.user_lock.acquire()
        self.users.pop(user_name)
        # self.user_lock.release()

    def send_message(self, message):
        #self.message_lock.acquire()
        print('Sending message to room', self.name, ':', message)
        self.messages.append(message)

    def get_messages(self, last_received_id):
        # self.message_lock.acquire()
        messages = self.messages[last_received_id:]
        # self.message_lock.release()
        return messages

    