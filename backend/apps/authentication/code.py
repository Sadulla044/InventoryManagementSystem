from django.conf import settings


class Code:
    def __init__(self, request):
        self.session = request.session
        code = self.session.get(settings.CODE_SESSION_ID)

        if not code:
            code = self.session[settings.CODE_SESSION_ID] = {}

        self.code = code

    def add(self, id, code):
        user_id = str(id)

        if user_id not in self.code:
            self.code[user_id] = {'code': code}
        else:
            self.code[user_id]['code'] = code

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, id):
        user_id = str(id)

        if user_id in self.code:
            del self.code[user_id]

        self.save()

    def get(self, id):
        user_id = str(id)

        if user_id in self.code:
            user_code = self.code[user_id]['code']
            return user_code
        else:
            return None
