![vkbee](https://github.com/asyncvk/vkbee/blob/master/vkbee/bgtio.png?raw=true)

[Documentation](https://asyncvk.github.io)

[Example Bot](https://pastebin.com/raw/hxhXPyb9)

### vkbee
## Установка
```bash
pip3 install vkbee
```
Simple Async VKLibrary faster than vk_api
# Пример работы
```python
import asyncio
import vkbee

async def main(loop):
    token = "сюдатокен"
    vk_s = vkbee.VkApi(token, loop=loop)
    vk = vk_s.get_api()
    await vk_s.messages.send(
        chat_id=1,
        message='VKBEE',
        random_id=0
    )
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
```



