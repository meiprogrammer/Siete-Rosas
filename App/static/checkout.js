document.addEventListener('DOMContentLoaded', () => {
    var submitButton = document.querySelector('#submit');

    function loadCity() {
        var state = document.querySelector('#state').value;
        var city = document.querySelector('#city');
        city.innerHTML = '<option value="">Sua cidade:</option>';

        if (state) {
            fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${state}/municipios`)
            .then(response => response.json())
            .then(data => {
                 data.forEach(cityData => {
                    var cityElement = document.createElement("option");
                    cityElement.innerHTML = `${cityData.nome}`;
                    cityElement.value = cityData.id;
                    city.appendChild(cityElement);
                })
            })
            .catch(error => {
                console.error(error);
            });
        }; 
    };

    function verifyCEP() {
        var CEP = document.querySelector('#cep').value;
        var cepMsg = document.querySelector('#cepMsg');
        var city = document.querySelector('#city');
        var selectedCity = city.selectedOptions[0]?.innerHTML;
            
        if (CEP) {
            fetch(`https://viacep.com.br/ws/${CEP}/json/`)
            .then(response => {
                if (response.ok) {  
                    submitButton.disabled = false;                
                    return response.json();
                } else {
                    submitButton.disabled = true;
                    cepMsg.innerHTML = 'CEP inválido';
                }
            })
            .then(data => {
                if (data.localidade === selectedCity) {
                    submitButton.disabled = false;
                    cepMsg.innerHTML = `${data.bairro}, ${data.logradouro}`;
                    document.querySelector('#street').value = `${data.logradouro}`;
                } else {
                    submitButton.disabled = true;
                    cepMsg.innerHTML = `Sua localidade não corresponde ao seu CEP.`;
                }
           });
        };
    };

    document.querySelector('#state').addEventListener('change', loadCity);
    document.querySelector('#city').addEventListener('change', verifyCEP);
    document.querySelector('#cep').addEventListener('change', verifyCEP); 
});
