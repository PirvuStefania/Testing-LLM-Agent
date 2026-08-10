Reguli pentru testarea modului de autentificare si token-uri JWT

Capcane de evitat:
1. Expirarea token-ului:
   - Problema: Testele pentru rutele protejate pică uneori pentru că durata de viață a token-ului este prea scurtă.
   - Soluția: Folosește funcția mock care generează token-uri ce nu expiră atunci când testezi unitar.
2. Baza de date la login:
   - Problema: Dacă încerci să te legi la baza de date reală în timpul testelor de auth, vei primi erori.
   - Soluția: Folosește mereu o bază de date temporară în memorie (sqlite).

Scenarii obligatorii care trebuie acoperite:
- Cazul fericit (Happy Path): Un header valid cu token trebuie să returneze codul 200 OK și datele utilizatorului.
- Cazul de eroare (Token invalid): Un token stricat sau modificat trebuie să returneze codul 401 Unauthorized.
- Cazul lipsă token: Dacă cererea nu are header de autorizare, trebuie să returneze codul 401 sau 403.