document.addEventListener("DOMContentLoaded", function () {
    const allStar = document.querySelectorAll(".rating .star");
    const ratingValue = document.querySelector(".rating input");
    const feedbackForm = document.querySelector(".feedback-wrapper form");
    const cancelBtn = document.querySelector(".btn.cancel");
    const feedbackWrapper = document.querySelector(".feedback-wrapper");
    const bookingConfirmation = document.querySelector(".booking-confirmation-popup");

    allStar.forEach((item, idx) => {
        item.addEventListener("click", function () {
            let click = 0;
            ratingValue.value = idx + 1;

            allStar.forEach((i) => {
                i.classList.replace("bxs-star", "bx-star");
                i.classList.remove("active");
            });
            for (let i = 0; i < allStar.length; i++) {
                if (i <= idx) {
                    allStar[i].classList.replace("bx-star", "bxs-star");
                    allStar[i].classList.add("active");
                } else {
                    allStar[i].style.setProperty("--i", click);
                    click++;
                }
            }
        });
    });

    const getIpAddress = async () => {
        try {
            const response = await fetch("https://api64.ipify.org?format=json");
            const data = await response.json();
            return data.ip;
        } catch (error) {
            console.error("Error fetching IP address:", error);
            return null;
        }
    };

    cancelBtn.addEventListener("click", function (event) {
        event.preventDefault();
        feedbackWrapper.style.display = "none";
    });

    feedbackForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const rating = ratingValue.value;
        const opinion = this.opinion.value;
        const dateTime = new Date().toISOString();

        getIpAddress().then((ipAddress) => {
            const feedbackData = {
                rating,
                opinion,
                dateTime,
                ipAddress,
            };

            sendFeedbackToServer(feedbackData);
            displayConfirmationMessage();
            this.reset();

            bookingConfirmation.classList.add("show");
        });
    });

    function sendFeedbackToServer(feedback) {
        fetch("http://localhost:5000/submit-feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(feedback),
        })
            .then((response) => {
                if (response.ok) {
                    console.log("Feedback submitted successfully.");
                } else {
                    console.error("Failed to submit feedback.");
                }
            })
            .catch((error) => {
                console.error("Error submitting feedback:", error);
            });
    }

    function displayConfirmationMessage() {
        const confirmationMessage = document.createElement("div");
        confirmationMessage.textContent = "Feedback submitted successfully!";
        document.body.appendChild(confirmationMessage);

        setTimeout(() => {
            confirmationMessage.remove();
        }, 3000);
    }
});