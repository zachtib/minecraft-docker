import os
import time
import re

import docker
from slackclient import SlackClient

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+)>(.*)"
DOCKER_SOCKET = None
MESSAGE_REGEX

class SlackBridge:
    def __init__(self, slack_bot_token, docker_container, channel):
        self.slack_client = SlackClient(slack_bot_token)
        self.slackbot_id = None
        client = docker.from_env()
        self.container = client.containers.get(docker_container)
        self.channel = channel
    
    async def monitor_container(self, container):
        for line in container.logs(stream=True):
            line = line.strip()
            matches = re.search(MESSAGE_REGEX, line)
            if matches:
                send_message_to_slack(self.channel, matches.group(1), matches.group(2))

    def send_message_to_slack(self, channel, sender, message):
        self.slack_client.api_call(
            'chat.postMessage',
            channel=channel,
            text=f'{sender}: {message}'
        )
    
    def send_message_to_minecraft(self, sender, message):
        command = f'/say {sender}: {message}'
        pass
    
    def start(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print('Connected and running')



if __name__ == '__main__':
    print('Starting slack bridge...')
    token = os.environ.get('SLACK_BOT_TOKEN', '')
    bridge = SlackBridge(token)
    bridge.start()
    print('Stopping')