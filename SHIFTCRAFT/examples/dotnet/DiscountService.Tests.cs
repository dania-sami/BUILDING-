// Illustrative xUnit test snippet. Requires a .NET test project with xUnit references.
using Xunit;
using Shiftcraft.Examples;

namespace Shiftcraft.Examples.Tests;

public sealed class DiscountServiceTests
{
    private readonly DiscountService _service = new();

    [Theory]
    [InlineData(100, 0.1, 90)]
    [InlineData(100, 0, 100)]
    [InlineData(0, 0.5, 0)]
    public void ApplyDiscount_ForKnownInputs_ReturnsExpected(
        decimal price, decimal rate, decimal expected)
    {
        Assert.Equal(expected, _service.ApplyDiscount(price, rate));
    }

    // Discuss with product owner: negative prices, rate < 0 and rate > 1.
}
