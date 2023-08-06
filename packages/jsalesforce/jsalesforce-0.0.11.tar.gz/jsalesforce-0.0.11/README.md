# jSalesforce

jSalesforce is the python library for accessing the ETH juniors Salesforce. It currently is a collection of useful functions gathered for the jupyter notebooks on jautomatio.ethjuniors.ch.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install jSalesforce in development mode. First, copy the repo. The login for gitlab.ethz.ch is in the jWiki.

```bash
git clone "https://gitlab.ethz.ch/eth-juniors/jsalesforce"
```

Then install the package in development mode. This allows you to simply change the code or pull from gitlab without having to reinstall the package.

```bash
pip install --user -e jsalesforce
```

## Usage

To log in to Salesforce you need your username, password and security_token. This token can be obtained from the setup page from Salesforce. You get it by email and need to reset it if you loose it.
Credentials can be found on jautomation.ethjuniors.ch

```python
import jSalesforce

sf = jSalesforce.login(
    username="...",
    password="...",
    security_token="...",
)

# TODO: Show rest of the library
```
