import os
from pathlib import Path

from aws_cdk import Stack, Tags
from constructs import Construct
from git import Repo
from my_service.lambda_cron_construct import LambdaCronConstruct  # type: ignore

from cdk.my_service.constants import SERVICE_NAME


def get_stack_name() -> str:
    repo = Repo(Path.cwd())
    try:
        username = os.getlogin().replace('.', '-')
    except Exception:
        username = 'github'
    print(f'username={username}')
    try:
        return f'{username}-{repo.active_branch}-{SERVICE_NAME}'
    except TypeError:
        return f'{username}-{SERVICE_NAME}'


class ServiceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        Tags.of(self).add('schedule', SERVICE_NAME)

        self.lambdas = LambdaCronConstruct(self, f'{id}cron_lambda'[0:64])
