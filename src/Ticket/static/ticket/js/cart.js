
let cart = [];
$('input[type="checkbox"]').on("change", function () {
  const ticketId = $(this).val();
  const quantityInput = $(`#quantity_${ticketId}`);
  if ($(this).is(":checked")) {
    quantityInput.prop("disabled", false);
  } else {
    quantityInput.prop("disabled", true).val(1);
  }
});

$("#addToCartGlobal").on("click", function () {
  $('input[name="tickets"]:checked').each(function () {
    const ticketId = $(this).val();
    const ticketLabel = $(`label[for="ticket_${ticketId}"]`).text();
    const quantity = $(`#quantity_${ticketId}`).val();
    const price = parseFloat($(`#price_${ticketId}`).val());

    // Vérifier si le ticket est déjà dans le panier
    const existingTicket = cart.find((item) => item.id === ticketId);
    if (existingTicket) {
      existingTicket.quantity =
        parseInt(existingTicket.quantity) + parseInt(quantity);
    } else {
      cart.push({
        id: ticketId,
        label: ticketLabel,
        quantity: parseInt(quantity),
        price: price, // Ajout du prix au panier
      });
    }
  });

  updateCartDisplay();
});


function updateCartDisplay() {
  const cartItemsContainer = $("#cartItems");
  const totalPriceContainer = $("#totalPrice");
  cartItemsContainer.empty();
  let total = 0;

  if (cart.length > 0) {
    $("#submitCart").show();

    cart.forEach((item) => {
      // Calcul du total
      total += item.price * item.quantity;

      cartItemsContainer.append(
        `<li>${item.label} - Quantité : ${item.quantity}, Prix : ${(
          item.price * item.quantity
        ).toFixed(2)}€</li>`
      );
    });

    totalPriceContainer.text(total.toFixed(2));
  } else {
    $("#submitCart").hide(); // Cacher le bouton de validation si le panier est vide
    cartItemsContainer.append("<li>Le panier est vide.</li>");
    totalPriceContainer.text("0");
  }
}

$("#resetCart").on("click", function () {
  cart = []; // Réinitialiser le panier
  $('input[name="tickets"]').prop("checked", false); // Décocher toutes les cases à cocher
  $('input[type="number"]').val(1).prop("disabled", true); // Réinitialiser les quantités et désactiver les champs
  updateCartDisplay(); // Mettre à jour l'affichage du panier
});

$("#submitCart").on("click", function () {
  $.ajax({
    url: processPurchaseUrl,
    method: "POST",
    data: JSON.stringify({
      tickets: cart,
    }),
    headers: {
      "X-CSRFToken": csrfToken,
    },
    contentType: "application/json",
    success: function (response) {
      if (response.status === "success") {
        let confirmationHTML = "<h3>Achat confirmé !</h3>";
        response.purchases.forEach(function (purchase) {
          confirmationHTML += `<p>Ticket: ${purchase.ticket}, Prix: ${purchase.price}</p>`;
        });
        $("#confirmation").html(confirmationHTML);
        cart = []; // Vider le panier après confirmation
        updateCartDisplay();
      } else {
        $("#confirmation").html(
          "<p>Une erreur est survenue lors de l'achat.</p>"
        );
      }
    },
    error: function (xhr, status, error) {
        console.error("Erreur lors de la soumission du formulaire :", xhr.responseText);
        $("#confirmation").html(
            `<p>Erreur lors de la soumission du formulaire : ${xhr.responseText}</p>`
    );
   },

  });
});
