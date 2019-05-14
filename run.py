from website.config import PORT, HOST
from website.app import app
import website.routes

app.run(port=PORT, host=HOST)
