from umbreon import Client, RoutingTable
import trio


TOKEN = '<TOKEN>'
client = Client(TOKEN)


@client.on_dispatch('MESSAGE_CREATE')
async def message_counter(client, message):
    if message.author.bot:
        return

    if not message.author.storage.messages:
        message.author.storage.messages = 0

    message.author.storage.messages += 1

    if message.content == '!messages':
        await client.http.request(
            RoutingTable.create_message,
            {
                'content':
                f'you\'ve sent {message.author.storage.messages} messages.'
            },
            channel_id=message.channel_id
        )
    elif message.content == '!hoist':
        role = message.member.hoisted_role
        if role:
            role = role.name

        await client.http.request(
            RoutingTable.create_message,
            {'content': f'your hoisted role is **{role}**'},
            channel_id=message.channel_id
        )


async def test():
    async with trio.open_nursery() as nursery:
        await client.start_gateway(nursery)

trio.run(test)
