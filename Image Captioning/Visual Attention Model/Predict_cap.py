from Visual_Attention_Model import evaluate, plot_attention
from PIL import Image
import cv2

print("Necessary Packages loaded..")

def predict_caption(image):

    image_path = 'predicted_images/get_cap.jpg'
    # image_path = image
    cv2.imwrite(image_path, image)
    result, attention_plot = evaluate(image_path)
    return ' '.join(result[:-1])


    # plot_attention(image_path, result, attention_plot)

    # Opening the image
    # Image.open(image_path)


# predict_caption('sample.jpg')

