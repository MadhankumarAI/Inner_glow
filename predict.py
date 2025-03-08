import numpy as np
import tensorflow as tf
import cv2
import sys

# Load the trained model
model = tf.keras.models.load_model('skin_disease_model.h5')

# Class labels
CLASS_NAMES = ['MEL', 'NV', 'BCC', 'AKIEC', 'BKL', 'DF', 'VASC']

def predict_image(image_path):
    # Load and preprocess the image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Make prediction
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction)
    
    print(f"🔹 Predicted Class: {CLASS_NAMES[predicted_class]}")
    print(f"🔹 Confidence Scores: {prediction[0]}")

# Run prediction on given image
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide an image path!")
    else:
        predict_image(sys.argv[1])
