# Visão Computacional para Contador de Pontos numa partida de Volei

Este projeto utiliza técnicas de visão computacional para verificar quantos pontos cada equipe realizou. Ele verifica cada imagem do video, observando se a bola caiu no chão, se sim, conta ponto para equipe.
Verifica também, quantas pessoas estão na quadra

## Etapas
- Bola caiu no chão
- No campo direito, conta ponto para equipe direita, no campo esquerdo, para equipe a esquerda.
- Verificar Pessoas na quadra


## Como é Feito
- Os pontos de referencia são os dois campos, um do lado esquerdo e o outro no direito. 
- Verifica em pixels brancos, se aumentou a quantidade em um dos campos, se sim, conta ponta para a equipe.

## Necessário
- Arquivo de configuração: yolov3.cfg = https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg
- Arquivo de pesos: yolov3.weights = https://pjreddie.com/media/files/yolov3-tiny.weights
- Arquivo de nomes das classes: coco.names = https://github.com/pjreddie/darknet/blob/master/data/coco.names

## Funções 

### Função `processImage`

A função `processImage` é responsável por tratar o frame, transformando em cores brancas e pretas, e retornando uma imagem dilatada no final


### Função `verifiyFields`

A função `verifyFields` verifica se aumentou a quantidade de pixels brancos em cada campo, se sim, conta no scoreBoard e retorna o placar no final


### Função `showScoreboard`

A função `showScoreboard` tem o papel de mostrar o resultado final do placar.

### Função `loadPretainedModel`

A função `loadPretainedModel` Carrega o modelo pra utilizar pra identificar os objetos

### Função `preProcessFrame`

A função `preProcessFrame` pre processa a imagem

### Função `detectObject`

A função `detectObject` Identifica o objeto

### Função `drawDetections`

A função `drawDetections` tem o papel de desenhar os retangulos por volta do objeto



