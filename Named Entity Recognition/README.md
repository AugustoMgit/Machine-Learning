Reconhecimento de entidades através do Spacy.

No arquivo datasets.rar estão compactados os datasets necessários para o processamento ao treino e teste.
Para esse estudo de caso, dois modelos são treinados para reconhecerem a entidade FOOD, posteriormente, a quantidade de acertos e a previsão
No modelo 1, está sendo treinado apenas as entidades foods, descartando as entidades que já vem com o spacy. Além disso, o treino e teste são dados gerados a partir de algumas frases fixas, mudando apenas o nome que configura aquela entidade.
No modelo 2, o treinamento está habilitado tanto para o reconhecimento de entidades foods, quanto as entidades já salvas no modelo. Para isso, foi usado as várias palavras do arquivo food e textos do arquivo articles.

