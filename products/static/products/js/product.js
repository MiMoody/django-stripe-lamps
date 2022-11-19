async function addProduct(obj){

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
        },);
}

async function deleteProduct(obj){

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
        },).then(()=>loadProducts());
}

