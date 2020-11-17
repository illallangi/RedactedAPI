from sys import stderr

from click import Choice as CHOICE, STRING, argument, group, option

from loguru import logger

from notifiers.logging import NotificationHandler

from illallangi.redactedapi import API as RED_API, ENDPOINTDEF as RED_ENDPOINTDEF


@group()
@option('--log-level',
        type=CHOICE(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'SUCCESS', 'TRACE'],
                    case_sensitive=False),
        default='DEBUG')
@option('--slack-webhook',
        type=STRING,
        envvar='SLACK_WEBHOOK',
        default=None)
@option('--slack-username',
        type=STRING,
        envvar='SLACK_USERNAME',
        default=__name__)
@option('--slack-format',
        type=STRING,
        envvar='SLACK_FORMAT',
        default='{message}')
def cli(log_level, slack_webhook, slack_username, slack_format):
    logger.remove()
    logger.add(stderr, level=log_level)

    if slack_webhook:
        params = {
            "username": slack_username,
            "webhook_url": slack_webhook
        }
        slack = NotificationHandler("slack", defaults=params)
        logger.add(slack, format=slack_format, level="SUCCESS")


@cli.command(name='get-index')
@option('--api-key',
        '--redacted-api-key',
        type=STRING,
        required=True)
@option('--endpoint',
        type=STRING,
        required=False,
        default=RED_ENDPOINTDEF)
@option('--cache/--no-cache', default=True)
def get_index(api_key, endpoint, cache):
    logger.info(RED_API(api_key, endpoint, cache).get_index())


@cli.command(name='get-torrent')
@option('--api-key',
        '--redacted-api-key',
        type=STRING,
        required=True)
@option('--endpoint',
        type=STRING,
        required=False,
        default=RED_ENDPOINTDEF)
@option('--cache/--no-cache', default=True)
@argument('hash',
          type=STRING,
          required=True)
def get_torrent(api_key, endpoint, hash, cache):
    logger.info(RED_API(api_key, endpoint, cache).get_torrent(hash))


@cli.command(name='get-group')
@option('--api-key',
        '--redacted-api-key',
        type=STRING,
        required=True)
@option('--endpoint',
        type=STRING,
        required=False,
        default=RED_ENDPOINTDEF)
@option('--cache/--no-cache', default=True)
@argument('hash',
          type=STRING,
          required=True)
def get_group(api_key, endpoint, hash, cache):
    logger.info(RED_API(api_key, endpoint, cache).get_group(hash))


@cli.command(name='get-directory')
@option('--api-key',
        '--redacted-api-key',
        type=STRING,
        required=True)
@option('--endpoint',
        type=STRING,
        required=False,
        default=RED_ENDPOINTDEF)
@option('--cache/--no-cache', default=True)
@argument('hash',
          type=STRING,
          required=True)
def get_directory(api_key, endpoint, cache, hash):
    logger.info(RED_API(api_key, endpoint, cache).get_directory(hash))


@cli.command(name='rename-torrent-file')
@option('--api-key',
        '--redacted-api-key',
        type=STRING,
        required=True)
@option('--endpoint',
        type=STRING,
        required=False,
        default=RED_ENDPOINTDEF)
@option('--cache/--no-cache', default=True)
@argument('hash',
          type=STRING,
          required=True)
@argument('path',
          type=STRING,
          required=True)
def rename_torrent_file(api_key, endpoint, cache, hash, path):
    logger.info(RED_API(api_key, endpoint, cache).rename_torrent_file(hash, path))


if __name__ == "__main__":
    cli()
