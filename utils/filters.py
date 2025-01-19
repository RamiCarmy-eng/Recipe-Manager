from markupsafe import Markup

def nl2br(value):
    result = str(value).replace('\n', '<br>\n')
    return Markup(result) 