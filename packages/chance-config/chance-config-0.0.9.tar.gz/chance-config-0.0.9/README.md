# Config ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

Config is a Python-based project for reading configurations from YAML files.

## Installation

### Requirements

- Python 2.7 and up
- pkg_resources
- pyYAML

```bash
pip install chance-config
```

## Usage

### Read configs with `chanconfig`

```python
import chanconfig

# With package given
chanconfig.Config('test.yaml', 'foo.conf')

# With relative/absolute path
chanconfig.Config('foo/conf/test.yaml')

# With arguments and settings
# The priority is: Env > Args > Config files
# Settings should be a dict of key and env name, process method and default
# value. Notice that env name can be None adn process method should be callable.
fake_process = lambda x: int(x)

chanconfig.MultipleConfig(
    # config files
    # {'test': 'test', 'test_nested': {'test': 'test'}}
    "test.yml", "chanconfig.conf",
    # command arguments
    {
        '--test_arg': 'test',
        '--kafka.ok': 'ok',
        '--test_nested.test': 'new_test'
    },
    # arguments settings, as { key: (env_name, process_method, default) }
    {
        'test_env': ('FAKE_ENV', fake_process, None),
        'test_def': (None, fake_process, 3),
        'test': ('FAKE_TEST', None, None),
        'test_exception': ('FAKE_TEST', None, None),
        'test_nested.test': ('FAKE_TEST', None, None),
        'test_nested.test_def': ('FAKE_TEST', None, 'test'),
    }
)
```

### Configs result

```python
{
    'kafka': {
       'ok': 'ok'
    },
    'test': 'test',
    'test_arg': 'test',
    'test_def': 3,
    'test_env': 3,
    'test_exception': None,
    'test_nested': {
        'test': 'new_test', 'test_def': 'test'
    }
}
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
