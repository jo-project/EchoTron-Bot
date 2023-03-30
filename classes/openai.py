import openai
import os
import aiohttp
import io
import discord
import replicate
openai.api_key = os.getenv("OPENAI_KEY")

async def generate_image(user: str, prompt: str):
    completion = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
    )
    image_url = completion.data[0].url
    file = await url_to_image(user, image_url)
    return file

async def generate_image_replica(user: str, prompt: str, type: str):
    if type == 'diffusion':
        output = replicate.run("tstramer/midjourney-diffusion:436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b", input={"prompt": f"mdjrny-v4 style {prompt}", "scheduler": "K_EULER_ANCESTRAL"})
    elif type == 'openjourney':
        output = replicate.run("prompthero/openjourney:9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb", input={"prompt": f"mdjrny-v4 {prompt}"})
    
    print(output[0])
    url = output[0]
    file = await url_to_image(user, url)
    return file
    
async def generate_answer(prompt: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an assistant that is super good at programming. You alwasys explain every single detail of a function. You always format code using markdown like in discord"}, {"role": "user", "content": f"{prompt}"}]
    )
    res = completion.choices[0].message['content']
    return res
    
async def url_to_image(user: str, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return print('Could not download')
            data = io.BytesIO(await resp.read())
            return discord.File(data, f"{user}.png")