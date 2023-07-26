import yaml

class Config(object):
    def __init__(self, path=None) -> None:
        self.server = {}
        self.server['name'] = None
        self.server['ip'] = None
        self.server['port'] = None

        self.auth = {}
        self.auth['ip-list'] = []
        self.auth['api-keys'] = []

        self.epics = {}
        self.epics['state'] = None
        self.epics['set-env'] = None
        self.epics['addr-list'] = None
        self.epics['auto-addr'] = None
        self.epics['server-port'] = None
        self.epics['pv-list'] = []
        if path is None:
            path = '.\\config.yaml'
        self.read_config(path)
    
    def read_config(self, path):
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
            self.server['name'] = config['server']['name']
            self.server['ip'] = config['server']['ip']
            self.server['port'] = config['server']['port']

            self.auth['ip-list'] = config['auth']['ip-list']
            self.auth['api-keys'] = config['auth']['api-keys']

            self.epics['state'] = config['epics']['state']
            self.epics['set-env'] = config['epics']['set-env']
            self.epics['addr-list'] = config['epics']['addr-list']
            self.epics['auto-addr'] = config['epics']['auto-addr']
            self.epics['server-port'] = config['epics']['server-port']
            self.epics['pv-list'] = config['epics']['pv-list']

if __name__ == '__main__':
    config = Config()
    print(config.server)
    print(config.auth)
    print(config.epics)