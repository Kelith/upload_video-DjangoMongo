import os,datetime
import ffmpeg
from werkzeug.utils import secure_filename
from .serializers import VideoMetadataSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage



UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/media/'
ALLOWED_EXTENSIONS = set(['.webm', '.mp4', '.m4a', '.m4v', '.wmv', '.wma', '.mpeg', '.mov', '.avi', '.wmv', '.flv'])


# Returns True if the extension of filename is in the list of allowed extensions
def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

# Helper function that saves the video file coming from the POST request at /video, extracts his metadata
# and saves the metadata into a mongoDB database.
# Currently saving Name - Path - Timestamp - Duration - Bitrate
def save_video(file):
    now = datetime.datetime.now()
    timestamp = str(now.strftime("%Y-%m-%d_%H-%M-%S"))       
    filenameTimestamped = os.path.splitext(file.name)[0]+"__"+timestamp+ os.path.splitext(file.name)[1]
    filename = secure_filename(filenameTimestamped)

    with default_storage.open(''+filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    video_path = os.path.join(UPLOAD_FOLDER, filename)   
    file = open(os.path.join(UPLOAD_FOLDER, filename), 'rb')


    metadata = ffmpeg.probe(video_path)

    serializer = VideoMetadataSerializer(data={'name': filename,'path': metadata.get("format").get("filename"),'timestamp': now,'duration_s':metadata.get("format").get("duration"),'bit_rate_kbps':int(int(metadata.get("streams")[0].get("bit_rate"))/1000)})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
