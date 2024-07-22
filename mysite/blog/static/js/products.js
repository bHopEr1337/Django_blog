// Получаем все ссылки в списке стран
const countryLinks = document.querySelectorAll('.country-list a');

// Получаем элементы для отображения цены, флага и валюты
const priceElement = document.querySelectorAll('.price');
const countryButtonElement = document.querySelectorAll('.country-button img');
const currencySymbolElement = document.querySelectorAll('.currency-symbol');

// Массив для хранения оригинальных цен
let originalPrices = [5000, 4500, 3000];

// Массив для хранения валюты
const currencies = {
    'USA': '$',
    'Russia': '₽',
    'Germany': '€'
};

// Задаем курс валют
const exchangeRates = {
    'USA': 0.014,
    'Russia': 1,
    'Germany': 0.013
};

// Функция для обновления цены, флага и валюты
function updatePriceAndFlag(country) {
    // Обновляем цены
    priceElement.forEach((price, index) => {
        const newPrice = originalPrices[index] * exchangeRates[country];
        price.textContent = `${currencies[country]}${newPrice.toFixed(2)}`;
    });

    // Обновляем флаг
    countryButtonElement.forEach((button, index) => {
        button.src = `${STATIC_URL}images/${country.toLowerCase()}_0.jpeg`;
    });

    // Обновляем валюту
    currencySymbolElement.forEach((symbol, index) => {
        symbol.textContent = currencies[country];
    });

    // Сохраняем выбранную страну в localStorage
    localStorage.setItem('selectedCountry', country);
}

// Обработчик события клика на ссылки в списке стран
countryLinks.forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault();
        const selectedCountry = event.target.textContent;
        updatePriceAndFlag(selectedCountry);
    });
});

// При загрузке страницы проверяем, есть ли сохраненная страна в localStorage
const savedCountry = localStorage.getItem('selectedCountry');
if (savedCountry) {
    updatePriceAndFlag(savedCountry);
} else {
    // Сохраняем оригинальные цены в массив
    priceElement.forEach((price) => {
        originalPrices.push(parseFloat(price.textContent.replace(/[^0-9.-]+/g, '')));
    });

    updatePriceAndFlag('Russia'); // Устанавливаем начальную страну по умолчанию
}
