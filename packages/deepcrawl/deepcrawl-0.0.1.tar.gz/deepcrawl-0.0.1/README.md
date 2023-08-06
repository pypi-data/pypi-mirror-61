# DeepCrawl API Wrapper

This is a package to simplify use of the DeepCrawl API.

pip install deepcrawl

# Usage

import deepcrawl

#Specify your API credentials
API_ID = '1234'
API_KEY = 'myapikey'

# Create a new connection using API credentials
dc = deepcrawl.ApiConnection(API_ID, API_KEY)

# Get a specific project and output the name
account_id = 19
project_id = 314267
project = dc.get_project(account_id, project_id)
print(project.project_settings.name)

