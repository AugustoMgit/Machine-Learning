let cart = []; //carrinho de compra
let modalQt = 1;
let modalKey = 0;

//define constantes, o qual recebe elementos que queremos selecionar que retorna o elemento desejado, pelo el
/*cons c = (el) =>{
    return document.querySelector(el)
}*/
//diminui código
const c = (el)=>document.querySelector(el); //o item
const cs = (el)=>document.querySelectorAll(el); //array com itens

// Listagem das pizzas
pizzaJson.map((item, index)=>{
    let pizzaItem = c('.models .pizza-item').cloneNode(true); //clona a classe pizza-item para replicar a todas a pizzas que tem
    //document.querySelector('.pizza-item').append(pizzaItem); //coloca na tela a estrutura das pizzas
    //append() = insere no final do elemento selecionado, não dentro, é após


    //atribuindo as features de cada pizza através do json que tem o conteúdo das pizzas
    //setAttribute = seta um atributo na tag html. Nesse caso, para saber em qual pizza clicamos para abrir o modal com as informações corretas, pelo index da pizza
    //.src = acessa o src da tag img do html e coloca no src a origem da imagem pelo json
    //innerHTML = substitui
    pizzaItem.setAttribute('data-key', index);//coloca um atributo na tag do html data-key que se chama data-key
    pizzaItem.querySelector('.pizza-item--img img').src = item.img; //imagem
    pizzaItem.querySelector('.pizza-item--price').innerHTML = `R$ ${item.price.toFixed(2)}`;//formata o preço interpolando-o
    pizzaItem.querySelector('.pizza-item--name').innerHTML = item.name; //nome
    pizzaItem.querySelector('.pizza-item--desc').innerHTML = item.description; //descrição
    
    //seleciona a tag e 'a' da classe models pizza-item e adiciona um evento de click para abrir um modal de compra
    //addEventListener('click', funcao)
    pizzaItem.querySelector('a').addEventListener('click', (e)=>{
        //preventDefault(): evita a ação padrão de acontecer. Como selecionamos a tag a href, que direciona para um link, evitamos isso para abrir um modal
        e.preventDefault(); //para não atualizar a tela. Previne a ação padrão de direcionar a um link
                            //ex2:https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_event_preventdefault2
        console.log("Clicou na pizza");
        //a partir da tag a, procura o elemento mais próximo que tem a classe pizza-item
        //target = próprio elemento, tag a
        //closest = acha o elemento mais próximo, ou dentro, ou fora
        //key = pizza que clicamos pegado pelo adributo data-key, que é o índice de cada pizza no json
        let key = e.target.closest('.pizza-item').getAttribute('data-key'); //pega o id da pizza colocado anteriormente
        modalQt = 1; //variável do modal, para sempre abrir o modal ter a quantidade 1 de pizzas selecionadas
        modalKey = key; //qual é a pizza, id: usado ao finalizar o carrinho para saber qual pizza foi selecinada

        //pega e substitui as informações no modal da pizza clicada, selecionada, no MODAL
        c('.pizzaBig img').src = pizzaJson[key].img;
        c('.pizzaInfo h1').innerHTML = pizzaJson[key].name;
        c('.pizzaInfo--desc').innerHTML = pizzaJson[key].description;
        c('.pizzaInfo--actualPrice').innerHTML = `R$ ${pizzaJson[key].price.toFixed(2)*modalQt}`; 
        c('.pizzaInfo--size.selected').classList.remove('selected'); //remove a classe selected ao abrir outro modal. Sempre deixa por padrão a pizza grande
        cs('.pizzaInfo--size').forEach((size, sizeIndex)=>{ //tamanho da pizza
            if(sizeIndex == 2) {
                size.classList.add('selected');//deixa sempre selecionado a pizza grande, automaticamente
            }
           size.querySelector('span').innerHTML = pizzaJson[key].sizes[sizeIndex];//preenche a gramos da pizza
        });

        c('.pizzaInfo--qt').innerHTML = modalQt;

        c('.pizzaWindowArea').style.opacity = 0; //inicia com a opacidade 0 para gerar animação, aparecendo
        c('.pizzaWindowArea').style.display = 'flex'; //aparecer a área do modal que estava inativada 
        //transforma a opacidade de 0 a 1, gerando um efeito de animação. É preciso fzer o setTimeout para gerar um efeito de animação
        setTimeout(()=>{
            c('.pizzaWindowArea').style.opacity = 1;
        }, 200); //espera 200ms para colocar opacidade 1, gerando um efeito de animação
    });

    c('.pizza-area').append( pizzaItem );// um clone da classe pizza-item
});

//Eventos do MODAL de click, fechar, somar...
function closeModal() {
    //fechar o modal
    c('.pizzaWindowArea').style.opacity = 0;
    setTimeout(()=>{
        c('.pizzaWindowArea').style.display = 'none'; //tira o modal, demorando 0.5 segundos
    }, 500);
}
cs('.pizzaInfo--cancelButton, .pizzaInfo--cancelMobileButton').forEach((item)=>{
    item.addEventListener('click', closeModal);
});
//botão de diminuir a quantidade de pizzas selecionadas
c('.pizzaInfo--qtmenos').addEventListener('click', (e)=>{
    if(modalQt > 1) {
        modalQt--;
        c('.pizzaInfo--qt').innerHTML = modalQt;
    }
 
});
//botão de aumentar a quantidade de pizzas selecionadas
c('.pizzaInfo--qtmais').addEventListener('click', ()=>{
    modalQt++; //soma a variável já definida como 1, e depois que fechar o modal e entrar de novo, reseta a quantidade
    c('.pizzaInfo--qt').innerHTML = modalQt; //div da quantidade de pizzas
});
//preencimento de fundo do tamanho da pizza selecionada. PEQUENA, MÉDIA OU GRANDE
cs('.pizzaInfo--size').forEach((size, sizeIndex)=>{
    size.addEventListener('click', (e)=>{
        c('.pizzaInfo--size.selected').classList.remove('selected');
        size.classList.add('selected');//size=item, adiciona a class selected na pizzaInfo--size e não em qualquer outra coisa que foi clicado
    });
});
//evento de clicar em adicinoar o carrinho e finalizar a compra
c('.pizzaInfo--addButton').addEventListener('click', ()=>{
    //console.log("pizza ", modalKey);
    //modalKey: acessa o id da pizza pelo json, QUAL É A PIZZA

    //data-key: tag na html: 0, pequena, 1- media, 2 - grande
    //.selected pois quando clicamos em um tamanho, é adicionado a classe selected
    let size = parseInt(c('.pizzaInfo--size.selected').getAttribute('data-key')); //tamanho da pizza
    //parseInt = string em inteiro
    //console.log("Tamanho da pizza: ",size);
    //mesma pizza do mesmo tamanho precisam estar juntas, apenas somares
    let identifier = pizzaJson[modalKey].id+'@'+size; //junta o id da pizza com o tamanho:IDENTIFICA(id igual, soma quantidade de tamanho)
    //ex: Calabresa1@2
    
    //verifica se no carrinho já tem o mesmo identificador(identifier). Se tiver, então soma, não cria mais um item dentro do array
    //findIndex = procura por algum item, dentro do array, que for igual
    let key = cart.findIndex((item)=>item.identifier == identifier);
    //retorna -1 se não encontrou
    if(key > -1) {
        cart[key].qt += modalQt;//se achou, adiciona a quantidade da pizza igual ao carrinho 
    } else { //se não achou, então adiciona no carrinho
        cart.push({ //adiciona ao carrinho um array
            identifier, //identificador de cada pizza
            id:pizzaJson[modalKey].id, //id da pizza;
            size, //tamanho da pizza;
            qt:modalQt //quantidade de pizzas
        });
    }
    updateCart();
    closeModal();
});

c('.menu-openner').addEventListener('click', () => {
    if(cart.length > 0) {
        c('aside').style.left = '0';
    }
});
c('.menu-closer').addEventListener('click', ()=>{
    c('aside').style.left = '100vw';
});


//atualiza o carrinho 
function updateCart() {
    c('.menu-openner span').innerHTML = cart.length;

    //se tiver itens no carrinho, mostra o carrinho na tela 
    if(cart.length > 0) {
        c('aside').classList.add('show'); //adiciona a classe show, para exibir, aparecer. Foi configurado assim no html e css
        c('.cart').innerHTML = '';//quais serão as pizzas. SEMPRE ZERA TUDO E DEPOIS MOSTRA TUDO

        let subtotal = 0;
        let desconto = 0;
        let total = 0;

        for(let i in cart) { //faz um for no carrinho
            let pizzaItem = pizzaJson.find((item)=>item.id == cart[i].id);//procura no json arquivo que tem o id da pizza
            subtotal += pizzaItem.price * cart[i].qt; //calcula o valor total sem descontos

            let cartItem = c('.models .cart--item').cloneNode(true);//CLONA O LOCAL DAS PIZZAS NO CARRINHO

            let pizzaSizeName;
            switch(cart[i].size) {
                case 0:
                    pizzaSizeName = 'P';
                    break;
                case 1:
                    pizzaSizeName = 'M';
                    break;
                case 2:
                    pizzaSizeName = 'G';
                    break;
            }
            let pizzaName = `${pizzaItem.name} (${pizzaSizeName})`;

            cartItem.querySelector('img').src = pizzaItem.img;
            cartItem.querySelector('.cart--item-nome').innerHTML = pizzaName;
            cartItem.querySelector('.cart--item--qt').innerHTML = cart[i].qt;
            cartItem.querySelector('.cart--item-qtmenos').addEventListener('click', ()=>{
                if(cart[i].qt > 1) {
                    cart[i].qt--;
                } else {
                    cart.splice(i, 1);
                }
                updateCart();
            });
            cartItem.querySelector('.cart--item-qtmais').addEventListener('click', ()=>{
                cart[i].qt++;
                updateCart();
            });

            c('.cart').append(cartItem);
        }

        desconto = subtotal * 0.1;
        total = subtotal - desconto;

        c('.subtotal span:last-child').innerHTML = `R$ ${subtotal.toFixed(2)}`;
        c('.desconto span:last-child').innerHTML = `R$ ${desconto.toFixed(2)}`;
        c('.total span:last-child').innerHTML = `R$ ${total.toFixed(2)}`;

    } else {
        c('aside').classList.remove('show');
        c('aside').style.left = '100vw';
    }
}