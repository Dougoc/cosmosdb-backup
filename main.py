from azure.cosmos import CosmosClient, PartitionKey, exceptions
import json
import click
import os


@click.group()
def cli():
    """A CLI wrapper for architecturing map"""


@click.option('--container', help='List of endpoints')
@click.option('--database', help='List of endpoints')
@click.option('--key', help='List of endpoints')
@click.option('--host', help='List of endpoints')
@cli.command()
def backup(host: str, key: str, database: str, container: str):
    """A CLI wrapper for backup CosmosDB"""
    url = host
    key = key
    client = CosmosClient(url, credential=key)
    database_name = database
    database = client.get_database_client(database_name)
    container_name = container
    container = database.get_container_client(container_name)
    entrances = []
    for item in container.query_items(
            query='SELECT * FROM account',
            enable_cross_partition_query=True):
        entrances.append(item)

    to_save = [dict(x) for x in entrances]
    _write_backup(to_save)

    print('Backup finished')


def _write_backup(content):
    backup_file = 'cosmosdb.db'
    if os.path.isfile(backup_file):
        os.remove(backup_file)

    with open(backup_file, 'a') as file:
        file.write(json.dumps(content, indent=True))


@click.option('--file', default='cosmosdb.db', help='Backup filed to restore')
@click.option('--container', help='CosmosDB Container name')
@click.option('--database', help='CosmosDB Database name')
@click.option('--key', help='CosmosDB Key')
@click.option('--host', help='CosmosDB Host')
@cli.command()
def restore(host: str, key: str, database: str, container: str, file: str):
    """A CLI wrapper for Restore cosmosDB"""
    url = host
    key = key
    client = CosmosClient(url, credential=key)
    database_name = database
    container_name = container

    try:
        database = client.create_database(database_name)
    except exceptions.CosmosResourceExistsError:
        database = client.get_database_client(database_name)

    try:
        container = database.create_container(id=container_name, partition_key=PartitionKey(path="/productName"))
    except exceptions.CosmosResourceExistsError:
        container = database.get_container_client(container_name)
    except exceptions.CosmosHttpResponseError:
        raise

    print('open file')
    with open(file, 'r') as content:
        full_backup = json.loads(content.read())
        for item in full_backup:
            print(f'Write item {item}')
            #print(json.dumps(item, indent=4))
            container.upsert_item(item)

    print('Restore finished')


if __name__ == '__main__':
    cli()
# commands = click.CommandCollection(sources=[cli])