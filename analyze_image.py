from initfile import * 

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))

# create face client from url: get face attributes
def face_url(url, is_url=True):
	face_attributes = ['age','gender', 'headPose', 'smile', 'facialHair', 'glasses', 'emotion']
	if is_url == True:
		image_name = os.path.basename(url)
		detected_faces = face_client.face.detect_with_url(url=url, return_face_landmarks=True, return_face_attributes=face_attributes)
	else: 
		detected_faces = face_client.face.detect_with_stream(url, return_face_landmarks=True, return_face_attributes=face_attributes)
	if not detected_faces:
		raise Exception('No face detected from image {}'.format(image_name))
	return detected_faces
	
# visualize face detection
def plot_faces(image_url, detected_faces, is_url=True):
	if is_url == True:
		response = requests.get(image_url) # Download the image from the url
		img = Image.open(BytesIO(response.content))
	else:
		img = Image.open(image_url)
	
	# For each face returned use the face rectangle and draw a red box.
	#print('Drawing rectangle around face... see popup for results.')
	draw = ImageDraw.Draw(img)
	for face in detected_faces:
		draw.rectangle(getRectangle(face), outline='red')
		draw.text(getRectangle(face)[0], 'age: ' + str(face.face_attributes.age))
	img.show()

def path2img(img_url, subfolder=''):
	IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
	image_array = glob.glob(os.path.join(IMAGES_FOLDER, subfolder, img_url))
	image = open(image_array[0], 'r+b')
	return image

############
### MAIN ###
############

# example from a url img
if True:
	#image_url = 'http://www.historyplace.com/kennedy/president-family-portrait-closeup.jpg'
	image_url = 'https://www.telegraph.co.uk/content/dam/film/InsideOut/pixarfaces.jpg'
	detected_faces = face_url(image_url) # detect face and attributes
	plot_faces(image_url, detected_faces)

if True:
	# example from file in computer
	img_url = 'r1.jpg'
	subfolder = 'resultant_img'
	image = path2img(img_url, subfolder)
	#img_url = 'president-family-portrait-closeup.jpg'
	detected_faces = face_url(image, is_url=False) # detect face and attributes
	plot_faces(image, detected_faces, is_url=False)