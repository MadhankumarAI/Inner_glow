import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report

# Load model
model = tf.keras.models.load_model('skin_disease_model.h5')

# Load validation data
X_val = np.load('X_val.npy')
y_val = np.load('y_val.npy')

# Predict on validation data
y_pred = model.predict(X_val)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_val, axis=1)

# Print classification report
print(classification_report(y_true_classes, y_pred_classes, target_names=['MEL', 'NV', 'BCC', 'AKIEC', 'BKL', 'DF', 'VASC']))
