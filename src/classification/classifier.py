import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import keras
from keras import layers, callbacks, optimizers
import numpy as np


def train_model(symbol_paths):
    num_classes = len(symbol_paths)
    input_shape = (32, 32, 1)
    index_to_label = {}
    all_images = []
    for i, path in enumerate(symbol_paths):
        with(open(path, "rb")) as f:
            loaded_images = pickle.load(f)
            for image in loaded_images:
                all_images.append((i, image[1]))
            index_to_label[i] = image[0]
    data = pd.DataFrame(all_images, columns=["label", "image"])
    X_train, X_test, y_train, y_test = train_test_split(data["image"], data["label"], test_size=0.2, random_state=42)
    model = keras.Sequential([
        keras.Input(shape=input_shape),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation="softmax")
    ])
    batch_size = 256
    epochs = 10
    model.compile(
        loss="sparse_categorical_crossentropy",
        optimizer=optimizers.RMSprop(),
        metrics=["accuracy"]
    )
    callbacks = [
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=2),
    ]
    model.fit(np.stack(X_train, axis=0), y_train, batch_size=batch_size, epochs=epochs, validation_split=0.15,
              callbacks=callbacks)
    score = model.evaluate(np.stack(X_test, axis=0), y_test, verbose=0)
    print("Test accuracy:", score[1])
    return model, index_to_label
