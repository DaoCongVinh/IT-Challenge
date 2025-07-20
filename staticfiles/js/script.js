const bar = document.getElementById('bar');
const nav = document.getElementById('navbar');
const navLinks = nav.querySelectorAll('#header #navbar a');
const currentPath = window.location.pathname;


if(bar) {
  bar.addEventListener('click', () => {
    nav.classList.add('active');
  })
};

navLinks.forEach(link => {
  if (link.getAttribute('href') === currentPath) {
      link.classList.add('active'); // Add active class to the matching link
  } else {
      link.classList.remove('active'); // Remove active class from others
  }
});

