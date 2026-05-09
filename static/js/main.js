document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = getCookie('csrftoken');
    if (!csrfToken) {
        console.error('CSRF token not found! Ensure you are logged in and cookies are enabled.');
    }

    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;
            const type = this.dataset.type;   // "question" или "answer"

            fetch(`/${type}/${id}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Обновляем счётчик в той же карточке
                const card = this.closest('.card');
                if (!card) return;
                const countSpan = card.querySelector('.likes-count');
                if (countSpan) {
                    countSpan.textContent = data.likes_count;
                }

                // Визуальная обратная связь: заливка сердечка красным
                if (data.liked) {
                    this.classList.add('active');
                    this.style.color = '#dc3545';  // Bootstrap danger
                } else {
                    this.classList.remove('active');
                    this.style.color = '';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
