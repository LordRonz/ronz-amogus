from utils.reddit import Reddit

async def get_r34():
    reddit = Reddit('rule34')

    return await reddit.get()
