document.addEventListener('DOMContentLoaded', () => {
    // Скролл
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
      if (window.scrollY > 100) {
        header.classList.add('shrink');
      } else {
        header.classList.remove('shrink');
      }
    });
  
    // Бургер
    if (!window.burgerBtn) {
      const burgerBtn = document.querySelector('.burger-btn');
      const mobileModal = document.querySelector('.mobile-modal');
      const closeBtn = document.querySelector('.close-btn');
      const modalContent = document.querySelector('.mobile-modal-content');
  
      burgerBtn.addEventListener('click', () => {
        mobileModal.classList.add('active');
        document.body.style.overflow = 'hidden';
        burgerBtn.classList.add('active');
      });
  
      closeBtn.addEventListener('click', () => closeModal());
      mobileModal.addEventListener('click', e => {
        if (e.target === mobileModal) closeModal();
      });
  
      function closeModal() {
        mobileModal.classList.remove('active');
        document.body.style.overflow = '';
        burgerBtn.classList.remove('active');
      }
  
      window.burgerBtn = burgerBtn;
    }
  
    // Отзывы
    const testimonialsUrl = window.testimonialsUrl;
    const testimonialCreateUrl = window.testimonialCreateUrl;
    
    let allTestimonials = [];
    let visibleCount = 0;
    const testimonialsPerPage = 5;
    
    async function loadTestimonials() {
      const res = await fetch(testimonialsUrl);
      allTestimonials = await res.json();
      visibleCount = 0;
    
      const testimonialList = document.getElementById('testimonialList');
      if (testimonialList) testimonialList.innerHTML = '';
    
      renderTestimonials(); // показываем первые 5
    }
    
    function renderTestimonials() {
      const testimonialList = document.getElementById('testimonialList');
      const showMoreBtn = document.getElementById('showMoreBtn');
    
      const nextItems = allTestimonials.slice(visibleCount, visibleCount + testimonialsPerPage);
      nextItems.forEach(t => {
        const stars = '★★★★★☆☆☆☆☆'.slice(5 - t.rating, 10 - t.rating);
        const div = document.createElement('div');
        div.classList.add('testimonial-item');
        div.innerHTML = `
          <div class="testimonial-card">
            <div class="testimonial-avatar">
              <img src="${avatarUrl}" alt="Аватар" />
            </div>
            <div class="testimonial-content">
              <div class="testimonial-header">
                <span class="testimonial-name">${t.name}</span>
                <span class="testimonial-stars">${stars}</span>
              </div>
              <div class="testimonial-text">${t.text}</div>
            </div>
          </div>
        `;
        testimonialList.appendChild(div);
      });
    
      visibleCount += testimonialsPerPage;
    
      if (visibleCount >= allTestimonials.length) {
        showMoreBtn.style.display = 'none';
      } else {
        showMoreBtn.style.display = 'inline-block';
      }
    }
    
    // Обработка формы отправки отзыва
    const testimonialForm = document.getElementById('testimonialForm');
if (testimonialForm) {
  testimonialForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    // Очистить старые ошибки
    document.getElementById('nameError').textContent = '';
    document.getElementById('textError').textContent = '';
    document.getElementById('ratingError').textContent = '';

    const ratingInput = this.querySelector('input[name="rating"]:checked');
    const name = this.elements['name'].value.trim();
    const text = this.elements['text'].value.trim();

    let hasError = false;

    if (!ratingInput) {
      document.getElementById('ratingError').textContent = 'Пожалуйста, выберите оценку.';
      hasError = true;
    }
    if (!name) {
      document.getElementById('nameError').textContent = 'Пожалуйста, введите имя.';
      hasError = true;
    }
    if (!text) {
      document.getElementById('textError').textContent = 'Пожалуйста, введите отзыв.';
      hasError = true;
    } else if (text.length > 250) {
      document.getElementById('textError').textContent = 'Максимум 250 символов.';
      hasError = true;
    }

    if (hasError) return;

    const res = await fetch(testimonialCreateUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': window.csrfToken
      },
      body: JSON.stringify({
        rating: parseInt(ratingInput.value),
        name,
        text,
      })
    });

    if (res.ok) {
      this.reset();
      await loadTestimonials();
    } else {
      document.getElementById('textError').textContent = 'Ошибка при отправке отзыва.';
    }
  });
}
    
    // Кнопка "Показать ещё"
    const showMoreBtn = document.getElementById('showMoreBtn');
    if (showMoreBtn) {
      showMoreBtn.addEventListener('click', renderTestimonials);
    }
    
    // Первая загрузка
    loadTestimonials();
  });