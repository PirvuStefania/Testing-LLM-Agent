# Playbook TypeScript

Framework: Jest (sau Vitest — sintaxă foarte similară)
Coverage: Istanbul, inclus în Jest (--coverage --coverageReporters=cobertura)

## Sintaxă test
```typescript
import { validateToken } from "../auth";

describe("[unit] AuthService", () => {
  it("[happyPath] returns 200 and user data for a valid token", () => {
    const result = validateToken("valid-token");
    expect(result.status).toBe(200);
    expect(result.userData).toBeDefined();
  });

  it("[errorPath][security] returns 401 for an invalid token", () => {
    const result = validateToken("invalid-token");
    expect(result.status).toBe(401);
  });
});
```

## Reguli
- Markere: Jest NU are markere native. Convenție agreată: prefix `[tip]` la începutul textului din `it(...)`/`test(...)`, ex: `it("[unitTest][happyPath] ...")`. Poate avea mai multe tag-uri.
- Grupare: `describe("[nivel] NumeModul", ...)` pentru a grupa testele pe modul/componentă.
- Mock-uri: `jest.mock(...)`, `jest.fn()`, `jest.spyOn(...)`.
- Assert-uri: `expect(...).toBe(...)`, `.toEqual(...)`, `.toThrow(...)`, `.toBeDefined()`.
- Async: teste asincrone folosesc `async () => { await ... }`, niciodată callback-uri `done` (stil vechi, evitat).
- Denumire fișier: `<numeModul>.test.ts` sau `<numeModul>.spec.ts`.
- Citare vault: comentariu `// vault_ref: <titlu notă>` deasupra blocului `it(...)`, sau `// vault_ref: none`.

## Capcane cunoscute
- `toBe` face comparație strictă (`===`) — pentru obiecte/array-uri folosește `toEqual`, altfel testul pică fals-negativ chiar și când datele sunt logic identice.
- Mock-urile create cu `jest.mock()` la nivel de modul trebuie resetate între teste (`jest.clearAllMocks()` în `beforeEach`), altfel starea se scurge între teste.
- TypeScript compilează cu `tsc` înainte de rulare — erori de tip pot bloca execuția chiar dacă JS-ul rezultat ar fi valid.