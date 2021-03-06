import numpy as np
import cv2



def init_yolo(configPath, weightsPath):

	net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
	
	return net

	
def recognize_image(input_file, output_file, labelsPath, net):

	confidence_value = 0.5
	threshold = 0.3

	image = cv2.imread(input_file)
	(H, W) = image.shape[:2]

	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	ln = net.getLayerNames()
	ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
	layerOutputs = net.forward(ln)
	LABELS = open(labelsPath).read().strip().split("\n")

	COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
		dtype="uint8")

	boxes = []
	confidences = []
	classIDs = []

	for output in layerOutputs:

		for detection in output:

			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			if confidence > confidence_value:

				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)


	idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_value,
		threshold)

	if len(idxs) > 0:

		for i in idxs.flatten():

			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
			cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, color, 2)

	cv2.imwrite(output_file, image)

# usage
# net = init_yolo('yolov3.cfg', 'yolov3.weights')
# recognize_image('inp.png', 'out.png', 'coco.names', net)