# Chance-mock-logger ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

ChanceMockLogger is a Python library for capturing the output of logging to be evaluated in tests.

## Installation

### Requirements
* Linux
* Python 2.7 and up

`$ pip install chance-mock-logger`

## Usage

```python
from mock_logger import MockLoggingHandler


# Initialize handler
HANDLER = MockLoggingHandler()


# Setup logger
logger = logging.getLogger(THE_NAME_OF_YOUR_LOGGER)
logger.addHandler(HANDLER)


# Start Capture
HANDLER.reset()

#...Something is done with logger

# Checkout the output
HANDLER.messages("error")
HANDLER.messages("info")
HANDLER.messages("warning")
HANDLER.messages("debug")
```

## Development
```
$ virtualenv mock_logger
$ . mock_logger/bin/activate
$ pip install -e .
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
