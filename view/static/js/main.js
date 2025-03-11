const API_URL = '/api/search';

document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.getAttribute('data-tab');
            
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(`${tabId}-tab`).classList.add('active');
            
            document.getElementById('search-result').style.display = 'none';
            document.getElementById('download-btn').style.display = 'none';
            document.getElementById('error-message').style.display = 'none';
        });
    });
    
    async function performSearch(type, query) {
        document.querySelector('.loading').style.display = 'block';
        document.getElementById('search-result').style.display = 'none';
        document.getElementById('download-btn').style.display = 'none';
        document.getElementById('error-message').style.display = 'none';
        
        
        let searchUrl = API_URL;
        if (type === 'username') {
            searchUrl += `?u=${encodeURIComponent(query)}`;
        } else if (type === 'fullname') {
            searchUrl += `?fn=${encodeURIComponent(query)}`;
        } else if (type === 'ip') {
            searchUrl += `?ip=${encodeURIComponent(query)}`;
        }
        
        try {
            const response = await fetch(searchUrl);
            const data = await response.json();
            
            document.querySelector('.loading').style.display = 'none';
            
            if (data.error) {
                const errorElement = document.getElementById('error-message');
                errorElement.textContent = data.error;
                errorElement.style.display = 'block';
                return;
            }
            
            const resultElement = document.getElementById('search-result');
            
            if (type === 'username') {
                let formattedResult = data.result;

                formattedResult = formattedResult.replace(/\x1B\[[0-9;]*m/g, "");
                
                // Remplacer les lignes avec YES en vert
                formattedResult = formattedResult.replace(/✅.*YES/g, match => 
                    `<span class="found">${match}</span>`);
                // Remplacer les lignes avec NO en rouge
                formattedResult = formattedResult.replace(/❌.*NO/g, match => 
                    `<span class="not-found">${match}</span>`);
                
                formattedResult = formattedResult.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');

                resultElement.innerHTML = formattedResult;
            } else if (type === "fullname"){
                const rawResult = data.result;

                const addressMatch = rawResult.match(/Address:\s*(.*)/);
                const numberMatch = rawResult.match(/Number:\s*(.*)/);

                const address = addressMatch ? addressMatch[1] : '';
                const number = numberMatch ? numberMatch[1] : '';

                const mapUrl = `https://www.google.com/maps?q=${encodeURIComponent(address)}`;

                let formattedResult = rawResult;

                if (address) {
                    formattedResult = formattedResult.replace(address, `<a href="${mapUrl}" target="_blank">${address}</a>`);
                }

                if (number) {
                    formattedResult = formattedResult.replace(number, `<a href="tel:${number}">${number}</a>`);
                }

                resultElement.innerHTML = formattedResult;
            }else{
                const rawResult = data.result;  

                const ipMatch = rawResult.match(/IP Address:\s*(\S+)/);
                const cityMatch = rawResult.match(/City:\s*(.*)/);
                const countryMatch = rawResult.match(/Country:\s*(.*)/);
                const ispMatch = rawResult.match(/ISP:\s*(.*)/);
                const latLonMatch = rawResult.match(/City Lat\/Lon:\s*\(([-+]?\d*\.\d+)\)\/\(([-+]?\d*\.\d+)\)/);

                const ip = ipMatch ? ipMatch[1] : '';
                const city = cityMatch ? cityMatch[1] : '';
                const country = countryMatch ? countryMatch[1] : '';
                const isp = ispMatch ? ispMatch[1] : '';
                const lat = latLonMatch ? latLonMatch[1] : ''; 
                const lon = latLonMatch ? latLonMatch[2] : ''; 

                const ipUrl = `https://ipinfo.io/${encodeURIComponent(ip)}`;
                const cityUrl = `https://www.google.com/maps?q=${encodeURIComponent(city)}`;
                const countryUrl = `https://en.wikipedia.org/wiki/${encodeURIComponent(country)}`;
                const ispUrl = `https://www.${encodeURIComponent(isp.toLowerCase())}.com`;
                const latLonUrl = `https://www.google.com/maps?q=${encodeURIComponent(lat)},${encodeURIComponent(lon)}`;

                let formattedResult = rawResult;

                if (ip) {
                    formattedResult = formattedResult.replace(ip, `<a href="${ipUrl}" target="_blank">${ip}</a>`);
                }

                if (city) {
                    formattedResult = formattedResult.replace(city, `<a href="${cityUrl}" target="_blank">${city}</a>`);
                }

                if (country) {
                    formattedResult = formattedResult.replace(country, `<a href="${countryUrl}" target="_blank">${country}</a>`);
                }

                if (isp) {
                    formattedResult = formattedResult.replace(isp, `<a href="${ispUrl}" target="_blank">${isp}</a>`);
                }

                if (lat && lon) {
                    formattedResult = formattedResult.replace(`(${lat})/(${lon})`, `<a href="${latLonUrl}" target="_blank">${lat}/${lon}</a>`);
                }

                resultElement.innerHTML = formattedResult; 
            }
            
            resultElement.style.display = 'block';
            document.getElementById('download-btn').style.display = 'block';
            
            return data.result;
        } catch (error) {
            document.querySelector('.loading').style.display = 'none';
            const errorElement = document.getElementById('error-message');
            errorElement.textContent = "Erreur de connexion à l'API. Assurez-vous que le serveur est en cours d'exécution.";
            errorElement.style.display = 'block';
            console.error('Error:', error);
        }
    }
    
    document.getElementById('username-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        await performSearch('username', username);
    });
    
    document.getElementById('fullname-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fullname = document.getElementById('fullname').value;
        await performSearch('fullname', fullname);
    });
    
    document.getElementById('ip-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const ip = document.getElementById('ip').value;
        await performSearch('ip', ip);
    });
    
    document.getElementById('download-btn').addEventListener('click', () => {
        const result = document.getElementById('search-result').innerText;
        const blob = new Blob([result], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'passive_result.txt';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    });
});