document.querySelectorAll('.votes').forEach(vote => {

    let countEl = vote.querySelector('.count');
    let like = vote.querySelector('.like-btn');
    let dislike = vote.querySelector('.dislike-btn');

    let count = parseInt(countEl.innerText);

    like.onclick = () => {
        count++;
        countEl.innerText = count;

        like.classList.add('active');
        dislike.classList.remove('active');
    };

    dislike.onclick = () => {
        count--;
        countEl.innerText = count;

        dislike.classList.add('active');
        like.classList.remove('active');
    };

});
