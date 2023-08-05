# jx-bigquery

JSON Expressions for BigQuery


## Status

Feb 2020 - Active but incomplete:  Can insert [tidy](https://en.wikipedia.org/wiki/Tidy_data) JSON documents into BigQuery while managing the schema.

## Overview

The library is intended to manage multiple Big Query tables to give the illusion of one table with a dynamicly managed schema. 



## Background

* `partition` - Big data is split into separate containers based on age. This allows queries on recent data to use less resources, and allows old data to be dropped quickly
* `cluster` - A "cluster" is another name for the sorted order of the data in a partition. Sorting by the most commonly lookup will make queries faster
* `id` - The set of columns that identifies the document 


## Configuration

* `table` - Any name you wish to give to this table series
* `top_level_fields` - BigQuery demands that control columns are top-level.  Define them here.
* `partition` - 
  * `field` - The dot-delimited field used to partition the tables (must be time)
  * `expire` - When BigQuery will automatically drop your data. 
* `id` - The identification of documents 
  * `field` - the set of columns to uniquely identify this document
  * `version` - column used to determine age of a document; replacing newer with older
* `cluster` - Columns used to sort the partitions 
* `schema` - name: type dictionary - needed when there is no data and BigQuery demands column definitions
* `sharded` - *boolean* - set to `true` if you allow this library to track multiple tables. It allows for schema migration (expansion only), and for faster insert from a multitude of machines  
* `account_info` - The information BigQuery provides to connect 


### Example

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
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-project.iam.gserviceaccount.com"
    }
}
```

## Usage

Setup `Dataset` with an application name

```python
    destination = bigquery.Dataset(
        dataset=application_name, 
        kwargs=settings
    ).get_or_create_table(settings.destination)
```

Insert documents as you please


```python
    destination.extend(documents)
```

