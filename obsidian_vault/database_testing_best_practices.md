Bune practici pentru testarea bazelor de date

Izolarea datelor:
- Nu rula niciodată teste pe baza de date de producție.
- Fiecare test trebuie să curețe datele după ce rulează sau să folosească o sesiune izolată care dă rollback automat la final, ca să nu strice datele pentru testele următoare.

Fixture-uri recomandate în Pytest:
- O sesiune curată de baza de date pentru fiecare test în parte.
- Inserarea automată a unor utilizatori de test (de exemplu, un admin și un utilizator normal) pentru a putea testa drepturile de acces.

Cazuri limită de acoperit:
- Date goale: Trimiterea unor câmpuri obligatorii lăsate necompletate trebuie să returneze o eroare de validare (cod 422).
- Valori numerice limită: La paginare, testează ce se întâmplă dacă utilizatorul trimite valori negative sau egale cu zero.