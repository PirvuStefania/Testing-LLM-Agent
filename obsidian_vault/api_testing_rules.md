Reguli pentru testarea rutelor si a API-urilor

Structura testelor:
- Folosește clientul de testare oferit de FastAPI pentru a simula cererile HTTP rapid, fără să pornești un server real.
- Testează rutele și cu date greșite sau lipsă (de exemplu, trimiterea unui text în loc de un număr pentru un ID) ca să te asiguri că API-ul știe să dea eroare de validare (cod 422).

Categorii de teste și markeri:
- Pune markerul de unit test pe funcțiile izolate.
- Pune markerul de integration test pe rutele care trec prin logica aplicației și ating baza de date mock-uită.
- Fiecare rută importantă trebuie să aibă cel puțin un test care verifică o eroare (de exemplu, resursă negăsită - cod 404).