document.getElementById('estimateForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const sqft = parseFloat(document.getElementById('sqft').value);
  const neighborhood = document.getElementById('neighborhood').value;
  const architect = document.getElementById('architect').value;
  const features = Array.from(document.getElementById('features').selectedOptions).map(opt => opt.value);

  // Base price per sqft in Charlotte luxury markets
  let basePrice = 650; // mid-range $500-$800

  // Neighborhood multipliers
  const neighborhoodMultiplier = {
    eastover: 1.1,
    foxcroft: 1.05,
    myers_park: 1.2
  };

  // Architect adjustments
  const architectMultiplier = {
    garret_nelson: 1.1,
    presley_dixon: 1.15
  };

  // Feature costs per sqft
  const featureCosts = {
    pool: 50,
    marble: 75,
    slate_roof: 40,
    wood_roof: 30
  };

  let featureCostTotal = features.reduce((sum, f) => sum + featureCosts[f], 0);

  let estimatedCost = sqft * basePrice * neighborhoodMultiplier[neighborhood] * architectMultiplier[architect] + sqft * featureCostTotal;

  document.getElementById('result').innerHTML = `<h3>Estimated Cost: $${estimatedCost.toLocaleString()}</h3>`;
});
