from Visual_Attention_Model import evaluate, plot_attention
from PIL import Image

print("Necessary Packages loaded..")
def predict_caption(image_path):

    result, attention_plot = evaluate(image_path)
    print('Prediction Caption:', ' '.join(result[:-1]))
    # plot_attention(image_path, result, attention_plot)

    # Opening the image
    Image.open(image_path)


predict_caption('sample.jpg')

