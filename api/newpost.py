from flask import *
from model.model import s3
newpost_blueprint = Blueprint('newpost', __name__)


@newpost_blueprint.route("/api/image", methods=["POST"])
def newpost():
    file = request.files['file']
    filename = file.filename
    s3.Bucket("myawscloudfiles").put_object(
        Key=file.filename, Body=file)
    return {"imgurl": f"https://d33yfiwdj1z4d4.cloudfront.net/{filename}"}
