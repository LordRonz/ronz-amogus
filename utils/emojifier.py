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
    if len(msg) > 69:
        return 'Keep it under 69 characters fam'

    msg = ' '.join(msg.split())

    return ''.join(f':regional_indicator_{c}: ' if c.isalpha() else f'{SPECIALCODES[c]} ' if c in SPECIALCODES else '' for c in msg)
