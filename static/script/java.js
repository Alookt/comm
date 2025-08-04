const currentPath = window.location.pathname;
  document.querySelectorAll('nav a.nav-link').forEach(link => {
    if(link.getAttribute('href') === currentPath) {
      link.classList.add('active'); // Add your active styles
    }
  });

  document.addEventListener('DOMContentLoaded', function() {
    const homepageContent = document.getElementById('homepage-content');
    if (!homepageContent) return;

    // Get the current path (e.g. "/" or "/cart/")
    const path = window.location.pathname;

    // Show only if on homepage, else hide
    if (path === '/') {
      homepageContent.style.display = 'block';
    } else {
      homepageContent.style.display = 'none';
    }
  });
  document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('id_profile_picture'); 
    const preview = document.getElementById('profilePreview');

    if (input && preview) {
      input.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function (event) {
            preview.src = event.target.result;
          }
          reader.readAsDataURL(file);
        } else {
          preview.src = 'https://via.placeholder.com/100?text=Preview'; 
        }
      });
    }
  });
  fetch('/api/products/')
  .then(res => res.json())
  .then(data => {
     console.log(data);  // your array of products
  });
