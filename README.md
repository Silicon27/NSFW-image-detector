# NSFW-image-detector
An NSFW image detector built with the nsfw_detector library in Python. Python side hosted as Flask application, and is accessed via a node entry point (Node sends POST request to python side) then value is returned. 

Flask endpoint processes the image encoded in base64 then returns the predicted result.

Mkae sure to download the model as well.
