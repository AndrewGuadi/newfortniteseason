document.addEventListener('DOMContentLoaded', function () {
    function updateTimer() {
        const targetDate = new Date('May 24, 2024 02:00:00').getTime();
        const now = new Date().getTime();
        const distance = targetDate - now;

        if (distance < 0) {
            clearInterval(interval);
            const countdownElement = document.getElementById('countdown');
            if (countdownElement) {
                countdownElement.innerHTML = "Chapter 5 Season 3 Started May 24th @ 2:00 A.M. est";
                countdownElement.classList.add("countdown-style");
            } else {
                console.error("Element with ID 'countdown' not found.");
            }
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        console.log(`Days: ${days}, Hours: ${hours}, Minutes: ${minutes}, Seconds: ${seconds}`);

        setDigit('days', days);
        setDigit('hours', hours);
        setDigit('minutes', minutes);
        setDigit('seconds', seconds);
    }

    function setDigit(groupId, value) {
        const group = document.getElementById(groupId);
        if (group) {
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
        } else {
            console.error(`Element with ID '${groupId}' not found.`);
        }
    }

    const interval = setInterval(updateTimer, 1000);
    updateTimer();
});
