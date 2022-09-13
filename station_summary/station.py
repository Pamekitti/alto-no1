# Station Class
class Station:
    """
    Extract data from a sracped html while, at the same time, store them as a class
    This class is used in get_id_table.py
    """
    def __init__(self, content, name, href, st_id):
        self.content = content
        self.name = name
        self.href = href
        self.id = st_id

    # Get station info
    @classmethod
    def from_datasource(cls, content):
        name = content.text.strip()
        href = content['href']
        st_id = int(href.split('=')[1])
        return cls(content, name, href, st_id)
