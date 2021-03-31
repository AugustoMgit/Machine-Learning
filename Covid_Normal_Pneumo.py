'''MACHINE LEARNING '''

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

image = tf.keras.preprocessing.image.load_img(r'chest_xray/test/PNEUMONIA/person1_virus_6.jpeg', target_size=(224,224))

plt.imshow(image);

train_datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.resnet50.preprocess_input,
                                   rotation_range = 50,
                                   width_shift_range = 0.2,
                                   height_shift_range = 0.2,
                                   zoom_range = 0.1,
                                   horizontal_flip = True,
                                   vertical_flip = True)
#os.listdir(f'{directory_test_img1}')
train_generator = train_datagen.flow_from_directory(r'chest_xray/train',
                                                    target_size = (224, 224),
                                                    batch_size=16,
                                                    class_mode = 'categorical',
                                                    shuffle = True)

train_generator.n

train_generator.batch_size

test_datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.resnet50.preprocess_input)

test_generator = test_datagen.flow_from_directory(r'chest_xray/test',
                                                  target_size=(224,244),
                                                  batch_size=1,
                                                  class_mode = 'categorical',
                                                  shuffle = False)

step_size_train = train_generator.n // train_generator.batch_size
step_size_train

step_size_test = test_generator.n // test_generator.batch_size
step_size_test

base_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False)

base_model.summary()

x = base_model.output

x = tf.keras.layers.GlobalAveragePooling2D()(x)

x = tf.keras.layers.Dense(1024, activation='relu')(x)
x = tf.keras.layers.Dense(1024, activation='relu')(x)
x = tf.keras.layers.Dense(512, activation='relu')(x)
preds = tf.keras.layers.Dense(3, activation='softmax')(x)

model = tf.keras.Model(inputs = base_model.input, outputs = preds)

model.summary()


for i, layer in enumerate(model.layers):
  print(i, layer.name)

for layer in model.layers[:175]:
  layer.trainable = False

for layer in model.layers[175:]:
  layer.trainable = True

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit_generator(generator=train_generator,
                              epochs=8,
                              steps_per_epoch=4, #step_size_train
                              validation_data = test_generator,
                              validation_steps=step_size_test)


## Gráficos
np.mean(history.history['val_accuracy'])

np.std(history.history['val_accuracy'])

plt.plot(history.history['loss'], label='Training loss')
plt.plot(history.history['val_loss'], label='Validation loss')
plt.title('Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend();

plt.plot(history.history['accuracy'], label='Training accuracy')
plt.plot(history.history['val_accuracy'], label='Validation accuracy')
plt.title('Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend();

"""## Previsões"""

filenames = test_generator.filenames
filenames

len(filenames)

#predizerá as imagens com dois índices
predictions = model.predict_generator(test_generator, steps = len(filenames))

predictions

len(predictions)

predictions2 = []
for i in range(len(predictions)):
  #print(predictions[i])
  predictions2.append(np.argmax(predictions[i]))

predictions2

test_generator.classes

test_generator.class_indices

from sklearn.metrics import accuracy_score, confusion_matrix
accuracy_score(predictions2, test_generator.classes)

cm = confusion_matrix(predictions2, test_generator.classes)
cm

sns.heatmap(cm, annot=True);


"""## Teste com imagem"""

'''SELECIONAR IMAGEM A SER PREDICTA'''
image = tf.keras.preprocessing.image.load_img(r'chest_xray/train/COVID/01E392EE-69F9-4E33-BFCE-E5C968654078.jpeg', target_size=(224,224))
plt.imshow(image);

type(image)

#formato necessário para o tensorflow, um array com 3 dimensões
image = tf.keras.preprocessing.image.img_to_array(image)
np.shape(image)

#type(image)

np.max(image), np.min(image)

#expande a dimensão da imagem
#o formato muda (1, 224,224,3) -> o 1 indica o batch size, que é necessário para o formato do tensorflow
#esse batch size indica que faremos a classificação de 1 imagem apenas, e na sequência as dimensões
image = np.expand_dims(image, axis = 0)
np.shape(image)

#diminiu a escala de cores e aplica o preprocessamento do resnet50 que foi aplicado na rede neural 
image = tf.keras.applications.resnet50.preprocess_input(image)

np.max(image), np.min(image)

#faz a predição da imagem de acordo com o modelo
#OBS: se o batch size da imagem fosse maior que 1, então ela predizeria mais de um valor no modelo
predictions = model.predict(image)
print(predictions)

predictions[0]

#índice de maior valor
#np.argmax(predictions[0])
arg_max = int(np.argmax(predictions[0]))
arg_max

tipo = list(train_generator.class_indices)

resultado = tipo[arg_max]

print("Resultado do RaioX do paciente:",resultado)

train_generator.class_indices
list(train_generator.class_indices)

#busca aquele que tem o maior valor
prediction = list(train_generator.class_indices)[np.argmax(predictions[0])]
prediction