class Config:
    class DbDev:
        dbname = ""
        user = ""
        password = ""
        host = ""
        port = 0

    class DbMaster:
        dbname = ""
        user = ""
        password = ""
        host = ""
        port = 0

    class DbLocal:
        dbname = "postgres"
        user = "postgres"
        password = "mysecretpassword"
        host = "0.0.0.0"
        port = 5432
