import sys
import psycopg2
import logging
import configparser
import hashlib


class Logger(object):
    _logger = None

    @classmethod
    def _init_logger(cls):
        cls._logger = logging.getLogger('Main')
        cls._logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        ch.setFormatter(formatter)
        cls._logger.addHandler(ch)

    @classmethod
    def get_logger(cls):
        if not cls._logger:
            cls._init_logger()
        return cls._logger


class TM(object):
    connections = None
    logger = None

    def __init__(self):
        self.connections = []
        self.logger = Logger.get_logger()

    def add(self, query, connect):
        if connect not in self.connections:
            connect.tpc_begin(
                connect.xid(0,
                            u'tran{0:s}'.format(
                                hashlib.sha224(
                                    query.encode('utf-8')).hexdigest()),
                            ''))
            self.connections.append(connect)
            self.logger.info('connect %s was successfully added' % str(connect))

        cursor = connect.cursor()
        cursor.execute(query)

    def commit(self):
        try:
            for connect in self.connections:
                connect.tpc_prepare()

        except psycopg2.Error as e:
            self.logger.error('Exception: %s\nRollback all' % str(e))
            for connect in self.connections:
                connect.tpc_rollback()

        else:
            self.logger.info('Ok. Committing all...')
            for connect in self.connections:
                connect.tpc_commit()


class Connector(object):
    conn = None
    logger = None

    def __init__(self, dbname):
        self.logger = Logger.get_logger()
        self._get_config_options()
        try:
            self.conn = psycopg2.connect("dbname=%s user=%s "
                                         "host=%s password=%s" %
                                         (dbname, self.user,
                                          self.host,
                                          self.password))
        except Exception as e:
            self.logger.error("Unable to connect to the database: {0}".format(e))
            sys.exit(2)

    def _get_config_options(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        section = 'database'
        try:
            self.host = config.get(section, 'host')
            self.user = config.get(section, 'user')
            self.password = config.get(section, 'password')
        except Exception as e:
            self.logger.error("Config reading exception: {0}".format(e))
            sys.exit(2)

    def get_connect(self):
        return self.conn
