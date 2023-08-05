# jx-bigquery
JSON Expressions for BigQuery


## Configuration

```json
{
    "table": "my_table_name",
    "top_level_fields": {},
    "partition": {
        "field": "submit_time",
        "expire": "2year"
    },
    "id": {
        "field": "id",
        "version": "last_modified"
    },
    "cluster": [
        "id",
        "last_modified"
    ],
    "schema": {
        "id": "integer",
        "submit_time": "time",
        "last_modified": "time"
    },
    "sharded": true,
    "account_info": {
        "private_key_id": {
            "$ref": "env://BIGQUERY_PRIVATE_KEY_ID"
        },
        "private_key": {
            "$ref": "env://BIGQUERY_PRIVATE_KEY"
        },
        "type": "service_account",
        "project_id": "my-project-id",
        "client_email": "me@my_project.iam.gserviceaccount.com",
        "client_id": "12345",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test-treeherder-extract%40moz-fx-dev-ekyle-treeherder.iam.gserviceaccount.com"
    }
}
```


* `table` - Any name you wish to give to this table, the 
* `top_level_fields` - Map from 
* `partition` - 
        "field": "submit_time",
        "expire": "2year"
    },
* `id` - 
        "field": "id",
        "version": "last_modified"
    },
* `cluster` - 
        "id",
        "last_modified"
    ],
* `schema` - 
        "id": "integer",
        "submit_time": "time",
        "last_modified": "time"
    },
* `sharded": true` - 
* `account_info` - The content of the application  






## Usage

Setup `Dataset` with an applicaiotn name

```python
    destination = bigquery.Dataset(
        dataset=application_name, 
        kwargs=settings
    ).get_or_create_table(settings.destination)
```




```python
    destination.extend(documents)
```

