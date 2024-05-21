function countdown() {
    const countToDate = new Date("2024-05-24T00:00:00").getTime(); // Replace "YYYY-MM-DDT00:00:00" with the actual date and time
    const now = new Date().getTime();
    const difference = countToDate - now;

    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((difference % (1000 * 60)) / 1000);

    document.getElementById('timer').innerHTML = days + "d " + hours + "h "
    + minutes + "m " + seconds + "s ";

    if (difference < 0) {
        clearInterval(x);
        document.getElementById('timer').innerHTML = "EXPIRED";
    }
}

const x = setInterval(countdown, 1000);
