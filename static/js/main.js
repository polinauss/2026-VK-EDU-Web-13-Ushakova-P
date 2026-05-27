document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = getCookie('csrftoken');

    document.querySelectorAll('.like-btn, .dislike-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;
            const type = this.dataset.type;
            const action = this.dataset.action;
            const like = action === 'like' ? '1' : '0';

            fetch(`/${type}/${id}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `like=${like}`
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Network error'); });
                }
                return response.json();
            })
            .then(data => {
                const card = this.closest('.card');
                if (!card) return;
                const countSpan = card.querySelector('.likes-count');
                if (countSpan) countSpan.textContent = data.likes_count;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    document.querySelectorAll('.mark-correct-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;

            fetch(`/answer/${id}/correct/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Network error'); });
                }
                return response.json();
            })
            .then(data => {
                document.querySelectorAll('.correct-badge').forEach(el => el.remove());
                document.querySelectorAll('.mark-correct-btn').forEach(el => el.style.display = 'inline-block');

                const answerCard = document.getElementById(`answer-${data.answer_id}`);
                if (answerCard) {
                    const textDiv = answerCard.querySelector('.flex-grow-1');
                    if (textDiv) {
                        const badge = document.createElement('span');
                        badge.className = 'text-success fw-bold correct-badge';
                        badge.textContent = '✔ Правильный ответ';
                        textDiv.insertBefore(badge, textDiv.querySelector('p.text-muted'));
                    }
                    const markBtn = answerCard.querySelector('.mark-correct-btn');
                    if (markBtn && data.is_correct) markBtn.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert(error.message);
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
});
