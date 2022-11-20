

function createCheckouSessionOneProduct(btn){
    btn.classList.add("a-off");
    let tmpText = btn.innerHTML
    btn.text = "Loading..."
    let quantity = btn.getAttribute("data-quantity")
    let url = btn.getAttribute("data-url")+`?quantity=${quantity}`

    fetch(url, {
      method: "GET",
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (session) {
        btn.classList.remove("a-off");
        btn.innerHTML = tmpText
        return stripe.redirectToCheckout({ sessionId: session.id });
      })
      .then(function (result) {
        // If redirectToCheckout fails due to a browser or network
        // error, you should display the localized error message to your
        // customer using error.message.
        if (result.error) {
          alert(result.error.message);
        }
      })
      .catch(function (error) {
        console.error("Error:", error);
      });
}

function createCheckouSessionMoreProduct(btn){
  btn.classList.add("a-off");
  let tmpText = btn.innerHTML
  btn.text = "Loading..."
  let selectedCurrency = document.querySelector("#currencies").value
  let url = "order/" + selectedCurrency
  fetch(url, {
    method: "GET",
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (session) {
        if (session.empty_cart_products){
          btn.text = "Cart empty!"
          setTimeout(()=>{
            btn.classList.remove("a-off");
            btn.innerHTML = tmpText
          }, 1000)
        }
        else{
          btn.classList.remove("a-off");
          btn.innerHTML = tmpText
          loadCartProducts()
          return stripe.redirectToCheckout({ sessionId: session.id });
        }
    })
    .then(function (result) {
      // If redirectToCheckout fails due to a browser or network
      // error, you should display the localized error message to your
      // customer using error.message.
      // if (result.error) {
      //   alert(result.error.message);
      // }
    })
    .catch(function (error) {
      console.error("Error:", error);
    });
}