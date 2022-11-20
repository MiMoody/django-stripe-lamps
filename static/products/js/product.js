
async function loadAllProducts(){
    // Загружает все товары в системе

    let selectedCurrency = document.querySelector("#currencies").value
    let url = `products?currency=${selectedCurrency}`
    let response = await fetch(url);
    let products = await response.text();
    document.querySelector("#products").innerHTML = products
}

async function loadCartProducts(){
    // Загружает товары из корзины
    
    let selectedCurrency = document.querySelector("#currencies").value
    let url = `list-cart-product/${selectedCurrency}`
    let response = await fetch(url);
    let products = await response.text();
    document.querySelector("#products").innerHTML = products
}

async function addProduct(obj){
    // Добавляет продукт в корзину 
    let tmpText = obj.innerHTML
    obj.text = "Added"
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let url = "/cart"
    let quantity = obj.getAttribute("data-quantity")
    if (quantity==null) quantity = 1
    await fetch(url,{
          method: "POST",
          headers: {
              'X-CSRFToken': csrftoken
          },
          body: JSON.stringify({
            product_id: obj.getAttribute("data-product_id"),
            currency_code: obj.getAttribute("data-currency-code"),
            quantity: quantity
            })
        },).then(()=>{
            setTimeout(()=>{
                obj.innerHTML = tmpText
            }, 700)
        }
        );
}

async function deleteProduct(obj){
    // Удаляет продукт из корзины

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let url = "cart"
    await fetch(url,{
          method: "DELETE",
          headers: {
              'X-CSRFToken': csrftoken
          },
          body: JSON.stringify({
            product_id: obj.getAttribute("data-product_id"),
            currency_code: obj.getAttribute("data-currency-code"),
            })
        },).then(()=>loadCartProducts());
}

