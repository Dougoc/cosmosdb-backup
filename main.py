from azure.cosmos import CosmosClient, PartitionKey, exceptions
import json
import click
import os


@click.group()
def cli():
    """A CLI wrapper for architecturing map"""


@click.option('--container', help='CosmosDB Container name')
@click.option('--database', help='CosmosDB Database name')
@click.option('--key', help='CosmosDB Key')
@click.option('--host', help='CosmosDB Host')
@cli.command()
def backup(host: str, key: str, database: str, container: str):
    """A CLI wrapper for backup CosmosDB"""
    client = CosmosClient(host, credential=key)
    db = client.get_database_client(database)
    ct = db.get_container_client(container)
    entrances = []
    for item in ct.query_items(
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
    client = CosmosClient(host, credential=key)

    try:
        db = client.create_database(database)
    except exceptions.CosmosResourceExistsError:
        db = client.get_database_client(database)

    try:
        ct = db.create_container(id=container, partition_key=PartitionKey(path="/productName"))
    except exceptions.CosmosResourceExistsError:
        ct = db.get_container_client(container)
    except exceptions.CosmosHttpResponseError:
        raise

    print('open file')
    with open(file, 'r') as content:
        full_backup = json.loads(content.read())
        for item in full_backup:
            print(f'Write item {item}')
            ct.upsert_item(item)

    print('Restore finished')


if __name__ == '__main__':
    cli()

commands = click.CommandCollection(sources=[cli])
