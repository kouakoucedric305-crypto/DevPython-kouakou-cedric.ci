/**
 * JavaScript principal - MonEntreprise
 * - Hamburger menu mobile
 * - Auto-fermeture des messages flash
 * - Compteurs animés
 * - Désactivation bouton envoi formulaire
 */
document.addEventListener('DOMContentLoaded', function () {

  // ── MENU HAMBURGER MOBILE ──────────────────────────────
  var hamburger = document.getElementById('hamburger');
  var navMobile = document.getElementById('navMobile');

  if (hamburger && navMobile) {
    hamburger.addEventListener('click', function () {
      navMobile.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', navMobile.classList.contains('open'));
    });
    // Fermer au clic sur un lien
    navMobile.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { navMobile.classList.remove('open'); });
    });
  }

  // ── FERMETURE AUTO DES MESSAGES FLASH (5s) ────────────
  document.querySelectorAll('.alert').forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity .5s ease';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 500);
    }, 5000);
  });

  // ── COMPTEURS ANIMÉS ──────────────────────────────────
  function animateCounter(el, target, duration) {
    var suffix = el.textContent.replace(/[\d]/g, '');
    var start  = 0;
    var step   = target / (duration / 16);
    var current = start;
    var timer = setInterval(function () {
      current = Math.min(current + step, target);
      el.textContent = Math.floor(current) + suffix;
      if (current >= target) clearInterval(timer);
    }, 16);
  }

  var statsSection = document.querySelector('.stats-section');
  if (statsSection) {
    var observed = false;
    var obs = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting && !observed) {
        observed = true;
        document.querySelectorAll('.stat-number').forEach(function (el) {
          var val = parseInt(el.textContent.replace(/\D/g, ''), 10);
          if (!isNaN(val)) animateCounter(el, val, 1500);
        });
      }
    }, { threshold: 0.3 });
    obs.observe(statsSection);
  }

  // ── FORMULAIRE : DÉSACTIVER LE BOUTON PENDANT L'ENVOI ─
  var form = document.querySelector('.contact-form');
  if (form) {
    form.addEventListener('submit', function () {
      var btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Envoi en cours…';
        setTimeout(function () {
          btn.disabled = false;
          btn.textContent = 'Envoyer le message';
        }, 8000);
      }
    });
  }
});
