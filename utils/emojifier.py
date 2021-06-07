from string import ascii_lowercase

SPECIALCODES = {
    '0': ':zero:',
    '1': ':one:',
    '2': ':two:',
    '3': ':three:',
    '4': ':four:',
    '5': ':five:',
    '6': ':six:',
    '7': ':seven:',
    '8': ':eight:',
    '9': ':nine:',
    '#': ':hash:',
    '*': ':asterisk:',
    '?': ':grey_question:',
    '!': ':grey_exclamation:',
    ' ': '   '
}

async def get_emojified_text(msg: str) -> str:
    msg = ' '.join(msg.split())

    if len(msg) > 69:
        return 'Keep it under 69 characters fam'

    return ''.join(f':regional_indicator_{c}: ' if c in ascii_lowercase else f'{SPECIALCODES[c]} ' if c in SPECIALCODES else '' for c in msg.lower())
