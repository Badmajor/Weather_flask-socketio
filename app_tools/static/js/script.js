document.addEventListener("DOMContentLoaded", () => {
    const socket = io();
    const inputField = document.getElementById("inputField");
    const sendButton = document.getElementById("sendButton");
    const responseParagraph = document.getElementById("response");
    const userSession = document.getElementById("userSession").getAttribute("user-session");

    inputField.addEventListener("input", () => {
        const query = inputField.value;
        if (query.length > 2) {
            fetchSuggestions(query);
        } else {
            suggestions.innerHTML = "";
        }
    });

    function fetchSuggestions(query) {
        fetch(`/get_city_suggestions?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestions.innerHTML = "";
                data.forEach(city => {
                    const suggestion = document.createElement("div");
                    suggestion.textContent = city;
                    suggestion.addEventListener("click", () => {
                        inputField.value = city;
                        suggestions.innerHTML = "";
                    });
                    suggestions.appendChild(suggestion);
                });
            });
    }

    sendButton.addEventListener("click", () => {
        const inputData = inputField.value;
        socket.emit('weather', {city: inputData, user_session: userSession});
    });

    socket.on('response_weather', (data) => {
        if (data.result) {
            const weather = data.result;
            const location = data.location;
            const city = location.city;
            const country = location.country;
            const temp = weather.temperature;
            const humidity = weather.humidity;
            const precipitation_probability = weather.precipitation_probability;
            const weather_icon = weather.weather_icon;

            responseParagraph.innerText = `
            В городе ${city}/${country} сейчас ${weather_icon}

            Температура: ${temp}
            Влажность: ${humidity}
            Вероятность осадков ${precipitation_probability}`;
        } else {
            responseParagraph.innerText = `Проверьте название города!`
        }
    });
});
