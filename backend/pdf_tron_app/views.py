from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FileUploadSerializer
from .models import FileUpload
from django.http import HttpResponse
from PDFNetPython3 import *
import os

# Create your views here.
class FileUploadView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)

        file_name = str(request.FILES['file']).replace(' ','_')
        
        
        if serializer.is_valid():
            serializer.save()
            cwd = os.getcwd()
            
            input_path = cwd + "/media/my_files/"
            output_path = cwd + "/media/"
            PDFNet.Initialize("demo:1660901533629:7a0d2a20030000000043672b6af0d5efbbce5dec7852b806be2a763b74")
            
            PDFNet.AddResourceSearchPath(cwd+"/Lib/Linux/")
            
            # doc = PDFDoc()
            # f = ElementBuilder()            # Used to build new Element objects
            # writer = ElementWriter() 
            
            # page = doc.PageCreate()
            # writer.Begin(page)
            
            # img = Image.Create(doc.GetSDFDoc(), input_path + file_name)
            # element = f.CreateImage(img, 50, 500, img.GetImageWidth()/2, img.GetImageHeight()/2)
            # writer.WritePlacedElement(element)
            # writer.End()
            
            # case 2:
            input_file = input_path + file_name
            Convert.ToWord(input_file, output_path+"test_success.docx")
            
            
            # doc.PagePushBack(page)
            # doc.Save((output_path+"my_test_file.pdf"), SDFDoc.e_linearized)
            # doc.Close()
            file_loc = output_path+"test_success.docx"
            return Response({"processed_file_path": file_loc})
        
    def get(self, request):
        data = FileUpload.objects.all()
        serializer = FileUploadSerializer(data, many=True)
        return Response(serializer.data)
    


# Create your views here.

def main(request):
    cwd = os.getcwd()
    print(cwd)
    input_path = cwd + "/static/"
    # You need to initialize the PDFNet library 
    # Before calling any PDF related methods
    PDFNet.Initialize("demo:1660901533629:7a0d2a20030000000043672b6af0d5efbbce5dec7852b806be2a763b74")

    # This example creates a new document
    # and a new page, then adds the page
    # in the page sequence of the document
    doc = PDFDoc()
    
    f = ElementBuilder()            # Used to build new Element objects
    writer = ElementWriter()        # Used to write Elements to the page
    
    page1 = doc.PageCreate()
    
    writer.Begin(page1)              # Begin writing to this page

    # ----------------------------------------------------------
    # Add JPEG image to the output file
    img = Image.Create(doc.GetSDFDoc(), input_path + "peppers.jpg")
    element = f.CreateImage(img, 50, 500, img.GetImageWidth()/2, img.GetImageHeight()/2)
    writer.WritePlacedElement(element)
    
    # ----------------------------------------------------------
    # Add a PNG image to the output file    
    img = Image.Create(doc.GetSDFDoc(), input_path + "butterfly.png")
    element = f.CreateImage(img, Matrix2D(100, 0, 0, 100, 300, 500))
    writer.WritePlacedElement(element)
    
    writer.End()
    doc.PagePushBack(page1)

    # We save the document in a linearized
    # format which is the most popular and 
    # effective way to speed up viewing PDFs
    doc.Save(("linearized_output.pdf"), SDFDoc.e_linearized)

    doc.Close()
    return HttpResponse("Hi Human!")
