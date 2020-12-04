class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://hardware_store:qwerty@localhost:5432/kauppa'
    SQLALCHEMY_TRACK_MODIFICATIONS = False