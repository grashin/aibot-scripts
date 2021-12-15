import yolov5

# load model
def init_yolo():
    model = yolov5.load("yolov5s6.pt")
    return model

    # set image
def recognize_image(img, output_dir, model):

    results = model(img)

    # inference with larger input size
    results = model(img, size=1280)

    # inference with test time augmentation
    results = model(img, augment=True)

    # parse results
    predictions = results.pred[0]
    boxes = predictions[:, :4] # x1, x2, y1, y2
    scores = predictions[:, 4]
    categories = predictions[:, 5]

    # results.show()

    results.save(output_dir)

model = init_yolo()
recognize_image('img.png','path/to/dir/', model)
