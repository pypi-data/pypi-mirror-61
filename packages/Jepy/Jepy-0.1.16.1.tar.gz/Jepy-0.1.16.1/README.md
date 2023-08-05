# Jepy

A simple Python wrapper to access the Johns Eastern Company API.

## Installation

To get Jepy on your machine, ensure you're running Python 3.7 or higher and use `pip install jepy`.

(Note that it will almost definitely work on Python 3.4+ and will likely work on any version of Python 3 or higher but has not been tested below 3.7).

## Getting Started

Jepy is designed to handle the JWT authentication required by the API for you easily.

Import Jepy and set up the client.

```python
from jepy import Jepy

creds = {'user_id': '0123456789', 'password': '0123456789876543210'}
client = Jepy(**creds)
```

Then use the client you've set up to make calls.

```python
client.claims(claim_num = '012345')
```

### Usage

Jepy supports all endpoints of the API. See the [wiki](https://github.com/JECO/jepy/wiki) for detailed information.

For information on the API itself, see the [API wiki](https://github.com/JECO/jeapi-docs/wiki).

### Interpreting Results

The API answers calls by dumping results into a JSON file with one of three keys. Jepy handles these as follows:
  * Results - Returns a dictionary keyed as 'results', value will be a list of dictionaries.
  *	Message - Like results, this returns a dictionary keyed as 'message', the value is a message from the server that is not an error. Most often this means no results were found.
  *	Error - Raises an exception. Usually indicates authentication failed, the request syntax is bad, or the server is down.

## Troubleshooting

If you're continuously getting errors, check the status of the server to ensure it is up.

__Simply checking server status does not require authentication__ (and is the only command that does not).

Run `print(Jepy())` with no arguments. You'll either get `JEAPI is up.` or an exception. (Note that if you do try to check status with credentials a la `print(Jepy(**creds))` you will get the object).

If the server is up, your credentials may be invalid and you should contact the [Johns Eastern Helpdesk](https://je.zendesk.com/hc/en-us/requests/new) for assistance.

You can also [click here](https://je-api.com/) to see if the server is up, too.

## Operating System

This package is operating system agnostic. It has been tested on Windows 10 and Ubuntu 19.10.

## Dependencies

Jepy wouldn't be possible without [Requests](https://pypi.org/project/requests/). It is the only non-built-in dependency (and it will automatically install with `pip`).

## Bug Reports/Feature Requests

To report a bug, please use the "New issue" button on the project's [Issues page](https://github.com/JECO/jepy/issues). You may also contact the help desk below to report bugs.

Please submit a ticket at the [Johns Eastern Helpdesk](https://je.zendesk.com/hc/en-us/requests/new) for all feature requests.

Note that features that require changes to the API itself may not require any update in the wrapper (such as a change to a query). In this case, the branch will not be public and will exist under the API's repository.

## License

This project is licensed under the GNU General Public License v3.0. Please see the [LICENSE.md](LICENSE.md) file for details.
