# GeoSpock CLI

## Installation

### Installing the CLI from pip
```
    $ python -m venv geospock_cli
    $ source geospock_cli/bin/activate
    $ python -m pip install geospock-cli
```

### Installing the CLI from Git

- Clone the repo to your computer
- Run the following commands in the geospock-cli directory:
```
 $ virtualenv venv
 $ . venv/bin/activate
 $ pip install --editable .
```

### Initialisation and Getting Credentials
The `init` command creates a configuration file with the argument values for your your deployment:

`geospock init --clientid abcdefgh1234 --audience https://testaudience.geospock.com --auth0url login.test.com 
--request-address https://testrequest.geospock.com/graphql`

An optional `--profile {profileID}` argument can be used to set up configurations for multiple GeoSpock deployments.
All subsequent `geospock` commands can then use this profile flag to specify that deployment.

To authenticate the CLI to use your GeoSpock account, the following command can be used (alternatively this will be run
automatically when a user first tries to use a command).

`geospock get-credentials [--profile {profileID} --no-browser]`

This will open a web-page in the user's default web browser to authenticate. If the `--no-browser` flag is added, this 
will instead provide a web-address for a user to visit in order to authenticate.
The user should enter their GeoSpock username and password when requested to authorise the CLI.
This process should only be required once per user per profile.

### Running the CLI
The CLI can be activated at the command line using `geospock COMMAND ... [--profile {profileID}]`
A list of commands can be shown by using `geospock help [--profile {profileID}]`. Further information on the 
input types of each command can be obtained by running `geospock help COMMAND [--profile {profileID}]`.