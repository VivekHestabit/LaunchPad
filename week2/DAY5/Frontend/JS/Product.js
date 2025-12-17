const productsContainer = document.getElementById("products");
const searchInput = document.getElementById("search");
const sortSelect = document.getElementById("sort");

let productsData = [];

fetch("https://dummyjson.com/products")
  .then(res => res.json())
  .then(data => {
    productsData = data.products;
    renderProducts(productsData);
  });

function renderProducts(products) {
  productsContainer.innerHTML = "";

  products.forEach(product => {
    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
      <img height = "0" width ="0" src="${product.thumbnail}" />
      <h3>${product.title}</h3>
      <p>₹ ${product.price}</p>
    `;

    productsContainer.appendChild(card);
  });
}


searchInput.addEventListener("input", () => {
  const value = searchInput.value.toLowerCase();

  const filtered = productsData.filter(p =>
    p.title.toLowerCase().includes(value)
  );

  renderProducts(filtered);
});

sortSelect.addEventListener("change", () => {
  let sorted = [...productsData];

  if (sortSelect.value === "high") {
    sorted.sort((a, b) => b.price - a.price);
  }

  if (sortSelect.value === "low") {
    sorted.sort((a, b) => a.price - b.price);
  }

  renderProducts(sorted);
});
