import urllib.parse

def create_link(text):

    return (
        "https://wa.me/?text="
        + urllib.parse.quote(text)
    )
