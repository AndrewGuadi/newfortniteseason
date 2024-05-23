document.addEventListener('DOMContentLoaded', function () {
    function updateTimer() {
        const targetDate = new Date('May 24, 2024 02:00:00').getTime();
        const now = new Date().getTime();
        const distance = targetDate - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        setDigit('days', days);
        setDigit('hours', hours);
        setDigit('minutes', minutes);
        setDigit('seconds', seconds);

        if (distance < 0) {
            clearInterval(interval);
            document.getElementById('countdown').innerHTML = "Expect Downtime until 5am EST";
        }
    }

    function setDigit(groupId, value) {
        const group = document.getElementById(groupId);
        const digits = String(value).padStart(2, '0').split('');

        digits.forEach((digit, i) => {
            const currentDigit = group.children[i];
            if (currentDigit.innerText !== digit) {
                currentDigit.classList.add('rotate');
                setTimeout(() => {
                    currentDigit.innerText = digit;
                    currentDigit.classList.remove('rotate');
                }, 300);
            }
        });
    }

    const interval = setInterval(updateTimer, 1000);
    updateTimer();
});
