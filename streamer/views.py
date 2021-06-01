from datetime import datetime
from tkinter.font import names
from unicodedata import name
from django.http.response import HttpResponseServerError, StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import cv2
import datetime 
import face_recognition
from face_recognition.api import face_encodings
import numpy
import os
import pickle
from .models import Person
from django.db import connection

studs=Person
connection.close()

def arrtobyte(arr):
    return arr.dumps()

def bytetoarr(text):
    return pickle.loads(text)

def findEncodings(images):      #returns list Encoded images of all the photos in Train Image
    encodedImages=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encodedImages.append(face_recognition.face_encodings(img)[0])
    return encodedImages

temp=list(studs.objects.values_list('face_encodes',flat=True))
names=list(studs.objects.values_list('name',flat=True))
faces=[pickle.loads(x) for x in temp]
face_encodes=findEncodings(faces)
def index(request):
    try:
        try:
            d4 = datetime.date.today().strftime("%Y-%m-%d")
            if d4==request.POST['date']:
                return render(request,'template.html',{'date':'LiveTable','student':Person.objects.all()})
                print('today')
            else:
                d4=datetime.strptime(request.POST['date'], '%Y-%m-%d')
                return render(request,'template.html',{'date':d4.strftime('%d-%m-%Y'),'student':Person.objects.all()})
                print(d4)
        except:
            return render(request,'template.html',{'date':'LiveTable','student':Person.objects.all()})
            print(d4,'execption')
    except:
        return "Something went Wrong!"



def getframe():
    stream=cv2.VideoCapture(0)
    while True:
        result,frame= stream.read()
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        faceLoc=face_recognition.face_locations(frameRGB)
        encodedFrames = face_recognition.face_encodings(frameRGB,faceLoc)

        for enFace,loc in zip(encodedFrames,faceLoc):
            cv2.rectangle(frame, (loc[3], loc[0]), (loc[1], loc[2]), (0, 0, 255), 2)
            matches = face_recognition.compare_faces(face_encodes,enFace)
            faceDis = face_recognition.face_distance(face_encodes,enFace)
            mostAccInx = numpy.argmin(faceDis)

            if matches[mostAccInx]:
                name1=names[mostAccInx]
                student=Person.objects.filter(name=name1)[0]
                student.duration= student.duration + datetime.timedelta(seconds=1)
                student.save()
                cv2.putText(frame,name1,(loc[3], loc[0]-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8,(0,255,0),2)
        frame=cv2.imencode('.jpg',frame)[1]
        strimg=frame.tostring()
        yield (b'--frame\r\n'b'Content-Type: image/plain\r\n\r\n'+strimg+b'\r\n')
    del(cam)


def dynamic_stream(request,stream_path="video"):
    try:
        return StreamingHttpResponse(getframe(),content_type='multipart/x-mixed-replace;boundary=frame')
    except :
        return "Technical Error"
