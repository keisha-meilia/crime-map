import os
DATABASE_URL = os.environ['DATABASE_URL']
JWT_SECRET = os.environ['JWT_SECRET']
JWT_EXPIRE_MINUTES = int(os.environ.get('JWT_EXPIRE_MINUTES', '60'))
JWT_ALGORITHM = 'HS256'
