// main.js — students will add JavaScript here as features are built

// "See how it works" video modal (landing page)
(function () {
    var YOUTUBE_VIDEO_ID = '-Lt-ntUDj-g';

    var modal = document.querySelector('[data-video-modal]');
    if (!modal) return;

    var trigger = document.querySelector('[data-video-trigger]');
    var closers = modal.querySelectorAll('[data-video-close]');
    var frame = modal.querySelector('[data-video-frame]');

    function openModal() {
        frame.innerHTML =
            '<iframe src="https://www.youtube.com/embed/' + YOUTUBE_VIDEO_ID + '?autoplay=1" ' +
            'title="Product demo video" allow="autoplay; encrypted-media" allowfullscreen></iframe>';
        modal.hidden = false;
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.hidden = true;
        frame.innerHTML = ''; // stop playback
        document.body.style.overflow = '';
    }

    if (trigger) trigger.addEventListener('click', openModal);
    closers.forEach(function (el) {
        el.addEventListener('click', closeModal);
    });
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !modal.hidden) closeModal();
    });
})();
