// ===== DASHBOARD STATS =====
fetch("/stats")
  .then(r => r.json())
  .then(d => {
    document.getElementById("totalProducts").innerText = d.total_products;
    document.getElementById("avgRating").innerText = d.avg_rating + " ⭐";
  })
  .catch(err => console.error("Stats error:", err));

// ===== TOP RECOMMENDATIONS =====
fetch("/api/recommendations")
  .then(r => r.json())
  .then(list => {
    const box = document.getElementById("recommendations");
    box.innerHTML = "";
    list.forEach(p => {
      box.innerHTML += `
        <div style="margin-bottom:10px;">
          <b>${p.product_name}</b><br>
          ${p.category} | Rs ${p.price} | ⭐ ${p.rating}
        </div>
      `;
    });
  })
  .catch(err => console.error("Recs error:", err));

  
const titles = {
 'dashboard': 'Dashboard',
'recommendations': "Recommendations",
  'products': "Products",
  'analytics': "Analytics",
  'users': "Users",
  'algorithms': "Algorithms"
};

if (pageId === "products") {
  loadProducts();
  loadProductStats();   // 🔥 YEH LINE
}
