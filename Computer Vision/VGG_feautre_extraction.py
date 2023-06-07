from keras import Model
from keras.applications.vgg16 import VGG16
from keras.layers import Flatten, Dense
import cv2


# Get VGG-16 Model
def getVGG16Model(lastFourTrainable=False):

    vgg_model = VGG16(weights='imagenet', input_shape=(224, 224,3), include_top=True)

    # Make all layers untrainable
    for layer in vgg_model.layers[:]:
        layer.trainable = False

    # Add fully connected layer which have 100 neuron to VGG-16 model
    output = vgg_model.get_layer('fc2').output
    output = Flatten(name='new_flatten')(output)
    output = Dense(units=500, activation='relu', name='new_fc')(output)
    output = Dense(units=500, activation='softmax')(output)
    vgg_model = Model(vgg_model.input, output)

    # Compile VGG-16 model
    vgg_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    vgg_model.summary()
    return vgg_model


# Get feature extractor model from last layer of vgg_model_a
vgg_model_a = getVGG16Model()

# vgg_model_a.load_weights('/content/drive/MyDrive/Colab Notebooks/cinic-10/model_vgg_nontrainable.h5')
feature_model_vgg_a = Model(inputs=vgg_model_a.input, outputs=vgg_model_a.get_layer('new_fc').output)

feature_model_vgg_a.save('VGG_model.h5')



