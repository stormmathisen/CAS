import yaml

with open('.\config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    print(config)
    print(config['server']['name'])