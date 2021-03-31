import os
import requests
from bs4 import BeautifulSoup
from random import randint

images = []
list_imgs = []
tw_pages= 0
print("Digite duas imagens para comprar:")
name_img1 = str(input("Nome imagem 1:"))
name_img2 = str(input("Nome imagem 2:"))
#diretory = str(input("Em qual pasta você deseja quardar?"))
num_images = int(input("Quantas imagens fazer downloads?"))
base_test = int(input("Quantos % para a base de teste?" ))
#base_train = int(input("Quantos % para a base de treino?" ))
print(f'Realizando download das imagens: {name_img1} and {name_img2}')
pages_boolean = True

#CRIANDO DIRETÓRIO CENTRAL PARA ARMAZENAR AS IMAGENS
#linux: directory = f'/home/augusto/Desktop/Aprendizagem_{name_img1}_and_{name_img2}'
#windows:
directory = f'C:/Users/Augusto M/Desktop/PY/Aprendizagem_{name_img1}_and_{name_img2}'
os.mkdir(directory)

#DIRETÓRIO DAS IMAGENS DE TREINAMENTO
directory_train = f'{directory}/train'
os.mkdir(directory_train)

directory_train_img1 = f'{directory_train}/imagens_{name_img1}'
directory_train_img2 = f'{directory_train}/imagens_{name_img2}'
os.mkdir(directory_train_img1)
os.mkdir(directory_train_img2)

#DIRETÓRIO DAS IMAGENS DE TESTE
directory_test= f'{directory}/test'
os.mkdir(directory_test)

directory_test_img1 = f'{directory_test}/imagens_{name_img1}'
directory_test_img2 = f'{directory_test}/imagens_{name_img2}'
os.mkdir(directory_test_img1)
os.mkdir(directory_test_img2)


img1_list =[]
img2_list =[]
#url_ready = f'https://www.google.com/search?hl=pt-BR&biw=1294&bih=667&gbv=1&tbm=isch&oq=&aqs=&q={img1}'
#url1 = f'https://www.google.com/search?q={img1}&tbm=isch&ved=2ahUKEwi2m7fLpcvsAhVwL7kGHeJsC88Q2-cCegQIABAA&oq=cavalo&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIHCAAQsQMQQzIFCAAQsQMyBQgAELEDMgQIABBDMgcIABCxAxBDMgUIABCxAzICCAAyBQgAELEDUIGMA1jbnwNgqqADaAJwAHgAgAHIAYgBoQqSAQUwLjYuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=IBqTX7aLLPDe5OUP4tmt-Aw&bih=667&biw=1294&hl=pt-BR'
#url2 = f'https://www.google.com/search?q={img2}&tbm=isch&ved=2ahUKEwi2m7fLpcvsAhVwL7kGHeJsC88Q2-cCegQIABAA&oq=cavalo&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIHCAAQsQMQQzIFCAAQsQMyBQgAELEDMgQIABBDMgcIABCxAxBDMgUIABCxAzICCAAyBQgAELEDUIGMA1jbnwNgqqADaAJwAHgAgAHIAYgBoQqSAQUwLjYuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=IBqTX7aLLPDe5OUP4tmt-Aw&bih=667&biw=1294&hl=pt-BR'

list_random_test_img1 = []
list_random_train_img1 = []
qnt_random_test = int(num_images*(base_test/100))
 
reset_list_random_train =  list_random_test_img1.copy()

#teste img1
while(len(list_random_test_img1) < qnt_random_test):
        number = randint(0,num_images-1)
        if number not in list_random_test_img1:
            list_random_test_img1.append(number)
 #train img1  
for i in range(num_images):
    if i not in list_random_test_img1:
        list_random_train_img1.append(i)
        
             
'''imagem 2'''
list_random_test_img2 = []
list_random_train_img2 = []
#teste img 2
while(len(list_random_test_img2) < qnt_random_test):
        number = randint(0,num_images-1)
        if number not in list_random_test_img2:
            list_random_test_img2.append(number)
   
 #train img1  
for i in range(num_images):
    if i not in list_random_test_img2:
        list_random_train_img2.append(i)    

            
while(pages_boolean):
    links1 =[]
    links1_list = []
    links2_list = []
    links2 = []
    url1 = f'https://www.google.com/search?q={name_img1}&hl=pt-BR&biw=1294&bih=667&gbv=1&tbm=isch&ei=EWaTX_7nAu-e5OUP9buPqAQ&start={tw_pages}&sa=N'
    url2 = f'https://www.google.com/search?q={name_img2}&hl=pt-BR&biw=1294&bih=667&gbv=1&tbm=isch&ei=EWaTX_7nAu-e5OUP9buPqAQ&start={tw_pages}&sa=N'
    
    req1 = requests.get(url1)
    req2 = requests.get(url2)
    
    soup1 = BeautifulSoup(req1.text, 'html.parser') #pega todo o html
    soup2 = BeautifulSoup(req2.text, 'html.parser')

    save = True
    while(save):
#imagem 1
        for img in soup1.find_all('img'):
            links1_list.append(img.get('src'))
        
        for links1 in links1_list:
            if links1[-3:]=='gif':
                continue
            img1_list.append(requests.get(links1))
                
        for i, imgl1 in enumerate(img1_list):
                if i in list_random_test_img2:
                    as_save_imgl1 = f'{directory_test_img1}/{name_img1}_imagem{i}.jpeg'
                    with open(as_save_imgl1, 'wb') as f:
                        f.write(imgl1.content)
                else:
                    as_save_imgl1 = f'{directory_train_img1}/{name_img1}_imagem{i}.jpeg'
                    with open(as_save_imgl1, 'wb') as f:
                        f.write(imgl1.content)
#imagem 2                     
        for img in soup2.find_all('img'):
            links2_list.append(img.get('src'))
            
        for links2 in links2_list:
            if links2[-3:]=='gif':
                continue
            img2_list.append(requests.get(links2))
            
        for j, imgl2 in enumerate(img2_list):
            if j in list_random_test_img2:
                as_save_imgl2 = f'{directory_test_img2}/{name_img2}_imagem{j}.jpeg'
                with open(as_save_imgl2, 'wb') as f:
                    f.write(imgl2.content)      
            else:
                as_save_imgl2 = f'{directory_train_img2}/{name_img2}_imagem{j}.jpeg'
                with open(as_save_imgl2, 'wb') as f:
                    f.write(imgl2.content)
        
        save = False
        
    tw_pages+=20
    if tw_pages == num_images:
        break
print("Foram realizados", num_images, "downloads")

    


'''MACHINE LEARNING '''

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#image = tf.keras.preprocessing.image.load_img(rf'{directory_test_img1}/{name_img1}_imagem1.jpeg', target_size=(224,224))
image = tf.keras.preprocessing.image.load_img(rf'{directory_test_img1}/{name_img1}_imagem3.jpeg', target_size=(224,224))
plt.imshow(image);


train_datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.resnet50.preprocess_input,
                                   rotation_range = 50,
                                   width_shift_range = 0.2,
                                   height_shift_range = 0.2,
                                   zoom_range = 0.1,
                                   horizontal_flip = True,
                                   vertical_flip = True)
#os.listdir(f'{directory_test_img1}')
train_generator = train_datagen.flow_from_directory(f'{directory}/train',
                                                    target_size = (224, 224),
                                                    batch_size=16,
                                                    class_mode = 'categorical',
                                                    shuffle = True)

train_generator.n

train_generator.batch_size


test_datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.resnet50.preprocess_input)

test_generator = test_datagen.flow_from_directory(f'{directory}/test',
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
preds = tf.keras.layers.Dense(2, activation='softmax')(x)

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
                              steps_per_epoch=8, #step_size_train
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
image = tf.keras.preprocessing.image.load_img(r'//home/augusto/Desktop/tigre.jpg', target_size=(224,224))
plt.imshow(image);

type(image)

#formato necessário para o tensorflow, um array com 3 dimensões
image = tf.keras.preprocessing.image.img_to_array(image)
np.shape(image)

type(image)

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
np.argmax(predictions[0])

train_generator.class_indices
list(train_generator.class_indices)

#busca aquele que tem o maior valor
prediction = list(train_generator.class_indices)[np.argmax(predictions[0])]
prediction