

function createCheckouSessionOneProduct(btn){
    btn.onclick = function() { return true; };
    let quantity = btn.getAttribute("data-quantity")
    let url = btn.getAttribute("data-url")+`?quantity=${quantity}`

    fetch(url, {
      method: "GET",
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (session) {
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