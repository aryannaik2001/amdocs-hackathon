document.addEventListener('DOMContentLoaded', function() {
    const factCheckInput = document.getElementById('factCheckInput');
    const checkButton = document.getElementById('checkButton');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultContainer = document.getElementById('resultContainer');
    const confidenceScore = document.getElementById('confidenceScore');
    const reliabilityStatus = document.getElementById('reliabilityStatus');
    const evidence = document.getElementById('evidence');
    const sourcesList = document.getElementById('sourcesList');
  
    checkButton.addEventListener('click', handleFactCheck);
  
    async function handleFactCheck() {
      const text = factCheckInput.value.trim();
      if (!text) return;
  
      try {
        // Show loading state
        loadingIndicator.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        checkButton.disabled = true;
  
        const response = await fetch('http://localhost:8000/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({ text }),
        });
  
        if (!response.ok) {
          throw new Error('Failed to analyze text');
        }
  
        const data = await response.json();
        displayResults(data);
      } catch (error) {
        console.error('Error:', error);
        evidence.textContent = 'Error analyzing text. Please try again.';
      } finally {
        loadingIndicator.classList.add('hidden');
        resultContainer.classList.remove('hidden');
        checkButton.disabled = false;
      }
    }
  
    function displayResults(data) {
      // Display confidence score
      confidenceScore.textContent = `${Math.round(data.confidence * 100)}%`;
      
      // Display reliability status
      reliabilityStatus.textContent = data.credibility_level.replace('_', ' ');
      
      // Display evidence
      evidence.textContent = data.evidence[0];
      
      // Display sources
      sourcesList.innerHTML = '';
      data.sources.slice(0, 2).forEach(source => {
        const li = document.createElement('li');
        li.textContent = new URL(source).hostname;
        sourcesList.appendChild(li);
      });
    }
  });