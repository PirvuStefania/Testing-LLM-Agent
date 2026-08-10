# Playbook C#

Framework: xUnit
Coverage: Coverlet (export --format cobertura)

## Sintaxă test
```csharp
using Xunit;
using Moq;

public class AuthServiceTests
{
    [Fact]
    [Trait("Category", "unitTest")]
    [Trait("Category", "happyPath")]
    public void ValidToken_ReturnsOkAndUserData()
    {
        // Arrange
        var mockTokenService = new Mock<ITokenService>();
        mockTokenService.Setup(t => t.Validate(It.IsAny<string>())).Returns(true);

        // Act
        var result = mockTokenService.Object.Validate("valid-token");

        // Assert
        Assert.True(result);
    }

    [Theory]
    [InlineData("")]
    [InlineData(null)]
    [Trait("Category", "edgeCase")]
    public void MissingToken_ReturnsUnauthorized(string token)
    {
        // testul primeste mai multe input-uri prin [InlineData]
    }
}
```

## Reguli
- Markere: `[Trait("Category", "<tip>")]` deasupra fiecărei metode de test (unitTest, integrationTest, happyPath, edgeCase, errorPath, security, e2e, regression). O metodă poate avea mai multe `[Trait]`.
- `[Fact]` pentru un singur caz fix; `[Theory]` + `[InlineData(...)]` pentru mai multe input-uri pe aceeași logică de test.
- Mock-uri: biblioteca `Moq` (`new Mock<T>()`, `.Setup(...)`, `.Returns(...)`).
- Assert-uri: clasa statică `Assert` din xUnit (`Assert.Equal`, `Assert.True`, `Assert.Throws<T>(...)`).
- Denumire metodă: `MetodaTestata_Conditie_RezultatAsteptat` (PascalCase, underscore doar între cele 3 părți).
- Clasa de test: `<NumeClasaTestata>Tests`, `public class`.
- Citare vault: comentariu `// vault_ref: <titlu notă>` deasupra metodei, sau `// vault_ref: none`.
- Async: dacă metoda testată e `async`, testul trebuie să fie `public async Task NumeTest()`, nu `void`.

## Capcane cunoscute
- Nu confunda `[Fact]` cu `[Theory]` — `[Theory]` fără `[InlineData]`/`[MemberData]` nu rulează nimic, dar nici nu dă eroare vizibilă imediat.
- `Assert.Equal(expected, actual)` — ordinea contează pentru mesajele de eroare, deși testul trece oricum dacă valorile sunt egale.
- Verifică `using`-urile complete (`Xunit`, `Moq`, namespace-ul clasei testate) — cod corect sintactic poate eșua la compilare din lipsă de `using`.