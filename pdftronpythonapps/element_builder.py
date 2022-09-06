import sys, os
from PDFNetPython3 import *


LicenseKey = "demo:1660901533629:7a0d2a20030000000043672b6af0d5efbbce5dec7852b806be2a763b74" 

cwd = os.getcwd()
print("===>>",cwd)

input_path = cwd.split('element_builder')[0]+ "/test_files/"
output_path = cwd.split('element_builder')[0]+ "/test_files/output/"

print(input_path)
print(output_path)

PDFNet.Initialize(LicenseKey)       # Initializing the PDFNet Object


# Element Builder CreateGroupBegin/ CreateGroupEnd:
# ===========================================================================

doc = PDFDoc()

# ElementBuilder is used to build new Element objects
eb = ElementBuilder()

# ElementWriter is used to write Elements to the page
writer = ElementWriter()

# Start a new page ------------------------------------
# Construct and draw a path object using different styles
page = doc.PageCreate(Rect(0, 0, 612, 794))

writer.Begin(page)  # begin writing to this page
eb.Reset()          # Reset the GState to default

# Create an Image that can be reused in the document or on the same page.
img = Image.Create(doc.GetSDFDoc(), input_path + "peppers.jpg")

eb.PathBegin()      # start constructing the path

# Use the path as a clipping path
writer.WriteElement(eb.CreateGroupBegin())    # Save the graphics state

# Start constructing the new path (the old path was lost when we created 
# a new Element using CreateGroupBegin()).
eb.PathBegin()
eb.MoveTo(306, 396)
eb.CurveTo(681, 771, 399.75, 864.75, 306, 771)
eb.CurveTo(212.25, 864.75, -69, 771, 306, 396)
eb.ClosePath()
element = eb.PathEnd()    # path is now constructed
element.SetPathClip(True)    # this path is a clipping path
element.SetPathStroke(True)        # this path should be filled and stroked
gstate = element.GetGState()
gstate.SetTransform(0.5, 0, 0, 0.5, -20, 0)

writer.WriteElement(element)

writer.WriteElement(eb.CreateImage(img, 100, 300, 400, 600))
    
writer.WriteElement(eb.CreateGroupEnd())    # Restore the graphics state

writer.End()  # save changes to the current page
doc.PagePushBack(page)

doc.Save((output_path + "element_builder.pdf"), SDFDoc.e_remove_unused)

doc.Close()
PDFNet.Terminate()
print("Done. Result saved in element_builder.pdf...")

# ===========================================================================

# Element Builder CreateForm : 1st Example
# ===========================================================================
input_path = cwd.split('element_builder')[0]+ "/test_files/newsletter.pdf"
output_path = cwd.split('element_builder')[0]+ "/test_files/output/newsletter_booklet.pdf"

print("-------------------------------------------------")
print("Opening the input pdf...")

args = []


filein = args[1] if len(args)>1 else input_path
fileout = args[2] if len(args)>2 else output_path

in_doc = PDFDoc(filein)
in_doc.InitSecurityHandler()

# Create a list of pages to import from one PDF document to another
import_pages = VectorPage()
itr = in_doc.GetPageIterator()
while itr.HasNext():
    import_pages.append(itr.Current())
    itr.Next()

new_doc = PDFDoc()
imported_pages = new_doc.ImportPages(import_pages)

# Paper dimension for A3 format in points. Because one inch has 
# 72 points, 11.69 inch 72 = 841.69 points
media_box = Rect(0, 0, 1190.88, 841.69)
mid_point = media_box.Width()/2

builder = ElementBuilder()
writer = ElementWriter()

i = 0    
while i < len(imported_pages):
    # Create a blank new A3 page and place on it two pages from the input document.
    new_page = new_doc.PageCreate(media_box)
    writer.Begin(new_page)
    
    # Place the first page
    src_page = imported_pages[i]
    
    element = builder.CreateForm(imported_pages[i])
    sc_x = mid_point / src_page.GetPageWidth()
    sc_y = media_box.Height() / src_page.GetPageHeight()
    scale = sc_x if sc_x < sc_y else sc_y # min(sc_x, sc_y)
    element.GetGState().SetTransform(scale, 0, 0, scale, 0, 0)
    writer.WritePlacedElement(element)
    
    # Place the second page
    i = i + 1
    if i < len(imported_pages):
        src_page = imported_pages[i]
        element = builder.CreateForm(src_page)
        sc_x = mid_point / src_page.GetPageWidth()
        sc_y = media_box.Height() / src_page.GetPageHeight()
        scale = sc_x if sc_x < sc_y else sc_y # min(sc_x, sc_y)
        element.GetGState().SetTransform(scale, 0, 0, scale, mid_point, 0)
        writer.WritePlacedElement(element)
        
    writer.End()
    new_doc.PagePushBack(new_page)
    i = i + 1
    
new_doc.Save(fileout, SDFDoc.e_linearized)
PDFNet.Terminate()
print("Done. Result saved in newsletter_booklet.pdf...")

# ===========================================================================
# Element Builder CreateForm : 2nd Example
# ===========================================================================

input_path = cwd.split('element_builder')[0]+ "/test_files/"
output_path = cwd.split('element_builder')[0]+ "/test_files/output/"


# A utility function used to add new Content Groups (Layers) to the document.
def CreateLayer(doc, layer_name):
    grp = Group.Create(doc, layer_name)
    cfg = doc.GetOCGConfig()
    if not cfg.IsValid():
        cfg = Config.Create(doc, True)
        cfg.SetName("Default")
        
    # Add the new OCG to the list of layers that should appear in PDF viewer GUI.
    layer_order_array = cfg.GetOrder()
    if layer_order_array is None:
        layer_order_array = doc.CreateIndirectArray()
        cfg.SetOrder(layer_order_array)
    layer_order_array.PushBack(grp.GetSDFObj())
    return grp

def CreateGroup1(doc, layer):
    writer = ElementWriter()
    writer.Begin(doc.GetSDFDoc())
    
    # Create an Image that can be reused in the document or on the same page.
    img = Image.Create(doc.GetSDFDoc(), input_path + "peppers.jpg")
    builder = ElementBuilder()
    element = builder.CreateImage(img, Matrix2D(img.GetImageWidth()/2, -145, 20, img.GetImageHeight()/2, 200, 150))
    writer.WritePlacedElement(element)
    
    gstate = element.GetGState()    # use the same image (just change its matrix)
    gstate.SetTransform(200, 0, 0, 300, 50, 450)
    writer.WritePlacedElement(element)
    
    # use the same image again (just change its matrix).
    writer.WritePlacedElement(builder.CreateImage(img, 300, 600, 200, -150))
    
    grp_obj = writer.End()
    
    # Indicate that this form (content group) belongs to the given layer (OCG).
    grp_obj.PutName("Subtype","Form")
    grp_obj.Put("OC", layer)
    grp_obj.PutRect("BBox", 0, 0, 1000, 1000)   # Set the clip box for the content.
    
    return grp_obj

# Creates some content (a path in the shape of a heart) and associate it with the vector layer
def CreateGroup2(doc, layer):
    writer = ElementWriter()
    writer.Begin(doc.GetSDFDoc())
    
    # Create a path object in the shape of a heart
    builder = ElementBuilder()
    builder.PathBegin()     # start constructing the path
    builder.MoveTo(306, 396)
    builder.CurveTo(681, 771, 399.75, 864.75, 306, 771)
    builder.CurveTo(212.25, 864.75, -69, 771, 306, 396)
    builder.ClosePath()
    element = builder.PathEnd() # the path geometry is now specified.

    # Set the path FILL color space and color.
    element.SetPathFill(True)
    gstate = element.GetGState()
    gstate.SetFillColorSpace(ColorSpace.CreateDeviceCMYK())
    gstate.SetFillColor(ColorPt(1, 0, 0, 0))    # cyan
    
    # Set the path STROKE color space and color
    element.SetPathStroke(True)
    gstate.SetStrokeColorSpace(ColorSpace.CreateDeviceRGB())
    gstate.SetStrokeColor(ColorPt(1, 0, 0))     # red
    gstate.SetLineWidth(20)
    
    gstate.SetTransform(0.5, 0, 0, 0.5, 280, 300)
    
    writer.WriteElement(element)
    
    grp_obj = writer.End()
    
    # Indicate that this form (content group) belongs to the given layer (OCG).
    grp_obj.PutName("Subtype","Form")
    grp_obj.Put("OC", layer)
    grp_obj.PutRect("BBox", 0, 0, 1000, 1000)       # Set the clip box for the content.
    
    return grp_obj

# Creates some text and associate it with the text layer
def CreateGroup3(doc, layer):
    writer = ElementWriter()
    writer.Begin(doc.GetSDFDoc())
    
    # Create a path object in the shape of a heart.
    builder = ElementBuilder()
    
    # Begin writing a block of text
    element = builder.CreateTextBegin(Font.Create(doc.GetSDFDoc(), Font.e_times_roman), 120)
    writer.WriteElement(element)
    
    element = builder.CreateTextRun("A text layer!")
    
    # Rotate text 45 degrees, than translate 180 pts horizontally and 100 pts vertically.
    transform = Matrix2D.RotationMatrix(-45 * (3.1415/ 180.0))
    transform.Concat(1, 0, 0, 1, 180, 100)
    element.SetTextMatrix(transform)
    
    writer.WriteElement(element)
    writer.WriteElement(builder.CreateTextEnd())
    
    grp_obj = writer.End()
    
    # Indicate that this form (content group) belongs to the given layer (OCG).
    grp_obj.PutName("Subtype","Form")
    grp_obj.Put("OC", layer)
    grp_obj.PutRect("BBox", 0, 0, 1000, 1000)   # Set the clip box for the content.
    
    return grp_obj


# Create three layers...
doc = PDFDoc()
image_layer = CreateLayer(doc, "Image Layer")
text_layer = CreateLayer(doc, "Text Layer")
vector_layer = CreateLayer(doc, "Vector Layer")

# Start a new page ------------------------------------
page = doc.PageCreate()

builder = ElementBuilder()    # ElementBuilder is used to build new Element objects
writer = ElementWriter()      # ElementWriter is used to write Elements to the page
writer.Begin(page)            # Begin writting to the page

# Add new content to the page and associate it with one of the layers.
element = builder.CreateForm(CreateGroup1(doc, image_layer.GetSDFObj()))
writer.WriteElement(element)

element = builder.CreateForm(CreateGroup2(doc, vector_layer.GetSDFObj()))
writer.WriteElement(element)

# Add the text layer to the page...
if False: 
    # set to true to enable 'ocmd' example.
    # A bit more advanced example of how to create an OCMD text layer that 
    # is visible only if text, image and path layers are all 'ON'.
    # An example of how to set 'Visibility Policy' in OCMD.
    ocgs = doc.CreateIndirectArray()
    ocgs.PushBack(image_layer.GetSDFObj())
    ocgs.PushBack(vector_layer.GetSDFObj())
    ocgs.PushBack(text_layer.GetSDFObj())
    text_ocmd = OCMD.Create(doc, ocgs, OCMD.e_AllOn)
    element = builder.CreateForm(CreateGroup3(doc, text_ocmd.GetSDFObj()))
else:
    element = builder.CreateForm(CreateGroup3(doc, text_layer.GetSDFObj()))
writer.WriteElement(element)

# Add some content to the page that does not belong to any layer...
# In this case this is a rectangle representing the page border.
element = builder.CreateRect(0, 0, page.GetPageWidth(), page.GetPageHeight())
element.SetPathFill(False)
element.SetPathStroke(True)
element.GetGState().SetLineWidth(40)
writer.WriteElement(element)

writer.End()    # save changes to the current page
doc.PagePushBack(page)
# Set the default viewing preference to display 'Layer' tab
prefs = doc.GetViewPrefs()
prefs.SetPageMode(PDFDocViewPrefs.e_UseOC)

doc.Save(output_path + "pdf_layers.pdf", SDFDoc.e_linearized)
doc.Close()
print("Element Builder CreateForm : 2nd Example Done.")


# ===========================================================================
# CreateTextBegin/CreateTextEnd:
# ===========================================================================
doc = PDFDoc()
    
f = ElementBuilder()            # Used to build new Element objects
writer = ElementWriter()        # Used to write Elements to the page

page = doc.PageCreate()         # Start a new page
writer.Begin(page)  

# Write 'Hello World' text string under the image
writer.WriteElement(f.CreateTextBegin(Font.Create(doc.GetSDFDoc(), Font.e_times_roman), 32))
element = f.CreateTextRun("Hello World")
element.SetTextMatrix(1, 0, 0, 1, 10, 700)
writer.WriteElement(element)
writer.WriteElement(f.CreateTextEnd())

writer.End()                    # Finish writing to the page
doc.PagePushBack(page)

doc.Save((output_path + "addimage.pdf"), SDFDoc.e_linearized);
doc.Close()
PDFNet.Terminate()

print("Done. Result saved in addimage.pdf...")
# ===========================================================================