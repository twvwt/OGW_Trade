const axios = require('axios');
const cheerio = require('cheerio');

const url = 'https://yandex.ru/images/search?from=tabbar&text=iPhone%2016%20128%20Teal'; // Замените на нужный URL

axios.get(url)
    .then(response => {
        const $ = cheerio.load(response.data);
        
        // Находим все элементы <a> внутри <div class="SerpPage">
        const links = [];
        $('.SerpPage a').each((index, element) => {
            const link = $(element).attr('href');
            if (link) {
                links.push(link);
            }
        });

        // Выводим все ссылки
        console.log('Ссылки на странице в div SerpPage:');
        links.forEach(link => {
            console.log(link);
        });
    })
    .catch(error => {
        console.error('Ошибка при получении данных:', error);
    });
