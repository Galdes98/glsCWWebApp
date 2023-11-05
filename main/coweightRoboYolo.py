from roboflow import Roboflow
from PIL import Image, ImageDraw
import numpy as np

def pesaje(imagen):
    rf = Roboflow(api_key="3E7t3sq8f4V5liAfrAtD")
    project = rf.workspace().project("coweight")
    model = project.version(5).model    
    values = {
        'weight': 0,
        'distance': 0,
        'width': 0,
        'height': 0,   
        'message': 'No se pudo calcular el peso'     
    }

    # infer on a local image
    modelJson = model.predict("./media/"+imagen).json()

    # save an image annotated with your predictions
    model.predict("./media/"+imagen, confidence=60).save("./media/prediction.jpg")

    im = Image.open("./media/prediction.jpg")
    # Get the metadata of the image
    metadata = im.info

    # Return 0 if the confidence is less than 80%
    for prediction in modelJson['predictions']:
        # Check the confidence of each prediction
        print ('confianza '+ str(prediction['confidence']) )
        if prediction['confidence'] < 0.60:
            return values

    # Loop to draw the points
    for i in modelJson['predictions']:
        polygon_points = []
        #print (i['x'], i['y'])    
        x_old, y_old = None, None
        for n in i['points']:
            #print (n['x'], n['y'])
            x, y = n['x'], n['y']
            polygon_points.append((x, y))  

    # Create a mask of the polygon
    mask = Image.new('L', im.size, 0)
    mask = np.array(mask)

    # Calculate the width and height inside the polygon in pixels
    width_pixels = np.sum(mask, axis=1).max() - np.sum(mask, axis=1).min()
    height_pixels = np.sum(mask, axis=0).max() - np.sum(mask, axis=0).min()

    # Calculate the resolution in pixels per centimeter
    sensor_size = 1/2.0 * 2.54 # Sensor size in inches to centimiters
    distance = 170 # Distance from the camera to the object in centimeters
    image_width_pixels, image_height_pixels = im.size
    resolution = (sensor_size * distance) / max(image_width_pixels, image_height_pixels)
    #resolution = 0.25344541484716157205240174672489

    # Convert the width and height from pixels to centimeters
    width_cm = width_pixels * resolution
    height_cm = height_pixels * resolution

    # Calculate the distance between each pair of adjacent points in the polygon in centimeters
    distances_cm = []
    for i in range(len(polygon_points)):
        x1, y1 = polygon_points[i]
        x2, y2 = polygon_points[(i + 1) % len(polygon_points)]
        distance_pixels = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        distance_cm = distance_pixels * resolution
        distances_cm.append(distance_cm)

    tot_dist_cm = 0

    # Display the distances between each pair of adjacent points in the polygon in centimeters
    for i, distance_cm in enumerate(distances_cm):
        tot_dist_cm = tot_dist_cm + distance_cm

    # calculate the weight
    weight = round(-413.36 + (2.69 * (tot_dist_cm * 0.85)) + (1.50 * tot_dist_cm), 2)
    
    values = {
        'weight': weight,
        'distance': tot_dist_cm,
        'width': width_cm,
        'height': height_cm,   
        'message': 'Imagen guardada correctamente, con peso: '+str(weight)+' kg'     
    }
    print(values)

    return values
