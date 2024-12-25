# Ingest API content using Python

## Summary

This sample contains a Microsoft Graph connector built in Python that shows how to ingest api endpoints. it extracts the data and maps it to the external connection's schema and ingests the content. The ingested content is set to be visible to everyone in the organization.

## Contributors

- [Guy Mazouz](https://github.com/guyyosan)

## Prerequisites

- [Microsoft 365 Developer tenant](https://developer.microsoft.com/microsoft-365/dev-program)
- [Microsoft Graph CLI](https://devblogs.microsoft.com/microsoft365dev/microsoft-graph-cli-v1-0-0-release-candidate-now-with-beta-support/)
- [jq](https://jqlang.github.io/jq/)
- [pyenv](https://github.com/pyenv/pyenv)

## Minimal path to awesome

- Clone this repository
- Follow the script:

    ```sh
    # make the setup script executable
    chmod +x ./setup.sh
    # create Entra app
    ./setup.sh
    # ensure you've got Python 3.11 installed
    pyenv install 3.11
    # use Python 3.11 in the project
    pyenv local 3.11
    # create virtual environment
    python3 -m venv venv
    # activate virtual environment
    source venv/bin/activate
    # restore dependencies
    pip install -r requirements.txt
    # create connection
    python3 main.py create-connection
    # load content
    python3 main.py load-content
    # deactivate virtual environment
    deactivate
    ```

## Features

This sample shows how to ingest data from api  to Microsoft 365. The api data is parsed and ingested by the sample Microsoft Graph connector.

The sample illustrates the following concepts:

- script creating the Entra (Azure AD) app registration using the Microsoft Graph CLI
- create external connection including URL to item resolver to track activity when users share external links
- create external connection schema
- parse api data
- ingest data
- visualize the external content in search results using a custom Adaptive Card
- extend Microsoft Graph Python SDK with a middleware to wait for a long-running operation to complete
- extend Microsoft Graph Python SDK with a debug middleware to show information about outgoing requests and incoming responses

## Help

We do not support samples, but this community is always willing to help, and we want to improve these samples. We use GitHub to track issues, which makes it easy for  community members to volunteer their time and help resolve issues.


## Disclaimer

**THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.**
