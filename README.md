# External Backup and Restore CosmosDB CLI
Project to backup CosmosDB to file and restore to another CosmosDB Server.

## Starting

*  Clone this repo


*  Create venv and active

```bash
python3 -m venv env
source env/bin/activate
```
* install dependencys

```bash
pip install -r requirements.txt
```

* Use

## GET DB Info

```bash
RES_GROUP=<resource-group-name>
ACCT_NAME=<cosmos-db-account-name>

export ACCOUNT_URI=$(az cosmosdb show --resource-group $RES_GROUP --name $ACCT_NAME --query documentEndpoint --output tsv)
export ACCOUNT_KEY=$(az cosmosdb list-keys --resource-group $RES_GROUP --name $ACCT_NAME --query primaryMasterKey --output tsv)
```


## Backup

```bash
python3 -m main backup --container $COSMOSDB_CONTAINER --database $COSMOSDB_DB --host $ACCOUNT_URI --key ACCOUNT_KEY
```

## Restore

```bash
python3 -m main restore --container $COSMOSDB_CONTAINER --database $COSMOSDB_DB --host $COSMOSDB_URI --key $COSMOSDB_KEY
```
> If Container or database not exist, they will be created in restore process

## TODO
* More easy cli
* Install instructions