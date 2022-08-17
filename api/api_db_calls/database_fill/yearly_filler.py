from requests_html import HTMLSession


session = HTMLSession()

r = session.get("https://www.google.com")

h = r.html.find('h1')

print(h)