// Configuration de l'API
const API_URL = '/api/search';

// Attendre que le DOM soit entièrement chargé
document.addEventListener('DOMContentLoaded', function() {
    // Gestion des onglets
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.getAttribute('data-tab');
            
            // Activer l'onglet
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Afficher le contenu de l'onglet
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(`${tabId}-tab`).classList.add('active');
            
            // Cacher les résultats précédents
            document.getElementById('search-result').style.display = 'none';
            document.getElementById('download-btn').style.display = 'none';
            document.getElementById('error-message').style.display = 'none';
        });
    });
    
    // Fonction pour effectuer une recherche via l'API
    async function performSearch(type, query) {
        // Afficher le chargement
        document.querySelector('.loading').style.display = 'block';
        document.getElementById('search-result').style.display = 'none';
        document.getElementById('download-btn').style.display = 'none';
        document.getElementById('error-message').style.display = 'none';
        
        // Construire l'URL avec les paramètres de requête selon le type
        let searchUrl = API_URL;
        if (type === 'username') {
            searchUrl += `?u=${encodeURIComponent(query)}`;
        } else if (type === 'fullname') {
            searchUrl += `?fn=${encodeURIComponent(query)}`;
        } else if (type === 'ip') {
            searchUrl += `?ip=${encodeURIComponent(query)}`;
        }
        
        try {
            // Effectuer la requête API
            const response = await fetch(searchUrl);
            const data = await response.json();
            
            // Masquer le chargement
            document.querySelector('.loading').style.display = 'none';
            
            if (data.error) {
                // Afficher l'erreur
                const errorElement = document.getElementById('error-message');
                errorElement.textContent = data.error;
                errorElement.style.display = 'block';
                return;
            }
            
            // Formater et afficher les résultats
            const resultElement = document.getElementById('search-result');
            
            // Traitement spécial pour la recherche de nom d'utilisateur (coloration)
            if (type === 'username') {
                let formattedResult = data.result;
                // Remplacer les lignes avec YES en vert
                formattedResult = formattedResult.replace(/✅.*YES/g, match => 
                    `<span class="found">${match}</span>`);
                // Remplacer les lignes avec NO en rouge
                formattedResult = formattedResult.replace(/❌.*NO/g, match => 
                    `<span class="not-found">${match}</span>`);
                
                resultElement.innerHTML = formattedResult;
            } else {
                // Pour les autres types de recherche, afficher tel quel
                resultElement.textContent = data.result;
            }
            
            resultElement.style.display = 'block';
            document.getElementById('download-btn').style.display = 'block';
            
            return data.result;
        } catch (error) {
            // Gérer les erreurs
            document.querySelector('.loading').style.display = 'none';
            const errorElement = document.getElementById('error-message');
            errorElement.textContent = "Erreur de connexion à l'API. Assurez-vous que le serveur est en cours d'exécution.";
            errorElement.style.display = 'block';
            console.error('Error:', error);
        }
    }
    
    // Gestion des formulaires
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
    
    // Téléchargement des résultats
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