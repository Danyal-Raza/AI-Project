document.addEventListener('click', function(e) {
  const link = e.target.closest('a');

  if (link && link.href.startsWith('http')) {
    e.preventDefault();
    const targetUrl = link.href;

    fetch('http://127.0.0.1:5000/check_url', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({url: targetUrl})
    })
    .then(res => res.json())
    .then(data => {
      if (data.is_phishing) {
        const confirmVisit = confirm(
          `AI ALERT!\n\nThis link looks suspicious (Score: ${data.probability}).\n\nDo you want to visit it anyway?`
        );
        if (confirmVisit) window.location.href = targetUrl;
      } else {
        window.location.href = targetUrl;
      }
    })
    .catch(err => {
      console.log("Detection server offline. Proceeding normally...");
      window.location.href = targetUrl;
    });
  }
}, true);